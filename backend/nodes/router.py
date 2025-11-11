from models.schema import CustomerSupportState

def determine_route(support_state: CustomerSupportState) -> str:
    if support_state['query_sentiment'] == "Negative":
        return "escalate_to_human_agent"
    elif support_state['query_category'] == "Technical":
        return "generate_technical_response"
    elif support_state['query_category'] == "Billing":
        return "generate_billing_response"
    else:
        return "generate_general_response"
