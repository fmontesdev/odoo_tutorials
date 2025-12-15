# -*- coding: utf-8 -*-

from odoo import models, fields

# Extensión del modelo res.users a través de herencia
class ResUsers(models.Model):
  _inherit = 'res.users'
  
  # Relación One2many con estate.property para las propiedades vendidas por el usuario
  property_ids = fields.One2many(
    comodel_name='estate.property',
    inverse_name='salesman_id',
    string='Propiedades',
    domain=[('state', 'in', ['new', 'offer_received'])]
  )