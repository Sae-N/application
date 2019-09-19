'''
from django.shortcuts import render
from django.utils import timezone
from .models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'config/post_list.html', {'posts': posts})
'''

import os
from config import addCsv


UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'

def handle_uploaded_file(f):
    path = os.path.join(UPLOAD_DIR, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        addCsv.insert_csv_data(path)
    except Exception as exc:
        logger.error(exc)

    os.remove(path)

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FIELS['file'])
            return redirect('config:upload_complete')
    else:
        form = UploadFileForm()
    return render(request, 'config/upload.html', {'form':form})

def upload_complete(request):
    return render(request, 'config/upload_complete.html')
