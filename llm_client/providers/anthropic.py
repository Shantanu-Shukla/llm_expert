"""
Anthropic (Claude) provider implementations.
"""

from llm_client.clients.summarizer import WebsiteSummarizer
from llm_client.clients.extractor import ContentExtractor
from llm_client.clients.sentiment import SentimentAnalyzer
from llm_client.clients.seo import SEOAnalyzer


class AnthropicClientMixin:
    """
    Mixin to handle Claude-specific client interactions
    """

    def process(self, url, *args, **kwargs):
        """
        Process a URL using Anthropic's Claude model

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

        # Format the prompt for Claude
        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=4096,
        )

        # Extract the content from the response
        return response.content[0].text


class WebsiteSummarizerAnthropic(AnthropicClientMixin, WebsiteSummarizer):
    """
    Anthropic implementation of WebsiteSummarizer
    """

    pass


class ContentExtractorAnthropic(AnthropicClientMixin, ContentExtractor):
    """
    Anthropic implementation of ContentExtractor
    """

    pass


class SentimentAnalyzerAnthropic(AnthropicClientMixin, SentimentAnalyzer):
    """
    Anthropic implementation of SentimentAnalyzer
    """

    pass


class SEOAnalyzerAnthropic(AnthropicClientMixin, SEOAnalyzer):
    """
    Anthropic implementation of SEOAnalyzer
    """

    pass
