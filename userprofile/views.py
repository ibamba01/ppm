from django.contrib.auth import login  # login serve per loggare l'utente
from django.contrib.auth.decorators import login_required  # login_required serve per dire che per accedere a questa
# pagina bisogna essere loggati
from django.contrib.auth.forms import UserCreationForm
# UserCreationForm è un form che permette di creare un nuovo utente
from django.contrib.auth.models import User
from django.shortcuts import render, redirect  # redirect serve per reindirizzare l'utente verso un'altra pagina
from django.utils.text import slugify  # slugify serve per creare uno slug

from .models import Userprofile

from store.forms import ProductForm
from store.models import Product, Category, OrderItem, Order


def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)

    return render(request, "vendor_detail.html", {"user": user})
@login_required
def my_store(request):
    return render(request, "mystore.html")

@login_required  # alla fine non implementiamo questa funzione
def create_product(request):  # questa funzione serve per creare un nuovo prodotto
    form = ProductForm()   # crea un nuovo form vuoto

    if request.method == "POST":  # se il metodo è POST
        form = ProductForm(request.POST, request.FILES)  # prende i dati dal form

        if form.is_valid():  # se il form è valido
            title = request.POST.get("title")  # prende il titolo dal form

            product = form.save(commit=False)  # crea un nuovo prodotto ma non lo salva nel
            # database perché non ha la chiave primaria
            product.user = request.user  # assegna l'utente al prodotto
            product.slug = slugify(title)  # crea lo slug
            product.save()  # salva il prodotto nel database

            return redirect("my_store")  # reindirizza l'utente verso la pagina my_store
        else:
            form = ProductForm()

    return render(request, "create_product.html", {"form": form})

#@login_required
#def edit_product(request, pk):
 #   product = Product.objects.filter(user=request.user).get(pk=pk)

  #  form = ProductForm()

  #  return render(request, "edit_product.html", {"form": form, "product": product})

@login_required
def myaccount(request):
    return render(request, "myaccount.html")

@login_required
def ordini(request):
    orders_items = OrderItem.objects.filter(order__created_by=request.user)

    return render(request, "ordini.html", {"orders_items": orders_items})


def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect("frontpage")  # reindirizza l'utente verso la pagina frontpage
        else:
            form = UserCreationForm()  # se il form non è valido, manda alla creazione

    return render(request, "signup.html", {
        "form": form
    })
