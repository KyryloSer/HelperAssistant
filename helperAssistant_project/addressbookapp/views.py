from datetime import datetime, timedelta
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .forms import ContactForm, ContactEditForm
from .models import Contact, Phone, Email


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
        print('BIRTHDAYfunc')
        today = datetime.now()
        end = today + timedelta(days=7)
        today = today.strftime('%m-%d').split('-')
        end_birth = end.strftime('%m-%d').split('-')
        print('DATE OF END', end_birth)
        end_month = end_birth[0]
        end_day = end_birth[1]

        contact = Contact.objects.all()
        result = []
        for con in contact:
            print(con.birthday)
            con_birth = con.birthday.strftime('%m-%d').split('-')
            cont_month = con_birth[0]
            print(cont_month)
            cont_day = con_birth[1]
            print(cont_day)

            if (int(cont_month) >= int(today[0]) and int(cont_day) >= int(today[1])) \
                    and (int(cont_month) <= int(end_month) and int(cont_day) <= int(end_day)):
                result.append(con)
                print(result)
        print(result)
        return result


class SearchResultsView(ListView):
    model = Contact
    template_name = 'addressbookapp/search_results.html'

    def get_queryset(self):  # новый
        check_values = self.request.GET.get("optradio")

        print(check_values)
        query = self.request.GET.get('q')
        if check_values == "contact_box":
            object_list_1 = (Contact.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)))
            return object_list_1
        elif check_values == "phone_box":
            object_list_2 = Phone.objects.filter(phone__icontains=query)
            return object_list_2
        elif check_values == "phone_box":
            object_list_3 = Email.objects.filter(email__icontains=query)
            return object_list_3


def main(request):
    return render(request, 'home.html', {})


def create_phones(contact: Contact, out_phones):
    for phone in out_phones:
        if phone:
            Phone.objects.create(contact=contact, phone=phone)


def create_email(contact: Contact, email):
    if email:
        Email.objects.create(contact=contact, email=email)


def add_contact(request):
    if request.method == 'POST':
        data = dict(request.POST)
        if not data['name'][0]:
            return redirect(reverse('addressbookapp/add-contact'))

        contact = Contact.objects.create(
            # owner_id=request.user.id,
            name=data['name'][0],
            birthday=data['birthday'][0],
            address=data['address'][0],
            description=data['description']
        )

        create_phones(contact, out_phones=data['phone'])
        create_email(contact, email=data['email'][0])

        return redirect(reverse('detail', kwargs={'pk': contact.id if contact.id else 0}))

    return render(request, 'addressbookapp/add_contact.html')


# @login_required
def delete_contact(request, pk):
    contact = Contact.objects.get(id=pk)
    contact.delete()
    return redirect('main')


# @login_required
def edit_contact(request, pk):
    print("Edit", pk)

    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
        try:
            contact = Contact.objects.get(id=pk)
            if contact.name != str(data['name']):
                contact.name = str(data['name'])

            if contact.birthday != datetime.strptime(data['birthday'][0], '%Y-%m-%d'):
                contact.birthday = datetime.strptime(data['birthday'][0], '%Y-%m-%d')

            if contact.address != str(data['address']):
                contact.address = str(data['address'])

            if contact.description != str(data['description']):
                contact.description = str(data['description'])

            phone = Phone.objects.filter(contact_id=pk)
            print(list(i.phone for i in phone)), data.get('phone', [])
            if list(phone) != data['phone']:
                print(list(phone), data.get('phone'))

                print('PHONE')
                phone.delete()
                create_phones(contact, out_phones=(data.get('phone', []) + data.get('new_phone')))

            email = Email.objects.filter(contact_id=pk)
            if list(email) != data.get('email'):
                print(list(email), data.get('email'))

                print('Email')
                email.delete()
                create_email(contact, email=(data.get('email', []) + data.get('new_email')))

            # form = ContactForm(request.POST)
            # contact_form = form.save(commit=False)
            # # tag.user_id = request.user
            contact.save()
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'addressbokapp/home.html', {'form': ContactForm(), 'error': err})
        except IntegrityError as err:
            return render('addressbokapp/home.html', {'form': ContactForm(), 'error': 'Contact must be unique!'})

    context = dict()
    context['contact'] = Contact.objects.get(id=pk)
    context['phones'] = Phone.objects.filter(contact_id=pk)
    context['emails'] = Email.objects.filter(contact_id=pk)
    return render(request, 'addressbookapp/edit_contact.html', context)
    # return redirect(reverse('detail', kwargs={'pk': context['contact'].id}))

    #


# @login_required
def find_contacts(request):
    query = request.GET.get('q')

    pk = Contact.objects.filter(Q(name__icontains=query))[0].id
    # print(contact_id)
    return redirect('edit-contact', pk)

#
# def birthdays(request):
#     print('BIRTHDAYfunc')
#     today = datetime.now()
#     end = today + timedelta(days=7)
#     today = today.strftime('%m-%d').split('-')
#     end_birth = end.strftime('%m-%d').split('-')
#     print('DATE OF END',end_birth)
#     end_month = end_birth[0]
#     end_day = end_birth[1]
#
#     contact = Contact.objects.all()
#     result = []
#     for con in contact:
#         print(con.birthday)
#         con_birth = con.birthday.strftime('%m-%d').split('-')
#         cont_month = con_birth[0]
#         print(cont_month)
#         cont_day = con_birth[1]
#         print(cont_day)
#
#         if (int(cont_month) >= int(today[0]) and int(cont_day) >= int(today[1]))\
#                 and (int(cont_month) <= int(end_month) and int(cont_day) <= int(end_day)):
#             result.append(con)
#             print(result[0].name)
#
#         return redirect(reverse(BirthdayView, args=result))
#
