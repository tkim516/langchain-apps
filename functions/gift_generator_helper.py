from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def generate_gifts(recipient_hobbies, recipient_age, relationship, occasion, budget, api_key):
    """
    Generate gift suggestions using LangChain and OpenAI.

    Args:
        recipient_hobbies (str): Hobbies of the recipient.
        recipient_age (int): Age of the recipient.
        relationship (str): Relationship to the recipient.
        occasion (str): Occasion for the gift.
        budget (str): Budget range in USD.
        api_key (str): The API key for OpenAI.

    Returns:
        str: Generated gift suggestions.
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0.5, openai_api_key=api_key)
    
    prompt = PromptTemplate(
        template="""
        Using the details provided, generate a thoughtful list of gift suggestions that are well-suited to the individual’s interests, age, 
        the nature of your relationship with them, the occasion, and the given budget range. For each gift idea, include a brief explanation 
        of why it would be a suitable choice. Aim for unique, meaningful, and practical suggestions rather than generic options.

        Person's interests: {recipient_hobbies}
        Person's age in years: {recipient_age}
        Gift giver's relationship to the recipient: {relationship}
        Occasion: {occasion}
        Budget range in USD: {budget}
        """,
        input_variables=[
            "recipient_hobbies", "recipient_age", "relationship", "occasion", "budget"
        ]
    )

    # Format the prompt with user inputs
    message = prompt.format(
        recipient_hobbies=recipient_hobbies,
        recipient_age=recipient_age,
        relationship=relationship,
        occasion=occasion,
        budget=budget,
    )
    
    # Get the response
    response = llm(message)
    return response