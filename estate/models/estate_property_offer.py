from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Ofertes per a les Propietats immobiliàries"
    price = fields.Float('Preu')
    state = fields.Selection([('Accepted', 'Acceptada'), ('Rejected', 'Rebutjada'), ('Processing', 'En tractament')], default='Processing',
    string='Estat',  copy=False)
    comments = fields.Text('Comentaris')
    partner_id = fields.Many2one('res.partner', string='Comprador', required=True)
    property_id = fields.Many2one('estate.property', string='Propietat', required=True)
    buyer_id = fields.Many2one('res.partner', string='Comprador')

    @api.constrains('state')
    def _check_unique_acceptance(self):
        for offer in self:
            if offer.state == 'Accepted':
                accepted_offers = self.search([
                    ('property_id', '=', offer.property_id.id),
                    ('state', '=', 'Accepted'),
                    ('id', '!=', offer.id)
                ])
                if accepted_offers:
                    raise ValidationError("Ja existeix una oferta acceptada per a aquesta propietat.")
                    