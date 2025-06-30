from minsearch import Index
import json

with open("01. Intro/minsearch play data.json", "rt") as reader:
  docs = json.load(reader)

text_fields = ["title", "description"]
keyword_fields = ["category", "author"]

engine = Index(text_fields=text_fields, keyword_fields=keyword_fields)

engine.fit(docs)

response = engine.search(
  query="How to be healthy ?",
  num_results=2
)

print(response)


