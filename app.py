import os
import asyncio
import requests
import streamlit as st
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

st.set_page_config(page_title="Weather Agent", page_icon="🌤️")
st.title("🌤️ Weather Agent")
st.caption("An AI agent (built with Microsoft AutoGen) that fetches real-time weather using a tool call.")

# OpenWeather key stays yours — low risk, free tier, no reason to make visitors provide it
openweather_api_key = os.getenv("OPENWEATHER_API_KEY") or st.secrets.get("OPENWEATHER_API_KEY")

if not openweather_api_key:
    st.error("Missing OPENWEATHER_API_KEY. Please add it to your .env file or Streamlit secrets.")
    st.stop()

# --- OpenAI key: visitor provides their own ---
with st.sidebar:
    st.subheader("🔑 Your OpenAI API Key")
    st.caption("This app uses your own OpenAI key so your usage isn't billed to the app owner. "
               "Get one at platform.openai.com — it's never stored, only used for this session.")
    user_openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

if not user_openai_key:
    st.info("👈 Enter your OpenAI API key in the sidebar to start chatting.")
    st.stop()


async def get_weather(city: str) -> str:
    """Tool used by the agent to fetch real-time weather for a given city."""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": openweather_api_key,
            "units": "metric",
        }
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code != 200 or "weather" not in data:
            return f"Could not fetch the weather for {city}."
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        location = data["name"]
        return f"{location}: {desc}, {temp}°C"
    except Exception as e:
        return f"Error fetching the weather data: {str(e)}"


async def run_agent(question: str, api_key: str) -> str:
    """Create the agent fresh per request, using the visitor's own OpenAI key."""
    model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key)
    agent = AssistantAgent(
        name="Weather_Agent",
        model_client=model_client,
        tools=[get_weather],
        system_message=(
            "You are a helpful weather assistant. If the user asks about the weather, "
            "use the 'get_weather' tool to find real-time information."
        ),
        reflect_on_tool_use=True,
    )
    try:
        result = await agent.run(task=question)
        return result.messages[-1].content
    except Exception as e:
        # Catches invalid/expired keys, quota errors, etc. without crashing the app
        return f"⚠️ Couldn't complete the request. Check that your OpenAI API key is valid and has quota. ({str(e)})"
    finally:
        await model_client.close()


# --- Chat UI ---
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about the weather, e.g. 'What is the weather in Lahore?'")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Checking the weather..."):
            answer = asyncio.run(run_agent(user_input, user_openai_key))
        st.write(answer)
    st.session_state.history.append({"role": "assistant", "content": answer})
