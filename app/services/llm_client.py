from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.config import settings

llm = ChatOpenAI(
    model=settings.OPENROUTER_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
    temperature=0.3
)

PROMPT = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following content:\n{text}"
)

async def generate_summary(text: str) -> str:
    response = await llm.ainvoke(PROMPT.format(text=text))
    return response.content
