# Simple AI Agent Teaming Example

Simple application to demonstrate creating AI agents and also Teaming up agents together.

AI agents can be built using different frameworks like agno(formerly phidata), LangChain, LangGrap, CrewAI, Microsoft AutoGen etc 
Here we are demostrating building ai agent using agno

# How to Run?
### Prerequisites
Any LLM can be used for the application. Ollama is used in this example. Make sure Ollama is running.
    check http://localhost:11434
    ollama list will show available models. If this list is showing empty, then pull the required model using "ollama pull llama3.1"

create a virtual environment & install dependencies
    uv venv
    source .venv/bin/activate
    uv add -r requirements.txt
run the application
    uv run main.py

    It will print the "Tool calls" and "Response"

# How it works:
Each tool (like DuckDuckGoTools and YFinanceTools) has:
    Function descriptions that explain what the tool does
    Parameter schemas that define what inputs the tool expects
    Tool names that identify the specific function

In this case agno gets this info(we are importing the library) from tools and gives it to model

### How the LLM Makes Decisions:
The LLM decides which tool to call based on:
- Content Analysis: It analyzes the user's query to understand the intent
- Tool Matching: It matches the query intent with available tool capabilities
- Agent Selection: In team scenarios, it chooses the most appropriate agent based on:
    - Agent names and roles
    - Available tools in each agent
    - Instructions provided to each agent

The Process Flow:

    - User sends a query to agent_team
    - The main LLM analyzes the query
    - It determines which team member (agent) is best suited
    - It routes the query to that specific agent
    - The selected agent's LLM then decides which specific tool function to call
    - The tool executes and returns results
    - Results are formatted and returned to the user