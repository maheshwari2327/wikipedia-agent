import uuid
import streamlit as st
from agent import build_agent, ask

st.set_page_config(
    page_title="Wikipedia Research Assistant",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_agent():
    """Build and cache the LangGraph Wikipedia agent."""
    return build_agent()


# Initialize session states
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your **Wikipedia Research Assistant**.\n\n"
                "Ask me about any topic, person, place, or event, and I will search Wikipedia, "
                "summarise the key facts, explain complex concepts simply, and provide sources!"
            ),
        }
    ]

# Sidebar controls & information
with st.sidebar:
    st.title("📚 Wiki Assistant")
    st.caption("Powered by LangGraph, Ollama llama3.2 & Wikipedia")

    st.divider()

    st.markdown("### ⚙️ Agent Configuration")
    st.markdown("- **Model**: `llama3.2` (Ollama)")
    st.markdown("- **Temperature**: `0.3`")
    st.markdown("- **Loop**: LangGraph `create_react_agent`")
    st.markdown("- **Tool**: `search_wikipedia`")

    st.divider()

    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation reset! What would you like to explore?",
            }
        ]
        st.rerun()

    st.divider()
    st.markdown("### 💡 Example Questions")
    examples = [
        "Tell me about the Turing Test",
        "James Webb Space Telescope",
        "Who is Ada Lovelace?",
        "Quantum Computing",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.selected_example = example


# Main UI Header
st.title("📚 Wikipedia Research Agent")
st.caption("Ask questions, explore topics, and get concise Wikipedia-grounded summaries.")

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle example click or chat input
prompt = st.chat_input("Ask about any topic, person, place, or event...")

if "selected_example" in st.session_state and st.session_state.selected_example:
    prompt = st.session_state.selected_example
    del st.session_state.selected_example

if prompt:
    # Display user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching Wikipedia & generating summary..."):
            try:
                agent = get_agent()
                response = ask(agent, prompt, thread_id=st.session_state.thread_id)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                err_msg = f"⚠️ An error occurred: {e}"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
