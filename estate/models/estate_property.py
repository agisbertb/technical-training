from odoo import fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Propietats Inmobiliàries'
    name = fields.Char('Propietat Inmobiliària', required=True)
    description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal', required=True)
    date_availability = fields.Date('Data Disponibilitat', copy=False, default=lambda self: (datetime.now() + timedelta(days=30)).date())
    expected_price = fields.Float('Preu Esperat')
    selling_price = fields.Float('Preu de Venda', readonly=True, copy=False)
    best_offer = fields.Float('Millor Oferta', compute='_compute_best_offer', readonly=True)
    state = fields.Selection([('new', 'Nou'), ('offer_received', 'Oferta Rebut'), ('offer_accepted', 'Oferta Acceptada'), ('sold', 'Venut'), ('canceled', 'Cancel·lat')], string='Estat', default='new')
    bedrooms = fields.Integer('Habitacions', required=True)
    lift = fields.Boolean('Ascensor', default=False)
    parking = fields.Boolean('Parking', default=False)
    renewed = fields.Boolean('Renovat', default=False)
    bathrooms = fields.Integer('Banys', default=False)
    surface = fields.Integer('Superfície', required=True)
    price_per_sqm = fields.Float('Preu per m2', compute='_compute_price_per_sqm', readonly=True)
    year_build = fields.Integer('Any de Construcció')
    energy_certificate = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G')
    ], string='Certificat Energètic (Lletra)')
    active = fields.Boolean(default=True)
    offer_count = fields.Integer(compute='_compute_offer_count')
    buyer_id = fields.Many2one('res.partner', string='Comprador')
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    type_ids = fields.Many2one('estate.property.type',string='Tipus')