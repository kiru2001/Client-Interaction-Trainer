from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_chroma import Chroma
 
def create_compressed_retriever(pdf_paths):
    documents = []
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    embedding = HuggingFaceEmbeddings()
    retriever = Chroma.from_documents(texts, embedding).as_retriever(search_kwargs={"k": 20})
    compressor = FlashrankRerank()
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
    return compression_retriever

pdf_paths = ["FAQ_SWAYAM.pdf"]
compressed_retriever1 = create_compressed_retriever(pdf_paths)
retriever_dict={"project2":compressed_retriever1}
 
def rag_answer(project_id,question_text,audio_answer):
    retriever=retriever_dict[project_id]
    compressed_docs = retriever.invoke(f"question:{question_text},answer:{audio_answer}")
    combined_text = '\n\n'.join([doc.page_content for doc in compressed_docs])
    return combined_text

def relevent_answer(project_id,question_text):
    retriever=retriever_dict[project_id]
    compressed_docs = retriever.invoke(f"question:{question_text}")
    combined_text = '\n\n'.join([doc.page_content for doc in compressed_docs])
    return combined_text
 
# print(relevent_answer("project1","what is swayam"))