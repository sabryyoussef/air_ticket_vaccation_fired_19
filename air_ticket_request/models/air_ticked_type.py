
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AirTicketType(models.Model):
    _name = 'air.ticket.type'
    _description = 'Air Ticket Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Status fields
    state = fields.Selection([
        ('New', 'New'),
        ('Approved', 'Approved')
    ], string='Status', default='New', tracking=True, readonly=True)

    # Basic information
   
    name = fields.Char(string='Code', readonly=True, default='New',tracking=True)
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('air.ticket.type') or 'New'
        return super().create(vals)
    
    
    
    policy_name = fields.Char(string='Air Ticket Policy Name', tracking=True)
    type = fields.Selection([
        ('annual', 'Annual'),
        ('non-annual', 'Non-Annual')
    ], string='Air ticket Type', required=True, tracking=True)
    
    # Nationality settings
    nationality = fields.Selection([
        ('Native', 'Native'),
        ('Non-native', 'Non-native'),
        ('All Nationalities', 'All Nationalities')
    ], string='Nationality', tracking=True)
    
    can_request_exit_rentry = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Can request For Exist and R-entry', tracking=True)

    # Frequency and allocation settings
    frequency_air_ticket = fields.Selection([
        ('one time each', 'One Time Each'),
        ('Not allowed', 'Not Allowed'),
        ('other', 'Other')
    ], string='Frequency Air Ticket', tracking=True)
    
    number_of_months = fields.Float(string='Each', tracking=True)
    months_to_request_air_ticket = fields.Integer(
        string='The employee is allowed to request air ticket if his balance is greater than',
        tracking=True
    )
    maximum_accumulated_balance = fields.Integer(
        string='Maximum accumulated balance',
        tracking=True
    )
    
    allocation_technique = fields.Selection([
        ('fixed', 'Fixed'),
        ('proportional', 'Proportional')
    ], string='Allocation Technique', tracking=True)
    
    allocation_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('quarterly', 'Quarterly')
    ], string='Allocation Period', tracking=True)

    # Ticket settings
    air_ticket_class = fields.Selection([
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class')
    ], string='Air ticket class', tracking=True)
    
    give_cash_instead_tickets = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Allow to give cash to employees instead of tickets', tracking=True)

    # Relatives settings
    relatives_tickets = fields.Selection([
        ('Allow tickets for relatives', 'Allow tickets for relatives'),
        ('No tickets for relatives', 'No tickets for relatives')
    ], string='Relatives Tickets', tracking=True)
    
    number_of_wives = fields.Integer(string='Number Of Wives', tracking=True)
    children = fields.Integer(string='Number Of Children', tracking=True)
    max_child_age = fields.Integer(string='Max Age For Children', tracking=True)
    number_of_relatives = fields.Float(
        string='Number of relatives',
        compute='_compute_number_of_relatives',
        store=True,
        readonly=True
    )

    # Related models
    # loan_type_id = fields.Many2one(
    #     'hr_loans.loan_advance',
    #     string='Loan type',
    #     domain="[('type', '=', 'Loan'), ('for_air_ticket', '=', True)]",
    #     tracking=True
    # )
    
    air_ticket_request_ids = fields.One2many(
        'air.ticket.request',
        'air_ticket_type',
        string='Air ticket requests',
        readonly=True
    )
    
    air_ticket_request_count = fields.Integer(
        string='Number of requests',
        compute='_compute_air_ticket_request_count',
        store=True
    )

    # Additional fields
    notes = fields.Text(string='Notes', tracking=True)

    # Computed methods
    @api.depends('number_of_wives', 'children')
    def _compute_number_of_relatives(self):
        for record in self:
            record.number_of_relatives = record.number_of_wives + record.children

    @api.depends('air_ticket_request_ids')
    def _compute_air_ticket_request_count(self):
        for record in self:
            record.air_ticket_request_count = len(record.air_ticket_request_ids)

    # Action methods
    def ticket_approve(self):
        for record in self:
            if record.state != 'New':
                raise ValidationError(_("Only New air ticket types can be approved."))
            record.state = 'Approved'

    def ticket_set_new(self):
        for record in self:
            if record.state != 'Approved':
                raise ValidationError(_("Only Approved air ticket types can be set to New."))
            record.state = 'New'

    def open_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Air Ticket Requests'),
            'res_model': 'air.ticket.request',
            'view_mode': 'tree,form',
            'domain': [('air_ticket_type', '=', self.id)],
            'context': {'default_air_ticket_type': self.id}
        }

    # Constraints
    @api.constrains('frequency_air_ticket', 'air_ticket_class')
    def _check_air_ticket_class_required(self):
        for record in self:
            if (record.frequency_air_ticket != 'Not allowed' and 
                not record.air_ticket_class):
                raise ValidationError(_("Air ticket class is required when frequency is not 'Not allowed'."))

    @api.constrains('frequency_air_ticket', 'give_cash_instead_tickets')
    def _check_cash_instead_required(self):
        for record in self:
            if (record.frequency_air_ticket != 'Not allowed' and 
                not record.give_cash_instead_tickets):
                raise ValidationError(_("Cash instead of tickets option is required when frequency is not 'Not allowed'."))

    @api.constrains('frequency_air_ticket', 'relatives_tickets')
    def _check_relatives_tickets_required(self):
        for record in self:
            if (record.frequency_air_ticket != 'Not allowed' and 
                not record.relatives_tickets):
                raise ValidationError(_("Relatives tickets option is required when frequency is not 'Not allowed'."))