"""Streamlit front end for the OpenRouter Q&A system."""

import os
from typing import Optional

import streamlit as st

from qa_utils import DEFAULT_MODEL, run_qa_pipeline

st.set_page_config(page_title="OpenRouter Q&A", page_icon="❓")


def get_api_key() -> Optional[str]:
    """Return the API key, preferring Streamlit secrets when set."""

    preset = st.secrets.get("OPENROUTER_API_KEY", "") if hasattr(st, "secrets") else ""
    env_default = os.getenv("OPENROUTER_API_KEY", os.getenv("OPEN_ROUTER_KEY", ""))
    initial_value = st.session_state.get("OPENROUTER_API_KEY", preset or env_default)

    api_key = st.sidebar.text_input(
        "OpenRouter API Key",
        value=initial_value,
        type="password",
        help=(
            "Stored locally for this session. Use Streamlit secrets or host-level env vars to keep it private."
        ),
    )
    if api_key:
        st.session_state["OPENROUTER_API_KEY"] = api_key
    return api_key or st.session_state.get("OPENROUTER_API_KEY") or preset or env_default


def render_sidebar() -> tuple[str, str]:
    st.sidebar.header("Configuration")
    api_key = get_api_key()
    model = st.sidebar.text_input("Model", value=DEFAULT_MODEL)
    st.sidebar.markdown(
        "Using OpenRouter's free tier models. Update the name if you upgrade."
    )
    return api_key, model


def main() -> None:
    st.title("PromptPilot Q&A (OpenRouter)")
    st.write(
        "Ask a question, review the preprocessed text, and preview the prompt sent to the LLM."
    )

    api_key, model = render_sidebar()
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPEN_ROUTER_KEY")

    question = st.text_area("Your question", placeholder="How can I improve my focus while studying?")
    if st.button("Submit"):
        if not api_key:
            st.error("Please provide an OpenRouter API key in the sidebar or your environment.")
            return
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        with st.spinner("Waiting for OpenRouter..."):
            try:
                result = run_qa_pipeline(question, model=model, api_key=api_key)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Failed to reach OpenRouter: {exc}")
                return

        processed = result["processed"]
        prompt = result["prompt"]
        response = result["answer"]

        with st.expander("Processed question"):
            st.write(processed["cleaned"])
            st.write({"tokens": processed["tokens"]})

        with st.expander("Rendered prompt"):
            st.code(prompt)

        st.subheader("LLM response")
        st.write(response)


if __name__ == "__main__":
    main()
