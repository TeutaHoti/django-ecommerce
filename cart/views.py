from django.shortcuts import render, get_object_or_404
from .models import *
from products.models import Product
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def cart_add(request, product_id):
    cart_id = request.session.get("cart_id")
    
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
            
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, porduct=product)
        
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        
        response_data = {
            "success":True,
            "message":f"added {product.name} to cart "
        }
        
        return JsonResponse(response_data)
    
def cart_detail(request):
    cart_id = request.session.get('cart_id')
    cart = None
    
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        
    return render(request, 'cart/detail.html',{'cart':cart})
# Create your views here.
