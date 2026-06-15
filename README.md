Here's a README draft you can use for your current RAG project status.

# GraphRAG Research Assistant

A Retrieval-Augmented Generation (RAG) system for answering research paper questions using a hybrid retrieval pipeline combining document retrieval and knowledge graph reasoning.

## Current Status

The system is currently able to answer several paper-specific questions, extract key information from retrieved documents, and provide detailed explanations when sufficient context is available.
<!-- 
### Example Evaluation Results

| Query                                                                                                                                       | Result                                |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| What is the title of the paper?                                                                                                             | Not found in documents              |
| What does STLF stand for?                                                                                                                   | Short-Term Load Forecasting         |
| What are the main contributions in this paper?                                                                                              | Not found in documents              |
| What are the main contributions mentioned in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"? | Retrieved successfully              |
| Explain the problem formulation mentioned in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"  | Retrieved successfully              |
| What expert bank is built in the paper?                                                                                                     | Not found in documents              |
| What experts are used in this paper?                                                                                                        | Retrieved successfully              |
| What are the different types of experts used?                                                                                               | Retrieved successfully              |
| What data split is used in the experiment?                                                                                                  | Retrieved successfully |
| What is the NRMSE for MOMENT in zero-shot setting?                                                                                          | Not found in documents              |
| What is the formula for NRMSE?                                                                                                              | Retrieved successfully              |
| What main federated results were achieved?                                                                                                  | Retrieved successfully              |


-------------------------------------------------
query= what is the tittle of the paper? \
result= Not found in documents.
--------------------------------------------------
query= what does STLF stands for? \
result= STLF stands for Short-Term Load Forecasting.
--------------------------------------------------
query= what are the main contributions in this paper? \
result= Not found in documents.
--------------------------------------------------
query= what are the main contributions in mentioned in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"? \
result= The main contributions of the work "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" are:

1. **Personalized Federated Adaptation**: The study investigates personalized federated adaptation of pretrained Time-Series Foundation Models (TSFMs) for non-IID building energy forecasting, treating each building as a privacy-sensitive client.

2. **Post-Representation Sparse MoE Adapter**: The introduction of a post-representation sparse temporal Mixture-of-Experts (MoE) adapter with sequence-level top-k routing, enabling conditional adaptation without full-model fine-tuning.

3. **Effectiveness of Personalized Parameter Partitions**: The work shows that personalized parameter partitions are more effective than globally aggregating all trainable adaptation parameters under heterogeneous building-client distributions.

4. **Backbone-Aware Analysis**: A backbone-aware analysis is provided across MOMENT, Chronos-2, and Moirai, covering centralized and non-TSFM reference baselines, routing behavior, communication cost, and federated adaptation trends.
--------------------------------------------------
query= explain the problem formulation mentioned in  "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" \
result= The problem formulation in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" focuses on short-term building electricity forecasting using a personalized federated learning approach. Each building is treated as a client that keeps its raw electricity consumption data locally, and the goal is to learn accurate forecasting models across heterogeneous, non-IID clients without centralizing this data.

The formulation involves the following key components:

1. **Forecasting Task**: Each building is represented as a univariate hourly time series. The forecasting model maps a historical context window of length \( L \) (168 hours) to a future prediction horizon of length \( H \) (24 hours), predicting the next day's electricity consumption based on the past week of data.

2. **Personalized Federated Forecasting**: The study considers \( N \) clients (buildings), where the objective is to learn models that can generalize across these clients while respecting their individual data privacy. The trainable parameters are divided into:
   - **Shared Parameters (\( \theta_s \))**: These are aggregated by a central server and capture reusable temporal structures across buildings.
   - **Client-Private Parameters (\( \theta_i \))**: These remain local to each building and preserve client-specific consumption behavior.

3. **Personalized Federated Objective**: The objective function aims to minimize the loss across all clients, represented as:
   \[
   \min_{\theta_s, \{\theta_i\}_{i=1}^N} \sum_{i=1}^N \frac{n_i}{n} L_i(\theta_s, \theta_i)
   \]
   where \( n_i \) is the number of local training windows for client \( i \) and \( n \) is the total number of training windows across all clients. This formulation allows for collaborative learning of globally useful adaptation parameters while keeping client-specific components local.

Overall, the formulation emphasizes the need for a balance between shared knowledge and client-specific adaptations to effectively address the challenges posed by heterogeneous building data in a privacy-preserving manner.
--------------------------------------------------
query= what exper bank is built in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
result= Not found in documents.
--------------------------------------------------
query= what expert bank is built in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
result= Not found in documents.
--------------------------------------------------
query= what experts are used in this paper "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
result= The paper uses a post-representation sparse Mixture-of-Experts (MoE) adapter with sequence-level routing and heterogeneous temporal experts.
--------------------------------------------------
query= what are the different types of experts used?
result= The different types of experts used are:

