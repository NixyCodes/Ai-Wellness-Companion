# AI Wellness Companion 🧘‍♀️

A comprehensive wellness application that combines AI-powered chat support with various wellness tools for emotional well-being, stress management, and mood tracking.

## Features

- 🤖 AI Chat Companion powered by Google's Gemini AI
- 📊 Mood Tracking and History
- 🧠 Stress Management Tools
- 🌈 Emotional Check-ins
- 📝 Daily Journaling
- 🎯 Breathing Exercises
- 💭 Quick Prompts for Wellness Support

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wellness-companion
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Key**
   - Create a `.env` file in the project root directory
   - Add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

5. **Run the application**
   ```bash
   streamlit run chatbot.py
   ```

## Usage

### AI Chat Companion
- Use the chat interface to have conversations about wellness, mental health, and emotional support
- Try the quick prompts for common wellness topics
- The AI will provide supportive and helpful responses

### Wellness Tools (Sidebar)
1. **Mood Tracking**
   - Log your daily mood
   - Add notes about your feelings
   - View mood history

2. **Stress Management**
   - Track stress levels
   - Practice breathing exercises
   - Access quick stress relief techniques

3. **Emotional Check-ins**
   - Daily journaling
   - Emotion identification tool
   - Track emotional patterns

## Offline Mode
The application can be used without an API key, but the AI chat feature will be disabled. All other wellness tools in the sidebar will remain functional.

## Requirements
- Python 3.8 or higher
- Internet connection (for AI chat feature)
- Google Gemini API key (for AI chat feature)

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is licensed under the MIT License - see the LICENSE file for details. 