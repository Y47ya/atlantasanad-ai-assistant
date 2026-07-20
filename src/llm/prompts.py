SEMANTIC_METADATA_PROMPT = """
You are an expert document analyst.

Generate semantic metadata for the following document section.

Title:
{title}

Content:
{content}

Rules:
- Summary: maximum 2 sentences.
- Keywords: 3-8 concise keywords.
- Do not invent information.
- Return ONLY valid JSON.
- No markdown.
- No explanations.

Example:

{{
  "summary": "...",
  "keywords": [
    "...",
    "...",
    "..."
  ]
}}
"""