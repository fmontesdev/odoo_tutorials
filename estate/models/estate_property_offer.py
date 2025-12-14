# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

#Definimos el modelo de datos
class EstatePropertyOffer(models.Model):
  #Nombre y descripcion del modelo de datos
  _name = 'estate.property.offer'
  _description = 'Modelo de Oferta Inmobiliaria'

  # Los atributos siguientes no se declaran, odoo los gestiona solo: id, create_uid, create_date, write_uid, write_dates
  price = fields.Float(string='Precio')
  status = fields.Selection([
    ('accepted', 'Aceptada'),
    ('refused', 'Rechazada'),
  ], string='Estado', copy=False)

  # Relación Many2one con estate.property para la propiedad
  property_id = fields.Many2one(
    comodel_name='estate.property',
    required=True
  )

  # Relación Many2one con res.partner para el comprador
  partner_id = fields.Many2one(
    comodel_name='res.partner',
    string='Ofertante',
    required=True
  )

  # Campos calculados
  validity = fields.Integer(
    string='Validez (días)',
    default=7
  )
  date_deadline = fields.Date(
    string='Fecha Límite',
    compute='_compute_date_deadline',
    inverse='_inverse_date_deadline',
    store=True,
  )

  # Método para calcular la fecha límite
  @api.depends('create_date', 'validity')
  def _compute_date_deadline(self):
    for record in self:
      if record.create_date:
        record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
      else:
        record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)
  
  # Método inverso para actualizar la validez cuando se cambia la fecha límite
  def _inverse_date_deadline(self):
    for record in self:
      if record.create_date and record.date_deadline:
        delta = record.date_deadline - record.create_date.date()
        record.validity = delta.days
      else:
        delta = record.date_deadline - fields.Date.today()
        record.validity = delta.days
