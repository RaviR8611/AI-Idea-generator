import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="My AI Assistant", page_icon="🤖")

# 2. Add a Title and Description
st.title("🤖 AI Idea Generator")
st.write("Enter a topic, and I will generate 3 startup ideas for you.")

# 3. Sidebar for API Key (Keeps it secure)
# api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
# Replace the sidebar input line with this:
api_key = st.secrets["sk-...b6YA"]

# 4. The User Interface
user_topic = st.text_input("What topic are you interested in?", "Sustainable Energy")

# 5. The Logic
if st.button("Generate Ideas"):
    if not api_key:
        st.warning("Please enter your API Key in the sidebar first!")
    else:
        try:
            # Connect to AI
            client = OpenAI(api_key=api_key)
            
            with st.spinner('Thinking...'):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful startup consultant."},
                        {"role": "user", "content": f"Give me 3 innovative startup ideas regarding {user_topic}."}
                    ]
                )
            
            # Display Result
            st.success("Here are your ideas:")
            st.write(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
