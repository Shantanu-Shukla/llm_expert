"""
Example usage of the LLM client package.
"""

from llm_client import LLMClientFactory


def main():
    # Create the factory
    factory = LLMClientFactory()

    # Get an OpenAI client for website summarization
    summarizer = factory.create_client(
        "openai", model="gpt-4o-mini", client_type="summarizer"
    )
    print("Website Summary:")
    summary = summarizer.display_result("https://arthapeek.com/")
    print("\n" + "-" * 50 + "\n")

    # Get an OpenAI client for content extraction
    extractor = factory.create_client(
        "openai", model="gpt-4o-mini", client_type="content_extractor"
    )
    print("Extracted Content:")
    extracted_info = extractor.display_result(
        "https://arthapeek.com/", "company name, main services, contact information"
    )
    print("\n" + "-" * 50 + "\n")

    # Get an OpenAI client for sentiment analysis
    sentiment_analyzer = factory.create_client(
        "openai", model="gpt-4o-mini", client_type="sentiment_analyzer"
    )
    print("Sentiment Analysis:")
    sentiment = sentiment_analyzer.display_result("https://arthapeek.com/")
    print("\n" + "-" * 50 + "\n")

    # Get an OpenAI client for SEO analysis
    seo_analyzer = factory.create_client(
        "openai", model="gpt-4o-mini", client_type="seo_analyzer"
    )
    print("SEO Analysis:")
    seo_analysis = seo_analyzer.display_result("https://arthapeek.com/")
    print("\n" + "-" * 50 + "\n")

    # Using Ollama provider (if available)
    try:
        ollama_summarizer = factory.create_client(
            "ollama", model="llama3.2", client_type="summarizer"
        )
        print("Ollama Website Summary:")
        ollama_summary = ollama_summarizer.display_result("https://arthapeek.com/")
    except Exception as e:
        print(f"Ollama client error: {str(e)}")


if __name__ == "__main__":
    main()
