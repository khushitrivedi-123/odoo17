{
    'name': 'Hospital Website',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Module for Hospital Patient Management on Website',
    'description': """
        This module adds a patient form to the hospital website.
    """,
    'author': 'Your Name',
    'depends': ['website', 'base'],
    'data': [
        'views/website_patient_template.xml',
        'views/menus.xml',
        'views/patient_thank_you.xml',
    ],

    'installable': True,
    'application': False,
}
