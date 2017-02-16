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
  uploaded_filename = "out_test"
  # read the uploaded file and write it to disk.
  with open(uploaded_filename, 'wb+') as destination:
    for chunk in file.chunks():
      destination.write(chunk)
      
  # open the file that we just write to disk and
  # send it to processing
  ffile = open(uploaded_filename)
  parse_subtitles(ffile)

def parse_subtitles(subtitles):
  print("var SUBTITLES = [")
  while True:
    line = subtitles.readline()
    if line == '':
      break
    line_number = int(line)
    time = subtitles.readline()
    line1 = ""
    line2 = subtitles.readline()
    while True:
      line = subtitles.readline()
      if line and len(line) > 1:
        line1 = line2
        line2 = line
      else:
        break

    time = time.strip()
    line1 = line1.strip()
    line2 = line2.strip()

    line1 = line1.replace('"', "'")
    line2 = line2.replace('"', "'")

    print("{")
    print("  duration: \"%s\"," % time)
    print("  line1: \"%s\"," % line1)
    print("  line2: \"%s\"," % line2)
    print("},")
  print("];")
