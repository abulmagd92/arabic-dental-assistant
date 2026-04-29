import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key found: {api_key is not None}")
client = Anthropic(api_key=api_key)

def ask_dental_agent(question: str) -> str:
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""أنت مساعد ذكي متخصص في طب الأسنان.
        بتساعد المرضى وتجاوب على أسئلتهم بالعربي بلغة بسيطة وواضحة.
        لو حد سألك عن حاجة مش متعلقة بطب الأسنان، قوله إنك متخصص في طب الأسنان بس.""",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return message.content[0].text