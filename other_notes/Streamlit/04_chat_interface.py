"""
Modern Chat Interface - Built from scratch

A clean, ChatGPT-like interface with:
- Dark theme
- User messages on the right (blue)
- Assistant messages on the left (gray)
- ENTER key to send
- Smooth scrolling and animations

Run with:
    uvr -m streamlit run other_notes/Streamlit/05_chat_app.py
"""

from __future__ import annotations

import time

import streamlit as st


def init_session_state() -> None:
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""


def get_assistant_response(user_message: str) -> str:
    """Mock assistant response - replace with your LLM API call."""
    time.sleep(0.3)  # Simulate thinking
    return f"Echo: {user_message[::-1]}"


def main() -> None:
    """Main application."""
    st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")

    init_session_state()

    # Custom CSS for dark theme and chat styling
    st.markdown(
        """
        <style>
        /* Dark theme */
        .stApp {
            background-color: #1a1a1a;
        }
        
        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Chat messages container */
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.75rem;
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
            max-width: 75%;
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* User message - right aligned, blue */
        .user-message {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8f 100%);
            margin-left: auto;
            flex-direction: row-reverse;
        }
        
        /* Assistant message - left aligned, gray */
        .assistant-message {
            background: linear-gradient(135deg, #2f2f2f 0%, #3a3a3a 100%);
            margin-right: auto;
        }
        
        /* Avatar styling */
        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        
        .user-avatar {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        }
        
        .assistant-avatar {
            background: linear-gradient(135deg, #10a37f 0%, #0d8c6c 100%);
        }
        
        /* Message text */
        .message-text {
            color: #ececec;
            font-size: 15px;
            line-height: 1.6;
            word-wrap: break-word;
            flex: 1;
        }
        
        /* Input styling */
        .stTextInput input {
            background-color: #2f2f2f !important;
            color: #ececec !important;
            border: 2px solid #404040 !important;
            border-radius: 0.75rem !important;
            padding: 0.75rem 1rem !important;
            font-size: 15px !important;
        }
        
        .stTextInput input:focus {
            border-color: #10a37f !important;
            box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.2) !important;
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(135deg, #10a37f 0%, #0d8c6c 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 0.75rem !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(16, 163, 127, 0.4) !important;
        }
        
        /* Title styling */
        h1 {
            color: #ececec !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Caption styling */
        .stCaption {
            color: #9ca3af !important;
        }
        
        /* Divider */
        hr {
            margin: 2rem 0 1rem 0 !important;
            border-color: #404040 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.title("💬 Chat Assistant")
    st.caption("Press ENTER to send your message • Dark mode enabled")

    # Display chat messages
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class="chat-message user-message">
                        <div class="avatar user-avatar">👤</div>
                        <div class="message-text">{msg["content"]}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-message assistant-message">
                        <div class="avatar assistant-avatar">🤖</div>
                        <div class="message-text">{msg["content"]}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("👋 Start a conversation by typing a message below!")

    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)

    # Input area - using st.chat_input which handles ENTER automatically
    st.divider()

    # Simple, reliable chat input
    user_input = st.chat_input("Type your message... (press ENTER to send)")

    if user_input and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        # Get assistant response
        response = get_assistant_response(user_input.strip())
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Rerun to display new messages
        st.rerun()

    # Footer
    st.caption("💡 Tip: Replace `get_assistant_response()` with your LLM API call")


if __name__ == "__main__":
    main()
