

# import xmlrpc.client
# import json
# url = 'http://localhost:8018'
# db = 'odoo18_test'
# username = 'admin'
# password = 'admin'
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# # print(common.version()) #to check connection
# uid = common.authenticate(db, username, password, {})
# # print(uid)  # to check password

# if uid:
#     print("Authenticate")
#     models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# else:
#     print("UnAuthenticate")

# -*- coding: utf-8 -*-
"""
Production-style Odoo REST API controller (single-file example)
Supports:
 - Token-based authentication (simple token model with expiry)
 - Standardized JSON responses
 - Versioned endpoints: /api/v1/...
 - Partner resource with: list, retrieve, create, update (PUT/PATCH), delete (DELETE)
 - Input validation, pagination, basic search and ordering
 - Centralized error handling and logging

Drop this file in: your_module/controllers/api_controller.py
Add the module to addons and update/upgrade.

Notes for production hardening (recommended):
 - Use HTTPS for all traffic
 - Replace simple token model with JWT or OAuth2 if you need scopes / external clients
 - Consider rate-limiting and request logging at Nginx / gateway level
 - Limit sudo usage, apply record rules where possible
 - Add tests and Postman/Swagger documentation

This example is intentionally verbose and descriptive to be a clear, professional reference.
"""

from datetime import datetime, timedelta
import json
import logging
import secrets

from odoo import fields, http
from odoo.http import request
from odoo.exceptions import AccessError, ValidationError

_logger = logging.getLogger(__name__)

API_PREFIX = '/api/v1'
TOKEN_LIFETIME_HOURS = 24


# -----------------------------
# Helper / infrastructure
# -----------------------------

def _now():
    return datetime.utcnow()


def _json_response(body, status=200):
    # body should be a dict with keys: status, data, error (optional)
    payload = json.dumps(body, default=str)
    return request.make_response(payload, headers=[('Content-Type', 'application/json')], status=status)


def _ok(data=None):
    return _json_response({'status': 'ok', 'data': data or {}}, status=200)


def _error(message, code=400, details=None):
    body = {'status': 'error', 'error': {'message': message}}
    if details is not None:
        body['error']['details'] = details
    return _json_response(body, status=code)


# -----------------------------
# Lightweight token model helper
# -----------------------------
# We will create a small internal model `api.token` to store tokens. If the model
# doesn't exist (e.g. not created in module), we will fallback to ir.config_parameter.
# Production: create a real model with proper ACLs.


def _create_token_for_user(user, lifetime_hours=TOKEN_LIFETIME_HOURS):
    token = secrets.token_hex(32)
    expires_at = _now() + timedelta(hours=lifetime_hours)

    Token = request.env['api.token'].sudo() if 'api.token' in request.env else None
    if Token:
        Token.sudo().create({
            'user_id': user.id,
            'token': token,
            'expires_at': expires_at,
        })
    else:
        # fallback (not recommended for production)
        key = f'api.token.{user.id}'
        request.env['ir.config_parameter'].sudo().set_param(key, token)
        request.env['ir.config_parameter'].sudo().set_param(key + '.expires_at', expires_at.isoformat())
    return token, expires_at


def _find_user_by_token(token):
    if not token:
        return None
    Token = request.env['api.token'].sudo() if 'api.token' in request.env else None
    if Token:
        rec = Token.sudo().search([('token', '=', token)], limit=1)
        if not rec:
            return None
        if rec.expires_at and rec.expires_at < fields.Datetime.now():
            # expired
            return None
        return rec.user_id
    else:
        ICP = request.env['ir.config_parameter'].sudo()
        all_params = ICP.search([('key', 'like', 'api.token.%')])
        for p in all_params:
            if p.value == token:
                # key like api.token.<uid>
                try:
                    uid = int(p.key.split('.')[-1])
                    return request.env['res.users'].sudo().browse(uid)
                except Exception:
                    return None
        return None


# Decorator helper

def token_required(func):
    def wrapper(*args, **kwargs):
        token = None
        # Prefer header: Authorization: Bearer <token>
        auth_header = request.httprequest.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
        # Fallback to token param
        if not token:
            token = kwargs.pop('token', None) or request.params.get('token')

        user = None
        try:
            user = _find_user_by_token(token) if token else None
        except Exception as e:
            _logger.exception('Error while finding user by token')
            return _error('Authentication service error', 500)

        if not user or not user.exists():
            return _error('Unauthorized, invalid or expired token', 401)

        # attach current_api_user to request.env for handlers
        request._api_user = user
        return func(*args, **kwargs)

    # preserve name
    wrapper.__name__ = func.__name__
    return wrapper


