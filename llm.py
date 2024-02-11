import os
import urllib.request

import html2text
import predictionguard as pg
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import lancedb
from lancedb.embeddings import with_embeddings
import pandas as pd


os.environ['PREDICTIONGUARD_TOKEN'] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"
# Let's get the html off of a website.
fp = urllib.request.urlopen("file:////home/shaunak_joshi/gt/insuranceagent.html")
mybytes = fp.read()
html = mybytes.decode("utf8")
fp.close()

# And convert it to text.
h = html2text.HTML2Text()
h.ignore_links = True
text = h.handle(html)

# Clean things up just a bit.
text = text.split("Introduction")[1]
#print(text)
#text = text.split("Location, Location, Location")[0]
#print(text)
#print(type(text))

# Chunk the text into smaller pieces for injection into LLM prompts.
text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=50)
docs = text_splitter.split_text(text)
# Let's checkout some of the chunks!
#for i in range(0, 10):
#  print("Chunk", str(i+1))
#  print("----------------------------")
#  print(docs[i])
#  print("")
# Let's take care of some of the formatting so it doesn't conflict with our
# typical prompt template structure
docs = [x.replace('#', '-') for x in docs]


# Now we need to embed these documents and put them into a "vector store" or
# "vector db" that we will use for semantic search and retrieval.

# Embeddings setup
name="all-MiniLM-L12-v2"
model = SentenceTransformer(name)

def embed_batch(batch):
    return [model.encode(sentence) for sentence in batch]

def embed(sentence):
    return model.encode(sentence)

# LanceDB setup
os.mkdir(".lancedb")
uri = ".lancedb"
db = lancedb.connect(uri)

# Create a dataframe with the chunk ids and chunks
metadata = []
for i in range(len(docs)):
    metadata.append([i,docs[i]])
doc_df = pd.DataFrame(metadata, columns=["chunk", "text"])

# Embed the documents
data = with_embeddings(embed_batch, doc_df)

# Create the DB table and add the records.
db.create_table("linux", data=data)
table = db.open_table("linux")
table.add(data=data)

# Let's try to match a query to one of our documents.
#message = "What plays a crucial role in deciding insurance policies?"
#results = table.search(embed(message)).limit(5).to_pandas()
#print(results.head())


# Now let's augment our Q&A prompt with this external knowledge on-the-fly!!!
template = """### Instruction:
Read the below input context and respond with a short answer to the given question. Use only the information in the bel>

### Input:
Context: {context}

Question: {question}

### Response:
"""
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

def rag_answer(message):

  # Search the for relevant context
  results = table.search(embed(message)).limit(5).to_pandas()
  results.sort_values(by=['_distance'], inplace=True, ascending=True)
  doc_use = results['text'].values[0]
 # Augment the prompt with the context
  prompt = qa_prompt.format(context=doc_use, question=message)

  # Get a response
  result = pg.Completion.create(
      model="Nous-Hermes-Llama2-13B",
      prompt=prompt
  )

  return result['choices'][0]['text']

response = rag_answer("A house has been destroyed by a tornado and also has been set on fire. The water doesn't work but the gas lines are fine. The area the house is in is notorious for crime. It is built in an earthquake prone zone. There are cracks in the walls and it is quite old. Based on this information, generate three insights about the type of insurance policy the house will require and any other thing you find important. Keep the insights under 20 words each.")

print('')
print("RESPONSE:", response)
