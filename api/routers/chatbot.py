from fastapi import APIRouter
from pydantic import BaseModel
from utils.customer_filters import extract_customer_filters_from_message
from routers.customers import filter_customers

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class Query(BaseModel):
    message: str

@router.post("/")
async def get_response(query: Query):
    # Step 1: Try to extract filter params from the message
    filters = extract_customer_filters_from_message(query.message)
    if filters:
        # Only pass allowed filter keys
        allowed_keys = {"search", "sort_by", "sort_dir", "gender", "riskProfile", "aum_min", "aum_max", "age_min", "age_max"}
        filter_args = {k: v for k, v in filters.items() if k in allowed_keys}
        # Call the filter_customers function directly
        customers_result = filter_customers(**filter_args)
        # Format as a simple table string (showing key fields)
        if customers_result:
            table = "ID | Name | Age | Gender | Risk | AUM | LastContact\n"
            table += "-" * 65 + "\n"
            for c in customers_result:
                table += f"{c['id']} | {c['name']} | {c['age']} | {c['gender']} | {c['riskProfile']} | {c['aum']} | {c['lastContact']}\n"
            return {"response": table, "customers": customers_result}
        else:
            return {"response": "No customers found matching your criteria.", "customers": []}
    # Fallback: normal chat
    from utils.openai_message import process_message
    response = process_message(query.message)
    return {"response": response}
