# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Definimos el modelo de datos
class EstatePropertyType(models.Model):
  #Nombre y descripcion del modelo de datos
  _name = 'estate.property.type'
  _description = 'Modelo del tipo de propiedad inmobiliaria'
  _order = 'sequence, name' # Ordenar por secuencia y luego por nombre

  # Los atributos siguientes no se declaran, odoo los gestiona solo: id, create_uid, create_date, write_uid, write_dates
  name = fields.Char(string='Nombre', required=True)
  sequence = fields.Integer(string='Secuencia', default=1)

  # Relación One2many con estate.property
  property_ids = fields.One2many(
    comodel_name='estate.property',
    inverse_name='property_type_id',
    string='Propiedades'
  )

  # Relación One2many con estate.property.offer (campos relacionado)
  offer_ids = fields.One2many(
    comodel_name='estate.property.offer',
    inverse_name='property_type_id',
    string='Ofertas'
  )

  # Campo calculado
  offer_count = fields.Integer(
    string='Número de Ofertas',
    compute='_compute_offer_count',
  )

  # Método para calcular el número de ofertas asociadas a este tipo de propiedad
  @api.depends('offer_ids')
  def _compute_offer_count(self):
    for record in self:
      # Cuenta el número de ofertas relacionadas
      record.offer_count = len(record.offer_ids)

  # Restricciones SQL
  _uniq_type_name = models.Constraint('UNIQUE(name)', 'El nombre del tipo de propiedad debe ser único')
