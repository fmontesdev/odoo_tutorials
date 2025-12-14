# -*- coding: utf-8 -*-

from odoo import models, fields

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
