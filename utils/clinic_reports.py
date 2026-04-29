import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from utils.appointments import load_appointments

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_weekly_report() -> str:
    appointments = load_appointments()
    
    total = len(appointments)
    confirmed = len([a for a in appointments if a["status"] == "مؤكد"])
    cancelled = len([a for a in appointments if a["status"] == "ملغي"])
    
    reasons = {}
    for apt in appointments:
        reason = apt["reason"]
        reasons[reason] = reasons.get(reason, 0) + 1
    
    stats = f"""
    إجمالي المواعيد: {total}
    المواعيد المؤكدة: {confirmed}
    المواعيد الملغية: {cancelled}
    أكثر الشكاوى: {json.dumps(reasons, ensure_ascii=False)}
    """
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""أنت مساعد عيادة أسنان بتعمل تقارير أسبوعية.
        بتحلل البيانات وتقدم توصيات للدكتور بالعربي.""",
        messages=[
            {"role": "user", "content": f"اعمل تقرير أسبوعي بناءً على البيانات دي:\n{stats}"}
        ]
    )
    return message.content[0].text