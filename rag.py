import os
import urllib.request
import shutil
import html2text
import predictionguard as pg
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import lancedb
from lancedb.embeddings import with_embeddings
import pandas as pd
import json

os.environ['PREDICTIONGUARD_TOKEN'] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"
# get the ruleset from a local file
fp = urllib.request.urlopen("file:///home/ubuntu/insuranceagent.html")
mybytes = fp.read()
html = mybytes.decode("utf8")
fp.close()

# and convert it to text
h = html2text.HTML2Text()
h.ignore_links = True
text = h.handle(html)

text = text.split("Introduction")[1]

# Chunk the text into smaller pieces for injection into LLM prompts.
text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=50)
docs = text_splitter.split_text(text)

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
if os.path.exists(".lancedb"):
    shutil.rmtree(".lancedb")

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

# Now let's augment our Q&A prompt with this external knowledge on-the-fly!!!
template = """### Instruction:
Read the below input context and respond with a short answer to the given question. Use only the information in the below input to answer the question. If you cannot answer the question, respond with "Sorry, I can't find an answer, but you might try looking in the following resource."

### Input:
Context: {context}

Question: {question}

### Response:
"""
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

#define the pre-prompt in order to give the LLM a little bit of  expertise
pre_prompt="You are an expert insurance agent. You are getting information about a property. The information is a mixture of the state of the house and the homeowner's complaints. The state of the house will be just a few words describing the condition (for example, water damage). You will analyze the input and produce exactly three insights. These insights should constitute maintenance and protection recommendations for homeowners tailored to their home's condition. All the insights are at most 20 words long. Generate the insights in this form: Insight 1: (text), then on a new line, Insight 2: (text), then on a new line, Insight 3: (text). Only generate the insights and nothing else. Keep a professional tone. Do not make quote anyone. Do not add unrelated information. Do not add any code. Here is the home's condition: "

def rag_answer(message):

  # Search the for relevant context
  results = table.search(embed(message)).limit(10).to_pandas()
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

with open('vision_output.json','r') as json_file:
    data=json.load(json_file)

visionoutput=data['vision_output']

with open('data.json','r') as json_file:
    data=json.load(json_file)

ownercomplaint=data['text']

house_condition=visionoutput+". "+ownercomplaint

#house_condition="Water damage. The gas lines don't work. The kitchen is spotless. The building is in good condition and the walls do not have any cracks in them. There is a termite infestation in the basement."
response=rag_answer(pre_prompt+house_condition)

#response = rag_answer("A house has been destroyed by a tornado and also has been set on fire. The water doesn't work but the gas lines are fine. The area the house is in is notorious for crime. It is built in an earthquake prone zone. There are cracks in the walls and it is quite old.")

print('')
print("3 insights that we've generated based on your report are:\n", response)
with open('insights.json', 'w') as json_file:
   json.dump(response,json_file)

with open('stats_output.json','r') as json_file:
    data=json.load(json_file)

predicted_claim=str(data['stats'])
#predicted_claim=0.5 #input from statistical model
full_report_pre_prompt="You are an expert insurance agent. You have been given a list of personalized insights about a home that has been surveyed, along with a probability that the homeowner files a claim in the next 3 to 6 months. Based on this, give the property a rating from 1 to 5, where 5 means that the property is healthy, and also explain why the rating was given in not more than 180 words, based on the input insights. A rating of 1 means that the property is not healthy at all. In this scenario, a healthy property is one that has mostly positive or neutral insights and a low probability of having a claim filed. An unhealthy probability is one that has mostly negative insights and a high probability of having a claim filed. Remember that even if the homeowner has a high chance of filing a claim, the property may have positive insights and therefore you should give it a higher score. The rating should be at the beginning of your response. Ensure that you do not have any incomplete sentences. Do not quote anyone. Do not quote any insights verbatim. Keep the tone professional. You are permitted to expand upon the insights but do not stray. Ensure that you complete each sentence. Keep the report to only one continuous paragraph. The insights are: "
#full_report_temp_prompt=full_report_pre_prompt+response
full_report_final_prompt=full_report_pre_prompt+" .The probability of filing a claim is: "+str(predicted_claim)
full_report=rag_answer(full_report_final_prompt)
#full_report_temp_2=rag_answer(full_report_final_prompt)
#full_report_second_prompt="You are an insurance agent that was given an incomplete report. You have psychic powers and can complete missing reports, with perfect extrapolation. Complete the given incomplete report: "
#full_report=rag_answer(full_report_second_prompt+full_report_temp_2)
print("The full report is: ")
print(full_report)
with open('fullreport.json','w') as json_file:
    json.dump(full_report,json_file)
