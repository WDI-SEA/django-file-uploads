from django.shortcuts import render, redirect

# Create your views here.
def index(request):
  if request.method == "GET":
    return render(request, 'uploader/index.html')
  if request.method == "POST":
    srt_file = request.FILES['srt_file']
    handle_uploaded_file(srt_file)
    return redirect('index')
  
def handle_uploaded_file(file):
  with open('out_test', 'wb+') as destination:
    for chunk in file.chunks():
      destination.write(chunk)
