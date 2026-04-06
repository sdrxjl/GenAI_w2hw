"""
Customer Support Email Drafting Prototype
==========================================
Usage:
    1. Set your API key in a .env file:
           GEMINI_API_KEY=your-key-here
           MODEL=gemini-2.0-flash   # optional, defaults to gemini-2.0-flash
    2. Run:
           python app.py

Reads cases from eval_set.json, calls the Gemini API for each case,
and saves all generated replies to outputs.json.
"""

import json
import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL   = os.getenv("MODEL", "gemini-2.0-flash")

# Configurable system prompt — edit this to change the assistant's behaviour
SYSTEM_PROMPT = (
    "You are a professional and empathetic customer support representative. "
    "Draft a clear, polite, and helpful email reply to the customer.\n\n"
    "Rules:\n"
    "- Be warm, professional, and concise.\n"
    "- Write 1 short email reply in 3-5 sentences.\n"
    "- Use only the information in the customer message and provided context.\n"
    "- Do not invent company policies, warranties, shipping details, refunds, or product facts.\n"
    "- If customer details are missing (such as order number), politely ask for them.\n"
    "- If company policy details are missing or unclear, explicitly say you cannot confirm based on the available information.\n"
    "- When policy is unclear, suggest checking the official policy or escalating to a support specialist.\n"
    "- Clearly state the next step.\n"
    "- Do not overpromise outcomes.\n"
    "- Do not use placeholders like [Customer Name] or [Your Name].\n"
    "- Do not include a subject line unless asked."
)

INPUT_FILE  = "eval_set.json"
OUTPUT_FILE = "outputs.json"

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_user_message(customer_message: str, context: str) -> str:
    """Construct the prompt we send to the model for a single case."""
    return (
        f"Customer message:\n{customer_message}\n\n"
        f"Relevant policy / context:\n{context}\n\n"
        "Please draft a professional email reply to this customer."
    )


def draft_reply(model_client, customer_message: str, context: str) -> str:
    """Call the LLM API and return the generated reply text."""
    response = model_client.generate_content(build_user_message(customer_message, context))
    return response.text


def process_cases(cases: list) -> list:
    """Iterate over all cases, call the API, and collect results."""
    genai.configure(api_key=API_KEY)
    model_client = genai.GenerativeModel(MODEL, system_instruction=SYSTEM_PROMPT)
    results = []

    for i, case in enumerate(cases, start=1):
        case_id = case["id"]
        msg     = case["input"]["customer_message"]
        ctx     = case["input"]["context"]

        print(f"[{i}/{len(cases)}] Processing: {case_id}")
        print(f"  Customer: {msg[:80]}{'...' if len(msg) > 80 else ''}")

        try:
            reply = draft_reply(model_client, msg, ctx)
            status = "success"
        except Exception as exc:
            reply  = f"ERROR: {exc}"
            status = "error"
            print(f"  ! API error: {exc}")

        results.append({
            "id":     case_id,
            "status": status,
            "input":  {"customer_message": msg, "context": ctx},
            "output": reply,
        })

        print(f"  Status: {status}")
        print(f"  Reply preview: {reply[:120].strip()}...\n")

    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # Validate API key
    if not API_KEY:
        print("ERROR: GEMINI_API_KEY is not set. Add it to your .env file.")
        sys.exit(1)

    # Load eval cases
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found in the current directory.")
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} cases from {INPUT_FILE}")
    print(f"Model: {MODEL}\n")
    print("=" * 60)

    results = process_cases(cases)

    # Save outputs
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    success_count = sum(1 for r in results if r["status"] == "success")
    print("=" * 60)
    print(f"Done. {success_count}/{len(results)} cases succeeded.")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

