# home/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('homepage/', views.homepage_view, name='homepage'),
    path('products/', views.products_view, name='products'),
    path('collections/', views.collections_view, name='collections'),
    path('contact/', views.contact_view, name='contact'),
    path('details/<int:id>' ,views.details,name= "details"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),  
    path('cart/update/<int:product_id>/<str:action>/', views.update_cart_quantity, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)