"""
🌟 Women Coding Community Info Bot
Combines: Gemini Chatbot + Web Scraper for WCC Events
"""

import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from chatbot import SimpleBot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ----------------------------------------------------
# 🔍 SCRAPER FUNCTION: Get latest WCC events
# ----------------------------------------------------
def fetch_wcc_events():
    """Scrape event titles, dates, and links from the WCC website."""
    url = "https://www.womencodingcommunity.com/events"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Error fetching events: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    for section in soup.find_all(["article", "li", "div"]):
        title_elem = section.find(["h2", "h3", "strong", "a"])
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)

        date_elem = section.find(
            ["time", "p", "span"],
            string=lambda s: s and any(
                month in s for month in [
                    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                ]
            )
        )
        date = date_elem.get_text(strip=True) if date_elem else "Date not found"

        link_elem = section.find("a")
        link = link_elem["href"] if link_elem and "href" in link_elem.attrs else "No link"

        events.append(f"{title} — {date}\n{link}")

    if not events:
        return "No upcoming events found at the moment."

    return "\n\n".join(events)

# ----------------------------------------------------
# 🤖 SETUP CHATBOT WITH WCC SYSTEM PROMPT
# ----------------------------------------------------
wcc_events = fetch_wcc_events()

system_prompt = f"""
You are the Women Coding Community (WCC) Assistant — a friendly, inclusive guide.

About WCC:
- WCC supports women in technology through mentorship, workshops, and networking.
- Mission: Empower women and non-binary individuals to grow in tech careers.
- Focus: Community, learning, and collaboration.

Latest WCC events (if asked):
{wcc_events}

If unsure about something, suggest visiting https://www.womencodingcommunity.com
"""

# Initialize bot once and keep in session_state
if "bot" not in st.session_state:
    st.session_state.bot = SimpleBot(system_prompt=system_prompt)

# ----------------------------------------------------
# 🎨 STREAMLIT APP
# ----------------------------------------------------
st.set_page_config(page_title="WCC Info Bot", page_icon="💬", layout="centered")
st.title("🌟 Women Coding Community Info Bot")
st.markdown("Ask me anything about the Women Coding Community! 💪")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    role = "🧑 You" if msg["role"] == "user" else "🤖 WCC Assistant"
    st.markdown(f"**{role}:** {msg['content']}")

# Input box
user_input = st.text_input("Your question:")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate bot response
    with st.spinner("Thinking..."):
        response = st.session_state.bot.chat(user_input)

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("👩‍💻 **Women Coding Community (WCC)** — empowering women in tech.")
st.markdown("[Visit WCC Website 🌐](https://www.womencodingcommunity.com)")
