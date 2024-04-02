from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Propietats Inmobiliàries'
    name = fields.Char('Propietat Inmobiliària', required=True)
    description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal', required=True)
    date_availability = fields.Date('Data Disponibilitat', copy=False, default=lambda self: (datetime.now() + timedelta(days=30)).date())
    expected_selling_price = fields.Float('Preu Esperat')
    selling_price = fields.Float('Preu de Venda', readonly=True, copy=False, store=True, compute='_update_selling_details_on_offer_acceptance')
    state = fields.Selection([('new', 'Nou'), ('offer_received', 'Oferta Rebuda'), ('offer_accepted', 'Oferta Acceptada'),
    ('rejected', 'Rebutjat'), ('sold', 'Venut'), ('canceled', 'Cancel·lat')], string='Estat', default='new')
    bedrooms = fields.Integer('Habitacions', required=True)
    lift = fields.Boolean('Ascensor', default=False)
    parking = fields.Boolean('Parking', default=False)
    renewed = fields.Boolean('Renovat', default=False)
    bathrooms = fields.Integer('Banys', default=False)
    surface = fields.Integer('Superfície', required=True)
    avg_price = fields.Float('Preu per m2', compute='_calcularPreuPerMetre')
    year_build = fields.Integer('Any de Construcció')
    energy_certificate = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G')
    ], string='Certificat Energètic')
    active = fields.Boolean(default=True, invisible=True)
    offer_count = fields.Integer(compute='_compute_offer_count')
    buyer_id = fields.Many2one('res.partner', string='Comprador', compute='_update_selling_details_on_offer_acceptance', store=True)
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    type_ids = fields.Many2one('estate.property.type', string='Tipus')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Ofertes')
    best_offer = fields.Float('Millor Oferta', readonly=True, compute='_compute_best_offer')

    @api.depends('expected_selling_price', 'surface')
    def _calcularPreuPerMetre(self):
        for record in self:
            if record.surface > 0:
                record.avg_price = record.expected_selling_price / record.surface
            else:
                record.avg_price = None

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            best_offer = max(record.offer_ids.filtered(lambda offer: offer.state != 'rejected'), key=lambda offer: offer.price, default=None)
            record.best_offer = best_offer.price if best_offer else None

    @api.depends('offer_ids', 'offer_ids.state', 'offer_ids.price', 'offer_ids.partner_id')
    def _update_selling_details_on_offer_acceptance(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda offer: offer.state == 'Accepted')

            if accepted_offer:
                record.selling_price = accepted_offer.price
                record.buyer_id = accepted_offer.partner_id
            else:
                record.selling_price = ''
                record.buyer_id = ''
                
    _sql_constraints = [
        ('check_positive_expected_selling_price',
    'CHECK(expected_selling_price >= 0)',
        'El preu esperat ha de ser positiu.'),

        ('check_positive_selling_price',
        'CHECK(selling_price >= 0)',
        'El preu de venda ha de ser positiu.'),

        ('check_positive_surface',
        'CHECK(surface >= 0)',
        'La superfície ha de ser positiva.'),

        ('check_positive_bedrooms',
        'CHECK(bedrooms >= 0)',
        'El nombre d\'habitacions ha de ser positiu.'),

        ('check_positive_bathrooms',
        'CHECK(bathrooms >= 0)',
        'El nombre de banys ha de ser positiu.'),

        ('check_positive_year_build',
        'CHECK(year_build >= 0)',
        'L\'any de construcció ha de ser positiu.')
    ]

    @api.depends('selling_price', 'expected_selling_price')
    def _check_selling_price_vs_expected_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_selling_price*0.9:
                raise ValidationError('El preu de venda no pot ser inferior al preu esperat.')