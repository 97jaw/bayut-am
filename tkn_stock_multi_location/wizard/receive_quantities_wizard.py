# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ReceiveQuantitiesWizard(models.TransientModel):
    _name = 'receive.quantities.wizard'
    _description = 'Receive Quantity Wizard'

    stock_product_id = fields.Many2one("product.product", string="Product", readonly=True)
    receive_quantities_line_ids = fields.One2many('receive.quantities.line', 'wizard_id',
                                                  string="Receive Quantities")
    demand_quantity = fields.Float(readonly=True, string="Demand")

    @api.model
    def default_get(self, fields):
        res = super(ReceiveQuantitiesWizard, self).default_get(fields)
        stock_move = self.env['stock.move'].browse(self._context.get('active_id'))
        if not stock_move:
            return res

        res['stock_product_id'] = stock_move.product_id.id
        res['demand_quantity'] = stock_move.product_uom_qty

        internal_locations = self.env['stock.location'].search([('usage', '=', 'internal')])
        line_vals = []
        for location in internal_locations:
            line_vals.append((0, 0, {
                'product_id': stock_move.product_id.id,
                'destination_location_id': location.id,
            }))
        res['receive_quantities_line_ids'] = line_vals

        return res

    def apply_quantities(self):
        stock_move = self.env['stock.move'].browse(self._context.get('active_id'))
        if not stock_move:
            raise UserError("No active stock move found.")

        if not self.receive_quantities_line_ids:
            raise UserError("No quantities selected to receive!")

        picking_id = stock_move.picking_id
        purchase_line_id = stock_move.purchase_line_id.id

        # Search in the lines for the same location name
        for line in self.receive_quantities_line_ids:
            if line.qty_received > 0:
                existing_move = self.env['stock.move'].search([
                    ('picking_id', '=', picking_id.id),
                    ('product_id', '=', self.stock_product_id.id),
                    ('location_id', '=', stock_move.location_id.id),
                    ('location_dest_id', '=', line.destination_location_id.id),
                    ('purchase_line_id', '=', purchase_line_id),
                ], limit=1)
                # If found, we adjust the quantity only and do not add a new line.
                if existing_move:
                    existing_move.write({
                        'product_uom_qty': line.qty_received,
                        'quantity': line.qty_received,
                    })
                    # If there is no location, add a new line.
                else:
                    self.env['stock.move'].create({
                        'picking_id': picking_id.id,
                        'name': self.stock_product_id.name,
                        'product_id': self.stock_product_id.id,
                        'location_id': stock_move.location_id.id,
                        'location_dest_id': line.destination_location_id.id,
                        'product_uom': stock_move.product_uom.id,
                        'product_uom_qty': line.qty_received,
                        'quantity': line.qty_received,
                        'purchase_line_id': purchase_line_id,
                    })

        return {'type': 'ir.actions.act_window_close'}


class ReceiveQuantitiesLine(models.TransientModel):
    _name = 'receive.quantities.line'
    _description = 'Receive Quantities Line'

    wizard_id = fields.Many2one('receive.quantities.wizard', string="Wizard", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    destination_location_id = fields.Many2one('stock.location', string="Destination Location",  domain=[('usage', '=', 'internal')])
    qty_received = fields.Float(string="Qty Received")
    quantity = fields.Float(string="Available Quantity")
