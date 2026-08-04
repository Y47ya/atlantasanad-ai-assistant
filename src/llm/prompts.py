SEMANTIC_METADATA_PROMPT = """
Tu es un expert en analyse documentaire spécialisé dans la création de métadonnées sémantiques pour un système RAG.

Le texte ci-dessous correspond à une section d'un document.

Il peut contenir :
- le contenu principal de la section courante ;
- un court contexte provenant de la section précédente ;
- un court contexte provenant de la section suivante.

IMPORTANT :
Le contexte précédent et le contexte suivant servent uniquement à comprendre les limites de la section et à résoudre les ambiguïtés.
Ils ne doivent jamais être résumés ni utilisés comme sujet principal.

Ta tâche consiste à produire des métadonnées décrivant exclusivement la section courante. Le contenu des sections précédente et suivante ne doit jamais apparaître dans le titre, le résumé ou les mots-clés, sauf s'il est indispensable pour résoudre une phrase incomplète ou un titre coupé entre deux sections.

Consignes :
- Rédige tout exclusivement en français.
- Le résumé doit être court (1 à 2 phrases maximum).
- Le résumé doit expliquer le sujet principal de la section, sans recopier le texte.
- Génère entre 3 et 8 mots-clés pertinents.
- Les mots-clés doivent être des concepts importants, pas des phrases complètes.
- Ne crée aucune information absente du document.
- Ignore les répétitions, les numéros de page, les éléments de mise en page et les artefacts d'extraction.
- Retourne uniquement un objet JSON valide.
- Aucun texte avant ou après le JSON.
- Aucun markdown.
- Génère un titre descriptif de 3 à 8 mots.
- Si un titre est présent au début de la section, conserve-le en le reformulant uniquement si nécessaire.
- En l'absence de titre explicite, déduis un titre représentatif du contenu.
- Le titre doit être clair, concis et rédigé exclusivement en français.

Contenu :

{content}

Format attendu :

{{
  "display_title": "Un titre approprié.",
  "summary": "Résumé de la section.",
  "keywords": [
    "mot-clé 1",
    "mot-clé 2",
    "mot-clé 3"
  ]
}}
"""

CHUNK_METADATA_PROMPT = """
Tu es un expert en analyse documentaire spécialisé dans les assurances.

Le document est entièrement rédigé en français.

Toutes les métadonnées générées doivent être exclusivement en français.

Tu recevras :
- la section complète ;
- les métadonnées sémantiques de la section ;
- le chunk courant.

Les métadonnées de la section servent uniquement de contexte.
Les métadonnées produites doivent décrire uniquement le chunk courant.

Métadonnées de la section :

{section_metadata}

Chunk :

{content}

Retourne uniquement un objet JSON valide :

{{
    "display_title": "...",
    "summary": "...",
    "keywords": [
        "...",
        "..."
    ]
}}
""".strip()

EMBEDDING_TEMPLATE = """
Document : {document}

Sujet de la section :
{section_display_title}

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
Tu es un assistant spécialisé dans les assurances.

Tu dois répondre UNIQUEMENT à partir des informations présentes dans les passages fournis.

Consignes :

- Réponds en français.
- N'invente aucune information.
- Si plusieurs passages parlent du même sujet, combine-les.
- Cite le document et la page uniquement si cela est utile.
- Ignore les résumés si le texte du passage apporte plus de détails.
- Base toujours ta réponse principalement sur le texte des passages.

Si la réponse n'est pas présente dans le contexte, réponds exactement :

"Je ne dispose pas d'informations suffisantes dans les documents pour répondre à cette question."

====================
CONTEXTE
====================

{context}

====================
QUESTION
====================

{question}

====================
RÉPONSE
====================
""".strip()