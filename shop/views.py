from .models import Product  
from django.shortcuts import render 
from .models import Product
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def product_page(request):
    all_products = Product.objects.all()
    context = {
        'products': all_products
    }
    return render(request, 'shop/products.html', context)

def homepage_view(request):
    all_products = Product.objects.all()  
    context = {
        'products': all_products
    }
    return render(request, 'shop/homepage.html', context)

def products_view(request):
    category = request.GET.get('category', None)
    search_query = request.GET.get('search', None)
    
    # Get all categories for the filter dropdown
    all_categories = Product.objects.values_list('category', flat=True).distinct()
    
    # Filter products based on category if provided
    if category:
        products = Product.objects.filter(category=category)
    elif search_query:
        # Filter products based on search query
        products = Product.objects.filter(product_name__icontains=search_query)
    else:
        # Otherwise get all products
        products = Product.objects.all()
    
    context = {
        'products': products,
        'categories': all_categories,
        'selected_category': category,
        'search_query': search_query
    }
    return render(request, 'shop/products.html', context)

def collections_view(request):
    # Get all unique categories
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    # Create a dictionary to store products by category
    collections = {}
    
    # Get featured products for each category (up to 4 per category)
    for category in categories:
        collections[category] = Product.objects.filter(category=category)[:4]
    
    context = {
        'collections': collections,
        'categories': categories,
    }
    
    return render(request, 'shop/collections.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Form validation
        if not all([name, email, message]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'shop/contact.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            })
        
        # Handle the contact form submission
        contact_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        
        # Save to database or send email (email functionality would go here)
        try:
            # Uncomment when email is configured in settings.py
            # send_mail(
            #     subject or "Contact from RAW REBEL Website",
            #     contact_message,
            #     email,
            #     [settings.DEFAULT_FROM_EMAIL],
            #     fail_silently=False,
            # )
            
            messages.success(request, "Your message has been sent. We'll get back to you soon!")
            return redirect('contact')
        except Exception as e:
            messages.error(request, f"There was an error sending your message. Please try again later.")
            
    return render(request, 'shop/contact.html')

def details(request, id):
  Product_details = Product.objects.get(id=id)
  template = loader.get_template('shop/detail.html')
  context = {
    'product': Product_details 
  }
  return HttpResponse(template.render(context, request)) 

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    }) 
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('/cart/')


# Increment/Decrement
def update_cart_quantity(request, product_id, action):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if action == 'increment':
            cart[product_id] += 1
        elif action == 'decrement':
            if cart[product_id] > 1:
                cart[product_id] -= 1
            else:
                del cart[product_id]  # remove if quantity is 1 and user clicks '-'

    request.session['cart'] = cart
    return redirect('cart')  # Make sure your cart URL is named 'cart'

# Remove Product
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'shop/signup.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')  # or 'cart' or wherever you want
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'shop/login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')