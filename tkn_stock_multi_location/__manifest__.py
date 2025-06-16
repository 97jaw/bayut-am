# -*- coding: utf-8 -*-
{
    'name': "Stock Multi Location",

    'description': """
        🎯 Features
            ✅ Allow sales orders to deliver products from multiple warehouse locations.
            ✅ Allow purchase orders to receive products from multiple locations or suppliers.
            🔄 Seamless integration with stock picking and inventory.
            📦 Improved logistics planning for large, multi-location businesses.
            🛠️ Works out-of-the-box with Odoo's Sales, Purchase, and Inventory modules.
            📊 Accurate stock movements and traceability.
        
        💡 How It Works
            * On stock picking, choose multiple source locations for each product line.
            * System automatically splits pickings and keeps stock accurate.
            * Smart validation to ensure product availability per location.
            
        🔧 Use Cases
            * Companies managing distributed stock across cities or warehouses.
            * Businesses requiring partial deliveries from multiple warehouses.
            * Drop-shipping workflows that involve multiple vendors or delivery hubs.    
        """,

    'summary': """
        Allow sales orders to deliver products from multiple warehouse locations & 
        Allow purchase orders to receive products from multiple locations or suppliers & 
        Seamless integration with stock picking and inventory &
        Works out-of-the-box with Odoo's Sales, Purchase, and Inventory modules
    """,

    'version': '17.0',

    'license': 'OPL-1',

    'category': 'Inventory',

    'author': "TKN Solutions",

    'website': "https://www.TKN-solution.com",

    'depends': ['base', 'stock'],

    'data': [
        # security
        'security/ir.model.access.csv',
        # wizard
        'wizard/available_quantities_wizard_view.xml',
        'wizard/receive_quantities_wizard_view.xml',
        # view
        'views/stock_picking_view.xml',
    ],

    'images': ['static/description/banner.jpg'],
    'price': 18,
    'currency': 'EUR',

    'installable': True,
    'auto_install': False,
    'application': False,

    'sequence': 30,
}