# -----------------------------
# Controllers
# -----------------------------

class APIAuthController(http.Controller):
    """Authentication-related endpoints
    /api/v1/auth/login  -> POST {login, password}
    /api/v1/auth/logout -> POST (Authorization: Bearer <token>)
    """

    @http.route(API_PREFIX + '/auth/login', type='json', auth='public', csrf=False, methods=['POST'])
    def login(self, **payload):
        try:
            login = payload.get('login')
            password = payload.get('password')
            if not login or not password:
                return _error('Missing credentials', 400)

            # authenticate will raise or return uid (depending on session state)
            try:
                uid = request.session.authenticate(request.db, login, password)
            except Exception:
                return _error('Invalid credentials', 401)

            user = request.env['res.users'].sudo().browse(uid)
            token, expires_at = _create_token_for_user(user)

            data = {
                'uid': uid,
                'token': token,
                'expires_at': expires_at.isoformat() if expires_at else None,
            }
            return _ok(data)
        except Exception as e:
            _logger.exception('Login failed')
            return _error('Internal server error during login', 500)

    @http.route(API_PREFIX + '/auth/logout', type='json', auth='public', csrf=False, methods=['POST'])
    @token_required
    def logout(self, **payload):
        try:
            token = None
            auth_header = request.httprequest.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ', 1)[1].strip()
            if not token:
                token = request.params.get('token')

            Token = request.env['api.token'].sudo() if 'api.token' in request.env else None
            if Token:
                Token.sudo().search([('token', '=', token)]).unlink()
            else:
                # fallback cleanup
                ICP = request.env['ir.config_parameter'].sudo()
                key_to_delete = None
                for p in ICP.search([('key', 'like', 'api.token.%')]):
                    if p.value == token:
                        key_to_delete = p.key
                        break
                if key_to_delete:
                    ICP.sudo().search([('key', '=', key_to_delete)]).unlink()
                    ICP.sudo().search([('key', '=', key_to_delete + '.expires_at')]).unlink()

            return _ok({'message': 'Logged out'})
        except Exception:
            _logger.exception('Logout failed')
            return _error('Internal server error during logout', 500)


