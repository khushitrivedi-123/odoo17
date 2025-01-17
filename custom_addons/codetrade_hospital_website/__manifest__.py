{
    'name': 'Hospital Website',
    'version': '1.0',
    'category': 'Website',
    'license': 'LGPL-3',
    'summary': 'Module for Hospital Patient Management on Website',
    'author': 'Your Name',
    'depends': ['website', 'base'],
    'data': [
        'views/website_patient_template.xml',
        'views/menus.xml',
        # 'views/patient_thank_you.xml',
    ],

    'installable': True,
    'application': False,
}
