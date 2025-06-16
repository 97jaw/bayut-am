# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AvailableQuantitiesWizard(models.TransientModel):
    _name = 'available.quantities.wizard'
    _description = 'Available Quantity Wizard'

    stock_product_id = fields.Many2one("product.product", string="Product", readonly=True)
    available_quantities_line_ids = fields.One2many('available.quantities.line', 'wizard_id',
                                                    string="Available Quantities")

    @api.model
    def default_get(self, fields):
        res = super(AvailableQuantitiesWizard, self).default_get(fields)
        stock_move = self.env['stock.move'].browse(self._context.get('active_id'))
        if not stock_move:
            return res

        res['stock_product_id'] = stock_move.product_id.id
        stock_quant_id = self.env['stock.quant'].search(
            [('product_id', '=', stock_move.product_id.id), ('location_id.usage', '=', 'internal')]
        )

        line_data = {}

        for quant in stock_quant_id:
            location_id = quant.location_id.id
            if location_id in line_data:
                line_data[location_id]['quantity'] += quant.quantity
            else:
                line_data[location_id] = {
                    'product_id': quant.product_id.id,
                    'location_id': location_id,
                    'quantity': quant.quantity,
                }

        if line_data:
            res['available_quantities_line_ids'] = [(0, 0, data) for data in line_data.values()]

        return res

    def apply_quantities(self):
        stock_move = self.env['stock.move'].browse(self._context.get('active_id'))
        if not stock_move:
            raise UserError("No active stock move found.")

        if not self.available_quantities_line_ids:
            raise UserError("No quantities selected to move!")

        sale_line_id = stock_move.sale_line_id.id
        group_id = stock_move.group_id.id
        picking_id = stock_move.picking_id

        for quant in self.available_quantities_line_ids:
            if quant.qty_moved > 0:
                stock_move_lines = stock_move.filtered(
                    lambda line: line.location_id == quant.location_id and line.location_id == quant.location_id and
                                 quant.qty_moved > 0
                )
                if stock_move_lines:
                    # Update the quantity in the existing line
                    stock_move_lines[0].quantity = quant.qty_moved

                    stock_move_lines[0].product_uom_qty = quant.qty_moved
                else:
                    # Create a new move line
                    self.env['stock.move'].create({
                        'picking_id': picking_id.id,
                        'name': self.stock_product_id.name,
                        'product_id': self.stock_product_id.id,
                        'location_id': quant.location_id.id,
                        'location_dest_id': stock_move.location_dest_id.id,
                        'product_uom': stock_move.product_uom.id,
                        'product_uom_qty': quant.qty_moved,
                        'quantity': quant.qty_moved,
                        'sale_line_id': sale_line_id,
                        'group_id': group_id,
                    })

        return {'type': 'ir.actions.act_window_close'}


class AvailableQuantitiesLine(models.TransientModel):
    _name = 'available.quantities.line'
    _description = 'Available Quantities Line'

    wizard_id = fields.Many2one('available.quantities.wizard', string="Wizard", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    location_id = fields.Many2one('stock.location', string="Location")
    quantity = fields.Float(string="Available Quantity")
    qty_moved = fields.Float(string="Qty Moved")
