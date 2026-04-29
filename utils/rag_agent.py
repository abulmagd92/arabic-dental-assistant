import os
from anthropic import Anthropic
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./chroma_db")

embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="patients",
    embedding_function=embedding_fn
)

def add_patient_file(patient_id: str, patient_data: str):
    collection.add(
        documents=[patient_data],
        ids=[patient_id]
    )

def ask_with_patient_context(question: str, patient_id: str) -> str:
    results = collection.query(
        query_texts=[question],
        n_results=1
    )
    
    context = ""
    if results['documents'] and len(results['documents'][0]) > 0:
        context = results['documents'][0][0]
    
    if not context:
        return "مفيش بيانات للمريض ده. تأكد إنك حفظت الملف الأول."
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""أنت مساعد ذكي متخصص في طب الأسنان.
        بتساعد الدكتور وبتجاوب بناءً على ملف المريض.
        لو في معلومات عن المريض، استخدمها في إجابتك.""",
        messages=[
            {"role": "user", "content": f"معلومات المريض:\n{context}\n\nالسؤال: {question}"}
        ]
    )
    return message.content[0].text
    
    context = results['documents'][0][0] if results['documents'] else ""
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""أنت مساعد ذكي متخصص في طب الأسنان.
        بتساعد الدكتور وبتجاوب بناءً على ملف المريض.
        لو في معلومات عن المريض، استخدمها في إجابتك.""",
        messages=[
            {"role": "user", "content": f"معلومات المريض:\n{context}\n\nالسؤال: {question}"}
        ]
    )
    return message.content[0].text
    
    context = results['documents'][0][0] if results['documents'] else ""
    
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="""أنت مساعد ذكي متخصص في طب الأسنان.
        بتساعد الدكتور وبتجاوب بناءً على ملف المريض.
        لو في معلومات عن المريض، استخدمها في إجابتك.""",
        messages=[
            {"role": "user", "content": f"معلومات المريض:\n{context}\n\nالسؤال: {question}"}
        ]
    )
    return message.content[0].text