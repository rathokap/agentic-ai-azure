from models.schema import CustomerSupportState

def escalate_to_human_agent(support_state: CustomerSupportState) -> CustomerSupportState:
    support_state['final_response'] = "Apologies, we are really sorry! Someone from our team will be reaching out to you shortly!"
    return support_state
