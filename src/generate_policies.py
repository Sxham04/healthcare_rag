#create policy text files for rag system
import os

output_folder = "../data/policies"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#define visitor policy text
visitor_policy = """# Hospital Visitor Policy

## Visiting Hours
Standard visiting hours are from 8:00 AM to 8:00 PM every day.
Intensive Care Unit (ICU) visiting hours are from 10:00 AM to 12:00 PM and 5:00 PM to 7:00 PM.

## Visitor Rules
- Maximum 2 visitors per patient at one time.
- Visitors must get a visitor pass at the main desk.
- Sick visitors must not enter patient rooms.
"""

#define admission policy text
admission_policy = """# Admission and Discharge Policy

## Emergency Admission
Emergency patients must see an intake nurse immediately.

## Standard Admission
- Staff must check insurance cards and photo ID before assigning a room.
- Doctors must write admission orders in the system within 2 hours.

## Discharge Rules
- The doctor must sign a discharge paper.
- Staff must give prescription details to the patient before the patient leaves.
"""

#define billing policy text
billing_policy = """# Billing and Insurance Policy

## Payment Rules
- The hospital sends the bill after patient discharge.
- Patients must pay bills within 30 days.

## Insurance Rules
- Emergency care does not require prior insurance approval.
- Non-emergency care requires insurance approval 48 hours before treatment.
"""

#save visitor policy file
file1 = open(output_folder + "/visitor_policy.md", "w")
file1.write(visitor_policy)
file1.close()
print("Saved visitor policy.")

#save admission policy file
file2 = open(output_folder + "/admission_policy.md", "w")
file2.write(admission_policy)
file2.close()
print("Saved admission policy.")

#save billing policy file
file3 = open(output_folder + "/billing_policy.md", "w")
file3.write(billing_policy)
file3.close()
print("Saved billing policy.")

print("All policy documents are ready.")