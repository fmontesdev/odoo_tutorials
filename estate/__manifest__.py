# -*- coding: utf-8 -*-
{
    'name': 'Inmobiliaria',
    'summary': 'Venta de propiedades inmobiliarias',
    'description': 'Módulo para gestionar la venta de propiedades inmobiliarias',
    'author': 'Francisco Montés Doria',
    'website': '',
    # En la siguiente URL se indica que categorias pueden usarse
    # https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    'category': 'Sales',
    'version': '0.1',
    # Indicamos que es una aplicación
    'application': True,
    'installable': True,
    # Indicamos lista de modulos necesarios para que este funcione correctamente
    'depends': ['base'],
    # Carga los archivos para la política de seguridad y las vistas
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
    ],
}
