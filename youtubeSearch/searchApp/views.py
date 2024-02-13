from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
import json

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, "searchApp/index.html", {"query": ""})

    query = request.POST["query"].replace(" ", "+")

    

    r = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?maxResults=10&relevanceLanguage=en&type=video&q={query}&key={key}", params=request.GET)
    r = json.loads(r.text)

    videos = ""

    for video in r["items"]:
        if video == r["items"][-1]:
            videos += video["id"]["videoId"]
        else: 
            videos += video["id"]["videoId"]+"%2C"


    r2 = requests.get(f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={videos}&key=&key={key}", params=request.GET)
    r2 = json.loads(r2.text)
    items = r2["items"]

    finalData = []

    for video in items:
        snippet = video["snippet"]
        finalData.append([video["id"],snippet["title"], snippet["thumbnails"]["medium"]["url"], snippet["channelTitle"]])

    return render(request, "searchApp/index.html", {"results": finalData,
                                                    "query": request.POST["query"]})