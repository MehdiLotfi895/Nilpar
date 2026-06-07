from django.urls import path ,re_path
from . import views
from main.errors import error_403, error_404, error_405, error_500, error_400
urlpatterns = [
     re_path(
        r'^product/(?P<slug>[-\w\u0600-\u06FF\u200c]+)/$',
        views.Detail.as_view(),
        name='detail'
    ),
    path('login/', views.send_otp, name='send_otp'),
    path('otp/verify/', views.verify_otp, name='verify_otp'),
    path('otp/register/', views.complete_register, name='complete_register'),
    path('', views.Home.as_view(), name='home'),
    # path('product/<slug:slug>/', views.Detail.as_view(), name='detail'),
    path('order/', views.Ordering.as_view(), name='ordering'),
    # path('basket/', views.OrderBasketPage.as_view(), name='orderbasket'),
    path('logout/', views.logout, name='logout'),
    path('add_address_info/',views.add_address,name="add_address"),
    path('editProfile/',views.edit_profile,name="edit_profile"),
    path('test-404/', lambda r: int('not_number')),  # این خطای 500 میده
    path('products/<str:string>/',views.Products.as_view(),name="products"),
    path('products/',views.Products.as_view(),name="products"),
   path(
    'payment-method/<int:order_id>/',
    views.payment_method,
    name='payment_method'
),
path(
    'order-success/<int:order_id>/',
    views.order_success,
    name='order_success'
),
path(
    'orders/',
    views.OrderListView.as_view(),
    name='order_list'
),
path(
    'orders/<int:pk>/',
    views.OrderDetailView.as_view(),
    name='order_detail'
),
path(
    'addresses/',
    views.AddressListView.as_view(),
    name='addresses'
),

path(
    'addresses/<int:pk>/edit/',
    views.AddressUpdateView.as_view(),
    name='address_edit'
),

path(
    'addresses/<int:pk>/delete/',
    views.AddressDeleteView.as_view(),
    name='address_delete'
),

path(
    'favorites/',
    views.FavoriteProductsView.as_view(),
    name='favorite_products'
),
path(
    'favorite/<int:pk>/',
    views.toggle_favorite,
    name='toggle_favorite'
),
path(
    'my-activity/',
    views.UserActivityView.as_view(),
    name='user_activity'
),
 path(
        'blogs/',
        views.BlogListView.as_view(),
        name='blog_list'
    ),

    re_path(
    r'^blogs/(?P<slug>[-\w\u0600-\u06FF\u200c]+)/$',
    views.BlogDetailView.as_view(),
    name='blog_detail'
),
path(
    'payment/start/<int:pk>/',
    views.StartPaymentView.as_view(),
    name='start_payment'
),

path(
    'payment/verify/',
    views.VerifyPaymentView.as_view(),
    name='verify_payment'
),
    path('otp/resend/',views.resend_otp,name='resend_otp'),


]

handler403 = error_403
handler404 = error_404
handler405 = error_405
handler500 = error_500
handler400 = error_400