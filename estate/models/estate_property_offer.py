# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

#Definimos el modelo de datos
class EstatePropertyOffer(models.Model):
  #Nombre y descripcion del modelo de datos
  _name = 'estate.property.offer'
  _description = 'Modelo de Oferta Inmobiliaria'
  _order = 'price desc'

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

  #Campo relacionado
  property_type_id = fields.Many2one(
    comodel_name='estate.property.type',
    related='property_id.property_type_id',
    string='Tipo de Propiedad',
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

  # Acción para aceptar la oferta
  def action_accept(self):
    for record in self:
      if record.status == 'accepted':
        # Excepción que evita aceptar una oferta previamente aceptada
        raise UserError("La oferta ya ha sido aceptada.")
      
      if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
        # Excepción que evita aceptar una oferta si ya hay otra aceptada
        raise UserError("Ya existe una oferta aceptada para esta propiedad.")

      record.status = 'accepted'
      record.property_id.state = 'offer_accepted'
      record.property_id.buyer_id = record.partner_id
      record.property_id.selling_price = record.price

  # Acción para rechazar la oferta
  def action_refuse(self):
    for record in self:
      if record.status == 'refused':
        # Excepción que evita rechazar una oferta previamente rechazada
        raise UserError("La oferta ya ha sido rechazada.")
      
      record.status = 'refused'
      # Si la oferta rechazada era la aceptada, limpiar comprador y precio de venta
      if record.property_id.buyer_id == record.partner_id:
        record.property_id.buyer_id = False
        record.property_id.state = 'new'
        if record.property_id.selling_price == record.price:
          record.property_id.selling_price = 0

  # Sobrescribe el método create para añadir validaciones y lógica adicional
  @api.model
  def create(self, vals_list):   
    # Validar que el precio no sea inferior a ofertas existentes
    for vals in vals_list:
      if vals.get('property_id') and vals.get('price'):
        property_id = vals['property_id']
        new_price = vals['price']
        
        # Buscar ofertas existentes para esta propiedad
        existing_offers = self.search([('property_id', '=', property_id)])
        if existing_offers:
          max_existing_price = max(existing_offers.mapped('price'))
          if new_price < max_existing_price:
            raise UserError(f'El precio de la oferta ({new_price:.2f}) no puede ser inferior al de la máxima oferta existente ({max_existing_price:.2f}).')
    
    # Al crear las nuevas ofertas, cambia el estado de la propiedad a 'offer_received'
    offers = super().create(vals_list)
    for offer in offers:
      if offer.property_id.state == 'new':
        offer.property_id.state = 'offer_received'
    return offers

  # Restricciones SQL
  _check_price = models.Constraint('CHECK(price >= 0)', 'El precio de la oferta no puede ser negativo.')
