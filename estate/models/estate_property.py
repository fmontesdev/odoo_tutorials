# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

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

  # Campos calculados
  total_area = fields.Integer(
    string='Área Total',
    compute='_compute_total_area',
    store=True
  )
  best_price = fields.Float(
    string='Mejor Oferta',
    compute='_compute_best_price'
  )

  # Método para calcular el área total
  @api.depends('living_area', 'garden_area')
  def _compute_total_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area # Suma el área habitable y el área del jardín

  # Método para calcular la mejor oferta
  @api.depends('offer_ids.price')
  def _compute_best_price(self):
    for record in self:
      if record.offer_ids:
        record.best_price = max(record.offer_ids.mapped('price')) # Obtiene el precio máximo de las ofertas
      else:
        record.best_price = 0.0

  # Método onChange para actualizar los valores de área y orientación del jardín cuando se cambia el campo garden
  @api.onchange('garden')
  def _onchange_garden(self):
    if self.garden:
      self.garden_area = 10
      self.garden_orientation = 'north'
    else:
      self.garden_area = 0
      self.garden_orientation = False

  # Acciones para cambiar el estado de la propiedad
  def action_set_sold(self):
    for record in self:
      if record.state == 'sold':
        # Excepción que evita vender una propiedad previamente vendida
        raise UserError("La propiedad ya está vendida.")
      if record.state == 'canceled':
        # Excepción que evita vender una propiedad cancelada
        raise UserError("No se puede vender una propiedad cancelada.")
      if not record.offer_ids.filtered(lambda o: o.status == 'accepted'):
        # Excepción que evita vender una propiedad sin oferta aceptada
        raise UserError("No se puede vender una propiedad sin una oferta aceptada.")
      record.state = 'sold'
  
  def action_set_canceled(self):
    for record in self:
      if record.state == 'canceled':
        # Excepción que evita cancelar una propiedad previamente cancelada
        raise UserError("La propiedad ya está cancelada.")
      if record.state == 'sold':
        # Excepción que evita cancelar una propiedad vendida
        raise UserError("No se puede cancelar una propiedad vendida.")
      if record.offer_ids.filtered(lambda o: o.status == 'accepted'):
        # Excepción que evita cancelar una propiedad con oferta aceptada
        raise UserError("No se puede cancelar una propiedad con una oferta aceptada.")
      record.state = 'canceled'

  # Restricciones SQL
  _sql_constraints = [
    ('check_expected_price', 'CHECK(expected_price >= 0)', 'El precio esperado no puede ser negativo.'),
    ('check_selling_price', 'CHECK(selling_price >= 0)', 'El precio de venta no puede ser negativo.'),
    ('check_bedrooms', 'CHECK(bedrooms >= 0)', 'El número de dormitorios no puede ser negativo.'),
    ('check_living_area', 'CHECK(living_area >= 0)', 'El área habitable no puede ser negativa.'),
    ('check_facades', 'CHECK(facades >= 0)', 'El número de fachadas no puede ser negativo.'),
    ('check_garden_area', 'CHECK(garden_area >= 0)', 'El área del jardín no puede ser negativa.'),
  ]
