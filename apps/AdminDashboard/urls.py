from django.conf.urls import url
from .import views
from django.conf import settings
from django.conf.urls.static import static


app_name='AdminDashboard'

urlpatterns=[
    url(r'^$',views.admin, name='admin'),
    url(r'^searchOrders/$',views.searchOrders, name='searchOrders'),
    url(r'^viewProduct/(?P<order_id>\w+)$',views.viewProduct, name='viewProduct'),
    url(r'^in_stock/$',views.productsInStock, name='productsInStock'),
    url(r'^searchProduct/$',views.searchProduct, name='searchProduct'),
    url(r'^create/$',views.create, name='create'),
    url(r'^delete/$',views.delete, name='delete'),
    url(r'^edit/$',views.edit, name='edit'),
    url(r'^fetchProductInfo/$',views.fetchProductInfo, name='fetchProductInfo'),
    url(r'^changingProductStatus/$',views.changingProductStatus, name='changingProductStatus'),
    url(r'^makeAdminPage/$',views.makeAdminPage, name='makeAdminPage'),
    url(r'^makeAdminProcess/$',views.makeAdminProcess, name='makeAdminProcess')

    

]
# +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
