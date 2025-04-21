"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import KrogerFoodView, search_items, home_page, add_item, get_items, delete_item
# from .views import KrogerFood

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    # path('products/', KrogerFoodView, name='kroger-products'),

    path('generate-items/', search_items, name='search_items'),
    # path('get-access-token/', views.KrogerFood, name='KrogerFood'),
    path("add-item/", add_item),
    path("get-items/", get_items),
    path("delete-item/<int:item_id>/", delete_item),




]
