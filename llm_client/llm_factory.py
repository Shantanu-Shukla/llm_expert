"""
Factory module for creating LLM clients based on provider and type.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI


class LLMClientFactory:
    """
    A factory class to create different LLM clients
    """

    def __init__(self, load_env=True):
        """
        Initialize the factory with optional environment loading

        Args:
            load_env (bool): Whether to load environment variables from .env file
        """
        if load_env:
            load_dotenv(override=True)

        # Common headers for web requests
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        # Register all available providers with their creation methods
        self.providers = {
            "openai": self._create_openai_client,
            "ollama": self._create_ollama_client,
            # Add more providers here as needed
            # "anthropic": self._create_anthropic_client,
            # "cohere": self._create_cohere_client,
        }

    def _create_openai_client(self, **kwargs):
        """
        Internal method to create an OpenAI client

        Args:
            **kwargs: Additional arguments for client configuration
                      - model: The model to use (default: "gpt-4o-mini")
                      - client_type: Type of client to create (default: "summarizer")

        Returns:
            An instance of an OpenAI client of the requested type

        Raises:
            ValueError: If OPENAI_API_KEY is not found or client_type is unknown
        """
        # Import here to avoid circular imports
        from .providers.openai import (
            WebsiteSummarizerOpenAI,
            ContentExtractorOpenAI,
            SentimentAnalyzerOpenAI,
            SEOAnalyzerOpenAI,
        )

        model = kwargs.get("model", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        client_type = kwargs.get("client_type", "summarizer")

        # Map client types to their respective classes
        client_classes = {
            "summarizer": WebsiteSummarizerOpenAI,
            "content_extractor": ContentExtractorOpenAI,
            "sentiment_analyzer": SentimentAnalyzerOpenAI,
            "seo_analyzer": SEOAnalyzerOpenAI,
        }

        if client_type in client_classes:
            client_class = client_classes[client_type]
            client = client_class(model=model, client=OpenAI(), headers=self.headers)
        else:
            available_clients = ", ".join(client_classes.keys())
            raise ValueError(
                f"Unknown client type: {client_type}. Available types: {available_clients}"
            )

        return client

    def _create_ollama_client(self, **kwargs):
        """
        Internal method to create an Ollama client

        Args:
            **kwargs: Additional arguments for client configuration
                      - model: The model to use (default: "llama3.2")
                      - client_type: Type of client to create (default: "summarizer")
                      - base_url: The base URL for Ollama API (default: 'http://localhost:11434/v1')

        Returns:
            An instance of an Ollama client of the requested type

        Raises:
            ValueError: If client_type is unknown
        """
        # Import here to avoid circular imports
        from llm_client.providers.ollama import (
            WebsiteSummarizerOllama,
            ContentExtractorOllama,
            SentimentAnalyzerOllama,
            SEOAnalyzerOllama,
        )

        model = kwargs.get("model", "llama3.2")
        base_url = kwargs.get("base_url", "http://localhost:11434/v1")
        client_type = kwargs.get("client_type", "summarizer")

        # Map client types to their respective classes
        client_classes = {
            "summarizer": WebsiteSummarizerOllama,
            "content_extractor": ContentExtractorOllama,
            "sentiment_analyzer": SentimentAnalyzerOllama,
            "seo_analyzer": SEOAnalyzerOllama,
        }

        if client_type in client_classes:
            client_class = client_classes[client_type]
            client = client_class(
                model=model,
                client=OpenAI(base_url=base_url, api_key="ollama"),
                headers=self.headers,
            )
        else:
            available_clients = ", ".join(client_classes.keys())
            raise ValueError(
                f"Unknown client type: {client_type}. Available types: {available_clients}"
            )

        return client

    def create_client(self, provider, **kwargs):
        """
        Create a client based on provider name

        Args:
            provider (str): The provider to use (e.g., "openai", "ollama")
            **kwargs: Additional arguments for client configuration

        Returns:
            An instance of the requested client

        Raises:
            ValueError: If provider is unknown
        """
        provider_key = provider.lower()

        if provider_key in self.providers:
            return self.providers[provider_key](**kwargs)
        else:
            available_providers = ", ".join(self.providers.keys())
            raise ValueError(
                f"Unknown provider: {provider}. Available providers: {available_providers}"
            )

    def get_available_providers(self):
        """
        Return a list of all available providers

        Returns:
            list: The names of all available providers
        """
        return list(self.providers.keys())
