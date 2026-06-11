from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

from tools import pipeline as real_pipeline

load_dotenv()


# 🔧 TOOL
@tool
def youtube_tool(url: str) -> str:
    """
    Descarga audio de YouTube y devuelve la transcripción de la canción.
    """
    return real_pipeline(url)


# 🤖 LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [youtube_tool]


# 🧠 PROMPT CORRECTO
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un traductor de canciones. "
     "Siempre que recibas una URL debes usar la herramienta. "
     "Con el resultado debes: "
     "1. traducir la letra al español "
     "2. deducir el título de la canción "
     "3. devolver resultado limpio"),

    ("human", "{input}"),

    MessagesPlaceholder("agent_scratchpad"),
])


# 🧠 AGENTE
agent = create_tool_calling_agent(llm, tools, prompt)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=hmjfuuuRRYU"

    result = executor.invoke({
        "input": url
    })

    print("\n====================")
    print(result["output"])