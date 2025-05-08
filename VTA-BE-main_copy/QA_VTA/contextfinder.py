# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import re

# # Load the JSON corpus file
# with open('./training/new.json', 'r') as f:
#     corpus_data = json.load(f)

# # Extract contexts from the corpus data
# contexts_only = set([item["context"] for item in corpus_data])

# # Preprocess function to remove question words
# def preprocess_query(query):
#     question_words = ['who','who is', 'what is','what', 'where', 'when', 'why', 'how', 'which', 'whom','define' ]
#     # Remove question words
#     query = re.sub(r'\b(?:{})\b'.format('|'.join(question_words)), '', query, flags=re.IGNORECASE)
#     return query.strip()

# # Initialize TF-IDF vectorizer
# tfidf_vectorizer = TfidfVectorizer()

# # Iterate through each context
# for context in contexts_only:
#     # Fit-transform the corpus
#     tfidf_matrix = tfidf_vectorizer.fit_transform([context])

#     # Query
#     query = "who is manuel oriol"

#     # Preprocess query
#     processed_query = preprocess_query(query)

#     # Transform the query into TF-IDF vector
#     query_vector = tfidf_vectorizer.transform([processed_query])

#     # Calculate cosine similarity between query vector and corpus vectors
#     cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

#     # Get the index of the most similar document
#     most_similar_index = cosine_similarities.argmax()

#     # Get the most similar document
#     most_similar_document = context[most_similar_index]

#     print("Most similar document for context '{}':".format(context), most_similar_document)


import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load the JSON corpus file
with open('./training/new.json', 'r') as f:
    corpus_data = json.load(f)

# Extract contexts from the corpus data
contexts_only = set([item["context"] for item in corpus_data])

# Preprocess function to remove question words
def preprocess_query(query):
    question_words = ['who','who is', 'what is','what', 'where', 'when', 'why', 'how', 'which', 'whom','define' ]
    # Remove question words
    query = re.sub(r'\b(?:{})\b'.format('|'.join(question_words)), '', query, flags=re.IGNORECASE)
    return query.strip()

# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Query
query = "What are some historical systems for source code versioning?"

# Preprocess query
processed_query = preprocess_query(query)

# Fit-transform the query using the TF-IDF vectorizer
query_vector = tfidf_vectorizer.fit_transform([query])

# Calculate cosine similarity for each context and find the highest similarity
max_similarity_score = -1
most_similar_document = None

# Iterate through each context
for context in contexts_only:
    # Transform the current context using the TF-IDF vectorizer
    context_vector = tfidf_vectorizer.transform([context])

    # Calculate cosine similarity between query vector and current context vector
    cosine_similarity_score = cosine_similarity(query_vector, context_vector).flatten()[0]

    # Check if the current context has a higher similarity score
    if cosine_similarity_score > max_similarity_score:
        max_similarity_score = cosine_similarity_score
        most_similar_document = context

# Print the most similar document
print("Most similar document with the highest similarity:", most_similar_document)
