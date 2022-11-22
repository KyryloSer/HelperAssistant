from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Files


# Create your views here.
def view_files(request):
    files_all = Files.objects.all()
    ctx = {'files': files_all}
    return render(request, 'filestorageapp/files.html', ctx)

# def view_files(request):
#     files = []
#     if request.user.is_authenticated:
#         files = Files.objects.filter(user_id=request.user).all()
#     else:
#         files = Files.objects.filter(global_bool=True).all()
#     return render(request, 'filestorageapp/files.html', {"files": files})


# @login_required
def filter_files(request, filters):
    all_files = Files.objects.filter(user_id=request.user, type=filters).all()
    return render(request, 'filestorageapp/files.html', {'all_files': all_files, 'filter': filters})


# @login_required
def file_upload(request):
    ...



# @login_required
def file_download(request, file_id):
   ...
