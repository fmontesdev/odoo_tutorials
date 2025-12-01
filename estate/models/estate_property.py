# -*- coding: utf-8 -*-

from odoo import models, fields

#Definimos el modelo de datos
class EstateProperty(models.Model):
    #Nombre y descripcion del modelo de datos
    _name = 'estate.property'
    _description = 'Modelo de la propiedad inmobiliaria'

    # Los atributos siguientes no se declaran, odoo los gestiona solo: id, create_uid, create_date, write_uid, write_dates

    name = fields.Char(string='Título', required=True)
    description = fields.Text(string='Descripción')
    postcode = fields.Char(string='Código Postal')
    date_availability = fields.Date(string='Disponible Desde')
    expected_price = fields.Float(string='Precio Esperado', required=True)
    selling_price = fields.Float(string='Precio de Venta')
    bedrooms = fields.Integer(string='Dormitorios')
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

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'El precio esperado no puede ser negativo.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'El precio de venta no puede ser negativo.'),
        ('check_bedrooms', 'CHECK(bedrooms >= 0)', 'El número de dormitorios no puede ser negativo.'),
        ('check_living_area', 'CHECK(living_area >= 0)', 'El área habitable no puede ser negativa.'),
        ('check_facades', 'CHECK(facades >= 0)', 'El número de fachadas no puede ser negativo.'),
        ('check_garden_area', 'CHECK(garden_area >= 0)', 'El área del jardín no puede ser negativa.'),
    ]
