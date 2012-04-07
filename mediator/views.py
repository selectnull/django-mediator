from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils import simplejson as json
import os
from django.contrib.admin.views.decorators import staff_member_required
import fnmatch


class Failed(BaseException):
    pass

def no_result():
    return HttpResponse(json.dumps(None), mimetype="text/html")

def is_query_valid(root):
    if root.startswith('/'):
        return False

    os_path = os.path.join(settings.FILE_REPOSITORY_ROOT, root)
    if not os.path.isdir(os_path):
        return False

    return True

@staff_member_required
def list(request):
    files = []
    for x in os.walk(settings.FILE_REPOSITORY_ROOT):
        files.append(x)

    return render(request, 'mediator/index.html',
        {'title': 'Manage your files', 'files': files})

@staff_member_required
def query(request):
    q = request.GET.get('q', '')
    if not is_query_valid(q):
        return no_result()

    results = []
    files = os.listdir(os.path.join(settings.FILE_REPOSITORY_ROOT, q))
    # sort on name
    files.sort()
    for item in files:
        url = os.path.join(settings.FILE_REPOSITORY_URL, q, item)
        path, name = os.path.split(url)
        extension = os.path.splitext(url)[1]
        file_or_dir = 'f'
        if os.path.isdir(os.path.join(settings.FILE_REPOSITORY_ROOT, q, item)):
            file_or_dir = 'd'

        results.append(
            (url, path, name, extension, file_or_dir)
        )
    # sort on dir first, files second
    results.sort(lambda x,y: cmp(x[4], y[4]))
    return HttpResponse(json.dumps(results), mimetype="text/html")

@staff_member_required
def mkdir(request):
    q = request.GET.get('q', '')
    if q.startswith('/'):
        return no_result()

    root = settings.FILE_REPOSITORY_ROOT
    dirPath = os.path.join(root, q)

    if os.path.exists(dirPath) and os.path.isdir(dirPath):
        return no_result()
    else:
        os.mkdir(dirPath)
        return HttpResponse(json.dumps(True), mimetype="text/html")

@staff_member_required
def upload(request):
    q = request.GET.get('q', '')
    if q.startswith('/'):
        return no_result()

    root = settings.FILE_REPOSITORY_ROOT
    uploadPath = os.path.join(root, q)

    upload = request.FILES['fileToUpload']
    while os.path.exists(os.path.join(uploadPath, upload.name)):
        upload.name = '_' + upload.name
    dest = open(os.path.join(uploadPath, upload.name), 'wb')
    for chunk in upload.chunks():
        dest.write(chunk)
    dest.close()
    return HttpResponse(json.dumps(upload.name), mimetype="text/html")

@staff_member_required
def search(request):
    q = request.GET.get('q', '')
    if q.startswith('/'):
        return no_result()

    split_q = q.split()
    root = settings.FILE_REPOSITORY_ROOT
    base_url = settings.FILE_REPOSITORY_URL
    count_found_dirs = 0
    for sub_directory in split_q:
        if os.path.isdir(os.path.join(root, sub_directory)):
            count_found_dirs += 1
            root = os.path.join(root, sub_directory)
            base_url = os.path.join(base_url, sub_directory)
    file_patterns = split_q[count_found_dirs:]
    if not file_patterns:
        file_patterns = ['']

    found_dirs = os.walk(root)

    found_files = []
    for item in found_dirs:
        matching_files = []
        for pattern in file_patterns:
            matching_files += fnmatch.filter(
                map(lambda x: os.path.join(item[0], x), [y for y in item[2]]), 
                '*%s*' % pattern
            )

        for match in matching_files:
            found_files.append(match)

    results = []
    #results.append((root, base_url, count_found_dirs, file_patterns))
    for item in found_files:
        url = item.replace(settings.FILE_REPOSITORY_ROOT, settings.FILE_REPOSITORY_URL)
        path, name = os.path.split(url)
        extension = os.path.splitext(url)[1]
        file_or_dir = 'f'

        results.append(
            (url, path, name, extension, file_or_dir)
        )

    # sort on name
    results.sort(lambda x,y: cmp(x[0], y[0]))
    return HttpResponse(json.dumps(results), mimetype="text/html")

