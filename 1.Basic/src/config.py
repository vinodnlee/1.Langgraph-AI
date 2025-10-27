"""
Configuration management for LangGraph application.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Application configuration settings."""

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")

    # LangChain Settings
    LANGCHAIN_TRACING_V2: bool = os.getenv(
        "LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_ENDPOINT: str = os.getenv(
        "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_PROJECT: str = os.getenv(
        "LANGCHAIN_PROJECT", "langgraph-project")

    # LLM Settings
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7

    @classmethod
    def get_llm(cls) -> Optional[ChatOpenAI]:
        """
        Get configured LLM instance.

        Returns:
            ChatOpenAI instance if API key is available, None otherwise
        """
        if cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != "your_openai_api_key_here":
            return ChatOpenAI(
                model=cls.LLM_MODEL,
                temperature=cls.LLM_TEMPERATURE,
                api_key=cls.OPENAI_API_KEY
            )
        return None


# Global LLM instance
llm = Config.get_llm()
