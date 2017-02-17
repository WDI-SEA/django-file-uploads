from django.shortcuts import render, redirect

# Create your views here.
def index(request):
  context = {
    "subtitles": ""
  }
  if request.method == "POST":
    srt_file = request.FILES['srt_file']
    context["subtitles"] = handle_uploaded_file(srt_file)
    print(context)
  return render(request, 'uploader/index.html', context)
  
def handle_uploaded_file(file):
  uploaded_filename = "./uploader/static/subtitles/out_test"
  # read the uploaded file and write it to disk.
  with open(uploaded_filename, 'wb+') as destination:
    for chunk in file.chunks():
      destination.write(chunk)
      
  # open the file that we just write to disk and
  # send it to processing
  ffile = open(uploaded_filename)
  result = open(ffile.name + ".js", "w")
  parse_subtitles(ffile, result)
  result.close()
  return open(result.name, "r").read()

def parse_subtitles(subtitles, result):
  result.write("var SUBTITLES = [")
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

    line1 = line1.replace('"', '\\\"')
    line2 = line2.replace('"', '\\\"')

    result.write("{\n")
    result.write("  duration: \"%s\",\n" % time)
    result.write("  line1: \"%s\",\n" % line1)
    result.write("  line2: \"%s\",\n" % line2)
    result.write("},\n")
  result.write("];\n")
