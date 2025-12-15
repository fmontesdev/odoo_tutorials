# -*- coding: utf-8 -*-
{
  'name': 'Contabilidad Inmobiliaria',
  'summary': 'Generación de facturas para propiedades inmobiliarias',
  'description': 'Módulo para generar facturas de las propiedades inmobiliarias vendidas',
  'author': 'Francisco Montés Doria',
  'website': '',
  # En la siguiente URL se indica que categorias pueden usarse
  # https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
  'category': 'Sales',
  'version': '0.1',
  # Indicamos que es una aplicación
  'application': False,
  'installable': True,
  # Indicamos lista de modulos necesarios para que este funcione correctamente
  'depends': ['estate', 'account'],
  # Carga los archivos para la política de seguridad y las vistas
  'data': [],
}
