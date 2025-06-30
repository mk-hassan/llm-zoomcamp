# minsearch, How it works ?

## Idea
minsearch depends on the `vector search` scheme, which cares about the semantics of the sentance and not the words count but the meaning of words together.

vector search depends on finding the most realted document to the query you are searching for.

it works as follows:
### 1. converting documents to a vector of numbers (fit)
```python
# consider these data
docs = [
    “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”,
    “It is our choices, Harry, that show what we truly are, far more than our abilities.”,
    “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”,
    “The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”,
    “Imperfection is beauty, madness is genius and it’s better to be absolutely ridiculous than absolutely boring.”
]
```

after vectorizing the documents
$$
\text{TfidfVectorizer}(docs) =
\left\{
\begin{array}{c}
v_1 \\
v_2 \\
v_3 \\
\vdots \\
v_n \\
\end{array}
\right\}
$$

### 2. Search the documents

for `query = "How one should live?"` find the most related documents to this query.

1. convert the query to the vector form using the same **Vectorizer** used in fitting the documents. lets call it docs_vectorizer
$$
docs\_vectorizer.tranform(query) =
v_q
$$

2. Perform dot prodcut the query vector with docs vectors (consine similarity) 
3. get the top k scores positions and these are the most relatice documents 

> [!NOTE]
> minsearch generalizes the idea to be same as elastic serach engine, the docs is sipposed to be dicts. For each searchable key (text_field) you train a separate TfidfVectorizer just like we make with docs.
>
> Then we searching the docs you are summing up the scores prodced from each vectorizer after adding weight to each score separatly.
>
> Think about it you have multiple docs lists docs1 = [], docs2 = []. You perfrom consine similarity on both them sum the scores and get the top k scores.


