# Monitoring

> In [module 3](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/03-vector-search), we discussed how to compute or assess if vector retrieval is good enough?, Today we want to observe and monitor if the answer of the LLM and the quality is good enough?\
Shortly, Previously we evaluated the the `Retrieval` part, Now want to evaluate the `Generation` part.

### Why monitoring LLM/RAG systems?
You might read before about [racist](https://www.scientificamerican.com/article/even-chatgpt-says-chatgpt-is-racially-biased/) chat bots, or heared about microsoft's chatbot from 2016 [Tay](https://en.wikipedia.org/wiki/Tay_(chatbot)#Second_release_and_shutdown) which wrote rude and sexual tweets and incite to murder after less than 16h after its release.

![tay example tweet](https://media.shellypalmer.com/wp-content/images/2016/03/taytweet-censored-800x393.jpg)

As a product owner or a company, you just wnat to avoid to disappoint your customers. You don't want to be in the press for your chatbot not behaving well. So you want to moitor it and know what's going on overtime.
Building and depoying an LLM/RAG system isnot enough. You can't just hope the best but better to have eye on the system.

### What's so challenging about monoitorin and LLM System?
It's not just an if-else rule. It's not just a hard coded rule engine and rule based system. But it's LLMs where considered to be relatively intelligent. They generate answers using some sort of creativity and most importantly they really just answer in a way based on data that it's been fed to. 

### How do I now actually evaluate and monitor the answers quality of my LLM system? 
To know if the answer that my LLM is giving is good enough towards the user we do the following: 
- Compute different types of metrics (offline metrics, online metrics).
- Store the computed metrics on a relational database.
- Use some visualization tool like `grafana` to display those computed metrics overtime.

Also we can use user feed back to evaluate the LLM system. By storing the chat session and collecting the user feedback in a database. Then connect this database to a visualization tool like `grafana` to visualize the user feedback and the chat session overtime.

### What type of metrics you can compute to monitor the answers quality of RAG system?
To know that the LLM system gave a good answer, there're different types of metrics that you can compute. There's not this single metric that you can compute and you know everything about the RAG system. You gonna come up with a set of metrics that're going  to tell you if your model is doing good or if you want to readjust and refine it.

### Example of metrics we study in this moduel:
Those aren't the only metrics exist and not the most advanced ones. but they are a good start to use on the company you working on or a private project you build.

> [!NOTE] Vector similarity between expected and LLM answer
> This's an example of offline metrics, where evaluating the system accuracy before deploying it. 
> You have a dataset that contains the expected answer of a question, and you have the answer from the LLM. Both of them are stored as vector embeddings. Then you compute the vector similarity. This type of metric allows you to know how far is the generated answer from the expected answer. That gives you a clue of if it might make sense or if your LLM system completely off with generating the answer.

> [!NOTE] Using another LLM as a judge
> This method is a more complex way of judging if the answer is good enough and can detect more complex patterns, but it might also go too creative and that's why we also want to have the combination with the mathematical approach.\
> 1. LLM-as-a-judge to compute toxicity of LLM answer.\
You create a prompt contains Your LLM generated answer, and ask the judge LLM if he think if the answer is toxic or not. You can get a score for it. Such LLMs exist on huggingface available that assessing if a text is toxic or not, and give a score for it.
> 2. LLM-as-a-judge to compute quality of LLM answer.\
Besides the other LLM answer, we also provide the expected answer. and ask the LLM judge if he thinks the answer makes sense or not. It's like ranking the LLM answer as "Relative", "Non-Relative" based on the original-answer.
> After then we store the metrics in a database **postgresql** and use **grafana** to visualize the metrics easily overtime by adding graphics.

> [!NOTE] Monitoring answers quality with user feedback
> This is an example of Online metrics evaluation, that's evaluating the system after deploying it.
> 1. Thumb up and Thumb down feedback like in chatgpt.
> 2. Using starts to report the level of satisfaction with the answer.
> alongside this we need also to store the chat session, because if there's lots of negative feedback you need to find out which question does the user actually ask and what does the system answer, also you may need to store the whole chat history so that we can trace it back.

These are just simple three metrics but you can and should do more:
1. Bias and fairness of LLM system answers. You need to how fair is your system against different models and different genders, nationalities and regions of the world.
2. Clustering topics that your customers usually talking about. Then you know your customers usually uses you system.
3. Collecting user feedback, not just thumb-up and thumb-down but also textual feed back which is unstructured and challenging, but they can reason about why a cerain answer is not good enough. They are useful when the collected chat session and messages have a very negative feedback then you can dive into the textual feedback.
4. Out of the box ideas. In chatgpt, code snippts has the a button that allows the user to copy it. That could be an indirect sign the user likes what I'm proposing and  want to try out it.
5. measuring and monitoring system metrics, the 4 golden signals (latency, traffic, errors, saturation) they are also called the system metrics of your system.

> [!CAUTION] Not only quality metrics
> Besides the importance of quality metrics and user feedback, system metrics are also so important to involve in your system evaluation criteria.

> [!TIP] Cost
> Another non surprising fact, LLMs are not that cheap. If you have time you should also invest in monitoring the tracking the cost of your infrastructure .

---

### Conclusion
Even LLMs are smart enough, they still need to be evaluated. Using a variety of metrics to evaluate your system is crucial, and pricing calculations is also a really important thing to care about.
The metrics are general, they are used for evaluating LLMs not only RAG systems. So in this documentation I've used LLM & RAG for the same meaning. (LLM system === RAG system) in terms of evaluation.

#### Evaluation & Monitoring
**Evaluation**:
1. Offline evaluationo (before deploying the RAG-system)
   - Rouge Metrics
   - LLM as a sjudge scheme
   - Dot-product and Consine similarity (how close is the the LLM answer to the expected answer?)\
    If these and other metrics are good enough then deploy. Remeber how we evaluate the search in the previous medule before ***deployment***.
2. Online evaluation (Based on data collected from interacting with the system after deploying it)
   - User feedback
   - A/B test, expriments

**Monitoring**:\
Is the overall health of the system.