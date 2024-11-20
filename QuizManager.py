from DocumentProcessor import DocumentProcessor 
from TextEmbedder import TextEmbedder
from QuestionGenerator import QuizGenerator
import chromadb
from chromadb.config import Settings


class QuizManager:
    def __init__(self, file, topic, num_questions):
        document_processor = DocumentProcessor(file)

        embedder = TextEmbedder()
        embeddings, documents = embedder.embed_text(document_processor.chunks)
        
        chroma_client = chromadb.PersistentClient(path='./store', settings=Settings(allow_reset=True))
        chroma_client.reset()
        collection = chroma_client.get_or_create_collection('collection')
        if len(embeddings) == 0:
            raise Exception("This document cannot be coerced. Please try a different one.")
        collection.upsert(
            ids = [str(i) for i in range(len(embeddings))],
            documents= documents,
            embeddings= embeddings
        )
        self.questions = QuizGenerator().generate_questions(topic, collection, num_questions)