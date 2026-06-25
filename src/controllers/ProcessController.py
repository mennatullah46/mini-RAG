from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
from typing import List
from dataclasses import dataclass

@dataclass
class Document:
    page_content: str
    metadata: dict

class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):

        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None

    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()

        return None

    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_size: int=20):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks

    def process_simpler_splitter(self, texts: List[str], metadatas: List[dict], chunk_size: int, splitter_tag: str="\n"):
        
        full_text = " ".join(texts)

        # split by splitter_tag
        lines = [ doc.strip() for doc in full_text.split(splitter_tag) if len(doc.strip()) > 1 ]

        chunks = []
        current_chunk = ""

        for line in lines:
            current_chunk += line + splitter_tag
            if len(current_chunk) >= chunk_size:
                chunks.append(Document(
                    page_content=current_chunk.strip(),
                    metadata={}
                ))

                current_chunk = ""

        if len(current_chunk) >= 0:
            chunks.append(Document(
                page_content=current_chunk.strip(),
                metadata={}
            ))

        return chunks


    
    

# from .BaseController import BaseController
# from .ProjectController import ProjectController
# import os

# from langchain_classic.document_loaders import TextLoader
# from langchain_classic.document_loaders import PyMuPDFLoader
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# from models import ProcessingEnums

# import pytesseract
# from PIL import Image
# from pdf2image import convert_from_path


# class ProcessController(BaseController):

#     def __init__(self, project_id: str):
#         super().__init__()

#         self.project_id = project_id
#         self.project_path = ProjectController().get_project_path(project_id=project_id)

#     # ----------------------------
#     #  FILE HELPERS
#     # ----------------------------
#     def get_file_extension(self, file_id: str):
#         return os.path.splitext(file_id)[-1].lower()

#     def get_file_loader(self, file_id: str):

#         file_ext = self.get_file_extension(file_id)
#         file_path = os.path.join(self.project_path, file_id)

#         if file_ext == ProcessingEnums.TXT.value:
#             return TextLoader(file_path, encoding="utf-8")

#         if file_ext == ProcessingEnums.PDF.value:
#             return PyMuPDFLoader(file_path)

#         return None

#     # ----------------------------
#     #  TEXT VALIDATION
#     # ----------------------------
#     def is_text_sufficient(self, docs, min_words: int = 10) -> bool:
#         if not docs:
#             return False

#         text = " ".join([doc.page_content for doc in docs])
#         return len(text.strip().split()) >= min_words

#     # ----------------------------
#     #  OCR 
#     # ----------------------------
#     def ocr_from_image(self, image_path: str):
#         image = Image.open(image_path)
#         text = pytesseract.image_to_string(image)

#         return [
#             Document(
#                 page_content=text,
#                 metadata={"source": image_path, "ocr": True}
#             )
#         ]

#     def ocr_from_pdf(self, pdf_path: str):
#         images = convert_from_path(pdf_path)

#         docs = []
#         for i, img in enumerate(images):
#             text = pytesseract.image_to_string(img)

#             docs.append(
#                 Document(
#                     page_content=text,
#                     metadata={
#                         "page": i,
#                         "source": pdf_path,
#                         "ocr": True
#                     }
#                 )
#             )

#         return docs

#     # ----------------------------
#     #  GET CONTENT 
#     # ----------------------------
#     def get_file_content(self, file_id: str):
#         file_path = os.path.join(self.project_path, file_id)
#         file_ext = self.get_file_extension(file_id)

#         loader = self.get_file_loader(file_id)
#         docs = loader.load() if loader else []

#         # NORMAL PATH FIRST 
#         if self.is_text_sufficient(docs):
#             return docs

#         # OCR FALLBACK 
#         if file_ext == ".pdf":
#             return self.ocr_from_pdf(file_path)
#         else:
#             return self.ocr_from_image(file_path)


#     def process_file_content(self, file_content: list, file_id: str,
#                              chunk_size: int = 100, overlap_size: int = 20):

#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=overlap_size,
#             length_function=len,
#         )

#         file_content_texts = [
#             rec.page_content
#             for rec in file_content
#         ]

#         file_content_metadata = [
#             rec.metadata
#             for rec in file_content
#         ]

#         return text_splitter.create_documents(
#             file_content_texts,
#             metadatas=file_content_metadata
#         )