1. Fourier Expert (F)
2. Attention Expert (A)
3. Convolution Expert (C)
4. Decomposition Expert (D)
5. Wavelet Expert (W)
--------------------------------------------------
query= 
result= Not found in documents.
--------------------------------------------------
query= what data split is used in the experiment?
result= The data split used in the experiment is 50% train, 25% validation, and 25% test.
--------------------------------------------------
query= what is the NRMSE for MOMENT in zero-shot setting?
result= Not found in documents.
--------------------------------------------------
query= what is the NRMSE for MOMENT in zero-shot setting in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
result= Not found in documents.
--------------------------------------------------
query= what is the NRMSE for backbone MOMENT in zero-shot setting in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
result= Not found in documents.
--------------------------------------------------
query= what is the NRMSE for backbone MOMENT in zero-shot setting?
result= Not found in documents.
--------------------------------------------------
query= what data split is used in the experiment?
result= The data split used in the experiment is 50% train, 25% validation, and 25% test.
--------------------------------------------------
query= what is the formula for NRMSE?
result= NRMSE = 100 * (1 / 24M) * Σ (from m=1 to M) Σ (from h=1 to 24) (ym,h - ˆym,h)², where M is the number of 24-hour forecast windows and ¯y is the mean ground-truth electricity consumption over the evaluated windows.
--------------------------------------------------
query= what main federated results were achieved in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
result= The main federated results achieved in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" include:

1. **MOMENT Backbone**:
   - Best PFL-MoE Variant (top-1 routing): NRMSE = 12.769, sMAPE = 9.553
   - PFL without MoE: NRMSE = 12.890, sMAPE = 9.585
   - Shared-expert PFL-MoE: NRMSE = 12.893, sMAPE = 9.565
   - Private-expert PFL-MoE: NRMSE = 13.103, sMAPE = 9.403
   - Local MoE: NRMSE = 13.118, sMAPE = 9.688
   - Global FL-MoE: NRMSE = 13.912, sMAPE = 10.349
   - Zero-shot: NRMSE = 32.275, sMAPE = 28.112

2. **Chronos-2 Backbone**:
   - Best PFL-MoE Variant (F,A,D,W): NRMSE = 10.559, sMAPE = 6.924
   - Zero-shot: NRMSE = 10.573, sMAPE = 7.144
   - Best PFL-MoE Variant (F,A,C,D): NRMSE = 10.598, sMAPE = 6.791
   - Private-expert PFL-MoE: NRMSE = 10.662, sMAPE = 6.873
   - Shared-expert PFL-MoE: NRMSE = 10.834, sMAPE = 6.941
   - PFL without MoE: NRMSE = 10.992, sMAPE = 6.885
   - Local MoE: NRMSE = 11.215, sMAPE = 7.268
   - Global FL-MoE: NRMSE = 11.360, sMAPE = 7.764

These results indicate that personalized federated adaptation consistently improves over global aggregation and often improves over local-only adaptation.
--------------------------------------------------

 -->


## Sample Query Results

### Query

```text
what is the tittle of the paper?
```

### Result

```text
Not found in documents.
```

---

### Query

```text
what does STLF stands for?
```

### Result

```text
STLF stands for Short-Term Load Forecasting.
```

---

### Query

```text
what are the main contributions in this paper?
```

### Result

```text
Not found in documents.
```

---

### Query

```text
what are the main contributions in mentioned in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
```

### Result

```text
The main contributions of the work "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" are:

1. Personalized Federated Adaptation: The study investigates personalized federated adaptation of pretrained Time-Series Foundation Models (TSFMs) for non-IID building energy forecasting, treating each building as a privacy-sensitive client.

2. Post-Representation Sparse MoE Adapter: The introduction of a post-representation sparse temporal Mixture-of-Experts (MoE) adapter with sequence-level top-k routing, enabling conditional adaptation without full-model fine-tuning.

3. Effectiveness of Personalized Parameter Partitions: The work shows that personalized parameter partitions are more effective than globally aggregating all trainable adaptation parameters under heterogeneous building-client distributions.

4. Backbone-Aware Analysis: A backbone-aware analysis is provided across MOMENT, Chronos-2, and Moirai, covering centralized and non-TSFM reference baselines, routing behavior, communication cost, and federated adaptation trends.
```

---

### Query

```text
explain the problem formulation mentioned in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"
```

### Result

```text
The problem formulation in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" focuses on short-term building electricity forecasting using a personalized federated learning approach. Each building is treated as a client that keeps its raw electricity consumption data locally, and the goal is to learn accurate forecasting models across heterogeneous, non-IID clients without centralizing this data.

The formulation involves the following key components:

1. Forecasting Task: Each building is represented as a univariate hourly time series. The forecasting model maps a historical context window of length L (168 hours) to a future prediction horizon of length H (24 hours), predicting the next day's electricity consumption based on the past week of data.

2. Personalized Federated Forecasting:
   - Shared Parameters (θs): Aggregated by a central server.
   - Client-Private Parameters (θi): Remain local to each building.

3. Personalized Federated Objective:

min(θs,{θi}) Σ (ni/n) Li(θs, θi)

where ni is the number of local training windows for client i and n is the total number of training windows.

Overall, the formulation emphasizes balancing shared knowledge and client-specific adaptations.
```

