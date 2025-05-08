"""
Streamlit app for LLM client with tabbed interface.
"""

import streamlit as st

# Import the LLM client package
# This assumes the package is installed or in the same directory
from llm_client import LLMClientFactory

# Set page configuration
st.set_page_config(
    page_title="LLM Website Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "current_result" not in st.session_state:
        st.session_state.current_result = ""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = "openai"


def create_factory():
    """Create and return the LLM client factory."""
    try:
        factory = LLMClientFactory()
        return factory
    except Exception as e:
        st.error(f"Error initializing LLM Client Factory: {str(e)}")
        return None


def on_provider_change():
    """Called when the provider selection changes."""
    # This resets the model selection when the provider changes
    pass


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.title("LLM Website Analyzer")
        st.markdown("Analyze websites using various LLM providers.")

        # Create factory to get available providers and models
        factory = create_factory()
        if not factory:
            st.error("Failed to initialize LLM client factory.")
            return "", "openai", "gpt-4o-mini"  # Default values if factory fails

        # API Key input (first)
        st.header("API Key")
        api_key = st.text_input(
            "Enter API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter the API key for your selected LLM provider",
        )

        # Save API key to session state
        if api_key:
            st.session_state.api_key = api_key

        # LLM Settings (second)
        st.header("LLM Settings")

        # Get available providers
        try:
            available_providers = factory.get_available_providers()
            if not available_providers:
                st.warning(
                    "No LLM providers found. Please install at least one provider package."
                )
                available_providers = ["openai"]  # Default fallback
        except Exception as e:
            st.error(f"Error getting available providers: {str(e)}")
            available_providers = ["openai"]  # Fallback

        # Provider selection
        provider = st.selectbox(
            "Select Provider",
            options=available_providers,
            index=(
                available_providers.index(st.session_state.selected_provider)
                if st.session_state.selected_provider in available_providers
                else 0
            ),
            on_change=on_provider_change,
            key="provider_selector",
        )

        # Update the selected provider in session state
        st.session_state.selected_provider = provider

        # Get available models for the selected provider
        try:
            available_models = factory.get_available_models(provider)
        except Exception as e:
            st.error(f"Error getting available models: {str(e)}")
            available_models = []  # Fallback

            # Provider-specific fallbacks
            if provider == "openai":
                available_models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
            elif provider == "anthropic":
                available_models = [
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307",
                ]
            elif provider == "google":
                available_models = ["gemini-pro", "gemini-pro-vision"]

        # Model selection
        model = st.selectbox("Select Model", options=available_models, index=0)

        # Create a button to clear history
        if st.button("Clear History"):
            st.session_state.history = []
            st.session_state.current_result = ""
            st.success("History cleared!")

        return api_key, provider, model


def process_website(url, provider, model, client_type, api_key, additional_params=None):
    """
    Process a website using the specified LLM provider and client type.

    Args:
        url (str): The website URL to process
        provider (str): The LLM provider to use
        model (str): The model to use
        client_type (str): The type of analysis to perform
        api_key (str): The API key for the selected provider
        additional_params (dict, optional): Additional parameters for the client

    Returns:
        str: The processing result or error message
    """
    if not url:
        return "Please enter a website URL."

    if not api_key:
        return "Please enter your API key in the sidebar."

    try:
        factory = create_factory()
        if not factory:
            return "Failed to create LLM client factory."

        # Create client with selected options
        client_kwargs = {"model": model, "client_type": client_type, "api_key": api_key}

        client = factory.create_client(provider, **client_kwargs)

        # Process the URL with any additional parameters
        if additional_params:
            result = client.process(url, **additional_params)
        else:
            result = client.process(url)

        # Store the result
        st.session_state.current_result = result

        # Add to history
        st.session_state.history.append(
            {
                "url": url,
                "provider": provider,
                "model": model,
                "client_type": client_type,
                "result": result,
            }
        )

        return result

    except Exception as e:
        return f"Error processing website: {str(e)}"


def render_summarizer_tab(api_key, provider, model):
    """Render the website summarizer tab."""
    st.header("Website Summary")
    st.markdown("Get a concise summary of any website's content.")

    url = st.text_input(
        "Enter Website URL", value="https://example.com", key="summarizer_url"
    )

    process_clicked = st.button(
        "Generate Summary", type="primary", key="summarizer_btn"
    )

    if process_clicked:
        with st.spinner("Analyzing website..."):
            result = process_website(url, provider, model, "summarizer", api_key)
            st.markdown(result)


def render_extractor_tab(api_key, provider, model):
    """Render the content extractor tab."""
    st.header("Content Extraction")
    st.markdown("Extract specific information from websites.")

    url = st.text_input(
        "Enter Website URL", value="https://example.com", key="extractor_url"
    )

    extraction_targets = st.text_area(
        "Information to Extract",
        value="company name, main products, contact information",
        help="Specify what information to extract from the website",
    )

    process_clicked = st.button("Extract Content", type="primary", key="extractor_btn")

    if process_clicked:
        with st.spinner("Extracting content..."):
            result = process_website(
                url,
                provider,
                model,
                "content_extractor",
                api_key,
                {"target_info": extraction_targets},
            )
            st.markdown(result)


def render_sentiment_tab(api_key, provider, model):
    """Render the sentiment analyzer tab."""
    st.header("Sentiment Analysis")
    st.markdown("Analyze the sentiment and tone of website content.")

    url = st.text_input(
        "Enter Website URL", value="https://example.com", key="sentiment_url"
    )

    process_clicked = st.button(
        "Analyze Sentiment", type="primary", key="sentiment_btn"
    )

    if process_clicked:
        with st.spinner("Analyzing sentiment..."):
            result = process_website(
                url, provider, model, "sentiment_analyzer", api_key
            )
            st.markdown(result)


def render_seo_tab(api_key, provider, model):
    """Render the SEO analyzer tab."""
    st.header("SEO Analysis")
    st.markdown("Analyze website content for search engine optimization.")

    url = st.text_input("Enter Website URL", value="https://example.com", key="seo_url")

    process_clicked = st.button("Analyze SEO", type="primary", key="seo_btn")

    if process_clicked:
        with st.spinner("Analyzing SEO..."):
            result = process_website(url, provider, model, "seo_analyzer", api_key)
            st.markdown(result)


def render_history_tab():
    """Render the history tab."""
    st.header("Analysis History")

    if not st.session_state.history:
        st.info("No analysis history yet. Try analyzing a website first!")
        return

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(
            f"#{len(st.session_state.history) - i}: {item['url']} ({item['client_type']})"
        ):
            st.markdown(f"**Provider:** {item['provider']}")
            st.markdown(f"**Model:** {item['model']}")
            st.markdown(f"**Analysis Type:** {item['client_type']}")
            st.markdown("**Result:**")
            st.markdown(item["result"])


def main():
    """Main function to run the Streamlit app."""
    initialize_session_state()

    # Render sidebar and get configuration
    api_key, provider, model = render_sidebar()

    # Create tabs for different analysis types
    summarizer_tab, extractor_tab, sentiment_tab, seo_tab, history_tab = st.tabs(
        [
            "Website Summary",
            "Content Extraction",
            "Sentiment Analysis",
            "SEO Analysis",
            "History",
        ]
    )

    # Render content for each tab
    with summarizer_tab:
        render_summarizer_tab(api_key, provider, model)

    with extractor_tab:
        render_extractor_tab(api_key, provider, model)

    with sentiment_tab:
        render_sentiment_tab(api_key, provider, model)

    with seo_tab:
        render_seo_tab(api_key, provider, model)

    with history_tab:
        render_history_tab()


if __name__ == "__main__":
    main()
