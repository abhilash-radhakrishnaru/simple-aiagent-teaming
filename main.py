from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

#### Tool Registration
#When tools are instantiated, Agno automatically:
#1. Inspects the tool class using Python's introspection
#2. Extracts method signatures and docstrings
#3. Converts them into structured schemas
#4. Registers them with the LLM's function calling system
#Agent level routing based on functional descriptions from tools
web_agent = Agent(
    name="Web Agent",
    model=Ollama(id="llama3.1"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)


#- The `DuckDuckGoTools()` instance provides web search capabilities
#- The LLM receives the tool's function schemas during initialization
#- When a query comes in, the LLM matches the intent against available tool descriptions
#- The agent's instructions provide additional context for tool selection


#Agent level routing based on functional descriptions from tools
finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Ollama(id="llama3.1"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

#Team based routing based on functional descriptions from tools
#**Routing Process:**
#1. **Query Analysis**: The main LLM analyzes the user's query
#2. **Intent Recognition**: Identifies the type of task (web search, financial data, etc.)
#3. **Agent Selection**: Chooses the most appropriate team member based on:
#   - Agent names and roles
#   - Available tools in each agent
#   - Query content matching tool capabilities
#4. **Tool Execution**: The selected agent's LLM chooses specific tool functions

agent_team = Agent(
    model=Ollama(id="llama3.1"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Summarize analyst recommendations and share the latest news for HPE", stream=True)
# LLM recognizes this as a stock ticker → Routes to finance_agent → Uses YFinanceTools

#agent_team.print_response("Share the latest news on USA", stream=True)
#  LLM recognizes this as general web search → Routes to web_agent → Uses DuckDuckGoTools

#agent_team.print_response("Share the output of 2+2", stream=True)
# LLM recognizes this as a mathematical calculation → May route to either agent or handle directly

#agent_team.print_response("Summarize analyst recommendations and share the latest news for HPE. Also share latest news on USA", stream=True)
# LLM recognizes this as a finance and web search → Routes to finance_agent → Uses YFinanceTools Also to DuckDuckGoTools
