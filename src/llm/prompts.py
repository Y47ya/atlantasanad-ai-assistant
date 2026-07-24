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

EMBEDDING_TEMPLATE = """
Document : {document}

Section : {section}

Résumé de la section :
{section_summary}

Mots-clés de la section :
{section_keywords}

Résumé du chunk :
{chunk_summary}

Mots-clés du chunk :
{chunk_keywords}

Contenu :
{chunk}
""".strip()

RAG_PROMPT = """
You are an insurance assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information to answer this question."

====================
Context
====================

{context}

====================
Question
====================

{question}

====================
Answer
====================
"""