from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.dental_agent import ask_dental_agent
from utils.rag_agent import add_patient_file, ask_with_patient_context
from utils.treatment_agent import generate_treatment_plan, explain_treatment_to_patient
from utils.appointments import add_appointment, get_appointments, cancel_appointment, get_appointment_reminder
from utils.clinic_reports import generate_weekly_report

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class PatientRequest(BaseModel):
    patient_id: str
    patient_data: str

class PatientQuestionRequest(BaseModel):
    patient_id: str
    question: str

class TreatmentRequest(BaseModel):
    patient_data: str
    complaint: str

class AppointmentRequest(BaseModel):
    patient_name: str
    date: str
    time: str
    reason: str

class CancelRequest(BaseModel):
    appointment_id: int

@app.post("/ask")
def ask(req: QuestionRequest):
    answer = ask_dental_agent(req.question)
    return {"answer": answer}

@app.post("/patient/add")
def add_patient(req: PatientRequest):
    add_patient_file(req.patient_id, req.patient_data)
    return {"status": "ok"}

@app.post("/patient/ask")
def ask_patient(req: PatientQuestionRequest):
    answer = ask_with_patient_context(req.question, req.patient_id)
    return {"answer": answer}

@app.post("/treatment")
def treatment(req: TreatmentRequest):
    plan = generate_treatment_plan(req.patient_data, req.complaint)
    explanation = explain_treatment_to_patient(plan)
    return {"plan": plan, "explanation": explanation}

@app.post("/appointments/add")
def add_apt(req: AppointmentRequest):
    apt = add_appointment(req.patient_name, req.date, req.time, req.reason)
    reminder = get_appointment_reminder(apt)
    return {"appointment": apt, "reminder": reminder}

@app.get("/appointments")
def get_apts():
    return {"appointments": get_appointments()}

@app.post("/appointments/cancel")
def cancel_apt(req: CancelRequest):
    cancel_appointment(req.appointment_id)
    return {"status": "ok"}

@app.get("/report")
def report():
    r = generate_weekly_report()
    return {"report": r}