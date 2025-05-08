"""
Content extractor client module.
"""

from llm_client.llm_client import BaseClient


class ContentExtractor(BaseClient):
    """
    Client for extracting specific information from websites
    """

    def get_system_prompt(self):
        """
        Get the system prompt for the extractor

        Returns:
            str: The system prompt
        """
        return """You are an assistant that extracts specific information from websites.
                Extract only the requested information in a structured format."""

    def get_user_prompt(self, website_data, target_info, *args, **kwargs):
        """
        Get the user prompt for the extractor

        Args:
            website_data (dict): The website data
            target_info (str): The information to extract
            *args: Additional arguments (not used)
            **kwargs: Additional keyword arguments (not used)

        Returns:
            str: The user prompt
        """
        return f"""Extract the following information from this website titled {website_data['title']}: 
                {target_info}

                Website content:
                {website_data['text']}"""
