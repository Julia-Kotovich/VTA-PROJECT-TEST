from django.db import models

# Create your models here.
class Chat(models.Model):
    query = models.CharField(max_length=200, null=True, blank=True)
    response = models.CharField(max_length=600, null=True, blank=True)
    chat_context = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.query} - {self.response}"
    


class LikeResponse(models.Model):
    userId = models.UUIDField()
    userText = models.CharField(max_length=200, null=True, blank=True)
    VTAText = models.CharField(max_length=1000, null=True, blank=True)
    likeStatus = models.BooleanField()

    def __str__(self):
        return f"Rating: userText: { self.userText} - VTAText: {self.VTAText} - statue: {self.likeStatus} - userId: {self.userId}"
    

class DislikeResponse(models.Model):
    userId = models.UUIDField()
    userText = models.CharField(max_length=200, null=True, blank=True)
    VTAText = models.CharField(max_length=1000, null=True, blank=True)
    likeStatus = models.BooleanField()

    def __str__(self):
        return f"Rating: userText: { self.userText} - VTAText: {self.VTAText} - statue: {self.likeStatus} - userId: {self.userId}"
    
class Feedback(models.Model):
    userId = models.UUIDField()
    userFeedback = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Feedback: userId: { self.userId} - Feedback: {self.userFeedback}"
