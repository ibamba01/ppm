from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect # redirect serve per reindirizzare l'utente
# verso un'altra pagina, get_object_or_404 serve per prendere un oggetto dal database
# o dare un errore 404 se non esiste, render serve per renderizzare un template
from django.contrib.auth.decorators import login_required

from .cart  import Cart   # importa il carrello dal file cart.py
from .forms import OrderForm  # importa il form ProductForm dal file forms.py
from .models import Product, Category  # importa il modello Product dal file models.py
from .models import Order, OrderItem

def add_to_cart(request, product_id,):
    cart = Cart(request)  # crea un nuovo carrello
    cart.add(product_id)  # aggiunge il prodotto al carrello

    return redirect("cart_view")  # reindirizza l'utente verso la pagina frontpage

def remove_from_cart(request, product_id):
    cart = Cart(request)  # crea un nuovo carrello
    cart.remove(product_id)  # rimuove il prodotto dal carrello

    return redirect("cart_view")  # reindirizza l'utente verso la pagina frontpage

def change_quantity(request, product_id,):
    action = request.GET.get("action", '')
    cart = Cart(request)  # crea un nuovo carrello
    if action:
        quantity = 1
        if action == "decrease":
            quantity = -1
        cart.add(product_id, quantity, True)
    return redirect("cart_view")

def cart_view(request):
    cart = Cart(request)  # crea un nuovo carrello

    return render(request, "cart_view.html", {"cart": cart})

@login_required
def checkout(request):
    cart = Cart(request)  # crea un nuovo carrello

    if request.method == "POST":  # se il metodo è POST
        form = OrderForm(request.POST)  # prende i dati dal form

        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item["product"]
                total_price += product.price * int(item["quantity"])


            order = form.save(commit=False)  # crea un nuovo ordine ma non lo salva nel database
            order.created_by = request.user  # assegna l'utente all'ordine
            order.paid_amount = cart.get_total_cost()  # assegna il totale dell'ordine
            order.save()  # salva l'ordine nel database

            for item in cart:
                product = item["product"]
                quantity = int(item["quantity"])
                price = product.price * quantity
                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)


            cart.clear()  # svuota il carrello

            return redirect("myaccount")


    else:
      form = OrderForm()  # prende i dati dal form

    return render(request, "checkout.html", {"cart": cart, "form": form,})


def search(request):
    query = request.GET.get("query", "")
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
# il Q serve per fare una query su più campi, in questo caso title e description

    return render(request, "search.html", {"query": query, "products": products})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()  # prendi tutti i prodotti della categoria

    return render(request, "category_detail.html", {"category": category, "products": products})

def product_detail(request, category_slug, slug):
    cart = Cart(request)  # crea un nuovo carrello

    print(cart.get_total_cost())
    product = get_object_or_404(Product, slug=slug)  # matcha la slug del prodoto
# con la slug del url e fa aprire la pagina, se non la trova da errore 404
    return render(request, "product_detail.html", {"product": product})
