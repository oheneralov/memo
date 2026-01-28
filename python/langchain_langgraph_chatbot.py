"""
LangChain and LangGraph Chatbot Examples

This file demonstrates:
1. Basic LangChain chatbot with memory
2. LangGraph stateful chatbot with custom workflow
3. Advanced LangGraph chatbot with tools and conditional routing
"""

import os
from typing import Annotated, TypedDict, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# ============================================================================
# EXAMPLE 1: Basic LangChain Chatbot with Memory
# ============================================================================

def basic_langchain_chatbot():
    """
    Simple LangChain chatbot with conversation memory.
    Uses in-memory storage to maintain conversation context.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic LangChain Chatbot with Memory")
    print("="*70 + "\n")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a prompt template with memory
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Be concise and friendly."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    # Create the chain
    chain = prompt | llm
    
    # Set up memory storage
    store = {}
    
    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    # Wrap chain with message history
    chatbot = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    
    # Example conversation
    session_id = "user_123"
    
    # First message
    response1 = chatbot.invoke(
        {"input": "Hi! My name is Alex."},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"User: Hi! My name is Alex.")
    print(f"Bot: {response1.content}\n")
    
    # Second message (bot should remember the name)
    response2 = chatbot.invoke(
        {"input": "What's my name?"},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"User: What's my name?")
    print(f"Bot: {response2.content}\n")
    
    # Third message
    response3 = chatbot.invoke(
        {"input": "What did we talk about so far?"},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"User: What did we talk about so far?")
    print(f"Bot: {response3.content}\n")


# ============================================================================
# EXAMPLE 2: LangGraph Stateful Chatbot with Custom Workflow
# ============================================================================

class ChatState(TypedDict):
    """State definition for the chatbot"""
    messages: Sequence[BaseMessage]
    user_info: dict


def langgraph_stateful_chatbot():
    """
    LangGraph chatbot with custom state management and workflow.
    Demonstrates state persistence and custom node logic.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: LangGraph Stateful Chatbot")
    print("="*70 + "\n")
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Define graph nodes
    def extract_user_info(state: ChatState) -> ChatState:
        """Extract user information from messages"""
        messages = state["messages"]
        user_info = state.get("user_info", {})
        
        # Simple extraction logic (in real app, use LLM or NER)
        last_message = messages[-1].content.lower()
        if "name is" in last_message:
            name = last_message.split("name is")[1].strip().split()[0]
            user_info["name"] = name
        
        return {"messages": messages, "user_info": user_info}
    
    def chat_node(state: ChatState) -> ChatState:
        """Main chat processing node"""
        messages = state["messages"]
        user_info = state.get("user_info", {})
        
        # Add system message with user info if available
        system_msg = "You are a helpful assistant."
        if user_info.get("name"):
            system_msg += f" The user's name is {user_info['name']}."
        
        prompt_messages = [SystemMessage(content=system_msg)] + list(messages)
        response = llm.invoke(prompt_messages)
        
        return {
            "messages": messages + [response],
            "user_info": user_info
        }
    
    # Build the graph
    workflow = StateGraph(ChatState)
    
    # Add nodes
    workflow.add_node("extract_info", extract_user_info)
    workflow.add_node("chat", chat_node)
    
    # Define edges
    workflow.set_entry_point("extract_info")
    workflow.add_edge("extract_info", "chat")
    workflow.add_edge("chat", END)
    
    # Compile with memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    # Example conversation
    config = {"configurable": {"thread_id": "conversation_1"}}
    
    # First message
    print("User: Hello! My name is Sarah.")
    result1 = app.invoke(
        {"messages": [HumanMessage(content="Hello! My name is Sarah.")], "user_info": {}},
        config
    )
    print(f"Bot: {result1['messages'][-1].content}\n")
    
    # Second message
    print("User: What's my name?")
    result2 = app.invoke(
        {"messages": result1['messages'] + [HumanMessage(content="What's my name?")]},
        config
    )
    print(f"Bot: {result2['messages'][-1].content}\n")


