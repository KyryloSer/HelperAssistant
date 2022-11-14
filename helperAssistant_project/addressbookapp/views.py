from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import DetailView

from .forms import ContactForm, ContactEditForm
from .models import Contact, Phone


class ContactDetailView(DetailView):
    model = Contact
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['phones'] = Phone.objects.filter(id = context['contact'].id)

        return context


def main(request):
    return render(request, 'addressbookapp/home.html', {})


@login_required
def create_phones(out_phones):

    for phone in out_phones:
        if phone:
            Phone.objects.create(phone=phone)


@login_required
def add_contact(request):
    if request.method == 'POST':
        data = dict(request.POST)
        if not data['name'][0]:
            return redirect(reverse('addressbookapp/add-contact'))

        contact = Contact.objects.create(
            # owner_id=request.user.id,
            name=data['name'][0],
            birthday=data['birthday'][0],
            email=data['email'][0],
            description=data['description']
        )

        # создаются записи в Phone
        create_phones(out_phones=data['phone'])

        return redirect(reverse('detail', kwargs={'pk': contact.id}))

    return render(request, 'addressbookapp/add_contact.html')


@login_required
def delete_contact(request, pk):
    contact = Contact.objects.get(id=pk, user_id=request.user)
    contact.delete()
    return redirect('main')


@login_required
def edit_contact(request):
    pass


@login_required
def find_contacts(pk, request):
    pass







