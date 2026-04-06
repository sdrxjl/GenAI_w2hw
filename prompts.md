# Prompt

## initial version

prompt to claude code:

```
Goal:
Build a simple Python command-line prototype for customer support email drafting using an LLM.

What it should do:
- Read cases from `eval_set.json`
- For each case, call an LLM API
- Generate a professional customer support reply
- Save all results to `outputs.json`
- Print structured progress/results to terminal

Requirements:
- Must run with `python app.py`
- Must make at least one real LLM API call
- Must have at least one configurable system prompt or instruction
- Use environment variables for API key and model
- Include basic error handling
- Keep the code simple, readable, and reproducible
- Add comments and a short usage note at the top
```

## Revision 1

follow up with this prompt to claude code:

```
can you check app.py and .env? I wish to use gemini api now  
```

Reason: I have an existing gemini api and forget to tell claude code about this. In this way, it returns a python file that uses anthropic api.

## Revision 2

Change system prompts from

```python
    "You are a professional and empathetic customer support representative. "
    "Your job is to draft a clear, polite, and helpful email reply to a customer. "
    "Follow these rules:\n"
    "- Be warm but concise (3-5 sentences is usually enough).\n"
    "- Never invent product details, warranties, or policies not given in the context.\n"
    "- If you are missing information, politely ask for it.\n"
    "- Always end with an offer to help further."
```

to

```python
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
```

Reason:

In case_5_failure_hallucination_risk, the model should have said it cannot confirm warranty eligibility from the provided information and suggested checking policy or escalating. Instead, it asked for order/serial number as if confirmation would definitely be possible.

## What changed and why

I revised the system prompt to explicitly forbid inventing policy details and to require the model to state uncertainty when information is missing. I also added instructions to standardize tone and avoid placeholders or unsupported claims.

## What improved, stayed the same, or got worse

The updated prompt reduced hallucination and produced more grounded responses, especially in cases with unclear policy (e.g., warranty). Tone and structure became more consistent, while overall helpfulness remained strong with no major regressions.

Case5 asked for order number instead of suggesting checking policy before change. It performs well after change.
