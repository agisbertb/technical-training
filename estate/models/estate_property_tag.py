from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property_tag'
    description = 'Etiquetes per a les propietats immobiliàries'
    name = fields.Char('Etiqueta', required=True)
    