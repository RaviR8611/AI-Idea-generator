import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 AI Idea Generator")

# 2. Securely access the API Key
# This pulls the key from Streamlit's "Secrets" manager
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except FileNotFoundError:
    st.error("OpenAI API Key not found. Please set it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# 3. The User Interface
user_topic = st.text_input("What topic are you interested in?", "Sustainable Energy")

# 4. The Logic
if st.button("Generate Ideas"):
    with st.spinner('Thinking...'):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful startup consultant."},
                    {"role": "user", "content": f"Give me 3 innovative startup ideas regarding {user_topic}."}
                ]
            )
            st.success("Here are your ideas:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
