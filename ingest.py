"""This is the logic for ingesting Notion data into LangChain."""
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle


# List all markdown documents in the provided directory.
ps = list(Path("cloudflare-md-docs/").glob("**/*.md"))

data = []
sources = []
for p in ps:
    with open(p) as f:
        data.append(f.read())
    sources.append(p)

# Here we split the documents, as needed, into smaller chunks.
# We do this due to the context limits of the LLMs.
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
docs = []
metadatas = []
for i, d in enumerate(data):
    splits = text_splitter.split_text(d)
    docs.extend(splits)
    metadatas.extend([{"source": sources[i]}] * len(splits))

# Create list of docs that are greater than 1500 characters.
bad_docs = [ i for i, d in enumerate(docs) if len(d) > 1600 ]
# delete docs that are > 1600 characters (these are mostly noise, like pem keys)
for i in sorted(bad_docs, reverse=True):
    print('deleting doc due to size', f'size:{len(docs[i])} doc: {docs[i]}' )
    del docs[i]
    del metadatas[i]


# Here we create a vector store from the documents and save it to disk.
store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
faiss.write_index(store.index, "docs.index")
store.index = None
with open("cloudflare_docs.pkl", "wb") as f:
    pickle.dump(store, f)
