import streamlit as st
import google.generativeai as genai
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Gujarat Travel AI",
    page_icon="🦁",
    layout="wide"
)

# 2. Sidebar for API Key & Settings
with st.sidebar:
    st.image("https://www.gujarattourism.com/content/dam/gujrattourism/images/logo.png", width=200)
    st.title("⚙️ Settings")
    
    # --- CHANGED SECTION START ---
    # This logic checks if you set the secret in the cloud.
    # If yes, it uses it automatically. If no, it shows the text box.
    
    api_key = None
    
    # Check for the key in Streamlit Secrets
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key loaded automatically!")
    else:
        # Fallback: Ask the user to enter it manually
        api_key = st.text_input("Enter Google Gemini API Key:", type="password")
    # --- CHANGED SECTION END ---
    
    st.markdown("---")
    st.markdown("""
    ### 🎒 Suggested Questions:
    - *Plan a 3-day trip to Kutch for Rann Utsav.*
    - *Best places to eat authentic Gujarati Thali in Ahmedabad?*
    - *How do I book a safari in Gir National Park?*
    - *Itinerary for Dwarka and Somnath temples.*
    """)
    st.markdown("---")
    st.info("Powered by Google Gemini (Free Tier)")

# 3. Main Chat Interface
st.title("🦁 Namaste! Welcome to Gujarat Tourism AI")
st.write("I am your personal guide to the Land of Legends. Ask me anything about Gujarat!")

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Kem cho? I can help you plan trips to the Statue of Unity, the White Desert, Gir Forest, and more. Where would you like to go?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Brains (AI Logic)
if prompt := st.chat_input("Ask me about travel, food, or history..."):
    
    # A. Check for API Key
    if not api_key:
        st.error("Please enter your Google Gemini API Key in the sidebar to start!")
        st.stop()

    # B. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # C. Configure Gemini with "Expert" Knowledge
    try:
        genai.configure(api_key=api_key)
        
        system_instruction = """
        You are an expert travel agent for the state of Gujarat, India.
        Your tone should be warm, welcoming, and helpful ('Kem cho', 'Majama').
        
        Key Knowledge Areas:
        1. Destinations: Rann of Kutch (White Desert), Gir National Park (Asiatic Lions), Statue of Unity, Ahmedabad (UNESCO Heritage), Dwarka & Somnath (Pilgrimage), Saputara (Hill Station).
        2. Food: Recommend Dhokla, Thepla, Fafda-Jalebi, Undhiyu (winter special), and the best Thali places (like Agashiye).
        3. Logistics: Best time to visit is Oct-March. Mention Rann Utsav dates if asked.
        4. Safety: Gujarat is very safe for tourists.
        
        If the user asks about anything OUTSIDE of Gujarat travel, politely steer them back to Gujarat.
        """
        
        # --- UPDATED LOGIC TO FIX 404 ERRORS ---
        # Instead of hardcoding 'gemini-1.5-flash', we dynamically find a working model
        target_model = "gemini-1.5-flash" # Default fallback
        try:
            with st.spinner('Connecting to AI brain...'):
                # List all models available to your API key
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Logic: Look for Flash, then Pro, then anything else
                if any("gemini-1.5-flash" in m for m in available_models):
                    target_model = next(m for m in available_models if "gemini-1.5-flash" in m)
                elif any("gemini-pro" in m for m in available_models):
                    target_model = next(m for m in available_models if "gemini-pro" in m)
                elif available_models:
                    target_model = available_models[0] # Pick the first available one
                
                # st.toast(f"Using model: {target_model}") # Optional: show user which model picked
        except Exception as e:
            # If listing fails, stick to default
            pass

        model = genai.GenerativeModel(target_model)
        # ---------------------------------------
        
        # Create a chat session with history
        chat = model.start_chat(history=[])
        
        full_prompt = f"{system_instruction}\n\nUser Question: {prompt}"
        
        with st.spinner('Checking the map...'):
            response = chat.send_message(full_prompt)
            ai_response = response.text

        # D. Display AI Response
        with st.chat_message("model"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "model", "content": ai_response})

    except Exception as e:
        st.error(f"Error: {e}")
