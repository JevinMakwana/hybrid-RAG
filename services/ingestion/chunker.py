# hybrid_RAG\services\ingestion\chunker.py
def _get_block_text(block):
    """
    Safely extract text from a block based on its type.
    """
    if block["type"] == "key_value":
        key = block.get("key", "").strip()
        value = block.get("value", "").strip()
        return f"{key}: {value}".strip()

    return block.get("content", "").strip()


def _count_tokens(text):
    """
    Approximate token count using whitespace split.
    This is sufficient for chunking logic (fast + model-agnostic).
    """
    return len(text.split())


def chunk_blocks(blocks, max_tokens=300, overlap_tokens=50):
    """
    Create chunks using sliding window with overlap.

    Parameters:
        blocks: list of extracted blocks
        max_tokens: max tokens per chunk
        overlap_tokens: tokens to overlap between chunks

    Returns:
        List of chunks (each chunk = list of blocks)
    """
    chunks = []

    current_chunk = []
    current_token_count = 0

    i = 0
    n = len(blocks)

    while i < n:
        block = blocks[i]
        text = _get_block_text(block)

        if not text:
            i += 1
            continue

        token_len = _count_tokens(text)

        # If block itself exceeds max_tokens → force single-block chunk
        if token_len >= max_tokens:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_token_count = 0

            chunks.append([block])
            i += 1
            continue

        # If adding block exceeds limit → finalize chunk and start overlap
        if current_token_count + token_len > max_tokens:
            chunks.append(current_chunk)

            # -------------------------
            # CREATE OVERLAP WINDOW
            # -------------------------
            overlap_chunk = []
            overlap_count = 0

            # Walk backwards from current_chunk
            for prev_block in reversed(current_chunk):
                prev_text = _get_block_text(prev_block)
                prev_len = _count_tokens(prev_text)

                if overlap_count + prev_len > overlap_tokens:
                    break

                overlap_chunk.insert(0, prev_block)
                overlap_count += prev_len

            current_chunk = overlap_chunk.copy()
            current_token_count = overlap_count

        # Add block to chunk
        current_chunk.append(block)
        current_token_count += token_len

        i += 1

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def build_chunk_text(chunk):
    """
    Utility to convert a chunk (list of blocks) into a single string.
    Useful for embeddings and debugging.
    """
    texts = []

    for b in chunk:
        btype = b.get("type")
        
        if btype == "key_value":
            key = b.get("key", "").strip()
            value = b.get("value", "").strip()
            texts.append(f"{key}: {value}")
            
        elif btype == "paragraph":
            # Extract standard narrative text content
            content = b.get("content", "").strip()
            if content:
                texts.append(content)
                
        else:
            # Robust fallback for numbered_clause, table_row, or raw text blocks
            content = b.get("content") or b.get("text") or ""
            content = content.strip()
            if content:
                texts.append(content)

    return "\n\n".join(texts)