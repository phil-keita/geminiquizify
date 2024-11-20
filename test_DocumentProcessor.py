from DocumentProcessor import DocumentProcessor
from io import BytesIO
import pytest


def test_get_chunks():
    with open("./pdfs/PoythressVernRedeemingScience.pdf", "rb") as file:
        pdf = BytesIO(file.read())
        output = DocumentProcessor(pdf).get_chuncks(pdf)
        assert type(output) == list

def test_get_chunks_empty():
    """Attempting to get chunks from an empty
    document should return a ValueError
    """
    with open("./pdfs/empty.pdf", "rb") as file:
        pdf = BytesIO(file.read())
        with pytest.raises(ValueError):
            DocumentProcessor(pdf).get_chuncks(pdf)
            