from app.models.patient import Patient
from app.models.rooms import Room

def enrich_patient_data(patient: Patient):
    """
    Enriches patient data with room information.
    """
    room = Room.get_by_id(patient.room_id)
    if room:
        patient_data = {
            "patient_name": patient.name,
            "room_name": room.name
        }
        return patient_data
    else:
        return None