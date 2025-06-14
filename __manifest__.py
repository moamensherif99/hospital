{
    'name': 'Hospital Management',
    'author': 'Moamen Sherif Abdelkader',
    'category': 'Hospital',
    'sequence': -100,
    'version': '18.0.1.0',
    'summery':'Hospital management system',
    'depends': ['base','account', 'mail',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/kid_patient_view.xml',
        'views/appointment_view.xml',
        'views/menu.xml',

    ],
    'demo': [

    ],
    'application': True,
}