
from itertools import groupby


from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from .models import Tag, Note, User
from .forms import TagForm, NoteForm



# Create your views here.

def start(request):
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(user_id=request.user).all()
    return render(request, 'notebookapp/note_start.html', {"notes": notes})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user_id=request.user)
    note.tag_list = ', '.join([str(name) for name in note.tags.all()])
    return render(request, 'notebookapp/detail.html', {"note": note})


@login_required
def tag(request):
    if request.method == 'POST':
        try:
            form = TagForm(request.POST)
            tag = form.save(commit=False)
            tag.user_id = request.user
            tag.save()
            return redirect(to='start')
        except ValueError as err:
            return render(request, 'notebookapp/tag.html', {'form': TagForm(), 'error': err})
        except IntegrityError as err:
            return render(request, 'notebookapp/tag.html', {'form': TagForm(), 'error': 'Tag will be unique!'})
    return render(request, 'notebookapp/tag.html', {'form': TagForm()})


@login_required
def note(request):
    tags = Tag.objects.filter(user_id=request.user).all()

    if request.method == 'POST':
        try:
            list_tags = request.POST.getlist('tags')
            form = NoteForm(request.POST)
            new_note = form.save(commit=False)
            new_note.user_id = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=list_tags, user_id=request.user)  # WHERE name in []
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='start')
        except ValueError as err:
            return render(request, 'notebookapp/note.html', {"tags": tags, 'form': NoteForm(), 'error': err})

    return render(request, 'notebookapp/note.html', {"tags": tags, 'form': NoteForm()})


class FindView(ListView):
    model = Note
    template_name = 'notebookapp/find_note.html'

    def get_queryset(self, **kwargs):
        notes = []
        print("123")
        if self.request.method == 'GET':
            select = self.request.GET.get('q')
            note = Note.objects.filter(
                Q(user_id=self.request.user, tags__name__icontains=select) | Q(user_id=self.request.user,
                                                                               name__icontains=select)).all()
            notes.append(note)
        return notes


@login_required
def show_notes(request):
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(user_id=request.user).all()
    return render(request, 'notebookapp/find_note.html', {"notes": notes})


@login_required
@csrf_protect
def find_note(request, filter):
    notes = []
    if request.method == 'GET':
        search_value = request.GET.get('search_key')
        note = Note.objects.filter(
            Q(user_id=request.user, tags__name__icontains=search_value) | Q(user_id=request.user,
                                                                            name__icontains=search_value)).all()
        notes = list(note)
        new_notes = [el for el, _ in groupby(notes)]
        return render(request, 'notebookapp/find_note.html', {'notes': new_notes})


@login_required
def edit_note(request, note_id):
    note = Note.objects.get(pk=note_id, user_id=request.user)
    tags = Tag.objects.filter(user_id=request.user).all()
    if request.method == 'POST':
        try:
            list_tags = request.POST.getlist('tags')
            form = NoteForm(request.POST, instance=note)
            new_note = form.save(commit=False)
            new_note.user_id = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=list_tags, user_id=request.user)
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='start')
        except ValueError as err:
            return render(request, 'notebookapp/edit_note.html', {"tags": tags, 'form': NoteForm(), 'error': err})

    return render(request, 'notebookapp/edit_note.html', {"tags": tags, 'form': NoteForm(instance=note)})



@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user_id=request.user).update(done=True)
    return redirect('show_notes')



@login_required
def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id, user_id=request.user)
    note.delete()
    return redirect('show_notes')
