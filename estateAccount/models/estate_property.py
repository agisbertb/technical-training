from odoo import Command, models

import logging
_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"
 
    def vendre_propietat(self):
        _logger.info("vendre propietat")
        self.env['account.move'].create(
        {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    "name": "Comisió",
                    "quantity": "1",
                    "price_unit": 0.06*self.selling_price,
                }),
                Command.create({
                    "name": "Despeses administratives",
                    "quantity": "1",
                    "price_unit": "100",
                }),                
            ],
        }
        )
        return super().vendre_propietat()