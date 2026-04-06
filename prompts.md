# initial version

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

# Revision 1

```
can you check app.py and .env? I wish to use gemini api now  
```

Reason: I have an existing gemini api and forget to tell claude code about this. In this way, it returns a python file that uses anthropic api.

