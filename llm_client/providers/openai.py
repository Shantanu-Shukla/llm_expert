"""
OpenAI provider implementations.
"""

from llm_client.clients.summarizer import WebsiteSummarizer
from llm_client.clients import ContentExtractor
from llm_client.clients import SentimentAnalyzer
from llm_client.clients import SEOAnalyzer


class WebsiteSummarizerOpenAI(WebsiteSummarizer):
    """
    OpenAI implementation of WebsiteSummarizer
    """

    pass


class ContentExtractorOpenAI(ContentExtractor):
    """
    OpenAI implementation of ContentExtractor
    """

    pass


class SentimentAnalyzerOpenAI(SentimentAnalyzer):
    """
    OpenAI implementation of SentimentAnalyzer
    """

    pass


class SEOAnalyzerOpenAI(SEOAnalyzer):
    """
    OpenAI implementation of SEOAnalyzer
    """

    pass
