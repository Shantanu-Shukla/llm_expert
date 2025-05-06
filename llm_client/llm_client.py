"""
Base client module for LLM interactions and website processing.
"""

import requests
from bs4 import BeautifulSoup


class BaseClient:
    """
    Base class for all LLM clients with web content processing capabilities
    """

    def __init__(self, model, client, headers):
        """
        Initialize the base client

        Args:
            model (str): The model to use
            client: The client instance for the LLM provider
            headers (dict): Headers to use for HTTP requests
        """
        self.model = model
        self.client = client
        self.headers = headers

    def fetch_website_content(self, url):
        """
        Fetch and parse content from a website

        Args:
            url (str): The URL to fetch

        Returns:
            dict: A dictionary containing the website data
                - url: The original URL
                - title: The website title
                - text: The extracted text content
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title = soup.title.string if soup.title else "No title found"

            # Clean up the content
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                text = soup.body.get_text(separator="\n", strip=True)
            else:
                text = "No body content found"

            return {"url": url, "title": title, "text": text}

        except Exception as e:
            return {
                "url": url,
                "title": "Error",
                "text": f"Failed to fetch website: {str(e)}",
            }

    def get_system_prompt(self):
        """
        Get the system prompt for this client

        Returns:
            str: The system prompt

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        # Each subclass should override this method
        raise NotImplementedError("Subclasses must implement get_system_prompt()")

    def get_user_prompt(self, website_data, *args, **kwargs):
        """
        Get the user prompt for this client

        Args:
            website_data (dict): The website data
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            str: The user prompt

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        # Each subclass should override this method
        raise NotImplementedError("Subclasses must implement get_user_prompt()")

    def get_messages(self, website_data, *args, **kwargs):
        """
        Get the messages for the LLM

        Args:
            website_data (dict): The website data
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            list: A list of message dictionaries
        """
        return [
            {"role": "system", "content": self.get_system_prompt()},
            {
                "role": "user",
                "content": self.get_user_prompt(website_data, *args, **kwargs),
            },
        ]

    def process(self, url, *args, **kwargs):
        """
        Process a URL

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

    def display_result(self, url, *args, **kwargs):
        """
        Display the result

        Args:
            url (str): The URL to process
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            str: The processed result
        """
        result = self.process(url, *args, **kwargs)
        print(result)
        return result
