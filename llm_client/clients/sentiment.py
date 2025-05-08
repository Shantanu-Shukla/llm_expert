"""
Sentiment analyzer client module.
"""

from llm_client.llm_client import BaseClient


class SentimentAnalyzer(BaseClient):
    """
    Client for analyzing the sentiment of website content
    """

    def get_system_prompt(self):
        """
        Get the system prompt for the sentiment analyzer

        Returns:
            str: The system prompt
        """
        return """You are an assistant that analyzes the sentiment of website content.
                Categorize the sentiment as positive, negative, or neutral and explain why."""

    def get_user_prompt(self, website_data, *args, **kwargs):
        """
        Get the user prompt for the sentiment analyzer

        Args:
            website_data (dict): The website data
            *args: Additional arguments (not used)
            **kwargs: Additional keyword arguments (not used)

        Returns:
            str: The user prompt
        """
        return f"""Analyze the sentiment of this website titled {website_data['title']}. 
                Is it positive, negative, or neutral? Explain why.

                Content:
                {website_data['text']}"""
