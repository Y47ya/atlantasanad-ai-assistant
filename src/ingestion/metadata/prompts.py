SUMMARY_PROMPT = """
You are an expert document analyst.

Your task is to analyze one document section.

Return ONLY valid JSON.

{{
    "summary": "...",
    "keywords": [
        "...",
        "..."
    ]
}}

Rules:

- Preserve the original language.
- Do not invent information.
- No markdown.
- No explanations.

Section title:
{title}

Section content:
{content}
"""
