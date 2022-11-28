from datetime import timedelta, date
from itertools import chain

from django.core import paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator


from .forms import ContactForm, ContactEditForm
from .models import Contact, Phone, Email


# from faker import Faker

# faker = Faker('uk_UA')


class ContactDetailView(DetailView):
    model = Contact
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = Email.objects.filter(contact_id=context['contact'].id).first()
        context['phone'] = Phone.objects.filter(contact_id=context['contact'].id)
        return context


class BirthdayView(ListView ):
    model = Contact
    template_name = 'birthdays.html'

    def get_queryset(self):
        date_begin = date.today()
        date_end = date_begin + timedelta(days=7)
        date_begin = (date_begin.month, date_begin.day)
        date_end = (date_end.month, date_end.day)

        contact = Contact.objects.filter(owner_id=self.request.user.id)
        result = []
        for con in contact:
            if date_begin < (con.birthday.month, con.birthday.day) < date_end:

                result.append(con)
                print(result)
        return result


class AllView(ListView ):
    model = Contact, Phone, Email
    template_name = 'addressbook_home.html'

    def get_queryset(self):
        contact = Contact.objects.all()
        phone = Phone.objects.all()
        email = Email.objects.all()
        return contact


class SearchResultsView(ListView):
    model = Contact
    template_name = 'addressbookapp/search_results.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list_1 = (Contact.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)))
        object_list_2 = Phone.objects.filter(phone__icontains=query)
        object_list_3 = Email.objects.filter(email__icontains=query)
        object_list = chain(object_list_3,object_list_2,object_list_1)
        return object_list


def create_phones(contact: Contact, out_phones):
    for phone in out_phones:
        if phone:
            Phone.objects.create(contact=contact, phone=phone)


def create_email(contact: Contact, email):
    if email:
        Email.objects.create(contact=contact, email=str(email))

@login_required
def add_contact(request):
    if request.method == 'POST':
        data = dict(request.POST)
        if not data['name'][0]:
            return redirect(reverse('addressbookapp/add-contact'))

        contact = Contact.objects.create(
            owner_id=request.user.id,
            name=data['name'][0],
            birthday=data['birthday'][0],
            address=data['address'][0],
            description=data['description'][0]
        )

        create_phones(contact, out_phones=data['phone'])
        create_email(contact, email=data['email'][0])

        return redirect(reverse('detail', kwargs={'pk': contact.id if contact.id else 0}))

    return render(request, 'addressbookapp/add_contact.html')


@login_required
def delete_contact(request, pk):
    contact = Contact.objects.get(id=pk)
    contact.delete()
    return redirect('addressbookapp_main')


@login_required
def edit_contact(request, pk):

    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
        try:
            contact = Contact.objects.get(id=pk, owner_id=request.user.id,)
            if contact.name != str(data['name']):
                contact.name = str(data['name'][0])

            if contact.birthday != datetime.strptime(data['birthday'][0], '%Y-%m-%d'):
                contact.birthday = datetime.strptime(data['birthday'][0], '%Y-%m-%d')

            if contact.address != str(data['address']):
                contact.address = str(data['address'][0])

            if contact.description != data['description']:
                contact.description = str(data['description'][0])

            phone = Phone.objects.filter(contact_id=pk)

            if list(phone) != data['phone']:
                phone.delete()
                create_phones(contact, out_phones=(data.get('phone')))

            email = Email.objects.filter(contact_id=pk)
            if list(email) != data.get('email'):
                email.delete()
                create_email(contact, email=data.get('email')[0])

            contact.save()

            return redirect('addressbookapp_main')

        except ValueError as err:
            return render(request, 'addressbokapp/adressbook_home.html', {'form': ContactForm(), 'error': err})
        except IntegrityError as err:
            return render('addressbokapp/adressbook_home.html', {'form': ContactForm(), 'error': 'Contact must be unique!'})

    context = dict()
    context['contact'] = Contact.objects.get(id=pk)
    context['phones'] = Phone.objects.filter(contact_id=pk)
    context['emails'] = Email.objects.filter(contact_id=pk)
    return render(request, 'addressbookapp/edit_contact.html', context)


@login_required
def find_contacts(request):
    query = request.GET.get('q')
    try:
        pk = Contact.objects.filter(Q(name__icontains=query, owner_id=request.user.id))[0].id
        return redirect('edit-contact', pk)
    except IndexError or ValueError:
        return redirect('addressbookapp_main')


@login_required
def main(request):
    contacts = Contact.objects.filter(owner_id=request.user.id,).all()

    paginat = Paginator(contacts, 5)
    page_number = request.GET.get("page")
    page_obj = paginat.get_page(page_number)

    return render(request, 'addressbookapp/addressbook_home.html', {"page_obj": page_obj})


# @login_required
# def add_fake_contact(request):
#     for i in range(50):
#         contact = Contact.objects.create(
#             owner_id=request.user.id,
#             name=faker.name(),
#             birthday=faker.date_between(start_date='-60y', end_date='-10y'),
#             address=faker.address(),
#             description="Fake note"
#         )
#
#         for i in range(3):
#             Phone.objects.create(contact=contact, phone=faker.phone_number())
#
#         Email.objects.create(contact=contact, email=faker.email())
#     return redirect('addressbookapp_main')