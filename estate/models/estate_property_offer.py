from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Ofertes per a les Propietats immobiliàries"
    price = fields.Float('Preu')
    status = fields.Selection([('Accepted', 'Acceptada'), ('Refused', 'Rebutjada'), ('Processing', 'En tractament')], default='Processing', string='Estat',  copy=False)
    comments = fields.Text('Comentaris')
    partner_id = fields.Many2one('res.partner', string='Comprador', required=True)
    property_id = fields.Many2one('estate.property', string='Propietat', required=True)