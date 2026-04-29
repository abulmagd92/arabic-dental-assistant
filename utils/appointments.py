import os
import json
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

APPOINTMENTS_FILE = "appointments.json"

def load_appointments():
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(appointments, f, ensure_ascii=False, indent=2)

def add_appointment(patient_name: str, date: str, time: str, reason: str):
    appointments = load_appointments()
    appointment = {
        "id": len(appointments) + 1,
        "patient_name": patient_name,
        "date": date,
        "time": time,
        "reason": reason,
        "status": "مؤكد"
    }
    appointments.append(appointment)
    save_appointments(appointments)
    return appointment

def get_appointments():
    return load_appointments()

def cancel_appointment(appointment_id: int):
    appointments = load_appointments()
    for apt in appointments:
        if apt["id"] == appointment_id:
            apt["status"] = "ملغي"
    save_appointments(appointments)

def get_appointment_reminder(appointment: dict) -> str:
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system="""أنت مساعد عيادة أسنان بتكتب رسائل تذكير للمرضى بالعربي.
        الرسالة لازم تكون ودية وقصيرة.""",
        messages=[
            {"role": "user", "content": f"اكتب رسالة تذكير للمريض {appointment['patient_name']} بموعده يوم {appointment['date']} الساعة {appointment['time']} بسبب {appointment['reason']}"}
        ]
    )
    return message.content[0].text