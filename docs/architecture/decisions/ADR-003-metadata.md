# Metada layer

## Context

Metadata is used to improve retrieval quality, provide traceability, and simplify index maintenance.
## Candidate Approaches

### Option 1 — Chunk-level Metadata

Generate metadata independently for every chunk.

**Pros**
- Very specific metadata per chunk

**Cons**
- Expensive (LLM per chunk)
- Inconsistent metadata between chunks of the same section
- Higher indexing time


### Option 2 — Section-level Metadata (Selected)

Generate metadata once for each document section, then inherit it to all chunks created from that section.

**Pros**
- Lower indexing cost
- Consistent metadata across related chunks
- Better semantic representation
- Simple and scalable

**Cons**
- Chunks from the same section share identical metadata



## Decision

Use **section-level metadata generation**.

Pipeline:

```text
Parser
    ↓
Extract document hierarchy
    ↓
For each section
    ├─ Extract section title
    ├─ Generate section summary
    └─ Generate keywords
    ↓
Chunk inside the section
    ↓
Each chunk inherits the section metadata
    ↓
Embedding
    ↓
Qdrant
```


## Metadata Schema

```json
{
  "document_id": "...",
  "file_name": "...",

  "section": "...",
  "subsection": "...",
  "page": 12,

  "section_summary": "...",
  "keywords": ["...", "..."],

  "hash": "...",
  "indexed_at": "...",

  "embedding_model": "bge-m3",
  "chunking_strategy": "section_fixed_context"
}
```


## Why This Fits Our Use Case

Insurance documents are highly structured (sections, subsections, policies, procedures).

Generating metadata at the **section level** preserves this structure while avoiding unnecessary LLM calls for every chunk.

This approach provides:

- Better retrieval through section summaries and keywords.
- Consistent semantic context for all chunks within the same section.
- Lower indexing cost and faster processing.
- Easier document updates using document hash.
- A simple, production-ready pipeline suitable for large insurance knowledge bases.