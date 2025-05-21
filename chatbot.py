from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import datetime

# Initialize API connection state
api_connected = False

# Try to set up Gemini with error handling
try:
    import google.generativeai as genai
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        chat = model.start_chat(history=[])
        api_connected = True
except Exception as e:
    st.error(f"API connection error: {str(e)}")

def get_gemini_response(question):
    if api_connected:
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            st.error(f"Error getting response: {str(e)}")
            return None
    else:
        # Return a fallback response if API isn't connected
        return ["I'm sorry, but I'm not connected to the Gemini API right now. Please check your API key configuration."]

# Streamlit page config
st.set_page_config(
    page_title="AI Wellness Companion",
    page_icon="🧘‍♀",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed from collapsed to expanded
)

# Custom CSS for styling (with gradient background)
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #2c3e50, #3498db);
        background-attachment: fixed;
    }

    .stApp {
        background: transparent;
    }

    .main {
        background-color: transparent;
    }

    .stButton>button {
        background-color: #2980b9;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #3498db;
        transform: translateY(-2px);
    }

    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }

    .user-message {
        background-color: #34495e;
        border-left: 5px solid #2980b9;
        color: white;
    }

    .bot-message {
        background-color: #2c3e50;
        border-left: 5px solid #3498db;
        color: white;
    }

    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 10px 20px;
        background-color: #ecf0f1;
        color: #2c3e50;
    }

    h1, h2, h3 {
        color: #ecf0f1;
    }

    .sidebar .sidebar-content {
        background: #2c3e50;
    }
    
    .mood-tracker {
        background-color: #34495e;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .widget-label {
        color: #ecf0f1 !important;
    }
    
    .stExpander {
        background-color: #34495e !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    
if "mood_history" not in st.session_state:
    st.session_state["mood_history"] = []
    
if "stress_level" not in st.session_state:
    st.session_state["stress_level"] = []
    
if "journal_entries" not in st.session_state:
    st.session_state["journal_entries"] = {}
    
if "breathing_count" not in st.session_state:
    st.session_state["breathing_count"] = 0

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='background: linear-gradient(to right, #2c3e50 0%, #3498db 100%);
                    padding: 1rem;
                    border-radius: 10px;
                    margin-bottom: 1.5rem;
                    text-align: center;'>
            <h2 style='color: #ecf0f1; margin: 0;'>Wellness Tools</h2>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar tabs
    sidebar_tab = st.radio("Select Tool:", 
                         ["Mood Tracking", "Stress Management", "Emotional Check-ins"],
                         label_visibility="collapsed")
    
    if sidebar_tab == "Mood Tracking":
        st.markdown("<h3 style='color: #ecf0f1;'>📊 Mood Tracker</h3>", unsafe_allow_html=True)
        
        # Today's mood
        st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
        today = datetime.date.today().strftime("%Y-%m-%d")
        st.markdown(f"<p style='color: #ecf0f1;'>Date: {today}</p>", unsafe_allow_html=True)
        
        mood = st.select_slider(
            "How are you feeling today?",
            options=["Very Bad", "Bad", "Neutral", "Good", "Very Good"],
            value="Neutral"
        )
        
        mood_note = st.text_area("Notes about your mood (optional):", height=100)
        
        if st.button("Save Mood", key="save_mood_btn"):
            st.session_state["mood_history"].append({
                "date": today,
                "mood": mood,
                "notes": mood_note
            })
            st.success("Mood saved successfully!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mood history
        if st.session_state["mood_history"]:
            st.markdown("<h4 style='color: #ecf0f1;'>Recent Entries</h4>", unsafe_allow_html=True)
            for entry in reversed(st.session_state["mood_history"][-5:]):
                st.markdown(f"""
                    <div style='background-color: #2c3e50; padding: 0.7rem; border-radius: 10px; margin-bottom: 0.5rem;'>
                        <p style='color: #ecf0f1; margin: 0;'><strong>Date:</strong> {entry['date']}</p>
                        <p style='color: #ecf0f1; margin: 0;'><strong>Mood:</strong> {entry['mood']}</p>
                        <p style='color: #ecf0f1; margin: 0;'><strong>Notes:</strong> {entry['notes'] if entry['notes'] else 'No notes'}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    elif sidebar_tab == "Stress Management":
        st.markdown("<h3 style='color: #ecf0f1;'>🧠 Stress Management</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
        stress_level = st.slider("Current Stress Level", 0, 10, 5)
        
        if st.button("Log Stress Level"):
            st.session_state["stress_level"].append({
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "level": stress_level
            })
            st.success("Stress level logged!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Breathing exercise
        st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ecf0f1;'>Breathing Exercise</h4>", unsafe_allow_html=True)
        st.markdown("""
            <p style='color: #ecf0f1;'>Take a deep breath in for 4 seconds, hold for 4 seconds, exhale for 4 seconds.</p>
        """, unsafe_allow_html=True)
        
        if st.button("Start Breathing Exercise"):
            st.session_state["breathing_count"] += 1
            st.balloons()
            st.success(f"Great job! You've completed {st.session_state['breathing_count']} breathing exercises.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick stress relief
        st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ecf0f1;'>Quick Stress Relief</h4>", unsafe_allow_html=True)
        
        with st.expander("3-3-3 Grounding Technique"):
            st.markdown("""
                <p style='color: #ecf0f1;'>
                    <strong>Name 3 things you see</strong><br>
                    <strong>Name 3 things you hear</strong><br>
                    <strong>Move 3 parts of your body</strong>
                </p>
            """, unsafe_allow_html=True)
            
        with st.expander("Body Scan"):
            st.markdown("""
                <p style='color: #ecf0f1;'>
                    Take a moment to mentally scan your body from head to toe. 
                    Notice any areas of tension and consciously relax them.
                </p>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif sidebar_tab == "Emotional Check-ins":
        st.markdown("<h3 style='color: #ecf0f1;'>🌈 Emotional Check-ins</h3>", unsafe_allow_html=True)
        
        # Journaling
        st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ecf0f1;'>Daily Journal</h4>", unsafe_allow_html=True)
        
        journal_date = st.date_input("Date", datetime.date.today())
        journal_text = st.text_area("How are you feeling today? What's on your mind?", height=150)
        
        if st.button("Save Journal Entry"):
            date_str = journal_date.strftime("%Y-%m-%d")
            st.session_state["journal_entries"][date_str] = journal_text
            st.success("Journal entry saved!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Emotion wheels
        st.markdown("<div class='mood-tracker'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ecf0f1;'>Identify Your Emotions</h4>", unsafe_allow_html=True)
        
        primary_emotion = st.selectbox(
            "What primary emotion are you feeling?",
            ["Joy", "Sadness", "Fear", "Disgust", "Anger", "Surprise"]
        )
        
        secondary_emotions = {
            "Joy": ["Happy", "Grateful", "Inspired", "Proud", "Excited", "Content"],
            "Sadness": ["Disappointed", "Grieving", "Lonely", "Vulnerable", "Despair", "Neglected"],
            "Fear": ["Scared", "Anxious", "Insecure", "Helpless", "Worried", "Overwhelmed"],
            "Disgust": ["Disapproval", "Judgmental", "Avoidance", "Revulsion", "Aversion", "Loathing"],
            "Anger": ["Frustrated", "Annoyed", "Irritated", "Resentful", "Enraged", "Exasperated"],
            "Surprise": ["Amazed", "Confused", "Stunned", "Shocked", "Dismayed", "Disoriented"]
        }
        
        secondary = st.selectbox(
            "More specifically...",
            secondary_emotions[primary_emotion]
        )
        
        st.markdown(f"""
            <p style='color: #ecf0f1;'>You're feeling: <strong>{secondary}</strong> (a form of {primary_emotion})</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Main content area
# Header
st.markdown("""
    <div style='background: linear-gradient(to right, #2c3e50 0%, #3498db 100%);
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                text-align: center;'>
        <h1 style='color: #ecf0f1; margin: 0;'>🧘‍♀ AI Wellness Companion</h1>
        <p style='color: #ecf0f1; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>
            Your personal wellness chatbot for emotional check-ins, mood tracking, and stress relief
        </p>
    </div>
""", unsafe_allow_html=True)

# API Status Indicator
if not api_connected:
    st.warning("""
        ⚠️ Not connected to Gemini API. To enable the chatbot:
        1. Create a .env file in your project directory
        2. Add your Gemini API key: GOOGLE_API_KEY=your_api_key_here
        3. Restart the application
        
        You can still use the wellness tools in the sidebar while offline.
    """)


# Quick prompt section
st.markdown("""
    <div style='background-color: #2c3e50; padding: 1rem; border-radius: 15px; margin-bottom: 1.5rem;'>
        <h2 style='color: #ecf0f1; margin-bottom: 0.5rem;'>💭 Quick Prompts</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🧠 How are you feeling today?", use_container_width=True):
        st.session_state["input"] = "How are you feeling today?"
    if st.button("🌿 Suggest something to help reduce stress", use_container_width=True):
        st.session_state["input"] = "Suggest something to help reduce stress"
with col2:
    if st.button("📊 Can you help me track my mood?", use_container_width=True):
        st.session_state["input"] = "Can you help me track my mood?"
    if st.button("📔 I'd like a quick journaling prompt", use_container_width=True):
        st.session_state["input"] = "I'd like a quick journaling prompt"

# Chat interface
st.markdown("""
    <div style='background-color: #2c3e50; padding: 1rem; border-radius: 15px; margin: 1.5rem 0;'>
        <h2 style='color: #ecf0f1; margin-bottom: 0.5rem;'>💬 Chat with Your Wellness Companion</h2>
    </div>
""", unsafe_allow_html=True)

# Input box
user_input = st.text_input(
    "Type your message:",
    key="input",
    placeholder="Share your thoughts, feelings, or ask for guidance..."
)

# Send message
if st.button("Send Message", use_container_width=True):
    if user_input:
        response = get_gemini_response(user_input)
        st.session_state["chat_history"].append(("You", user_input))

        st.markdown("""
            <div style='background-color: #2980b9; padding: 1rem; border-radius: 15px; margin: 1rem 0;'>
                <h3 style='color: #ecf0f1; margin-bottom: 0.5rem;'>🤖 Wellness Companion</h3>
            </div>
        """, unsafe_allow_html=True)

        bot_reply = ""
        if response:
            # Handle both stream and non-stream responses
            if hasattr(response, '__iter__'):
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        bot_reply += chunk.text
                    else:
                        bot_reply += str(chunk)
            else:
                bot_reply = str(response)


        st.markdown(f"""
            <div class='chat-message bot-message'>
                <strong>Wellness Companion:</strong><br>{bot_reply}
            </div>
        """, unsafe_allow_html=True)

        st.session_state["chat_history"].append(("Bot", bot_reply))


# Chat history display
if st.session_state["chat_history"]:
    st.markdown("""
        <div style='background-color: #ecf0f1; padding: 1.5rem; border-radius: 15px; margin-top: 2rem;'>
            <h2 style='color: #2c3e50; margin-bottom: 1rem;'>🕒 Chat History</h2>
        </div>
    """, unsafe_allow_html=True)

    for role, text in st.session_state["chat_history"]:
        if role == "You":
            st.markdown(f"""
                <div class='chat-message user-message'>
                    <strong>You:</strong><br>{text}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='chat-message bot-message'>
                    <strong>Wellness Companion:</strong><br>{text}
                </div>
            """, unsafe_allow_html=True)