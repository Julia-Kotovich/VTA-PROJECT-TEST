import json
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_data_for_context_finder(file_path):
    with open(file_path, 'r') as f:
        corpus_data = json.load(f)
    unique_contexts = set([item["context"] for item in corpus_data])
    return list(unique_contexts)

def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = text.strip()
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

def get_context(query, contexts):
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')
    preprocessed_contexts = [preprocess_text(context) for context in contexts]
    preprocessed_query = preprocess_text(query)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_contexts)
    query_tfidf = vectorizer.transform([preprocessed_query])
    similarities = cosine_similarity(query_tfidf, tfidf_matrix)
    best_match_index = similarities.argmax()
    return contexts[best_match_index], similarities[0, best_match_index]

def find_best_qa_pair(user_question, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_questions = []
    all_answers = []
    for block in data:
        for qa in block.get('qas', []):
            all_questions.append(qa['question'])
            all_answers.append(qa['answers'][0]['text'][0])
    def preprocess(text):
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower().strip()
        return ' '.join([w for w in text.split() if w not in stopwords.words('english')])
    preprocessed_questions = [preprocess(q) for q in all_questions]
    preprocessed_user = preprocess(user_question)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)
    user_vec = vectorizer.transform([preprocessed_user])
    similarities = cosine_similarity(user_vec, tfidf_matrix)
    best_idx = similarities.argmax()
    best_score = similarities[0, best_idx]
    return all_questions[best_idx], all_answers[best_idx], best_score

