from app.services.ingest import chunk_text


def test_chunk_text_splits_on_sentence_boundaries():
    text = "First sentence. Second sentence. Third sentence."
    chunks = chunk_text(text, target_tokens=3, overlap_tokens=0)
    assert len(chunks) >= 2
    assert all(chunk.strip() for chunk in chunks)


def test_chunk_text_handles_empty_input():
    assert chunk_text("") == []


def test_chunk_text_keeps_short_text_as_one_chunk():
    text = "A short passage."
    chunks = chunk_text(text, target_tokens=400, overlap_tokens=50)
    assert chunks == ["A short passage."]
