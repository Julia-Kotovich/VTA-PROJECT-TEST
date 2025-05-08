import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download stopwords
try:
    stopwords.words('english')
    # print('Stop words already downloaded') -- debugging
except LookupError:
    nltk.download('stopwords')

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    text = text.strip()
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

# Sample contexts
contexts = [
    "The Capstone project provides a complete experience of software development from ideation to product. The formal course structure is a mix of formal presentations and guest presentations. The course structure of the capstone project includes Requirements elicitations with stakeholders, Fast design and prototyping, Architecture, Practicalities of cybersecurity development following agile processes, and Development using state-of-the-art development tools (git repositories, integration servers, static analyzers). If you want to learn more about this Capstone Project course, check the Article in the 2nd International Workshop on Frontiers in Software Engineering Education (FISEE 23), edited in Lecture Notes in Computer Science by Springer (https://link.springer.com/chapter/10.1007/978-3-031-48639-5_3). The instructor of the Capstone Project is Manuel Oriol. Manuel is a professor of computer science at Constructor Institute. He has 10 years of experience in academia, and 10 years in Industry, Co-authored 60+ articles on software engineering and software architecture, Graduated 4 doctoral students, and 25+ MSc students. The teaching assistants are Muhammad Khalid and Julia Kotovich. Mohammed is a  PhD Researcher and Lecturer at Constructor University.  Julia Kotovich is a PhD Researcher at Constructor Institute.",
    "The course plan for the capstone project includes Design & Ideation, Architecture and Initial Development, Portal ready and deployed, and Advanced concepts and refinements based on customer feedback. The main learnings of the capstone project course includes Creating and proposing mocks (term 1), Requirements elicitation (term 1), Prototyping (term 1), Architecture description (term 2), Coding in groups (term 2), Coding as a large team (term 2), Integration of independent works (term 2), Using a git repository (term 2), Specifying user stories (term 2), Practical cybersecurity (term 3), Practical discussions with stakeholders (term 3), Practicalities of machine learning (term 3), Continuous improvements (term 3).",
    "The organizational points or grading of the capstone project is structured as follows; 1/3 of the grade being a cohort (tribe) grade, and 2/3 of the grade being a group assignment. Note that in rare cases group members are regraded independently. The sprint is 2 weeks long, each review is typically graded, and each time student feedback is gathered using Menti. The plans for Semester one include Ideation, Requirements Elicitation, and Initial development.",
    "Teams are difficult to evolve within. The reasons for this are that you feel that everything is wrong, you do not understand the others, you are not understood, you think they are too different from you, that you won't be able to work with them, you cannot agree on common goals, it cannot be your fault (you have been well integrated before). The following are readings on team development/building; Tuckman's model (https://www.challengeapplications.com/stages-of-team-development, https://agilescrumguide.com/blog/files/tag-5-stages-of-team-development.html)",
     "A continuous integration server is a server that runs pipelines Pulls from a repository, Compiles the code, Runs tests automatically, and Notifies you if there is a problem. Few recognized and professional tools exist. Examples are Jenkins (open source and free), GitlabCI (open source and free), and Azure Pipelines (by Microsoft). In the capstone project course, we will use the processes and tools that we presented. Much of the training for tools should be done online by following tutorials. All these are the basics that everyone needs to understand to do a decent job. TA session will help and answer questions whenever possible."
]

# Preprocess contexts
preprocessed_contexts = [preprocess_text(context) for context in contexts]

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform contexts
tfidf_matrix = vectorizer.fit_transform(preprocessed_contexts)

# Function to find the most similar context
def find_best_context(question, contexts, vectorizer, tfidf_matrix):
    # Preprocess the question
    preprocessed_question = preprocess_text(question)
    
    # Transform the question using the same vectorizer
    question_tfidf = vectorizer.transform([preprocessed_question])
    
    # Calculate cosine similarity between the question and each context
    similarities = cosine_similarity(question_tfidf, tfidf_matrix)
    
    # Find the index of the most similar context
    best_match_index = similarities.argmax()
    
    return contexts[best_match_index], similarities[0, best_match_index]

# Example question
question = "What are some recommended tools for continuous integration?"

# Find the best context
best_context, similarity_score = find_best_context(question, contexts, vectorizer, tfidf_matrix)

print(f'The best context is: "{best_context}" with a similarity score of {similarity_score}')
