{
    "name": "Propietats immobiliàries",  # The name that will appear in the App list
    "version": "1.0.0",  # Version
    "author": "Andreu Gisbert Bel",  # Author
    "summary": 'Gestió i seguiment de propietats immobiliàries.', # A brief description of the module
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base", "account"],  # dependencies
    "data": [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    "images": ['static/description/icon.png'],
    "installable": True,
    'license': 'LGPL-3',
}
