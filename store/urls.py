from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.store, name='store'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),

    path('update_item/', views.updateItem, name='updateItem'),
    path('process_order/', views.processOrder, name='processOrder'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
