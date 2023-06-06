from django.conf import settings

from .models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session   # prende la sessione (informazioni dell'utente, browser, ecc.)
        cart = self.session.get(settings.CART_SESSION_ID)  # controlla se esiste un carrello

        if not cart:  # se non esiste un carrello
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():  # per ogni chiave del carrello (keys)
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)  # prende il prodotto dal database

        for item in self.cart.values():  # per ogni valore del carrello (values)
            item['total_price'] = int(item['product'].price) * int(item['quantity']) / 100  # calcola il prezzo totale
            # il prezzo è in centesimi, quindi lo dividiamo per 100
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())  # ritorna la lunghezza del
        # carrello (numero di prodotti)

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart  # salva il carrello nella sessione
        self.session.modified = True  # fa sapere al server che la sessione è stata modificata

    def add(self, product_id, quantity=1, update_quantity=False):  # aggiunge un prodotto al carrello
        product_id = str(product_id)  # converte l'id del prodotto in stringa

        if product_id not in self.cart:  # se il prodotto non è nel carrello
            self.cart[product_id] = {'quantity': int(quantity), 'id': product_id}  # crea un nuovo prodotto nel carrello

        if update_quantity:  # se la quantità deve essere aggiornata
            self.cart[product_id]['quantity'] += int(quantity)  # aggiorna la quantità del prodotto

        self.save()  # salva il carrello

    def remove(self, product_id):  # rimuove un prodotto dal carrello
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]

            self.save()  # salva il carrello

    def clear(self):  # svuota il carrello
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)  # prende il prodotto dal database

        return sum(int(item['product'].price) * int(item['quantity']) / 100 for item in self.cart.values())  # prende
        # il prezzo di un prodotto e lo moltiplica per la quantità, poi lo somma a tutti gli altri prodotti nel carrello
        # il prezzo è in centesimi, quindi lo dividiamo per 100 e ritorna il prezzo totale come un itero



