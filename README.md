# OpenRouter Q&A Starter

This project scaffolds a question-and-answering workflow that targets OpenRouter's free-access models. It ships with:

- A reusable prompt template with clear behavioral constraints.
- A Python CLI (`LLM_QA_CLI.py`) that preprocesses user questions, builds the prompt, and exposes a placeholder for the LLM call.
- A Streamlit front end (`app.py`) that mirrors the CLI workflow for deployment on Streamlit Cloud or similar hosting.

## Prompt design
The prompt template lives in [`prompts/qa_prompt.txt`](prompts/qa_prompt.txt). It emphasizes concise, assumption-aware answers and keeps formatting minimal. Both the CLI and the Streamlit app load this file to ensure consistent behavior across interfaces.

## Running the CLI
```bash
python LLM_QA_CLI.py "What are the benefits of regular walking?"
```

Flags:
- `--model`: OpenRouter model name (default: `gryphe/mythomist-7b`).
- `--show-prompt`: Display the full rendered prompt.

## Running the Streamlit app locally
```bash
streamlit run app.py
```

Adjust the model hint and API key in the sidebar. The LLM call is stubbed; add your OpenRouter HTTP request inside `send_to_llm_placeholder` in `qa_utils.py`.

## Deployment notes
The Streamlit UI is suitable for Streamlit Cloud, Render, or similar services. Ensure the following when deploying:
- Set the `OPENROUTER_API_KEY` environment variable.
- Keep `prompts/qa_prompt.txt` in the deployed bundle so the prompt remains consistent.
- After wiring the API call, avoid logging full prompts or keys to protect user data.