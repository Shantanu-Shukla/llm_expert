"""
Ollama provider implementations.
"""

from llm_client.clients.summarizer import WebsiteSummarizer
from llm_client.clients.extractor import ContentExtractor
from llm_client.clients.sentiment import SentimentAnalyzer
from llm_client.clients.seo import SEOAnalyzer


class WebsiteSummarizerOllama(WebsiteSummarizer):
    """
    Ollama implementation of WebsiteSummarizer
    """

    pass


class ContentExtractorOllama(ContentExtractor):
    """
    Ollama implementation of ContentExtractor
    """

    pass


class SentimentAnalyzerOllama(SentimentAnalyzer):
    """
    Ollama implementation of SentimentAnalyzer
    """

    pass


class SEOAnalyzerOllama(SEOAnalyzer):
    """
    Ollama implementation of SEOAnalyzer
    """

    pass
