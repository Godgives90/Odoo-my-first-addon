{
    'name': "Primo modulo di Antonio",
    'category': "Real Estate/Brokerage",
    'author': "Antonio Donadio",
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/properties_res_users_view.xml'
    ],
    'application': True,

}