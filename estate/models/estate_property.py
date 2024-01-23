from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    name = fields.Char('Propietat Inmobiliària', required=True)
    description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal')
    date_availability = fields.Date('Data Disponibilitat')
    selling_price = fields.Float('Preu de Venda')
    bedrooms = fields.Integer('Habitacions')
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'Nou'), ('offer_received', 'Oferta Rebut'), ('offer_accepted', 'Oferta Acceptada'), ('sold', 'Venut'), ('canceled', 'Cancel·lat')], string='Estat', default='new')