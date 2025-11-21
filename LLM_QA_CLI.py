"""Command-line interface for the OpenRouter Q&A system."""

import argparse
import os
from typing import Optional

from qa_utils import DEFAULT_MODEL, run_qa_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Send a question to an OpenRouter model with basic preprocessing and prompt templating."
        )
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Natural-language question to send to the LLM.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="OpenRouter model name (default: %(default)s)",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (defaults to OPENROUTER_API_KEY environment variable)",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Display the rendered prompt before sending it to the LLM.",
    )
    return parser.parse_args()


def get_question(question_arg: Optional[str]) -> str:
    if question_arg:
        return question_arg
    return input("Enter your question: ")


def main() -> None:
    args = parse_args()
    question = get_question(args.question)

    try:
        result = run_qa_pipeline(
            question,
            model=args.model,
            api_key=args.api_key,
        )
    except Exception as exc:  # noqa: BLE001
        print("Failed to reach OpenRouter:", exc)
        return

    processed = result["processed"]
    prompt = result["prompt"]
    response = result["answer"]

    if args.show_prompt:
        print("\n----- Prompt sent to OpenRouter -----")
        print(prompt)
        print("------------------------------------\n")

    print("Processed question:", processed["cleaned"])
    print("Tokens:", processed["tokens"])
    print("\nLLM response:\n", response)


if __name__ == "__main__":
    main()
