{
    "name": "Custom Website Form",
    "version": "17.0",
    "depends": ["website"],
    "license": "LGPL-3",
    "data": [
        "views/form_template.xml",
        "views/thank_you_template.xml",
        "views/menu_patient_registration.xml",
    ],
    "installable": True,
    "application": False,
    "models": ["models/hospital_patient.py"],
}
