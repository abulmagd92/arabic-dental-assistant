import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_treatment_plan(patient_data: str, complaint: str) -> str:
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system="""أنت طبيب أسنان خبير بتولد خطط علاج مفصلة.
        بتكتب خطة العلاج بالعربي بلغة واضحة.
        خطة العلاج لازم تشمل:
        1. التشخيص
        2. خطوات العلاج بالترتيب
        3. المدة المتوقعة
        4. التكلفة التقريبية
        5. تعليمات ما بعد العلاج
        6. موعد المتابعة""",
        messages=[
            {"role": "user", "content": f"بيانات المريض:\n{patient_data}\n\nالشكوى الرئيسية: {complaint}\n\nاكتب خطة علاج مفصلة."}
        ]
    )
    return message.content[0].text

def explain_treatment_to_patient(treatment_plan: str) -> str:
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""أنت مساعد بتشرح خطة العلاج للمريض بلغة بسيطة جداً.
        مش بتستخدم مصطلحات طبية معقدة.
        بتكون ودود ومطمّن.""",
        messages=[
            {"role": "user", "content": f"اشرح خطة العلاج دي للمريض بلغة بسيطة:\n{treatment_plan}"}
        ]
    )
    return message.content[0].text