class PartnerAPIController(http.Controller):
    """Partners resource controller
    Endpoints:
      GET  /api/v1/partners         -> list (supports ?page=1&per_page=20&name=foo&order=name)
      GET  /api/v1/partners/<id>    -> retrieve
      POST /api/v1/partners         -> create
      PUT  /api/v1/partners/<id>    -> update (full replace)
      PATCH /api/v1/partners/<id>  -> update (partial)
      DELETE /api/v1/partners/<id> -> delete
    All endpoints require token authentication (except you may allow read-only list to public if desired)
    """

    @http.route(API_PREFIX + '/partners', type='json', auth='public', csrf=False, methods=['GET'])
    @token_required
    def list_partners(self, **params):
        try:
            # pagination
            page = int(params.get('page', 1)) if str(params.get('page', '1')).isdigit() else 1
            per_page = int(params.get('per_page', 20)) if str(params.get('per_page', '20')).isdigit() else 20
            offset = (page - 1) * per_page

            # filters (very small example - expand as needed)
            domain = []
            if params.get('name'):
                domain += [('name', 'ilike', params.get('name'))]
            if params.get('email'):
                domain += [('email', 'ilike', params.get('email'))]

            order = params.get('order') or 'id desc'

            partners = request.env['res.partner'].sudo().search(domain, offset=offset, limit=per_page, order=order)
            total = request.env['res.partner'].sudo().search_count(domain)

            data = {
                'items': [
                    {
                        'id': p.id,
                        'name': p.name,
                        'email': p.email,
                        'phone': p.phone,
                        'is_company': bool(p.is_company),
                    } for p in partners
                ],
                'meta': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                }
            }
            return _ok(data)
        except Exception:
            _logger.exception('Error listing partners')
            return _error('Failed to list partners', 500)

    @http.route(API_PREFIX + '/partners/<int:partner_id>', type='json', auth='public', csrf=False, methods=['GET'])
    @token_required
    def get_partner(self, partner_id, **params):
        try:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                return _error('Partner not found', 404)

            data = {
                'id': partner.id,
                'name': partner.name,
                'email': partner.email,
                'phone': partner.phone,
                'street': partner.street,
                'city': partner.city,
                'country': partner.country_id.name if partner.country_id else None,
            }
            return _ok(data)
        except Exception:
            _logger.exception('Error retrieving partner')
            return _error('Failed to retrieve partner', 500)

    @http.route(API_PREFIX + '/partners', type='json', auth='public', csrf=False, methods=['POST'])
    @token_required
    def create_partner(self, **payload):
        try:
            name = payload.get('name')
            if not name:
                return _error('Missing field: name', 400)

            vals = {
                'name': name,
                'email': payload.get('email'),
                'phone': payload.get('phone'),
                'street': payload.get('street'),
                'city': payload.get('city'),
            }
            partner = request.env['res.partner'].sudo().create(vals)

            return _ok({'id': partner.id, 'message': 'Partner created'})
        except ValidationError as e:
            return _error('Validation error', 400, details=str(e))
        except Exception:
            _logger.exception('Error creating partner')
            return _error('Failed to create partner', 500)

    @http.route(API_PREFIX + '/partners/<int:partner_id>', type='json', auth='public', csrf=False, methods=['PUT', 'PATCH'])
    @token_required
    def update_partner(self, partner_id, **payload):
        try:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                return _error('Partner not found', 404)

            # sanitize and whitelist fields to avoid malicious write
            allowed = {'name', 'email', 'phone', 'street', 'city'}
            vals = {k: v for k, v in payload.items() if k in allowed}
            if not vals:
                return _error('No updatable fields provided', 400)

            partner.sudo().write(vals)
            return _ok({'id': partner.id, 'message': 'Partner updated'})
        except ValidationError as e:
            return _error('Validation error', 400, details=str(e))
        except Exception:
            _logger.exception('Error updating partner')
            return _error('Failed to update partner', 500)

    @http.route(API_PREFIX + '/partners/<int:partner_id>', type='json', auth='public', csrf=False, methods=['DELETE'])
    @token_required
    def delete_partner(self, partner_id, **payload):
        try:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                return _error('Partner not found', 404)

            # business rule example: prevent deleting companies that have invoices
            if partner.is_company:
                inv_count = request.env['account.move'].sudo().search_count([('partner_id', '=', partner.id)])
                if inv_count > 0:
                    return _error('Cannot delete company with related invoices', 400)

            partner.sudo().unlink()
            return _ok({'message': 'Partner deleted'})
        except AccessError:
            return _error('Access denied', 403)
        except Exception:
            _logger.exception('Error deleting partner')
            return _error('Failed to delete partner', 500)


# -----------------------------
# Optional: Small model definition instruction (add to module models)
# -----------------------------
# For a real implementation, add a simple model file in your module models/api_token.py:
#
# from odoo import models, fields
#
# class APIToken(models.Model):
#     _name = 'api.token'
#     _description = 'API tokens for external clients'
#
#     user_id = fields.Many2one('res.users', required=True, ondelete='cascade')
#     token = fields.Char(required=True, index=True)
#     expires_at = fields.Datetime()
#     active = fields.Boolean(default=True)
#
# And add appropriate access control (ir.model.access.csv) to allow only appropriate groups to manage tokens.
# -----------------------------

# End of file

    
    
    
    
    
    
    
    
    
    
    
    
    
# from odoo import http
# from odoo.http import request
# from odoo.addons.website.controllers.main import Website


# class WEBNadcoApi(http.Controller):
#     @http.route('/appointment_webform2', type='http', auth='public', website=True)
#     def appointment_webform(self, **kw):
#         print('inside appointment_webform ',kw)
#         return http.request.render('kitchen_design_data.create_break_down_appointment2', {})
    
#     @http.route('/create/web_appointment', type='http', auth='public', website=True)
#     def create_web_appointment(self, **kw):
#         print('inside create web_appointment ',kw)
#         request.env['breakdown.appointment'].sudo().create(kw)
#         return request.render('kitchen_design_data.appointment_thanks2', {})
        