# Chunking Layer

## Chunk Boundary Strategy

#### Selected Approach

*Section-based Chunking + Fixed-size Chunking*

#### Why?

##### 1. Section-based Chunking

Insurance documents are naturally divided into logical sections.

**Benefits**
- Preserves semantic context
- Prevents chunks from crossing different document sections
- Better retrieval precision

##### 2. Fixed-size Chunking (inside each section)

After extracting a section, split it into fixed-size chunks (with overlap if needed).

**Why?**
- Fast indexing
- Predictable chunk sizes
- Good scalability for large document collections
- Compatible with all embedding models and vector databases


## Embedding Strategy

#### Selected Approach

**Contextual Embedding**

Instead of embedding only the chunk, prepend contextual information before generating the embedding.

#### Why?

Many chunks begin with generic sentences such as:

> "The insured..."

Without context, these chunks may produce very similar embeddings.

## Proposed Pipeline

```text
Document
      ↓
Document Parsing
      ↓
Extract Sections
      ↓
Fixed-size Chunking
      ↓
Add Document + Section Context
      ↓
Generate Embeddings
      ↓
Qdrant
```


## Why This Fits Our Use Case

| Requirement | Proposed Solution |
|-------------|-------------------|
| Preserve document meaning | Section-based chunking |
| Fast indexing | Fixed-size chunking |
| Improve embedding quality | Contextual embedding |
| Production-ready | Simple, scalable pipeline |
| Insurance documentation | Uses existing document hierarchy |


## Decision Summary

- **Boundary Strategy:** Section-based + Fixed-size Chunking
- **Embedding Strategy:** Contextual Embedding
- **Goal:** Combine semantic preservation, indexing performance, and high retrieval quality for structured insurance documentation.