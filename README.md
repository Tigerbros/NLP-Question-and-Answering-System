# NLP Question-and-Answering System (CLI + Streamlit)

This project is a question-and-answering chatbot that connects to an OpenRouter-hosted LLM. It ships with both a Python CLI and a Streamlit front end so you can send a question, view the pre-processing and prompt, and receive an answer from the model.

## Prerequisites
- Python 3.10+
- An OpenRouter API key stored in `OPENROUTER_API_KEY` (recommended) or provided at runtime. `OPEN_ROUTER_KEY` is also accepted for convenience. A sample `.env` loader is included so you can store the key in a local `.env` file that remains untracked.

Install dependencies:
```bash
pip install -r requirements.txt  # Streamlit UI only; the CLI uses stdlib networking
```

Copy the sample environment file and keep your real key out of version control:
```bash
cp .env.example .env
echo "OPENROUTER_API_KEY=sk-or-..." >> .env  # .env is already gitignored
```

## Prompt and processing
- The reusable template lives in [`prompts/qa_prompt.txt`](prompts/qa_prompt.txt) and is tailored for concise, assumption-aware answers.
- Questions are lowercased, punctuation is removed, and tokens are displayed so you can see how the text is cleaned before being sent to the model.

Environment variables are loaded automatically from a local `.env` file (gitignored) if present, so you can keep your key out of version control while running locally.

## Part A — Python CLI (`LLM_QA_CLI.py`)
Run a question through preprocessing, prompt templating, and an OpenRouter request:

```bash
export OPENROUTER_API_KEY="your-key"  # or set it in a local .env file
python LLM_QA_CLI.py "What are the benefits of regular walking?"

# override defaults
python LLM_QA_CLI.py "How does photosynthesis work?" --model anthropic/claude-3-haiku --show-prompt
```

Flags:
- `--model`: OpenRouter model name (default: `x-ai/grok-4.1-fast:free`).
- `--api-key`: Provide the API key directly (falls back to `OPENROUTER_API_KEY`).
- `--show-prompt`: Print the rendered prompt before sending it.

The CLI prints the normalized question, token list, and the LLM response. Errors from the API are surfaced directly for easier debugging.

## Part B — Streamlit Web GUI (`app.py`)
Launch the UI locally:

```bash
export OPENROUTER_API_KEY="your-key"  # or set it in a local .env file
streamlit run app.py
```

Features:
- Sidebar fields for OpenRouter API key (persisted for the session) and model name (default `x-ai/grok-4.1-fast:free`).
- Text area for the user's question.
- Expanders showing the processed question (cleaned text and tokens) and rendered prompt.
- Live OpenRouter calls with inline error reporting and an end-to-end pipeline that pre-processes your question before sending it to the LLM.

### Streamlit Cloud secrets
- Add `OPENROUTER_API_KEY` to **Secrets** in Streamlit Cloud (preferred) or set it as an environment variable in your hosting platform.
- The UI reads secrets first, then session state, then environment variables. No keys are committed to the repository.

## Part C — Deployment notes
The Streamlit UI can be deployed on Streamlit Cloud, Render, PythonAnywhere, or similar services. Before deploying:
- Set `OPENROUTER_API_KEY` as an environment variable in the hosting platform.
- Keep `prompts/qa_prompt.txt` in the deployed bundle for consistent prompting.
- Ensure outgoing HTTPS access to `https://openrouter.ai/api/v1/chat/completions` is permitted by the host.

For submission, include `LLM_QA_hosted_webGUI_link.txt` with your name, matric number, live URL, and GitHub repository link (a template file is provided).

## Project layout
- [`qa_utils.py`](qa_utils.py): Shared preprocessing, prompt loading, and OpenRouter client logic.
- [`LLM_QA_CLI.py`](LLM_QA_CLI.py): CLI entry point.
- [`app.py`](app.py): Streamlit front end mirroring CLI behavior.
- [`prompts/qa_prompt.txt`](prompts/qa_prompt.txt): Reusable prompt template.
- `LLM_QA_hosted_webGUI_link.txt`: Fill in with your deployment details when hosted.
