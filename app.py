import streamlit as st
from utils.dental_agent import ask_dental_agent
from utils.rag_agent import add_patient_file, ask_with_patient_context
from utils.treatment_agent import generate_treatment_plan, explain_treatment_to_patient
from utils.appointments import add_appointment, get_appointments, cancel_appointment, get_appointment_reminder
from utils.clinic_reports import generate_weekly_report

st.set_page_config(
    page_title="المساعد الذكي لطب الأسنان",
    page_icon="🦷",
    layout="wide"
)

st.title("🦷 المساعد الذكي لطب الأسنان")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["سؤال عام", "ملف المريض", "خطة العلاج", "المواعيد", "تقارير العيادة"])

with tab1:
    st.subheader("اسأل أي سؤال عن الأسنان")
    question = st.text_input("سؤالك هنا:", key="general")
    if st.button("اسأل", key="btn_general"):
        if question:
            with st.spinner("بفكر..."):
                answer = ask_dental_agent(question)
            st.write(answer)
        else:
            st.warning("اكتب سؤالك الأول!")

with tab2:
    st.subheader("ملف المريض")
    with st.expander("إضافة ملف مريض جديد"):
        patient_id = st.text_input("كود المريض:", key="pid")
        patient_data = st.text_area("بيانات المريض:", key="pdata")
        if st.button("حفظ", key="btn_save"):
            if patient_id and patient_data:
                add_patient_file(patient_id, patient_data)
                st.success("اتحفظ!")
            else:
                st.warning("حط الكود والبيانات!")
    st.divider()
    patient_id_q = st.text_input("كود المريض:", key="pid_q")
    question_p = st.text_input("سؤالك عن المريض:", key="pquestion")
    if st.button("اسأل", key="btn_patient"):
        if patient_id_q and question_p:
            with st.spinner("بفكر..."):
                answer = ask_with_patient_context(question_p, patient_id_q)
            st.write(answer)
        else:
            st.warning("حط كود المريض والسؤال!")

with tab3:
    st.subheader("خطة العلاج")
    patient_data_t = st.text_area("بيانات المريض:", key="pdata_t")
    complaint = st.text_input("الشكوى الرئيسية:", key="complaint")
    if st.button("ولّد خطة العلاج", key="btn_treatment"):
        if patient_data_t and complaint:
            with st.spinner("بيولد خطة العلاج..."):
                plan = generate_treatment_plan(patient_data_t, complaint)
            st.subheader("خطة العلاج للدكتور:")
            st.write(plan)
            st.divider()
            with st.spinner("بيشرح للمريض..."):
                explanation = explain_treatment_to_patient(plan)
            st.subheader("الشرح للمريض:")
            st.write(explanation)
        else:
            st.warning("حط بيانات المريض والشكوى!")

with tab4:
    st.subheader("المواعيد")
    p_name = st.text_input("اسم المريض:", key="pname")
    apt_date = st.date_input("التاريخ:", key="apt_date")
    apt_time = st.time_input("الوقت:", key="apt_time")
    apt_reason = st.text_input("السبب:", key="apt_reason")
    if st.button("حفظ الموعد", key="btn_apt"):
        if p_name and apt_reason:
            apt = add_appointment(p_name, str(apt_date), str(apt_time), apt_reason)
            st.success("اتحفظ!")
            with st.spinner("بيعمل رسالة تذكير..."):
                reminder = get_appointment_reminder(apt)
            st.info(reminder)
        else:
            st.warning("حط اسم المريض والسبب!")
    st.divider()
    st.subheader("كل المواعيد")
    appointments = get_appointments()
    if appointments:
        for apt in appointments:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{apt['patient_name']}** — {apt['date']} {apt['time']} — {apt['reason']} — {apt['status']}")
            with col2:
                if apt["status"] == "مؤكد":
                    if st.button("إلغاء", key=f"cancel_{apt['id']}"):
                        cancel_appointment(apt["id"])
                        st.rerun()
    else:
        st.info("مفيش مواعيد لحد دلوقتي")

with tab5:
    st.subheader("تقارير العيادة")
    if st.button("ولّد تقرير أسبوعي", key="btn_report"):
        with st.spinner("بيحلل البيانات..."):
            report = generate_weekly_report()
        st.write(report)