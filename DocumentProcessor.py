from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
import fitz
from io import BytesIO

class DocumentProcessor:

    def __init__(self, file: UploadedFile):
        self.file = BytesIO(file.getvalue())
        self.documents = self.get_chuncks(self.file)
        self.chunks = [doc.page_content for doc in self.documents]
    
    def get_chuncks(self, file):
        pdf = fitz.open(stream=file, filetype="pdf")
        texts = [page.get_text() for page in pdf]

        if len(texts) == 1 and texts[0] == "":
            raise ValueError("The PDF file is empty")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False
        )
        return text_splitter.create_documents(texts)

    # def analyze_chunks(self):
    #     self.get_chuncks()
    #     for i, chunk in enumerate(self.chunks):
    #         print("Document ", i)
    #         print(chunk.page_content)
    #         print("\n\n")
