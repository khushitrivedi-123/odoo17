{
    "name": "Custom Website Form",
    "version": "17.0",
    "depends": ["website"],
    "license": "LGPL-3",
    "data": [
        "views/form_template.xml",
        "views/thank_you_template.xml",
        "views/menu_patient_registration.xml",
        "views/snippet/snippets.xml",
    ],
    "installable": True,
    "application": False,
    'assets': {
        'web.assets_frontend': [
            'hospital_website/static/src/css/custom_snippet.css',
        ],
    },
}
