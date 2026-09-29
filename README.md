# Document Retrieval System
A document retrieval system originally developed as part of my undergraduate studies and now being revisited and modernised as a personal project.

The system implements classical information retrieval techniques to retrieve and rank relevant documents from the CACM (Communications of the ACM) collection. It supports multiple term-weighting schemes and preprocessing configurations, allowing their effects on retrieval performance to be compared.

## Features

The original retrieval system supports:

- Binary term weighting
- Term Frequency (TF) weighting
- TF-IDF weighting
- Cosine similarity for document ranking
- Stopword removal
- Stemming
- Candidate document filtering
- Precomputed IDF values
- Top-10 document retrieval
- Evaluation using precision, recall, and F-measure

## Dataset

The project uses the CACM document collection, consisting of articles from *Communications of the ACM*.

The accompanying query collection contains information retrieval queries covering topics such as operating systems, distributed computing, algorithms, programming languages, computer graphics, and other areas of computer science.

A gold-standard relevance file identifies the documents considered relevant to each query and is used to evaluate retrieval performance.

## How It Works

The original retrieval pipeline can be summarized as:

```text
CACM Documents
      ↓
Preprocessing
      ├── Stopword Removal
      └── Stemming
      ↓
Document Index
      ↓
Term Weighting
      ├── Binary
      ├── TF
      └── TF-IDF
      ↓
Cosine Similarity
      ↓
Document Ranking
      ↓
Top 10 Documents
      ↓
Evaluation
```

For a given query, the system identifies candidate documents containing at least one query term. Query and document terms are weighted according to the selected weighting scheme, and cosine similarity is used to rank candidate documents.

The ten highest-ranked documents are returned for each query.

## Term Weighting

### Binary

Binary weighting represents whether a term occurs in a document.

```text
term present → 1
term absent  → 0
```

### Term Frequency (TF)

TF weighting uses the number of times a term occurs in a document.

### TF-IDF

TF-IDF combines term frequency with inverse document frequency, giving greater importance to terms that are frequent within a document but less common across the overall collection.

## Running the Retrieval System

The retrieval engine is run from the command line:

```bash
python IR_engine.py [options]
```

Available options include:

```text
-s              Enable stoplisting
-p              Enable stemming
-w binary       Use Binary weighting
-w tf           Use TF weighting
-w tfidf        Use TF-IDF weighting
-o FILE         Write retrieval results to FILE
```

For example, to run TF-IDF with both stoplisting and stemming:

```bash
python IR_engine.py -s -p -w tfidf -o results.txt
```

## Evaluation

The retrieved documents can be evaluated against the provided CACM gold-standard relevance judgments using:

```bash
python eval_ir.py -F cacm_gold_std.txt results.txt
```

The original experiments compared combinations of:

- Binary, TF, and TF-IDF weighting
- Without preprocessing
- Stoplisting
- Stemming
- Stoplisting + stemming

The strongest configuration in the original implementation used **TF-IDF with stoplisting and stemming**, producing:

| Metric | Score |
|---|---:|
| Precision | 0.27 |
| Recall | 0.22 |
| F-measure | 0.24 |

These results provide the baseline against which future improvements to the retrieval system can be evaluated.

## Project Modernisation

This repository revisits an information retrieval system I originally developed during my undergraduate studies.

Rather than replacing the original implementation, the goal is to use it as a reproducible baseline and progressively investigate more modern information retrieval techniques.

Planned improvements include:

- [x] Reproduce the original TF-IDF retrieval results
- [ ] Refactor and improve the original codebase
- [ ] Reproduce and document all original weighting/preprocessing experiments
- [ ] Implement BM25 retrieval
- [ ] Add ranking-oriented evaluation metrics such as Precision@K, Recall@K, MRR, and nDCG
- [ ] Implement semantic retrieval using text embeddings
- [ ] Investigate hybrid lexical-semantic retrieval
- [ ] Compare classical and modern retrieval approaches
- [ ] Develop a simple interface for exploring search results

## Project Structure

```text
.
├── IR_engine.py
├── my_retriever.py
├── eval_ir.py
├── IR_data.pickle
├── documents.txt
├── queries.txt
├── cacm_gold_std.txt
└── README.md
```

### `IR_engine.py`

Command-line entry point for selecting preprocessing options and weighting schemes, executing queries, and writing ranked retrieval results.

### `my_retriever.py`

Contains the retrieval implementation, including Binary, TF and TF-IDF weighting, candidate document selection, cosine similarity calculation, and document ranking.

### `eval_ir.py`

Evaluates retrieved documents against the CACM gold-standard relevance judgments and calculates retrieval performance measures.

### `IR_data.pickle`

Contains the preprocessed indexes and query representations used by the original retrieval system.

### `documents.txt`

The CACM document collection used by the retrieval system.

### `queries.txt`

The query collection used for retrieval experiments.

### `cacm_gold_std.txt`

Gold-standard relevance judgments identifying relevant documents for each query.

## Background

This project began as an undergraduate information retrieval assignment focused on implementing and evaluating classical document retrieval techniques.

I am revisiting the project to improve its software design, reproduce the original experiments, and explore how classical retrieval methods compare with modern lexical and semantic retrieval approaches.
