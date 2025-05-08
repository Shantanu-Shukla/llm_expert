"""
Google (Gemini) provider implementations.
"""

from llm_client.clients.summarizer import WebsiteSummarizer
from llm_client.clients.extractor import ContentExtractor
from llm_client.clients.sentiment import SentimentAnalyzer
from llm_client.clients.seo import SEOAnalyzer


class GoogleClientMixin:
    """
    Mixin to handle Google Gemini-specific client interactions
    """

    def process(self, url, *args, **kwargs):
        """
        Process a URL using Google's Gemini model

        Args:
            url (str): The URL to process
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            str: The processed result
        """
        website_data = self.fetch_website_content(url)
        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(website_data, *args, **kwargs)

        # Format the prompt for Gemini
        # Combine system prompt and user prompt since Gemini doesn't have a separate system prompt
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"

        try:
            # Get the model - ensure we're using the correct model name format
            # The model name in the factory might need to be adjusted based on the actual model name
            model_name = self.model
            gemini_model = self.client.GenerativeModel(model_name)

            # Generate content
            response = gemini_model.generate_content(combined_prompt)

            return response.text
        except Exception as e:
            # If there's an error with the model name, try to list available models
            try:
                available_models = [model.name for model in self.client.list_models()]
                available_models_str = ", ".join(available_models)
                return f"Error with Gemini model '{self.model}'. Available models: {available_models_str}\nOriginal error: {str(e)}"
            except:
                # If we can't list models, just return the original error
                return f"Error with Gemini model '{self.model}': {str(e)}"


class WebsiteSummarizerGoogle(GoogleClientMixin, WebsiteSummarizer):
    """
    Google implementation of WebsiteSummarizer
    """

    pass


class ContentExtractorGoogle(GoogleClientMixin, ContentExtractor):
    """
    Google implementation of ContentExtractor
    """

    pass


class SentimentAnalyzerGoogle(GoogleClientMixin, SentimentAnalyzer):
    """
    Google implementation of SentimentAnalyzer
    """

    pass


class SEOAnalyzerGoogle(GoogleClientMixin, SEOAnalyzer):
    """
    Google implementation of SEOAnalyzer
    """

    pass
