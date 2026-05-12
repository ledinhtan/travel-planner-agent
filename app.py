import datetime
import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="✈️ Travel Planner Agentic Application",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("✈️ Travel Planner Agentic")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("### 👋 Hi there! I'm your personal travel assistant.")
st.markdown("Tell me where you'd like to go, and I'll help you plan the perfect trip ✨")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tell me about your ideal trip..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("✈️ Planning your trip..."):
            try:
                payload = {"query": prompt}
                response = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
                
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                    
                    # Format the response nicely
                    markdown_content = f"""
### 🌍 Your AI Travel Plan
**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}  
**Assistant:** Atriyo's Travel Agent

---

{answer}

---

> ⚡ *Please verify all information (prices, operating hours, travel requirements) before your trip.*
                    """
                    st.markdown(markdown_content)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"❌ Bot failed to respond: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")