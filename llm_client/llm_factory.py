from openai import OpenAI

class LLMClientFactory:
    """
    A factory class to create different LLM clients
    """
    
    def __init__(self):
        """
        Initialize the factory
        """
        # Common headers for web requests
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        
        # Register all available providers with their creation methods
        self.providers = {
            "openai": self._create_openai_client,
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
            SEOAnalyzerOpenAI
        )
        
        model = kwargs.get('model', "gpt-4o-mini")
        api_key = kwargs.get('api_key')
        
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        client_type = kwargs.get('client_type', 'summarizer')
        
        # Map client types to their respective classes
        client_classes = {
            'summarizer': WebsiteSummarizerOpenAI,
            'content_extractor': ContentExtractorOpenAI,
            'sentiment_analyzer': SentimentAnalyzerOpenAI,
            'seo_analyzer': SEOAnalyzerOpenAI
        }
        
        if client_type in client_classes:
            client_class = client_classes[client_type]
            client = client_class(
                model=model,
                client=OpenAI(api_key=api_key),
                headers=self.headers
            )
        else:
            available_clients = ", ".join(client_classes.keys())
            raise ValueError(f"Unknown client type: {client_type}. Available types: {available_clients}")
            
        return client
    
    def create_client(self, provider, **kwargs):
        """
        Create a client based on provider name
        
        Args:
            provider (str): The provider to use (e.g., "openai")
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
            raise ValueError(f"Unknown provider: {provider}. Available providers: {available_providers}")
    
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
        else:
            raise ValueError(f"Unknown provider: {provider}")
            
    def get_available_client_types(self):
        """
        Return a list of all available client types
        
        Returns:
            list: The names of all available client types
        """
        return ["summarizer", "content_extractor", "sentiment_analyzer", "seo_analyzer"]
