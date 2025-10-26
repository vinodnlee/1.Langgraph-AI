"""
Data Transformer Node
Transforms the processed data using an LLM
"""
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.models.graph_state import GraphState


# Initialize the LLM (you can replace with any LLM)
# Only create LLM if API key is available
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key and openai_api_key != 'your_openai_api_key_here':
    llm = ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.7,
        api_key=openai_api_key
    )
else:
    llm = None  # Will use fallback logic


def data_transformer_node(state: GraphState) -> GraphState:
    """
    Node 2: Data Transformer
    Transforms the processed data using an LLM
    """
    processed_text = state.get("processed_text", "")

    # Transform the data using LLM
    if llm is not None:
        try:
            prompt = f"Transform this text into a creative format: {processed_text}"
            response = llm.invoke([HumanMessage(content=prompt)])
            transformed_text = response.content
        except Exception as e:
            print(f"⚠️ LLM invocation failed: {e}")
            # Fallback transformation if LLM fails
            fallback_text = processed_text.replace('PROCESSING:', 'ENHANCED:')
            transformed_text = f"✨ TRANSFORMED: {fallback_text} ✨"
    else:
        # Fallback transformation if LLM is not available
        fallback_text = processed_text.replace('PROCESSING:', 'ENHANCED:')
        transformed_text = f"✨ TRANSFORMED: {fallback_text} ✨"

    print(f"🔄 Data Transformer Node: {transformed_text}")

    return {
        **state,
        "transformed_text": transformed_text,
        "step": "data_transformed"
    }
