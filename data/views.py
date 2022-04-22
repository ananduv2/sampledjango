from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
# Create your views here.


class Login(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('index')
        else:
            form = AuthenticationForm()
            context = {'form':form}
            return render(request, 'login.html', context)

    def post(self,request):
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('index')
        else:
            context = {'form':form}
            return render(request, 'login.html', context)




class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class ListContact(View):
    def get(self,request):
        user = request.user
        if user.is_authenticated:
            contact = Contact.objects.filter(user=user)
            context = {'contact':contact,'user':user}
            return render(request, 'list_contact.html', context)
        else:
            return redirect('login')

class AddContact(View):
    def get(self,request):
        user = request.user
        if user.is_authenticated:
            form = AddContactForm()
            context = {'form':form}
            return render(request, 'add_contact.html', context)
        else:
            return redirect('login')
    
    def post(self,request):
        form = AddContactForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect('index')

        
class EditContact(View):
    def get(self,request,id):
        user = request.user
        if user.is_authenticated:
            contact = Contact.objects.get(id=id)
            if contact.user == user:
                form = AddContactForm(instance=contact)
                context = {'form':form,'contact':contact}
                return render(request, 'edit_contact.html', context)
            else:
                return HttpResponse("You dont have permission to edit this contact")
        else:
            return redirect('login')

    def post(self,request,id):
        contact = Contact.objects.get(id=id)
        form = AddContactForm(request.POST,instance=contact)
        if form.is_valid():
            form.save()
            return redirect('index')


class DeleteContact(View):
    def get(self,request,id):
        user = request.user
        if user.is_authenticated:
            contact = Contact.objects.get(id=id)
            if contact.user == user:
                context = {'contact':contact}
                return render(request, 'delete_contact.html', context)
            else:
                return HttpResponse("You dont have permission to delete this contact")
        else:
            return redirect('login')

    def post(self,request,id):
        contact = Contact.objects.get(id=id)
        contact.delete()   
        return redirect('index')
            


