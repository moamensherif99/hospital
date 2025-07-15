{
    'name': 'Hospital Management',
    'author': 'Moamen Sherif Abdelkader',
    'category': 'Hospital',
    'sequence': -100,
    'version': '18.0.1.0',
    'summery': 'Hospital management system',
    'depends': ['base', 'account', 'mail', 'product', 'sale_management'
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'wizard/cancel_appointment_view.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/kid_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
    ],
    'demo': [

    ],
    'application': True,
}
