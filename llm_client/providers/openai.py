"""
OpenAI provider implementations.
"""

from llm_client.clients.summarizer import WebsiteSummarizer
from llm_client.clients.extractor import ContentExtractor
from llm_client.clients.sentiment import SentimentAnalyzer
from llm_client.clients.seo import SEOAnalyzer


class OpenAIClientMixin:
    """
    Mixin to handle OpenAI-specific client interactions
    """

    def process(self, url, *args, **kwargs):
        """
        Process a URL using OpenAI model

        Args:
            url (str): The URL to process
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            str: The processed result
        """
        website_data = self.fetch_website_content(url)
        messages = self.get_messages(website_data, *args, **kwargs)

        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content


class WebsiteSummarizerOpenAI(OpenAIClientMixin, WebsiteSummarizer):
    """
    OpenAI implementation of WebsiteSummarizer
    """

    pass


class ContentExtractorOpenAI(OpenAIClientMixin, ContentExtractor):
    """
    OpenAI implementation of ContentExtractor
    """

    pass


class SentimentAnalyzerOpenAI(OpenAIClientMixin, SentimentAnalyzer):
    """
    OpenAI implementation of SentimentAnalyzer
    """

    pass


class SEOAnalyzerOpenAI(OpenAIClientMixin, SEOAnalyzer):
    """
    OpenAI implementation of SEOAnalyzer
    """

    pass
