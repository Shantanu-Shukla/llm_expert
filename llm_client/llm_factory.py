"""
Factory module for creating LLM clients based on provider and type.
"""

from openai import OpenAI
import importlib.util


class LLMClientFactory:
    """
    A factory class to create different LLM clients
    """

    def __init__(self, load_env=False):
        """
        Initialize the factory

        Args:
            load_env (bool): Deprecated parameter, kept for backwards compatibility
        """
        # Common headers for web requests
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        # Register all available providers with their creation methods
        self.providers = {
            "openai": self._create_openai_client,
            "anthropic": self._create_anthropic_client,
            "google": self._create_google_client,
        }

        # Check which providers are available based on installed packages
        self._available_providers = self._get_installed_providers()

    def _get_installed_providers(self):
        """
        Check which provider packages are installed

        Returns:
            dict: Dictionary with provider names as keys and boolean values indicating availability
        """
        available = {provider: False for provider in self.providers.keys()}

        # Check OpenAI
        available["openai"] = importlib.util.find_spec("openai") is not None

        # Check Anthropic
        available["anthropic"] = importlib.util.find_spec("anthropic") is not None

        # Check Google
        available["google"] = (
            importlib.util.find_spec("google.generativeai") is not None
        )

        return available

    def _create_openai_client(self, **kwargs):
        """
        Internal method to create an OpenAI client

        Args:
            **kwargs: Additional arguments for client configuration
                      - model: The model to use (default: "gpt-4o-mini")
                      - client_type: Type of client to create (default: "summarizer")
                      - api_key: OpenAI API key (required)

        Returns:
            An instance of an OpenAI client of the requested type

        Raises:
            ValueError: If api_key is not provided or client_type is unknown
        """
        # Import here to avoid circular imports
        from .providers.openai import (
            WebsiteSummarizerOpenAI,
            ContentExtractorOpenAI,
            SentimentAnalyzerOpenAI,
            SEOAnalyzerOpenAI,
        )

        model = kwargs.get("model", "gpt-4o-mini")
        api_key = kwargs.get("api_key")

        if not api_key:
            raise ValueError("OpenAI API key is required")

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
            client = client_class(
                model=model, client=OpenAI(api_key=api_key), headers=self.headers
            )
        else:
            available_clients = ", ".join(client_classes.keys())
            raise ValueError(
                f"Unknown client type: {client_type}. Available types: {available_clients}"
            )

        return client

    def _create_anthropic_client(self, **kwargs):
        """
        Internal method to create an Anthropic client

        Args:
            **kwargs: Additional arguments for client configuration
                      - model: The model to use (default: "claude-3-haiku-20240307")
                      - client_type: Type of client to create (default: "summarizer")
                      - api_key: Anthropic API key (required)

        Returns:
            An instance of an Anthropic client of the requested type

        Raises:
            ValueError: If api_key is not provided, client_type is unknown, or Anthropic package is not installed
        """
        if not self._available_providers["anthropic"]:
            raise ImportError(
                "Anthropic package is not installed. Please install it with 'pip install anthropic'"
            )

        # Import Anthropic
        from anthropic import Anthropic

        # Import provider classes
        from .providers.anthropic import (
            WebsiteSummarizerAnthropic,
            ContentExtractorAnthropic,
            SentimentAnalyzerAnthropic,
            SEOAnalyzerAnthropic,
        )

        model = kwargs.get("model", "claude-3-haiku-20240307")
        api_key = kwargs.get("api_key")

        if not api_key:
            raise ValueError("Anthropic API key is required")

        client_type = kwargs.get("client_type", "summarizer")

        # Map client types to their respective classes
        client_classes = {
            "summarizer": WebsiteSummarizerAnthropic,
            "content_extractor": ContentExtractorAnthropic,
            "sentiment_analyzer": SentimentAnalyzerAnthropic,
            "seo_analyzer": SEOAnalyzerAnthropic,
        }

        if client_type in client_classes:
            client_class = client_classes[client_type]
            client = client_class(
                model=model, client=Anthropic(api_key=api_key), headers=self.headers
            )
        else:
            available_clients = ", ".join(client_classes.keys())
            raise ValueError(
                f"Unknown client type: {client_type}. Available types: {available_clients}"
            )

        return client

    def _create_google_client(self, **kwargs):
        """
        Internal method to create a Google (Gemini) client

        Args:
            **kwargs: Additional arguments for client configuration
                      - model: The model to use (default: "gemini-pro")
                      - client_type: Type of client to create (default: "summarizer")
                      - api_key: Google API key (required)

        Returns:
            An instance of a Google client of the requested type

        Raises:
            ValueError: If api_key is not provided, client_type is unknown, or Google package is not installed
        """
        if not self._available_providers["google"]:
            raise ImportError(
                "Google Generative AI package is not installed. Please install it with 'pip install google-generativeai'"
            )

        # Import Google Generative AI
        import google.generativeai as genai

        # Import provider classes
        from .providers.google import (
            WebsiteSummarizerGoogle,
            ContentExtractorGoogle,
            SentimentAnalyzerGoogle,
            SEOAnalyzerGoogle,
        )

        model = kwargs.get("model", "gemini-pro")
        api_key = kwargs.get("api_key")

        if not api_key:
            raise ValueError("Google API key is required")

        # Configure the Google API client
        genai.configure(api_key=api_key)

        client_type = kwargs.get("client_type", "summarizer")

        # Map client types to their respective classes
        client_classes = {
            "summarizer": WebsiteSummarizerGoogle,
            "content_extractor": ContentExtractorGoogle,
            "sentiment_analyzer": SentimentAnalyzerGoogle,
            "seo_analyzer": SEOAnalyzerGoogle,
        }

        if client_type in client_classes:
            client_class = client_classes[client_type]
            client = client_class(model=model, client=genai, headers=self.headers)
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
            provider (str): The provider to use (e.g., "openai", "anthropic", "google")
            **kwargs: Additional arguments for client configuration

        Returns:
            An instance of the requested client

        Raises:
            ValueError: If provider is unknown
        """
        provider_key = provider.lower()

        if provider_key in self.providers:
            if not self._available_providers[provider_key]:
                raise ImportError(
                    f"The {provider_key} package is not installed. Please install it first."
                )
            return self.providers[provider_key](**kwargs)
        else:
            available_providers = ", ".join(self.providers.keys())
            raise ValueError(
                f"Unknown provider: {provider}. Available providers: {available_providers}"
            )

    def get_available_providers(self):
        """
        Return a list of all available providers that are installed

        Returns:
            list: The names of all available providers
        """
        return [
            provider
            for provider, installed in self._available_providers.items()
            if installed
        ]

    def get_available_models(self, provider):
        """
        Return a list of available models for the specified provider

        Args:
            provider (str): The provider to get models for

        Returns:
            list: The available models for the provider

        Raises:
            ValueError: If provider is unknown
        """
        provider_key = provider.lower()

        if provider_key == "openai":
            return ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
        elif provider_key == "anthropic":
            return [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
            ]
        elif provider_key == "google":
            return ["gemini-1.0-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def get_available_client_types(self):
        """
        Return a list of all available client types

        Returns:
            list: The names of all available client types
        """
        return ["summarizer", "content_extractor", "sentiment_analyzer", "seo_analyzer"]
