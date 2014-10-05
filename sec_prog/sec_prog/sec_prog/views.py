from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from shop.models import Shop, Cart, User_Votes
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import get_template
import json
import re


@login_required(login_url='/')
def shop(request):
    products = Shop.objects.all()
    return render_to_response('shop.html', {'products': products}, context_instance=RequestContext(request))


@login_required(login_url='/')
def checkout(request):
    cart_products = Cart.objects.filter(user_id=request.user.id)
    cart = []
    # for i in range(len(cart_products)):
    #     cart.append(cart_products[i].item_id)
    # all_products = Shop.objects.filter(id__in=cart)
    user_cart = [[ 0 for i in xrange(4)] for x in xrange(len(cart_products))]
    total_cost = 0
    for i in range(len(cart_products)):
        user_cart[i][0] = cart_products[i].qnty
        tmp = Shop.objects.get(id=cart_products[i].item_id)
        user_cart[i][1] = tmp.product_name
        user_cart[i][2] = tmp.price
        user_cart[i][3] = cart_products[i].item_id
        total_cost = total_cost + (tmp.price*cart_products[i].qnty)
        #user_cart[i].product_name = all_products[i].product_name
        # user_cart[i].price = all_products[i].price
        # user_cart[i].quantity = cart_products[
    # with open("/home/kirios/Desktop/test.txt", "a") as myfile:
    #     myfile.write(str(all_products))
    return render_to_response('checkout.html',{'products': user_cart, 'total_cost':total_cost}, context_instance=RequestContext(request))


@login_required
def logout_view(request):
    logout(request)

@login_required(login_url='/')
def proceedOrder(request):
    test = []
    products = []
    username = None
    username = request.user.username
    delivery_address = request.POST.get('delivery_address', '')
    #Get Post length so we can iterate through the array
    length = request.POST.get('length', '')
    #iterate through the array and store the product to the array "products"
    for i in range(int(length)):
        test.append(request.POST.getlist("product_array[" + str(i) + "][]"))
        if Shop.objects.filter(pk=int(test[i][2])).exists():
            products.append(Shop.objects.get(pk=int(test[i][2])))
    #Send Email
    mail_template = get_template('email.html')
    c = RequestContext(request, {'products': products, 'address': delivery_address, 'username': username})
    send_mail('Report', mail_template.render(c), 'console@exapmple.com',
              ['admin@example.com'], fail_silently=False)
    #Continue with ajax
    response_data = {}
    try:
        response_data['result'] = 'Writing the blog was a success!'
        response_data['message'] = 'Your order has been sent'
    except:
        response_data['result'] = 'Oh noes!'
        response_data['message'] = 'The subprocess module did not run the script correctly!'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/')
def search_product(request):
    products = []
    search_input = request.POST.get('search_input', '')
    try:
        products = Shop.objects.filter(product_name__icontains=search_input)
    except:
        products = None
    response_data = {}
    product_array = []
    for i in range(len(products)):
        product_array.append([re.escape(products[i].product_name), products[i].price, products[i].pk])
    try:
        response_data = {'result': 'Writing the blog was a success', 'message': product_array, 'array_length': len(products)}
    except:
        response_data = {'result': 'Oh noes', 'message': 'The subprocess module did  not run the script correctly', 'array_length': 0}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/')
def add_to_cart(request):
    userID = request.user.id
    itemID = int(request.POST.get('itemID', 0))
    quantity = int(request.POST.get('qnty', 0))
    try:
        item = Shop.objects.get(id=itemID)
    except:
        item = None

    cart = []
    try:
    #if len(Cart.objects.all()) > 0:
        cart = Cart.objects.get(item_id=itemID)
    except Cart.DoesNotExist:
        cart = None
    if not cart:
        cart = Cart(user_id=userID, item_id=itemID, qnty=quantity, total_price=item.price   )
    else:
        cart.qnty=cart.qnty+quantity
    cart.save()
    response_data = {}


    try:
        response_data['result'] = 'Ok'
    except:
        response_data['result'] = 'not ok'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/')
def remove_item(request):
    userID = request.user.id
    itemID = int(request.POST.get('itemID', ''))
    total_cost = float(request.POST.get('total_cost', ''))
    product_price = float(request.POST.get('product_price', ''))
    qnty = int(request.POST.get('qnty', ''))
    total_cost = total_cost - (product_price*float(qnty))
    try:
        Cart.objects.filter(item_id=itemID,user_id=userID).delete()
    except:
        la=1
    response_data = {}
    response_data['total_cost'] = total_cost
    try:
        response_data['result'] = 'Ok'
    except:
        response_data['result'] = 'not ok'
    return HttpResponse(json.dumps(response_data), content_type="application/json")