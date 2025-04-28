from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import requests, wikipedia, datetime
from langchain.schema.agent import AgentFinish
from langchain.schema.runnable import RunnablePassthrough
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory


class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    # Make the request
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.utcnow()
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']
    
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]
    
    return f'The current temperature is {current_temperature}°C'

@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

tool = [search_wikipedia, get_current_temperature]

functions = [format_tool_to_openai_function(t) for t in tool]


model = ChatOpenAI(model="gpt-3.5-turbo").bind(functions = functions)

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a sassy assistant"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name = "agent_scratchpad")
])

chain = prompt | model | OpenAIFunctionsAgentOutputParser()

# chain.invoke({"input": "what is the meaning of samsung"})

result = chain.invoke({
    "input": "what is the weather in vellore",
    "agent_scratchpad" : []
})

observation = get_current_temperature(result.tool_input)

result2 = chain.invoke({"input": "what is the weather in vellore",
                       "agent_scratchpad": format_to_openai_functions([(result, observation)])})

def run_agent(user_input):
    intermediate_steps = []
    while True:
        result = chain.invoke({"input": user_input,
                       "agent_scratchpad": format_to_openai_functions(intermediate_steps)})
        if isinstance(result, AgentFinish):
            return result
        tool = {
            "search_wikipedia": search_wikipedia,
            "get_current_temperature": get_current_temperature
        }[result.tool]
        
        observation = tool.run(result.tool_input)
        intermediate_steps.append((result, observation))
        

agent_chain = RunnablePassthrough.assign(
            agent_scratchpad = lambda x : format_to_openai_functions(x['intermediate_steps'])
) | chain

def run_agent(user_input):
    intermediate_steps = []
    while True:
        result = agent_chain.invoke({"input": user_input,
                       "intermediate_steps": intermediate_steps})
        if isinstance(result, AgentFinish):
            return result
        tool = {
            "search_wikipedia": search_wikipedia,
            "get_current_temperature": get_current_temperature
        }[result.tool]
        
        observation = tool.run(result.tool_input)
        intermediate_steps.append((result, observation))
        

run_agent("what is the weather in vellore")

agent_executor = AgentExecutor(agent = agent_chain, tools = tool, verbose = True)

agent_executor.invoke({"input": "what is the weather in vellore and chennai and which one is warmer"})

# still has no memory

agent_executor.invoke({"input": "what did i ask first"})

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are helpful but sassy assistant"),
    MessagesPlaceholder(variable_name= "chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name= "agent_scratchpad")
])

agent_chain = RunnablePassthrough.assign(
    agent_scratchpad = lambda x : format_to_openai_functions(x["intermediate_steps"])
) | prompt | model | OpenAIFunctionsAgentOutputParser()

memory = ConversationBufferMemory(return_messages = True, memory_key = "chat_history")

agent_executor = AgentExecutor(agent = agent_chain, tools = tool, verbose = True, memory=memory)

agent_executor.invoke({"input": "what is the weather in vellore"})

agent_executor.invoke({"input": "My name is Anand and i am from arcot"})

agent_executor.invoke({"input": "where is anand from"})

agent_executor.invoke({"input": "what is the first message i asked to you"})

