# from langchain_google_genai import ChatGoogleGenerativeAI

# from config.settings import GOOGLE_API_KEY

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=GOOGLE_API_KEY,
#     temperature=0
# )

from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_API_KEY

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=True
)