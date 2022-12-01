from django.db import models


class Camera(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    path = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class Upload(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.TextField(max_length=200)
    video = models.FileField(verbose_name="",null = True, upload_to="")
    name = models.CharField(max_length=100)
    content = models.CharField(default="A new content added",max_length=100)
    createdat = models.DateTimeField()
    
    def __str__(self):
        return self.name + str(self.video)
    
