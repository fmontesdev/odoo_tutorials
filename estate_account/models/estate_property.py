# -*- coding: utf-8 -*-

from odoo import models, fields, Command

#Definimos el modelo de datos
class EstateProperty(models.Model):
  _inherit = 'estate.property'

  # Relación Many2one con account.move para la factura asociada a la propiedad vendida
  invoice_id = fields.Many2one(
    comodel_name='account.move',
    string='Factura',
    readonly=True,
    copy=False
  )

  def action_set_sold(self):
    # print("\n" + "="*50, flush=True)
    # print("ESTATE_ACCOUNT: Método action_set_sold llamado", flush=True)
    # print("="*50 + "\n", flush=True)

    # Llamamos al método original para mantener su funcionalidad
    # Sin super, el método original no se ejecutaría
    result = super().action_set_sold()
    AccountMove = self.env['account.move']
    for property in self:
      if property.state == 'sold' and not property.invoice_id:
        # Crea la factura con sus líneas
        invoice_vals = {
          'partner_id': property.buyer_id.id,
          'move_type': 'out_invoice',
          'invoice_line_ids': [
            Command.create({
              'name': f'Compra de propiedad: {property.name}',
              'quantity': 1,
              'price_unit': property.selling_price * 0.06,
            }),
            Command.create({
              'name': 'Gastos administrativos',
              'quantity': 1,
              'price_unit': 100.00,
            })
          ],
        }
        invoice = AccountMove.create(invoice_vals)
        property.invoice_id = invoice
    return result
