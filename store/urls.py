from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path

class CustomLogoutView(LogoutView):
    template_name = 'templates/custom_logout.html'  # Use your custom template
    next_page = '/'  # Redirect to a specific page after logout

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='custom_logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('products/', views.product_list, name='product_list'),
    path('login/', views.user_login, name='login'),
    path('add_product/', views.add_product, name='add_product'),
    path('order_history/', views.order_history, name='order_history'),
    # path('cart/', views.cart, name='cart'), ## <== add decorater to the views
    path('checkout/', views.checkout, name='checkout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)