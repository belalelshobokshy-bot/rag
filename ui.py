import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="Scaffolding RAG Chatbot", page_icon="🏗️")
st.title("🏗️ مساعد السقالات الذكي ")

# رابط الـ API الخاص بـ FastAPI
API_URL = "http://127.0.0.1:8000/ask"

# تهيئة سجل المحادثة في الـ Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اطرح سؤالك حول السقالات..."):
    # عرض سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # إرسال الطلب لـ FastAPI
    with st.chat_message("assistant"):
        with st.spinner("جاري البحث والإجابة..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=90  # وقت أطول لأن Gemini أحياناً بياخد وقت (خصوصاً مع الـ thinking)
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "لم يتم إرجاع إجابة.")
                    
                    st.markdown(answer)
                    
                    # عرض المصادر المستخدمة في القائمة المنسدلة
                    if "sources" in data and data["sources"]:
                        with st.expander("🔍 المصادر المسترجعة من ChromaDB"):
                            for i, src in enumerate(data["sources"], 1):
                                st.write(f"**مصدر {i}:** {src}")
                                
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"خطأ في السيرفر: {response.status_code}")
            except Exception as e:
                st.error(f"عذراً، تعذر الاتصال بالسيرفر: {e}")