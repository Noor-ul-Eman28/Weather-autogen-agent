# Weather Agent (Microsoft AutoGen)

A conversational AI agent, built with Microsoft's AutoGen framework, that answers weather questions by calling a real-time weather API as a tool — deployed with a Streamlit chat interface.

## Features
- Natural language weather queries (e.g. "What is the weather in Lahore?")
- The agent autonomously decides when to call the `get_weather` tool based on the user's question
- Real-time data pulled from the OpenWeatherMap API
- Simple Streamlit chat UI with conversation history

## How It Works
1. The user asks a question in the chat input
2. An `AssistantAgent` (AutoGen) receives the task and, using `gpt-4o` as its reasoning model, decides to call the `get_weather` tool
3. The tool calls the OpenWeatherMap API for the requested city and returns the current conditions
4. The agent reflects on the tool's result and replies to the user in natural language

## Setup

1. Install dependencies:
```bash
py -3.11 -m pip install -r requirements.txt
```

2. Create a `.env` file in the project folder with your own keys:
```
OPENAI_API_KEY=sk-your-openai-key
OPENWEATHER_API_KEY=your-openweathermap-key
```
Get a free OpenWeatherMap key at openweathermap.org/api — note new keys can take up to 2 hours to activate.

3. Run the app:
```bash
py -3.11 -m streamlit run app.py
```

## Tech Stack
Python, Streamlit, Microsoft AutoGen (autogen-agentchat, autogen-ext), OpenAI API (gpt-4o), OpenWeatherMap API

## Note
Never commit your .env file or API keys to version control. Make sure .env is listed in .gitignore before pushing this project to GitHub.
