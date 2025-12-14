# -*- coding: utf-8 -*-

from odoo import models, fields

#Definimos el modelo de datos
class EstatePropertyTag(models.Model):
  #Nombre y descripcion del modelo de datos
  _name = 'estate.property.tag'
  _description = 'Modelo de Etiqueta de propiedad inmobiliaria'

  # Los atributos siguientes no se declaran, odoo los gestiona solo: id, create_uid, create_date, write_uid, write_dates
  name = fields.Char(string='Nombre', required=True)

  # Relación Many2many con estate.property
  property_ids = fields.Many2many(
    comodel_name='estate.property'
  )
