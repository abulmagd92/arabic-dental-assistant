import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [activeTab, setActiveTab] = useState("ask");

  return (
    <div className="app" dir="rtl">
      <header>
        <h1>🦷 المساعد الذكي لطب الأسنان</h1>
        <nav>
          <button onClick={() => setActiveTab("ask")} className={activeTab === "ask" ? "active" : ""}>سؤال عام</button>
          <button onClick={() => setActiveTab("patient")} className={activeTab === "patient" ? "active" : ""}>ملف المريض</button>
          <button onClick={() => setActiveTab("treatment")} className={activeTab === "treatment" ? "active" : ""}>خطة العلاج</button>
          <button onClick={() => setActiveTab("appointments")} className={activeTab === "appointments" ? "active" : ""}>المواعيد</button>
          <button onClick={() => setActiveTab("report")} className={activeTab === "report" ? "active" : ""}>التقارير</button>
        </nav>
      </header>

      <main>
        {activeTab === "ask" && <AskTab />}
        {activeTab === "patient" && <PatientTab />}
        {activeTab === "treatment" && <TreatmentTab />}
        {activeTab === "appointments" && <AppointmentsTab />}
        {activeTab === "report" && <ReportTab />}
      </main>
    </div>
  );
}

function AskTab() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!question) return;
    setLoading(true);
    const res = await fetch(`${API}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    setAnswer(data.answer);
    setLoading(false);
  };

  return (
    <div className="tab-content">
      <h2>اسأل أي سؤال عن الأسنان</h2>
      <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="سؤالك هنا..." />
      <button onClick={ask} disabled={loading}>{loading ? "بفكر..." : "اسأل"}</button>
      {answer && <div className="answer">{answer}</div>}
    </div>
  );
}

function PatientTab() {
  const [patientId, setPatientId] = useState("");
  const [patientData, setPatientData] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  const save = async () => {
    await fetch(`${API}/patient/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient_id: patientId, patient_data: patientData }),
    });
    setSaved(true);
  };

  const ask = async () => {
    if (!question || !patientId) return;
    setLoading(true);
    const res = await fetch(`${API}/patient/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient_id: patientId, question }),
    });
    const data = await res.json();
    setAnswer(data.answer);
    setLoading(false);
  };

  return (
    <div className="tab-content">
      <h2>ملف المريض</h2>
      <div className="card">
        <h3>إضافة مريض جديد</h3>
        <input value={patientId} onChange={e => setPatientId(e.target.value)} placeholder="كود المريض" />
        <textarea value={patientData} onChange={e => setPatientData(e.target.value)} placeholder="بيانات المريض" />
        <button onClick={save}>{saved ? "✅ اتحفظ!" : "حفظ"}</button>
      </div>
      <div className="card">
        <h3>اسأل عن المريض</h3>
        <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="سؤالك عن المريض" />
        <button onClick={ask} disabled={loading}>{loading ? "بفكر..." : "اسأل"}</button>
        {answer && <div className="answer">{answer}</div>}
      </div>
    </div>
  );
}

function TreatmentTab() {
  const [patientData, setPatientData] = useState("");
  const [complaint, setComplaint] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!patientData || !complaint) return;
    setLoading(true);
    const res = await fetch(`${API}/treatment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient_data: patientData, complaint }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="tab-content">
      <h2>خطة العلاج</h2>
      <textarea value={patientData} onChange={e => setPatientData(e.target.value)} placeholder="بيانات المريض" />
      <input value={complaint} onChange={e => setComplaint(e.target.value)} placeholder="الشكوى الرئيسية" />
      <button onClick={generate} disabled={loading}>{loading ? "بيولد..." : "ولّد خطة العلاج"}</button>
      {result && (
        <>
          <div className="card">
            <h3>خطة العلاج للدكتور</h3>
            <p>{result.plan}</p>
          </div>
          <div className="card">
            <h3>الشرح للمريض</h3>
            <p>{result.explanation}</p>
          </div>
        </>
      )}
    </div>
  );
}

function AppointmentsTab() {
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [reason, setReason] = useState("");
  const [appointments, setAppointments] = useState([]);
  const [reminder, setReminder] = useState("");
  const [loading, setLoading] = useState(false);

  const load = async () => {
    const res = await fetch(`${API}/appointments`);
    const data = await res.json();
    setAppointments(data.appointments);
  };

  const save = async () => {
    if (!name || !reason) return;
    setLoading(true);
    const res = await fetch(`${API}/appointments/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ patient_name: name, date, time, reason }),
    });
    const data = await res.json();
    setReminder(data.reminder);
    load();
    setLoading(false);
  };

  const cancel = async (id) => {
    await fetch(`${API}/appointments/cancel`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ appointment_id: id }),
    });
    load();
  };

  useState(() => { load(); }, []);

  return (
    <div className="tab-content">
      <h2>المواعيد</h2>
      <div className="card">
        <h3>موعد جديد</h3>
        <input value={name} onChange={e => setName(e.target.value)} placeholder="اسم المريض" />
        <input type="date" value={date} onChange={e => setDate(e.target.value)} />
        <input type="time" value={time} onChange={e => setTime(e.target.value)} />
        <input value={reason} onChange={e => setReason(e.target.value)} placeholder="السبب" />
        <button onClick={save} disabled={loading}>{loading ? "بيحفظ..." : "حفظ الموعد"}</button>
        {reminder && <div className="answer">{reminder}</div>}
      </div>
      <div className="card">
        <h3>كل المواعيد</h3>
        {appointments.length === 0 && <p>مفيش مواعيد</p>}
        {appointments.map(apt => (
          <div key={apt.id} className="appointment">
            <span><b>{apt.patient_name}</b> — {apt.date} {apt.time} — {apt.reason} — {apt.status}</span>
            {apt.status === "مؤكد" && <button onClick={() => cancel(apt.id)}>إلغاء</button>}
          </div>
        ))}
      </div>
    </div>
  );
}

function ReportTab() {
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    const res = await fetch(`${API}/report`);
    const data = await res.json();
    setReport(data.report);
    setLoading(false);
  };

  return (
    <div className="tab-content">
      <h2>تقارير العيادة</h2>
      <button onClick={generate} disabled={loading}>{loading ? "بيحلل..." : "ولّد تقرير أسبوعي"}</button>
      {report && <div className="answer">{report}</div>}
    </div>
  );
}

export default App;