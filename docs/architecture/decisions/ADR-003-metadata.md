# Metadata Layer

## Context

Metadata is used to improve retrieval quality, enrich embeddings, provide traceability, and simplify index maintenance.

---

## Candidate Approaches

### Option 1 — Chunk-level Metadata

Generate metadata independently for every chunk.

**Pros**
- Highly specific metadata.
- Better representation of each chunk.

**Cons**
- Expensive (LLM call for every chunk).
- Chunks lose the broader section context.
- Metadata may become inconsistent across chunks from the same section.

---

### Option 2 — Section-level Metadata

Generate metadata once for each document section.

**Pros**
- Low indexing cost.
- Consistent metadata for related chunks.
- Captures the overall topic of the section.

**Cons**
- Too coarse for small chunks.
- Different chunks within the same section share identical metadata.

---

### Option 3 — Hybrid Metadata Generation (Selected)

Generate metadata at both the section and chunk levels.

**Section Metadata**
- Section summary
- Section keywords

**Chunk Metadata**
- Chunk summary
- Chunk keywords

---

## Why?

Section metadata provides the high-level semantic context, while chunk metadata captures the precise meaning of each chunk.

During embedding, both metadata levels are combined with the original chunk text to generate richer contextual embeddings.

This provides more informative vectors without sacrificing chunk specificity.

---

## Decision

Use **hybrid metadata generation**.

Pipeline:

```text
Parser
    ↓
Extract document hierarchy
    ↓
For each section
    ├─ Generate section summary
    └─ Generate section keywords
    ↓
Recursive Chunking
    ↓
For each chunk
    ├─ Generate chunk summary
    └─ Generate chunk keywords
    ↓
Build contextual embedding text
    ↓
Generate embeddings
    ↓
Qdrant
```

---

## Metadata Schema

### Section Metadata

```json
{
  "summary": "...",
  "keywords": ["...", "..."],
  "generation": {
    "provider": "...",
    "model": "...",
    "prompt_version": "...",
    "generated_at": "..."
  }
}
```

### Chunk Metadata

```json
{
  "document_id": "...",
  "file_name": "...",

  "chunk_id": "...",
  "chunk_index": 3,

  "semantic": {
    "summary": "...",
    "keywords": ["...", "..."],
    "generation": {
      "provider": "...",
      "model": "...",
      "prompt_version": "...",
      "generated_at": "..."
    }
  },

  "indexing": {
    "embedding_provider": "...",
    "embedding_model": "...",
    "chunking_strategy": "...",
    "hash": "...",
    "indexed_at": "..."
  }
}
```

---

## Why This Fits Our Use Case

Insurance documents are naturally organized into sections containing multiple related topics.

Using metadata at both levels allows the system to:

- Preserve the semantic context of each section.
- Capture the specific meaning of every chunk.
- Produce richer contextual embeddings by combining:
  - document information,
  - section information,
  - section summary,
  - section keywords,
  - chunk summary,
  - chunk keywords,
  - original chunk text.
- Improve retrieval quality for semantically similar insurance documents.
- Maintain full traceability of LLM-generated metadata.
- Simplify future re-indexing and embedding regeneration.

---

## Decision Summary

- **Section Metadata:** Summary + Keywords
- **Chunk Metadata:** Summary + Keywords
- **Embedding:** Contextual embedding using both metadata levels
- **LLM Provenance:** Stored for every generated semantic metadata
- **Goal:** Maximize retrieval quality while maintaining a production-ready and traceable ingestion pipeline.