---

### Query

```text
what expert bank is built in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
```

### Result

```text
Not found in documents.
```

---

### Query

```text
what experts are used in this paper "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
```

### Result

```text
The paper uses a post-representation sparse Mixture-of-Experts (MoE) adapter with sequence-level routing and heterogeneous temporal experts.
```

---

### Query

```text
what are the different types of experts used?
```

### Result

```text
The different types of experts used are:

1. Fourier Expert (F)
2. Attention Expert (A)
3. Convolution Expert (C)
4. Decomposition Expert (D)
5. Wavelet Expert (W)
```

---

### Query

```text
what data split is used in the experiment?
```

### Result

```text
The data split used in the experiment is 50% train, 25% validation, and 25% test.
```

---

### Query

```text
what is the NRMSE for MOMENT in zero-shot setting?
```

### Result

```text
Not found in documents.
```

---

### Query

```text
what is the formula for NRMSE?
```

### Result

```text
NRMSE = 100 * (1 / 24M) * Σ (from m=1 to M) Σ (from h=1 to 24) (ym,h - ˆym,h)², where M is the number of 24-hour forecast windows and ¯y is the mean ground-truth electricity consumption over the evaluated windows.
```

---

### Query

```text
what main federated results were achieved in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting"?
```

### Result

```text
The main federated results achieved in "Personalized Federated Sparse Mixture-of-Experts Adaptation for Building Energy Forecasting" include:

1. MOMENT Backbone:
   - Best PFL-MoE Variant (top-1 routing): NRMSE = 12.769, sMAPE = 9.553
   - PFL without MoE: NRMSE = 12.890, sMAPE = 9.585
   - Shared-expert PFL-MoE: NRMSE = 12.893, sMAPE = 9.565
   - Private-expert PFL-MoE: NRMSE = 13.103, sMAPE = 9.403
   - Local MoE: NRMSE = 13.118, sMAPE = 9.688
   - Global FL-MoE: NRMSE = 13.912, sMAPE = 10.349
   - Zero-shot: NRMSE = 32.275, sMAPE = 28.112

2. Chronos-2 Backbone:
   - Best PFL-MoE Variant (F,A,D,W): NRMSE = 10.559, sMAPE = 6.924
   - Zero-shot: NRMSE = 10.573, sMAPE = 7.144
   - Best PFL-MoE Variant (F,A,C,D): NRMSE = 10.598, sMAPE = 6.791
   - Private-expert PFL-MoE: NRMSE = 10.662, sMAPE = 6.873
   - Shared-expert PFL-MoE: NRMSE = 10.834, sMAPE = 6.941
   - PFL without MoE: NRMSE = 10.992, sMAPE = 6.885
   - Local MoE: NRMSE = 11.215, sMAPE = 7.268
   - Global FL-MoE: NRMSE = 11.360, sMAPE = 7.764

These results indicate that personalized federated adaptation consistently improves over global aggregation and often improves over local-only adaptation.
```



## Current Limitations

The following types of queries still fail:

### 1. Metadata Extraction

Examples:

```text
What is the title of the paper?
```

Possible reasons:

* Title not indexed separately.
* Metadata not stored in graph nodes.
* Retrieval misses front matter.

### 2. Generic Reference Queries

Examples:

```text
What are the main contributions in this paper?
```

Without explicitly mentioning the paper title, retrieval often lacks sufficient context.

### 3. Fine-Grained Numerical Lookups

Examples:

```text
What is the NRMSE for MOMENT in zero-shot setting?
```

Possible reasons:

* Table retrieval limitations.
* Chunk boundaries split numerical results.
* Inadequate table indexing.

### 4. Expert Bank Queries

Examples:

```text
What expert bank is built in the paper?
```

The system identifies expert types but struggles with terminology variations such as:

* expert bank
* expert repository
* expert pool
* MoE experts

---

## Planned Improvements

### Retrieval

* Hybrid BM25 + Dense Retrieval
* Metadata-aware retrieval
* Better table indexing
* Citation-aware chunking

### Graph Layer

* Explicit Paper nodes
* Author nodes
* Section nodes
* Table and Figure nodes

### Query Understanding

* Query rewriting
* Acronym expansion
* Entity linking
* Multi-hop graph traversal

### Evaluation

* Precision@K
* Recall@K
* Faithfulness
* Context Relevance
* Answer Correctness

---

## Current Assessment

The system already performs well on:

* Conceptual questions
* Methodology explanations
* Experimental setup retrieval
* Expert identification
* Federated learning result summaries

The major remaining challenges are:

* Metadata retrieval
* Table-based numerical extraction
* Generic paper-reference questions
* Synonym and terminology normalization

Overall, the GraphRAG pipeline demonstrates promising performance for research paper question answering and provides a strong foundation for future improvements.
