from DocumentProcessor import DocumentProcessor 
from QuestionGenerator import QuizGenerator
import chromadb
from chromadb.config import Settings
import streamlit as st


class QuizManager:
    def __init__(self, files, topic, num_questions):
        self.files = files
        self.topic = topic
        self.num_questions = num_questions

        print("- Processing documents ...")
        document_processor = DocumentProcessor(files)
        
        chroma_client = chromadb.PersistentClient(path='./store', settings=Settings(allow_reset=True))
        chroma_client.reset()
        self.collection = chroma_client.get_or_create_collection('collection')
        print("- Collection created.")
        self.collection.upsert(
            ids = [str(i) for i in range(len(document_processor.documents))],
            documents= document_processor.documents
        )
        print("- Documents upserted.")
        self.quiz_gen = QuizGenerator()
        self.questions = self.quiz_gen.generate_questions(topic, self.collection, num_questions)