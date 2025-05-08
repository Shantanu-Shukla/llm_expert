"""
SEO analyzer client module.
"""

from llm_client.llm_client import BaseClient


class SEOAnalyzer(BaseClient):
    """
    Client for performing SEO analysis on website content
    """

    def get_system_prompt(self):
        """
        Get the system prompt for the SEO analyzer

        Returns:
            str: The system prompt
        """
        return """You are an SEO expert analyzing website content. Identify key SEO elements,
                keywords, and provide recommendations for improvement."""

    def get_user_prompt(self, website_data, *args, **kwargs):
        """
        Get the user prompt for the SEO analyzer

        Args:
            website_data (dict): The website data
            *args: Additional arguments (not used)
            **kwargs: Additional keyword arguments (not used)

        Returns:
            str: The user prompt
        """
        return f"""Perform an SEO analysis of this website titled {website_data['title']}. 
                Identify key keywords, meta information, and content structure.

                Content:
                {website_data['text']}"""