# ============================================================================
# EXAMPLE 3: Advanced LangGraph Chatbot with Tools and Routing
# ============================================================================

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Mock weather data
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Rainy, 60°F",
        "tokyo": "Cloudy, 68°F",
        "paris": "Partly cloudy, 65°F"
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Example: '2 + 2' or '10 * 5'"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"


class AgentState(TypedDict):
    """State for the agent chatbot"""
    messages: Sequence[BaseMessage]


def langgraph_agent_chatbot():
    """
    Advanced LangGraph chatbot with tool calling and conditional routing.
    Demonstrates function calling and dynamic workflow paths.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: LangGraph Agent Chatbot with Tools")
    print("="*70 + "\n")
    
    # Initialize LLM with tools
    tools = [get_weather, calculate]
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    
    # Define nodes
    def should_continue(state: AgentState):
        """Determine if we should continue to tools or end"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If there are no tool calls, we finish
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"
        else:
            return "continue"
    
    def call_model(state: AgentState):
        """Call the LLM"""
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile
    app = workflow.compile()
    
    # Example conversations
    examples = [
        "What's the weather in Tokyo?",
        "Calculate 156 * 23",
        "What's 100 divided by 4, and also tell me the weather in Paris?"
    ]
    
    for query in examples:
        print(f"User: {query}")
        result = app.invoke({
            "messages": [HumanMessage(content=query)]
        })
        print(f"Bot: {result['messages'][-1].content}\n")


# ============================================================================
# EXAMPLE 4: Multi-turn Agent with Memory
# ============================================================================

def langgraph_agent_with_memory():
    """
    Complete chatbot combining tools, memory, and conversational flow.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: LangGraph Agent with Memory")
    print("="*70 + "\n")
    
    tools = [get_weather, calculate]
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    
    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"
        return "continue"
    
    def call_model(state: AgentState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
    workflow.add_edge("tools", "agent")
    
    # Compile with memory checkpoint
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    # Multi-turn conversation
    config = {"configurable": {"thread_id": "agent_chat_1"}}
    
    conversation = [
        "What's the weather in London?",
        "How about New York?",
        "What's the difference in temperature? Calculate it for me.",
    ]
    
    messages = []
    for user_input in conversation:
        print(f"User: {user_input}")
        messages.append(HumanMessage(content=user_input))
        
        result = app.invoke({"messages": messages}, config)
        assistant_message = result["messages"][-1]
        messages = result["messages"]
        
        print(f"Bot: {assistant_message.content}\n")


# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LangChain and LangGraph Chatbot Examples")
    print("="*70)
    print("\nNote: Set OPENAI_API_KEY environment variable to run these examples.")
    print("Example: os.environ['OPENAI_API_KEY'] = 'your-api-key-here'\n")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found. Please set it to run the examples.")
        print("You can set it in code: os.environ['OPENAI_API_KEY'] = 'sk-...'")
        print("\nShowing code structure only (not executing).\n")
    else:
        # Uncomment to run examples
        # basic_langchain_chatbot()
        # langgraph_stateful_chatbot()
        # langgraph_agent_chatbot()
        # langgraph_agent_with_memory()
        pass
    
    print("\n" + "="*70)
    print("Examples Summary:")
    print("="*70)
    print("""
    1. basic_langchain_chatbot()
       - Simple chatbot with conversation memory
       - Uses LangChain's RunnableWithMessageHistory
       - Maintains context across messages
    
    2. langgraph_stateful_chatbot()
       - Custom state management with LangGraph
       - User information extraction
       - Stateful workflow with multiple nodes
    
    3. langgraph_agent_chatbot()
       - Tool-calling agent (weather, calculator)
       - Conditional routing based on tool needs
       - Function calling with dynamic paths
    
    4. langgraph_agent_with_memory()
       - Combines tools + memory + multi-turn conversation
       - Persistent state across interactions
       - Full-featured conversational agent
    
    To run examples, uncomment the function calls in the main block.
    """)
