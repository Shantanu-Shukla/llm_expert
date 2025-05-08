"""
Website summarizer client module.
"""

from llm_client.llm_client import BaseClient


class WebsiteSummarizer(BaseClient):
    """
    Client for summarizing website content
    """

    def get_system_prompt(self):
        """
        Get the system prompt for the summarizer

        Returns:
            str: The system prompt
        """
        return """You are an assistant that analyzes the contents of a website 
                and provides a short summary, ignoring text that might be navigation related. 
                Respond in markdown."""

    def get_user_prompt(self, website_data, *args, **kwargs):
        """
        Get the user prompt for the summarizer

        Args:
            website_data (dict): The website data
            *args: Additional arguments (not used)
            **kwargs: Additional keyword arguments (not used)

        Returns:
            str: The user prompt
        """
        return f"""You are looking at a website titled {website_data['title']}. 
                The contents of this website is as follows; 
                please provide a short summary of this website in markdown. 
                If it includes news or announcements, then summarize these too.

                {website_data['text']}"""
