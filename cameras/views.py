from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Camera,Upload
from math import ceil
import os
import numpy as np
import cv2
from datetime import datetime
import time


videos_path = settings.MEDIA_ROOT

def showCam(ip,vid_name):
    start = time.perf_counter()
    datestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    print(datestamp)
    capture = cv2.VideoCapture(ip)
    fourcc = cv2.VideoWriter_fourcc(*'PIM1')
    out = cv2.VideoWriter(
        f'{settings.BASE_DIR}/cam1/replay/{vid_name}-{datestamp}.mp4',
        fourcc, 20.0, (640,480))
    end = start
    while(True):
        # Capture frame-by-frame
        ret, frame = capture.read()
        if ret==True:
                frame = cv2.flip(frame,0)

                # write the flipped frame
                out.write(frame)
                end = time.perf_counter()
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
        else:
            break
        


    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()

def getVideos(request):
    
    data = []
    videos = list(Upload.objects.all())
    for video in videos:
        data.append({
            "name":video.name,
            "id":video.id,
            "content":video.content,
            "createdAt":video.createdat,
            "path":'/media//' + str(video.video),
        })  
    
    
    return JsonResponse({
        "videos":data
    })
    
def recordStream(request,cam_name,watch_link):
  if request.method == "POST":
     print(request.body)
     showCam(ip=int(watch_link),vid_name=cam_name)
     return JsonResponse({"message":"streaming"})
  else:
    showCam(ip=int(watch_link),vid_name=cam_name)
    return JsonResponse({"message":"streaming"}) 

def camerapage(request):
    return render(request=request,
                  template_name="cameras/watch.html",
                  context={"Cameras": Camera.objects.all()})
    
def recordCamStream(request,cam_name):
      for cam in Camera.objects.all():
        if cam.title == cam_name:
            showCam(ip=f"{cam.url}/video",vid_name=cam.title)
            return JsonResponse({"message":"streaming"})
        return JsonResponse({"error":"Not Found"})

def watch(request, cam_name):
    
    for cam in Camera.objects.all():
        if cam.title == cam_name:
            return render(request=request,
                          template_name="cameras/watch.html",
                          context={
                              "camera": cam, 
                              "stream":showCam,
                              "cameras": Camera.objects.all()
                         })
    return render(request=request,
                  template_name="home/unknown_page.html",
                  context={"cameras": Camera.objects.all()})


def replay(request,cam_name, page_number=1):
    try:
        page_number = int(page_number)
    except ValueError:
        return render(request=request,
                      template_name="home/unknown_page.html",
                      context={"cameras": Camera.objects.all()})

    class Video:
        def __init__(self, path, title,date=""):
            self.path = path
            self.title = title
            self.date = date

        def __str__(self):
            return self.title

    class Date:
        videos = []

        def __init__(self, path, date):
            self.path = path
            self.date = date

        def __str__(self):
            return self.date

    for cam in Camera.objects.all():
        if cam.title == cam_name:
            dates = []

            for dir_or_file in os.listdir(os.path.join(videos_path, cam.path)):
                date_folder_path = os.path.join(os.path.join(videos_path, cam.path), dir_or_file)
                if os.path.isdir(date_folder_path):
                    new_date = Date(date_folder_path, dir_or_file)
                    for possible_file in os.listdir(date_folder_path):
                        if str(possible_file).endswith("MJPEG.mp4"):
                            continue
                        file_path = os.path.join(date_folder_path, possible_file)
                        if os.path.isfile(file_path):
                            
                            createdAt = datetime.fromtimestamp(os.path.getctime(os.path.join(settings.MEDIA_ROOT+"\\replay", possible_file)))
                            
                            new_video = Video(os.path.join(dir_or_file, possible_file), possible_file.replace("-", ":"),createdAt)
                            new_date.videos.append(new_video)
                    dates.append(new_date)

            dates.sort(key=lambda x: x.date, reverse=True)
            for date in dates:
                date.videos.sort(key=lambda x: x.title, reverse=True)

            page_amount = ceil(len(dates)/7)
            begin = 0 + (page_number-1)*7
            end = 7 + (page_number-1)*7
            begin_end = "{}:{}".format(begin, end)
            

             
            return render(request=request,
                          template_name="cameras/replay.html",
                          context={"dates": dates, "page_amount": page_amount, "current_page": page_number,
                                   "begin_end": begin_end, "cameras": Camera.objects.all(), "camera": cam})

    return render(request=request,
                  template_name="home/unknown_page.html",
                  context={"cameras": Camera.objects.all()})
