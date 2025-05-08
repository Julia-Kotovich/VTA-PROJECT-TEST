# CAPSTONE VIRTUAL ASSISTANT
Virtual assistant  for the capstone project course

## Installation
* Clone repo: ``` https://github.com/kpodjison/new-vta-backend.git ```
* Download model: ``` https://drive.google.com/file/d/1RSLcMApBJVpNCT1jkSZ6wHeflh_AZLlo/view?usp=sharing ```
* Create a directory under vta_qa_model  named model and place your unzipped model ``` vta_qa_models->model->[downloaded model]```
* Install dependencies: ``` pip install -r requirements.txt ```
* Make database migrations: ``` python manage.py migrate ```

## Running the app
``` python manage.py runserver```
App runs on this localhost url [vta-backend](http://127.0.0.1:8000/)

All [Endpoints](http://127.0.0.1:8000/api/routes/)
```json
[
    {
        "Endpoint": "/vta-answer/",
        "method": "POST",
        "body": {
            "query": "What is a design tool used for?"
        },
        "description": "Returns an answer from the VTA"
    },
    {
        "Endpoint": "/vta/like/",
        "method": "GET",
        "body": {
            "VTAText": "a complete experience of software development from ideation to product",
            "dislike": true,
            "like": false,
            "likeStatus": true,
            "userId": "01900645-4a53-77f5-93c1-0d2be28460a2",
            "userText": "what is capstone project course?"
        },
        "description": "Like VTA response"
    },
    {
        "Endpoint": "/vta/dislike/",
        "method": "GET",
        "body": {
            "VTAText": "describing and defending a software architecture, coding in groups and as a large team, integrating independent works, using a source code versioning system",
            "dislike": false,
            "like": false,
            "likeStatus": true,
            "userId": "01900645-4a53-77f5-93c1-0d2be28460a2",
            "userText": "what is capstone?"
        },
        "description": "Like VTA response"
    },
    {
        "Endpoint": "/vta/feedback/",
        "method": "POST",
        "body": {
            "userFeedback": "i like the model",
            "userId": "5e7f6bad-0511-4411-9134-826C9250f335"
        },
        "description": "Give a general feedback on the VTA"
    }
]

```
Directory Info
📍**NB**: THIS REPO THAT NOT INCLUDE THE FINETUNED MODEL DUE TO ITS SIZE.

