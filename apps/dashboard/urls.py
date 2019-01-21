from django.conf.urls import url
from .import views

app_name='dashboard'

urlpatterns=[
    url(r'^$',views.dashboard, name='dashboard'),
    url(r'^product/(?P<product_id>\w+)/(?P<product_brand>(\w+|\w+(\s\w+)))$',views.product_page, name='product_page'),
    url(r'^checkout/$',views.checkout, name='checkout'),
    url(r'^thankYou/$',views.thankYou, name='thankYou'),
    url(r'^payementProcess/$',views.payementProcess, name='payementProcess'),
    url(r'^add_to_cart$',views.add_to_cart, name='add_to_cart'),
    url(r'^PriceRange/$',views.PriceRange, name='PriceRange'),
    url(r'^searchCategory/(?P<category>\w+)$',views.searchCategory, name='searchCategory'),
    url(r'^searchBrand/$',views.searchBrand, name='searchBrand'),
    url(r'^searchProducts/$',views.searchProducts, name='searchProducts'),
    url(r'^searchAllProducts/$',views.searchAllProducts, name='searchAllProducts'),
    url(r'^lookAtCart/$',views.lookAtCart, name='lookAtCart'),
    url(r'^deleteCartItem/(?P<itemId>\d+)$',views.deleteCartItem, name='deleteCartItem'),
    url(r'^NumberOfItemInCart/$',views.NumberOfItemInCart, name='NumberOfItemInCart'),
    url(r'^removeTags/(?P<tagKey>\w+)$',views.removeTags, name='removeTags')



    

]