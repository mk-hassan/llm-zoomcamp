# Vector Databases

## Introduction

During the first two modules, we used to use Elasticsearch as the database to store and retrieve documents from. Elasticsearch may give us relatively accurate results related to the question we asked, but till now we didn't discover the shiny part of which is searching using Vector Search.

The previous retieval of documents was by comparing words of the query with the words of the documents, then return the documents that contain the larger amount of words similar those are on the query which called `keyword search`.

Now we want to switch gears to what's called `Vector search` which is not searching by the words but the context or the meaning. So select the documents that sare the same meaning as the query.

## Why Vector databases?

1. Beacuse of the various representations of data from simple text to Audio and images, we need a way to store those data types as efficient as possible an not only that we also need to retreieve them in fast and efficieint way. But what if we also need to search for audios that contains info about a certain topic?

2. Short term memory of LLMs. Vector DBs provide tha ability to store and retrieve data for the LLMs.

## The Idea

Imagine how the search results will improve in case you aren't only searching for the words of a sentance but the meaning of the sentance? That's what vector search all about. Converting the sentance you want to store into the database to numbers that embeds the meaning of the sentance in an implicit way. Then whenever you wanna search for a query to get the corresponding related documents you also convert the query to numbers and then you check which doc's numbers are the closest to the query's numbers.

The idea is that those numbers are more related the whole context of the sentance or the document instead of the individual meanings of sentance's words.

## Conversion to numbers 🤔

The Process of converting data into numbers is called Embedding, and the resulting numbers is called the `embeddings vector`. We are not just converting words to number but also sentances, documents and even images and audios.

What we care about here is senntence embedding. That's were we convert a sentence to a vector of numbers besides mentaining the context of the sentence and the meaning of it.

