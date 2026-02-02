from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOllama

from langchain_openai import ChatOpenAI
from langchain.tools import tool

from ai_researcher.arxiv import search_arxiv_papers
from ai_researcher.read_pdf import read_pdf


@tool
def arxiv_search(topic: str) -> list[dict]:
    """Search arXiv papers by topic."""
    return search_arxiv_papers(topic)["entries"]


@tool
def pdf_reader(url: str) -> str:
    """Read and extract text from a PDF URL."""
    return read_pdf(url)


llm = ChatOllama(model="phi3:mini", temperature=0)


agent = initialize_agent(
    tools=[arxiv_search, pdf_reader],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


def chat(user_input: str) -> str:
    try:
        response = agent.run(user_input)
        return response
    except Exception as e:
        return "⚠️ API quota exceeded or model error. Please check billing or switch to a local model."

