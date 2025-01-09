{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'author': 'Khushi Trivedi',
    'license': 'LGPL-3',
    'depends': ['base','sale','web'],
    'data': [
        'views/hospital_menu.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_physician_views.xml',
        'security/ir.model.access.csv',
        'views/hospital_specialty_views.xml',
        'data/hospital_treatment_actions.xml',
        'views/hospital_treatment_views.xml',
        'wizard/hospital_treatment_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/hospital_diagnosis_views.xml',
        'views/hospital_disease_views.xml',
        'data/hospital_treatment_sequence.xml',
        'report/hospital_treatment_report.xml',
        'report/report_hospital_treatment_template.xml',

    ],
    'installable': True,
    'application': True,
}

