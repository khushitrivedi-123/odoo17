import xmlrpc.client

# Odoo server details
url = "http://localhost:9056"
db = "demo1"
username = "admin"
password = "admin"

# Authenticate
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)
uid = common.authenticate(db, username, password, {})

if not uid:
    raise Exception("Failed to authenticate")

# Create an object proxy
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)

def get_or_create(model, name_field, name_value, extra_fields={}):
    record = models.execute_kw(db, uid, password, model, "search", [[(name_field, "=", name_value)]])
    if record:
        return record[0]
    else:
        sanitized_fields = {k: (v if v is not None else "") for k, v in extra_fields.items()}
        sanitized_fields[name_field] = name_value
        return models.execute_kw(db, uid, password, model, "create", [sanitized_fields])

# Ensure patient exists with required fields
patient_id = get_or_create(
    "hospital.patient", "name", "patient2", {"email": "patient2@gmail.com"}
)

# Ensure physician exists with required fields
physician_id = get_or_create(
    "hospital.physician", "name", "Physician2", {"email": "Physician2@gmail.com"}
)

# Create a new treatment
new_treatment_id = models.execute_kw(
    db,
    uid,
    password,
    "hospital.treatment",
    "create",
    [
        {
            "patient_id": patient_id,
            "physician_id": physician_id,
            "treatment_date": "2025-02-07",
            "state": "draft",
        }
    ],
)
print(f"New Treatment Created with ID: {new_treatment_id}")
disease_id = get_or_create(
    "hospital.disease", "name", "Disease", 000
)

# Add diagnosis line
new_diagnosis_id = models.execute_kw(
    db,
    uid,
    password,
    "hospital.diagnosis",
    "create",
    [
        {
            "treatment_id": new_treatment_id,
            "diagnosis_type": "high",
            "disease_id": disease_id,
            "date": "2025-02-07",
        }
    ],
)
print(f"New Diagnosis Created with ID: {new_diagnosis_id}")

# Search for active treatments
treatment_ids = models.execute_kw(
    db, uid, password, "hospital.treatment", "search", [[("state", "=", "active")]]
)
print(f"Active Treatment IDs: {treatment_ids}")

# Set a treatment to 'done'
if treatment_ids:
    models.execute_kw(
        db, uid, password, "hospital.treatment", "write", [[treatment_ids[0]], {"state": "done"}]
    )
    print(f"Treatment {treatment_ids[0]} marked as done")

# Fetch treatment details
treatment_data = models.execute_kw(
    db, uid, password, "hospital.treatment", "read", [treatment_ids],
    {"fields": ["treatment_code", "patient_id", "state"]},
)
# Ensure None values are handled
cleaned_treatment_data = [
    {k: (v if v is not None else "") for k, v in record.items()} for record in treatment_data
]
print("Treatment Data:", cleaned_treatment_data)





# from xmlrpc import client as xmlrpclib
#
# url = "http://localhost:9056"
# user = "admin"
# password = "admin"
# db = "demo1"
#
# # Connect to common endpoint
# common = xmlrpclib.ServerProxy(f"{url}/xmlrpc/2/common")
# uid = common.authenticate(db, user, password, {})
# if not uid:
#     print("Authentication failed!")
#     exit()
#
# # Connect to object endpoint
# models = xmlrpclib.ServerProxy(f"{url}/xmlrpc/2/object")
# try:
#     records = models.execute_kw(db, uid, password, 'hospital.treatment', 'search_read', [],
#                                 {'fields': ['treatment_code', 'state']})
#     print("Before Operation:")
#     for record in records:
#         print(record)
#
#     treatment_id = models.execute_kw(db, uid, password, 'hospital.treatment', 'create', [{
#         'patient_id': 2,  # Replace with valid patient ID
#         'physician_id': 2,  # Replace with valid physician ID
#         'treatment_date': '2025-02-07',  # Adjust as needed
#         'company_id': 1,  # Replace with valid company ID
#         'state': 'draft'
#     }])
#     print(f"New treatment created with ID: {treatment_id}")
#
#     records = models.execute_kw(db, uid, password, 'hospital.treatment', 'search_read', [],
#                                 {'fields': ['treatment_code', 'state']})
#     print("After Insert:")
#     for record in records:
#         print(record)
#
# except Exception as e:
#     print(f"Error: {e}")
