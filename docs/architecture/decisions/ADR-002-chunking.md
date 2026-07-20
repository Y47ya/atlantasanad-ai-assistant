# Chunking Layer

## Chunk Boundary Strategy

#### Selected Approach

**Section-based Chunking + Recursive Chunking**

#### Why?

##### 1. Section-based Chunking

Insurance documents are naturally divided into logical sections.

**Benefits**
- Preserves semantic context
- Prevents chunks from crossing different document sections
- Better retrieval precision

##### 2. Recursive Chunking (inside each section)

After extracting each section, its content is split using LangChain's `RecursiveCharacterTextSplitter`.

**Why?**
- Preserves complete sentences and paragraphs whenever possible.
- Falls back to smaller separators only when necessary.
- Produces chunks with consistent maximum size while minimizing semantic fragmentation.
- Supports configurable overlap to preserve context across chunk boundaries.
- More robust than fixed-size chunking for heterogeneous insurance documents containing lists, paragraphs, and tables.

---

## Embedding Strategy

#### Selected Approach

**Contextual Embedding**

Instead of embedding only the chunk, prepend contextual information before generating the embedding.

### Context Added

Each chunk is embedded together with its document and section context.

Example:

```text
Document: Assurance Automobile
Section: GARANTIES INNOVANTES

<chunk text>
```

#### Why?

Many chunks begin with generic sentences such as:

> "The insured..."

Without contextual information, these chunks may produce very similar embeddings despite belonging to different topics.

Adding the document and section context improves the semantic representation while keeping the original chunk text unchanged for retrieval.

---

## Proposed Pipeline

```text
Document
      ↓
Document Parsing
      ↓
Extract Sections
      ↓
Recursive Chunking
      ↓
Add Document + Section Context
      ↓
Generate Embeddings
      ↓
Qdrant
```

---

## Why This Fits Our Use Case

| Requirement | Proposed Solution |
|-------------|-------------------|
| Preserve document meaning | Section-based chunking |
| Preserve sentence structure | Recursive chunking |
| Improve embedding quality | Contextual embedding |
| Production-ready | Simple, scalable pipeline |
| Insurance documentation | Uses existing document hierarchy |

---

## Decision Summary

- **Boundary Strategy:** Section-based + Recursive Chunking
- **Chunking Algorithm:** LangChain `RecursiveCharacterTextSplitter`
- **Embedding Strategy:** Contextual Embedding
- **Goal:** Combine semantic preservation, adaptive chunk splitting, and high retrieval quality for structured insurance documentation.