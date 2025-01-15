from langchain.text_splitter import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
import fitz # pdf documents
from docx import Document # word documents
from io import BytesIO
import streamlit as st

class DocumentProcessor:

    def __init__(self, files:list[UploadedFile]):
        self.files = files
        self.documents = self.get_chuncks(self.files)
        self.documents = [doc.page_content for doc in self.documents]
    
    def get_chuncks(self, files):
        full_text = ""
        for file in files:
            if file.size > 1000000:
                st.warning("The file uploaded is large, this can take minutes ...")
            if file.type == 'application/pdf':
                pdf = fitz.open(stream=BytesIO(file.getvalue()), filetype="pdf")
                for page in pdf:
                    full_text += page.get_text() + "\n"
                pdf.close()
            else:
                doc = Document(BytesIO(file.getvalue()))
                for para in doc.paragraphs:
                    full_text += para.text + "\n"
        # langchain text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=250,
            length_function=len,
            is_separator_regex=False
        )
        return text_splitter.create_documents([full_text])
