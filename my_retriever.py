from collections import defaultdict, Counter
import math


class Retrieve:
    """
    Document Retrieval System using different term weighting schemes:
    - Binary
    - TF (Term Frequency)
    - TF-IDF (Term Frequency-Inverse Document Frequency)
    
    """  
    def __init__(self,index,term_weighting): 
        self.index = index
        self.term_weighting = term_weighting
        self.num_docs = self.compute_number_of_documents()
        
        if term_weighting == "tfidf":
            self.idf = self.compute_idf()  # Call a method to precompute IDF for TF-IDF
            
        # Precompute document vector size for normalization
        self.doc_vector_size = self.compute_doc_vector_size()
        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        return len(self.doc_ids)
    
    
    # Method to precompute IDF for TF-IDF
    def compute_idf(self):
        """
        Precompute the IDF (Inverse Document Frequency) for all terms in the index.
        If no documents contains a particular term, the `max(len(doc_term_map), 1)` is used to avoid division by zero
        to ensure that the IDF score is still computed correctly.
        Returns: idf (dict): A dictionary where keys are terms and values are their corresponding IDF values.
        
        """
        idf = {}
        for term, doc_term_map in self.index.items():
            # To avoid division by zero when no documents contain a term, a max() function is implemented 
            idf[term] = math.log10(self.num_docs / max(len(doc_term_map),1)) 
        return idf
    
    # Method to precompute the document vector size for each document in the collection
    def compute_doc_vector_size(self):
        """
        Computes the vector size for each document in the collection.
        Returns: A dictionary where keys are document IDs, and values are their vector sizes.
        
        """
        doc_size = defaultdict(float)  # Set the default value of 0.0 for missing keys
        for term, doc_term_map in self.index.items():
            for doc_id, term_frequency in doc_term_map.items():
                weight = self.compute_weight(term,term_frequency)
                doc_size[doc_id] += math.pow(weight,2)
        return {doc_id: math.sqrt(size) for doc_id, size in doc_size.items()}
    
    def compute_weight(self,term,term_frequency):
        if self.term_weighting == "binary":
            return 1
        elif self.term_weighting == "tf":
            return term_frequency
        else:  # TF-IDF
            return term_frequency * self.idf[term]
        
        
    def get_candidate_docs(self,query):
        """
        Find candidate documents that contain at least one term from the query.
        Returns: A set of candidate document IDs.
        
        """
        candidate_docs = set()
        for term in query:
            if term in self.index:
                candidate_docs.update(self.index[term].keys())
        return candidate_docs
    
    def compute_cosine_similarity(self,query_weights,candidate_docs):
        """
        Computes the cosine similarity scores for the candidate documents.
        Returns: A dictionary of document IDs to their similarity scores.
        
        """
        similarity_scores = {}
        for doc_id in candidate_docs: # A set of candidate document IDs
            dot_product = 0
            for term, query_weight in query_weights.items():
                if term in self.index and doc_id in self.index[term]:
                    doc_weight = 1  # Binary weighting
                    if self.term_weighting == "tf":  #TF weighting
                        doc_weight = self.index[term][doc_id]
                    elif self.term_weighting == "tfidf":
                        doc_weight = self.index[term][doc_id] * self.idf[term]
                    
                    dot_product += query_weight * doc_weight
            
            # Normalize scores according to the document's vector size
            if doc_id in self.doc_vector_size and self.doc_vector_size[doc_id] > 0:
                similarity_scores[doc_id] = dot_product / self.doc_vector_size[doc_id]
        
        return similarity_scores
    
    
    def for_query(self,query):
        """
       Retrieves the top 10 most relevant documents for a given query.
       Returns: A list of document IDs for the 10 most relevant documents in ranked order.
       
       """
       # Convert query to a dictionary of term frequencies
        query_tf = Counter(query)

        # Compute query weights
        query_weights = {}
        for term, freq in query_tf.items():
            if term in self.index:
                if self.term_weighting == "binary":
                    query_weights[term] = 1
                elif self.term_weighting == "tf":
                    query_weights[term] = freq
                elif self.term_weighting == "tfidf":
                    query_weights[term] = freq * self.idf[term]

        # Call method to compute cosine similarity scores for candidate documents
        candidate_docs = self.get_candidate_docs(query)
        similarity_scores = self.compute_cosine_similarity(query_weights,candidate_docs)

        # Return the top 10 documents sorted by similarity
        ranked_docs = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        # A list of just the document IDs from the sorted ranked_docs
        return [doc_id for doc_id, _ in ranked_docs[:10]]

    
    



