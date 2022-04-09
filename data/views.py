from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import *
# Create your views here.

class ListContact(View):
    def get(self,request):
        contact = Contact.objects.all()
        context = {'contact':contact}
        return render(request, 'list_contact.html', context)

class AddContact(View):
    def get(self,request):
        form = AddContactForm()
        context = {'form':form}
        return render(request, 'add_contact.html', context)
    
    def post(self,request):
        form = AddContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        
class EditContact(View):
    def get(self,request,id):
        contact = Contact.objects.get(id=id)
        form = AddContactForm(instance=contact)
        context = {'form':form,'contact':contact}
        return render(request, 'edit_contact.html', context)

    def post(self,request,id):
        contact = Contact.objects.get(id=id)
        form = AddContactForm(request.POST,instance=contact)
        if form.is_valid():
            form.save()
            return redirect('index')


class DeleteContact(View):
    def get(self,request,id):
        contact = Contact.objects.get(id=id)
        context = {'contact':contact}
        return render(request, 'delete_contact.html', context)

    def post(self,request,id):
        contact = Contact.objects.get(id=id)
        contact.delete()   
        return redirect('index')
            


