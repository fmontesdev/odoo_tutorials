# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import models, fields

#Definimos el modelo de datos
class EstateProperty(models.Model):
  #Nombre y descripcion del modelo de datos
  _name = 'estate.property'
  _description = 'Modelo de la propiedad inmobiliaria'

  # Los atributos siguientes no se declaran, odoo los gestiona solo: id, create_uid, create_date, write_uid, write_dates
  name = fields.Char(string='Nombre', required=True)
  description = fields.Text(string='Descripción')
  postcode = fields.Char(string='Código Postal')
  date_availability = fields.Date(
    string='Disponible Desde',
    default=lambda self: fields.Date.today() + relativedelta(months=3),
    copy=False
  )
  expected_price = fields.Float(string='Precio Esperado', required=True)
  selling_price = fields.Float(string='Precio de Venta', readonly=True, copy=False)
  bedrooms = fields.Integer(string='Dormitorios', default=2)
  living_area = fields.Integer(string='Área Habitable')
  facades = fields.Integer(string='Fachadas')
  garage = fields.Boolean(string='Garaje')
  garden = fields.Boolean(string='Jardín')
  garden_area = fields.Integer(string='Área del Jardín')
  garden_orientation = fields.Selection([
    ('north', 'Norte'),
    ('south', 'Sur'),
    ('east', 'Este'),
    ('west', 'Oeste'),
  ], string='Orientación del Jardín')
  state = fields.Selection([
    ('new', 'Nuevo'),
    ('offer_received', 'Oferta Recibida'),
    ('offer_accepted', 'Oferta Aceptada'),
    ('sold', 'Vendido'),
    ('canceled', 'Cancelado'),
  ], string='Estado', default='new')
  active = fields.Boolean(default=True)

  # Relación Many2one con estate.property.type para el tipo de propiedad
  property_type_id = fields.Many2one(
    comodel_name='estate.property.type',
    string='Tipo de Propiedad',
  )

  # Relación Many2one con res.users para el vendedor
  salesman_id = fields.Many2one(
    comodel_name='res.users',
    string='Vendedor',
    default=lambda self: self.env.user,
  )

  # Relación Many2one con res.partner para el comprador
  buyer_id = fields.Many2one(
    comodel_name='res.partner',
    string='Comprador',
  )

  # Relación Many2many con estate.property.tag para las etiquetas
  tag_ids = fields.Many2many(
    comodel_name='estate.property.tag',
    string='Etiquetas'
  )

  # Relación One2many con estate.property.offer para las ofertas
  offer_ids = fields.One2many(
    comodel_name='estate.property.offer',
    inverse_name='property_id',
    string='Ofertas'
  )

  _sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price >= 0)', 'El precio esperado no puede ser negativo.'),
    ('check_selling_price', 'CHECK(selling_price >= 0)', 'El precio de venta no puede ser negativo.'),
    ('check_bedrooms', 'CHECK(bedrooms >= 0)', 'El número de dormitorios no puede ser negativo.'),
    ('check_living_area', 'CHECK(living_area >= 0)', 'El área habitable no puede ser negativa.'),
    ('check_facades', 'CHECK(facades >= 0)', 'El número de fachadas no puede ser negativo.'),
    ('check_garden_area', 'CHECK(garden_area >= 0)', 'El área del jardín no puede ser negativa.'),
  ]
