import sys
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from tools import search_wikipedia

SYSTEM_PROMPT = (
    "You are a knowledgeable research assistant with access to Wikipedia. When a "
    "user asks about a topic, person, place, or event, use the search_wikipedia tool "
    "to find accurate information. Summarise the key facts clearly, explain any "
    "complex concepts in simple terms, and highlight what makes the topic interesting "
    "or significant. Always be informative but concise."
)

_default_agent = None


def build_agent():
    """Build and return the LangGraph ReAct agent powered by Ollama llama3.2."""
    llm = ChatOllama(
        model="llama3.2",
        temperature=0.3,
    )
    tools = [search_wikipedia]
    checkpointer = MemorySaver()

    # create_react_agent prebuilt ReAct loop
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    return agent


def ask(agent_or_query, query: str | None = None, thread_id: str = "wikipedia_cli_session") -> str:
    """Send a user query to the agent and return the response text."""
    global _default_agent

    if query is None:
        if _default_agent is None:
            _default_agent = build_agent()
        agent = _default_agent
        user_query = agent_or_query
    else:
        agent = agent_or_query
        user_query = query

    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke({"messages": [("user", user_query)]}, config=config)
    last_message = result["messages"][-1]
    return last_message.content


def main():
    """Interactive CLI loop for the Wikipedia agent."""
    print("=" * 60)
    print("Wikipedia Research Assistant (LangGraph + Ollama llama3.2)")
    print("Type your question or 'quit' / 'exit' / 'q' to end.")
    print("=" * 60)

    try:
        agent = build_agent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye!")
                break

            response = ask(agent, user_input)
            print(f"\nAgent:\n{response}")

        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()
