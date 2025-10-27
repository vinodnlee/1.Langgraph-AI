"""
Streamlit Chat Application for LangGraph Router
A user-friendly chat interface with LLM agent and tool integration.
"""
import streamlit as st
from dotenv import load_dotenv

from main import create_workflow

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LangGraph Chat Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .tool-call {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
        font-size: 0.9rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "workflow" not in st.session_state:
        st.session_state.workflow = create_workflow()
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []


def display_message(role, content, tool_calls=None):
    """Display a chat message with styling."""
    css_class = "user-message" if role == "user" else "assistant-message"
    icon = "👤" if role == "user" else "🤖"

    with st.container():
        st.markdown(
            f'<div class="chat-message {css_class}">',
            unsafe_allow_html=True
        )
        st.markdown(f"**{icon} {role.title()}**")
        st.markdown(content)

        # Display tool calls if present
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.get('name', 'unknown')
                tool_args = tool_call.get('args', {})
                st.markdown(
                    f'<div class="tool-call">'
                    f'🔧 Tool Called: <b>{tool_name}</b><br>'
                    f'Arguments: {tool_args}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)


def run_agent(user_input):
    """Run the LangGraph workflow with user input."""
    # Create initial state
    initial_state = {
        "input_text": user_input,
        "processed_text": "",
        "transformed_text": "",
        "output_text": "",
        "step": "",
        "messages": st.session_state.conversation_history.copy()
    }

    # Run workflow
    result = st.session_state.workflow.invoke(initial_state)

    # Update conversation history
    st.session_state.conversation_history = result.get("messages", [])

    return result


def main():
    """Main application function."""
    initialize_session_state()

    # Header
    st.markdown(
        '<div class="main-header">🤖 LangGraph Chat Agent</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        "### Intelligent Assistant with Tool Integration",
        unsafe_allow_html=False
    )

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This chat application uses:
        - **LLM Agent**: GPT-4o-mini for intelligent responses
        - **Tool Integration**: Automatic multiply tool calling
        - **Smart Routing**: Decides when to use tools
        
        **Try asking:**
        - "What is 15 multiplied by 8?"
        - "Calculate 25 times 4"
        - "What is the capital of France?"
        - "Tell me about Python"
        """)

        st.divider()

        # Conversation stats
        st.header("📊 Stats")
        st.metric("Messages", len(st.session_state.messages))
        st.metric(
            "Tool Calls",
            sum(
                1 for msg in st.session_state.conversation_history
                if hasattr(msg, 'tool_calls') and msg.tool_calls
            )
        )

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.rerun()

        # Show conversation history toggle
        show_history = st.checkbox("Show Message Details", value=False)

    # Main chat area
    chat_container = st.container()

    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            display_message(
                message["role"],
                message["content"],
                message.get("tool_calls")
            )

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Display user message
        with chat_container:
            display_message("user", user_input)

        # Show processing indicator
        with st.spinner("🤔 Agent is thinking..."):
            try:
                # Run the agent
                result = run_agent(user_input)

                # Extract response and tool calls
                messages = result.get("messages", [])

                # Find tool calls in the conversation
                tool_calls = []
                assistant_response = result.get("output_text", "")

                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        tool_calls.extend(msg.tool_calls)

                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response,
                    "tool_calls": tool_calls if tool_calls else None
                })

                # Display assistant message
                with chat_container:
                    display_message(
                        "assistant",
                        assistant_response,
                        tool_calls if tool_calls else None
                    )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Sorry, I encountered an error: {str(e)}"
                })

        st.rerun()

    # Show conversation history in sidebar if enabled
    if show_history and st.session_state.conversation_history:
        with st.sidebar:
            st.divider()
            st.header("💬 Message History")
            for i, msg in enumerate(st.session_state.conversation_history, 1):
                msg_type = type(msg).__name__
                with st.expander(f"{i}. {msg_type}"):
                    st.json({
                        "type": msg_type,
                        "content": getattr(msg, 'content', 'N/A')[:100],
                        "has_tool_calls": bool(
                            getattr(msg, 'tool_calls', None)
                        )
                    })


if __name__ == "__main__":
    main()
