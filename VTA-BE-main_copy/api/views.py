from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChatSerializer, QuerySerializer, ResponseSerializer,FeebackSerializer
# from django.http import JsonResponse
from .models import Chat, LikeResponse, DislikeResponse,Feedback
from django.apps import apps
from rest_framework import status
from transformers import BertTokenizer, BertForQuestionAnswering
import os
from QA_VTA.qa_vta import VTA
from django.shortcuts import get_object_or_404

# API Routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {"Endpoint": '/vta-answer/',
         'method': 'POST',
         'body': {"query": "What is a design tool used for?"},
         'description': 'Returns an answer from the VTA'
         },
        {"Endpoint": '/vta/like/',
         'method': 'GET',
         'body': {"VTAText": "a complete experience of software development from ideation to product",
                  "dislike": True,
                  "like": False,
                  "likeStatus": True,
                  "userId": "01900645-4a53-77f5-93c1-0d2be28460a2",
                  "userText": "what is capstone project course?"},
         'description': 'Like VTA response'
         },
        {"Endpoint": '/vta/dislike/',
         'method': 'GET',
         'body': {
             "VTAText": "describing and defending a software architecture, coding in groups and as a large team, integrating independent works, using a source code versioning system",
             "dislike": False,
             "like": False,
             "likeStatus": True,
             "userId": "01900645-4a53-77f5-93c1-0d2be28460a2",
             "userText": "what is capstone?"},
         'description': 'Like VTA response'
         },
        {"Endpoint": '/vta/feedback/',
         'method': 'POST',
         'body': {"userFeedback": "i like the model", "userId": "5e7f6bad-0511-4411-9134-826C9250f335"},
         'description': 'Give a general feedback on the VTA'
         },

    ]
    return Response(routes)


# handle VTA conversations
@api_view(['POST'])
def getAnswer(request):
    query_serializer = QuerySerializer(data = request.data)
    if query_serializer.is_valid():
        query = query_serializer.validated_data['query']
        apiConfig = apps.get_app_config('api')
        capstone_vta = apiConfig.capstone_qa_vta 
        answer = capstone_vta.answer_question(query)
        # Сохраняем чат в базу данных
        Chat.objects.create(query=query, response=answer)
        return Response({'response': answer}, status=status.HTTP_200_OK)
    return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# handle VTA ratings
@api_view(['POST'])
def likeResponse(request):
    response_serializer = ResponseSerializer(data = request.data)
    if response_serializer.is_valid():
        userText = response_serializer.validated_data['userText']
        VTAText = response_serializer.validated_data['VTAText']
        userId = response_serializer.validated_data['userId']
        likeStatus = response_serializer.validated_data['likeStatus']

        if not likeStatus:
            rating = get_object_or_404(LikeResponse,userText = userText, VTAText = VTAText,userId=userId)
            rating.delete()
            return Response({'response': 'unlike successful'}, status=status.HTTP_200_OK)
        new_rating = LikeResponse.objects.create(userText = userText, VTAText = VTAText,userId=userId,likeStatus =likeStatus)
        return Response({'response': 'rating successful'}, status=status.HTTP_200_OK)
    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handle VTA ratings
@api_view(['POST'])
def dislikeResponse(request):
    response_serializer = ResponseSerializer(data = request.data)
    if response_serializer.is_valid():
        userText = response_serializer.validated_data['userText']
        VTAText = response_serializer.validated_data['VTAText']
        userId = response_serializer.validated_data['userId']
        likeStatus = response_serializer.validated_data['likeStatus']

        if not likeStatus:
            rating = get_object_or_404(DislikeResponse,userText = userText, VTAText = VTAText,userId=userId)
            rating.delete()
            return Response({'response': 'unlike successful'}, status=status.HTTP_200_OK)
        new_rating = DislikeResponse.objects.create(userText = userText, VTAText = VTAText,userId=userId,likeStatus =likeStatus)
        return Response({'response': 'rating successful'}, status=status.HTTP_200_OK)

    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# handle user feedback
@api_view(['POST'])
def feedback(request):
    feedback_serializer = FeebackSerializer(data = request.data)
    if feedback_serializer.is_valid():
        userFeedback = feedback_serializer.validated_data['userFeedback']
        userId = feedback_serializer.validated_data['userId']
        new_feedback = Feedback.objects.create(userFeedback = userFeedback,userId=userId)
        return Response({'response': 'Feedback sent! Thank you.'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid feedback data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def likeVTAAnswer(request,pk):
    chats = Chat.objects.all()
    serializer = ChatSerializer(chats,many=True)
    return HttpResponse(serializer.data)
   
   
def index(request):    
    return HttpResponse("Hello world")



