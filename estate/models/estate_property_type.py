from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipus de Propietats immobiliàries'
    name = fields.Char('Tipus', required=True)