# -*- coding: utf-8 -*-

from odoo import models, fields

#Definimos el modelo de datos
class EstatePropertyType(models.Model):
  #Nombre y descripcion del modelo de datos
  _name = 'estate.property.type'
  _description = 'Modelo del tipo de propiedad inmobiliaria'

  # Los atributos siguientes no se declaran, odoo los gestiona solo: id, create_uid, create_date, write_uid, write_dates
  name = fields.Char(string='Nombre', required=True)

  # Relación One2many con estate.property
  property_ids = fields.One2many(
    comodel_name='estate.property',
    inverse_name='property_type_id'
  )
