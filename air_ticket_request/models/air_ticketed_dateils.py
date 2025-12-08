from odoo import models, fields, api, _


class AirTicketDetails(models.Model):
    _name = 'air.ticket.details'
    _description = 'Air Ticket Details'
    
    name = fields.Char(string='Name', readonly=True)
    request_id = fields.Many2one('air.ticket.request', string='Air Ticket Request')
    check_box = fields.Boolean(string='Check')
    name_in_passport = fields.Char(string='Name in Passport')
    relation = fields.Char(string='Relation', readonly=True)
    ticket_type = fields.Selection([
        ('one_way', 'One Way'),
        ('return', 'Return')
    ], string='Ticket Type')
    departure_date = fields.Date(string='Departure Date')
    departure_airport = fields.Char(string='Departure Airport')
    flight_number = fields.Char(string='Flight Number')
    airlines = fields.Char(string='Airlines')
    return_date = fields.Date(string='Return Date')
    return_airport = fields.Char(string='Return Airport')
    return_flight_number = fields.Char(string='Return Flight Number')
    return_airlines = fields.Char(string='Return Airlines')
    ticket_price = fields.Float(string='Ticket Price')
    notes = fields.Text(string='Notes')
    date_of_birth = fields.Date(string='Date of Birth')
    current_age = fields.Char(string='Current Age', readonly=True)

class AirTicketRequestAttachment(models.Model):
    _name = 'air.ticket.request.attachment'
    _description = 'Air Ticket Request Attachment'
    
    source_id = fields.Many2one('air.ticket.request', string='Air Ticket Request')
    file = fields.Binary(string='File', required=True)
    name = fields.Char(string='Name', required=True)
    file_name = fields.Char(string='File Name')
    note = fields.Char(string='Note')
   