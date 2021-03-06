from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from django.contrib import admin
from views import shop, checkout, syncsearch, proceedOrder, search_product, add_to_cart, remove_item, update_cart, rate_product, settings, change_pass
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sec_prog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^thisisaverywellhiddenadminpanel/', include(admin.site.urls)),

    url(regex=r'^$',
        view='django.contrib.auth.views.login',
        kwargs={'template_name': 'main.html'},
        name='django.contrib.auth.views.login'),

    url(regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': '/'},
        name='logout'),

    url(regex=r'^shop1/$',
        view=shop,
        name='shop'),

    url(regex=r'^checkout/',
        view=checkout,
        name='checkout'),

    url(regex=r'^proceedOrder/$',
        view=proceedOrder,
        name='proceedOrder'),

    url(regex=r'^searchproduct/$',
        view=search_product,
        name='search_product'),

    url(regex=r'^addToCart/$',
	view=add_to_cart,
	name='add_to_cart'),

    url(regex=r'^remove_item/$',
        view=remove_item,
        name='remove_item'),

    url(regex=r'^update_cart/$',
        view=update_cart,
        name='update_cart'),

    url(regex=r'^rateproduct/$',
        view=rate_product,
        name='rate_product'),

    url(regex=r'^settings/$',
        view=settings,
        name='settings'),

    url(regex=r'^change_pass/$',
        view=change_pass,
        name='change_pass'),

    url(regex=r'^syncsearch/$',
        view=syncsearch,
        name='syncsearch'),




)
