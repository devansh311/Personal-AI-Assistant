import requests

from langchain_core.tools import tool

from config.settings import ALPHA_VANTAGE_API_KEY


@tool
def get_stock_price(symbol: str):
    """
    Get the latest stock price.
    Example:AAPL,TSLA,MSFT
    """

    url = ("https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={ALPHA_VANTAGE_API_KEY}"
    )

    response = requests.get(url)

    return response.json()