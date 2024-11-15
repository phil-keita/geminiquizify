from TextEmbedder import TextEmbedder
import pytest

def test_embed_text():
    texts = ["This is sample text"] * 20
    te = TextEmbedder()
    output = te.embed_text(texts=texts)
    assert type(output) == list
    assert len(output) == 20

def test_embed_text_max():
    texts = ["This is sample text"] * 500
    te = TextEmbedder()
    output = te.embed_text(texts=texts)
    assert type(output) == list
    assert len(output) == 500