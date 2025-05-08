from transformers import BertTokenizer

# Initialize the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Provided course plan text
course_plan_text = """
Scrum is a framework primarily used in Agile software development but is also applied in various other fields. In Scrum, work is organized into Sprints that last between 1 week and 1 month, during which requirements remain fixed. Each sprint begins with a sprint planning event where work items are scheduled. Throughout the sprint, daily 15-minute Scrum meetings are held for the team to organize and address potential issues, with team members sharing what they did the previous day and what they plan to do that day, as well as any impediments to sprint goals. At the end of the sprint, a sprint review presents the sprint's results to stakeholders, often using demos, and discusses future plans. Following this, a sprint retrospective is held where the team reviews impediments, issues, and positive aspects to improve the process for future sprints. Scrum roles include the Scrum Master, Product Owner, and Development Team. The Scrum Master manages the process, coaches the team on Scrum practices, ensures team harmony, and keeps everyone aligned. The Product Owner defines the product backlog, ensures understanding of the backlog and its direction, and sets the requirements for the project and sprints. The Development Team consists of developers who work on the tasks. Work in Scrum is organized using a backlog, a prioritized list of work items. These items should be achievable within a sprint and typically include a definition of done, often expressed as user stories in the format: "As a ... I want to ... so that ...". The product backlog encompasses the entire product, while the sprint backlog pertains to a specific sprint. Large user stories can be broken down into Epics, which contain several user stories. In the Capstone Project, sprints last 2 weeks, each review is usually graded, and student feedback is gathered using Menti.

"""

# Tokenize the text
tokens = tokenizer.tokenize(course_plan_text)

# Count the number of tokens
num_tokens = len(tokens)
print(f"Number of tokens: {num_tokens}")
