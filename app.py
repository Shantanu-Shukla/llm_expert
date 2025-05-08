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


def create_factory():
    """Create and return the LLM client factory."""
    try:
        factory = LLMClientFactory(load_env=False)
        return factory
    except Exception as e:
        st.error(f"Error initializing LLM Client Factory: {str(e)}")
        return None


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.title("LLM Website Analyzer")
        st.markdown("Analyze websites using OpenAI models.")

        # API Key input
        st.header("API Key")
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Your OpenAI API key is required to use this application",
        )

        # Save API key to session state
        if api_key:
            st.session_state.api_key = api_key

        # Model selection
        st.header("Model Settings")
        model = st.selectbox(
            "OpenAI Model", options=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0
        )

        # Create a button to clear history
        if st.button("Clear History"):
            st.session_state.history = []
            st.session_state.current_result = ""
            st.success("History cleared!")

        return api_key, model


def render_summarizer_tab(api_key, model):
    """Render the website summarizer tab."""
    st.header("Website Summary")
    st.markdown("Get a concise summary of any website's content.")

    url = st.text_input(
        "Enter Website URL", value="https://example.com", key="summarizer_url"
    )

    process_clicked = st.button(
        "Generate Summary", type="primary", key="summarizer_btn"
    )

    if process_clicked and url and api_key:
        with st.spinner("Analyzing website..."):
            try:
                factory = create_factory()
                if not factory:
                    st.error("Failed to create LLM client factory.")
                    return

                # Create summarizer client
                client = factory.create_client(
                    "openai", model=model, client_type="summarizer"
                )

                # Override the API key in the client
                client.client.api_key = api_key

                # Process the URL
                result = client.process(url)

                # Store the result
                st.session_state.current_result = result

                # Add to history
                st.session_state.history.append(
                    {
                        "url": url,
                        "model": model,
                        "client_type": "summarizer",
                        "result": result,
                    }
                )

                # Display result
                st.markdown(result)

            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")
    elif process_clicked and not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")


def render_extractor_tab(api_key, model):
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

    if process_clicked and url and api_key:
        with st.spinner("Extracting content..."):
            try:
                factory = create_factory()
                if not factory:
                    st.error("Failed to create LLM client factory.")
                    return

                # Create extractor client
                client = factory.create_client(
                    "openai", model=model, client_type="content_extractor"
                )

                # Override the API key in the client
                client.client.api_key = api_key

                # Process the URL
                result = client.process(url, extraction_targets)

                # Store the result
                st.session_state.current_result = result

                # Add to history
                st.session_state.history.append(
                    {
                        "url": url,
                        "model": model,
                        "client_type": "content_extractor",
                        "result": result,
                    }
                )

                # Display result
                st.markdown(result)

            except Exception as e:
                st.error(f"Error extracting content: {str(e)}")
    elif process_clicked and not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")


def render_sentiment_tab(api_key, model):
    """Render the sentiment analyzer tab."""
    st.header("Sentiment Analysis")
    st.markdown("Analyze the sentiment and tone of website content.")

    url = st.text_input(
        "Enter Website URL", value="https://example.com", key="sentiment_url"
    )

    process_clicked = st.button(
        "Analyze Sentiment", type="primary", key="sentiment_btn"
    )

    if process_clicked and url and api_key:
        with st.spinner("Analyzing sentiment..."):
            try:
                factory = create_factory()
                if not factory:
                    st.error("Failed to create LLM client factory.")
                    return

                # Create sentiment analyzer client
                client = factory.create_client(
                    "openai", model=model, client_type="sentiment_analyzer"
                )

                # Override the API key in the client
                client.client.api_key = api_key

                # Process the URL
                result = client.process(url)

                # Store the result
                st.session_state.current_result = result

                # Add to history
                st.session_state.history.append(
                    {
                        "url": url,
                        "model": model,
                        "client_type": "sentiment_analyzer",
                        "result": result,
                    }
                )

                # Display result
                st.markdown(result)

            except Exception as e:
                st.error(f"Error analyzing sentiment: {str(e)}")
    elif process_clicked and not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")


def render_seo_tab(api_key, model):
    """Render the SEO analyzer tab."""
    st.header("SEO Analysis")
    st.markdown("Analyze website content for search engine optimization.")

    url = st.text_input("Enter Website URL", value="https://example.com", key="seo_url")

    process_clicked = st.button("Analyze SEO", type="primary", key="seo_btn")

    if process_clicked and url and api_key:
        with st.spinner("Analyzing SEO..."):
            try:
                factory = create_factory()
                if not factory:
                    st.error("Failed to create LLM client factory.")
                    return

                # Create SEO analyzer client
                client = factory.create_client(
                    "openai", model=model, client_type="seo_analyzer"
                )

                # Override the API key in the client
                client.client.api_key = api_key

                # Process the URL
                result = client.process(url)

                # Store the result
                st.session_state.current_result = result

                # Add to history
                st.session_state.history.append(
                    {
                        "url": url,
                        "model": model,
                        "client_type": "seo_analyzer",
                        "result": result,
                    }
                )

                # Display result
                st.markdown(result)

            except Exception as e:
                st.error(f"Error analyzing SEO: {str(e)}")
    elif process_clicked and not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")


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
            st.markdown(f"**Model:** {item['model']}")
            st.markdown(f"**Analysis Type:** {item['client_type']}")
            st.markdown("**Result:**")
            st.markdown(item["result"])


def main():
    """Main function to run the Streamlit app."""
    initialize_session_state()

    # Render sidebar and get configuration
    api_key, model = render_sidebar()

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
        render_summarizer_tab(api_key, model)

    with extractor_tab:
        render_extractor_tab(api_key, model)

    with sentiment_tab:
        render_sentiment_tab(api_key, model)

    with seo_tab:
        render_seo_tab(api_key, model)

    with history_tab:
        render_history_tab()


if __name__ == "__main__":
    main()
