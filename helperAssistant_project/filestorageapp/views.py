import cloudinary_storage
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Picture, Category
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def upload(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        file = request.FILES.get('picture')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None
        picture = Picture.objects.create(
            title=data['title'],
            picture=file,
            uploaded_by=request.user,
            category=category
        )
        return redirect('gallery')
    return render(request, 'filestorageapp/upload.html', {'categories': categories})


@login_required
def gallery(request):
    category = request.GET.get('category')
    if category is None:
        pictures = Picture.objects.filter(uploaded_by=request.user.id)
    else:
        pictures = Picture.objects.filter(category__name=category, uploaded_by=request.user.id)
    categories = Category.objects.all()
    return render(request, 'filestorageapp/gallery.html', {'pictures': pictures, 'categories': categories})


@login_required
def viewPicture(request, pk):
    picture = Picture.objects.get(id=pk)
    return render(request, 'filestorageapp/picture.html', {'picture': picture})


@login_required
def delete_picture(request, pk):
    if request.method == 'POST':
        print(pk)
        picture = Picture.objects.get(id=pk)
        try:

            # cloudinary.uploader.destroy(picture.picture.public_id, invalidate=True)
            # cloudinary_storage.delete(name=picture.picture.name)
            picture.delete()
        except:
            pass
    return redirect('gallery')
