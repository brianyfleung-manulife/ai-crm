from langchain.schema import HumanMessage
import json
import re

from utils.openai_client import initialize_chat_client

def extract_customer_filters_from_message(message: str) -> dict:
    """
    Use the LLM to extract customer filter parameters from a user message.
    Returns a dict of filter params, e.g. {"gender": "female", "riskProfile": "high", "aum_min": 100000}
    """
    chat = initialize_chat_client()
    system_prompt = (
        "You are an assistant that extracts filter parameters for a customer table. "
        "Given a user message, return a JSON object with any of these fields if present: "
        "gender, riskProfile, aum_min, aum_max, age_min, age_max, search, sort_by, sort_dir. "
        "If a field is not mentioned, omit it. Only return the JSON object."
    )
    prompt = f"{system_prompt}\nUser message: {message}\nJSON:"
    messages = [HumanMessage(content=prompt)]
    response = chat.invoke(messages)
    try:
        # Find the first JSON object in the response
        match = re.search(r'{.*}', response.content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return {}
    except Exception:
        return {}
