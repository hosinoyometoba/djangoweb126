from django.conf.urls import url
from . views import usersviews,typesviews

urlpatterns = [
    url(r'^$',usersviews.index,name="selfadmin_index"),
    url(r'^ulist/$',usersviews.ulist,name="selfadmin_ulist"),
    url(r'^add/$',usersviews.add,name="selfadmin_add"),
    url(r'^delete/$',usersviews.delete,name="selfadmin_delete"),
    url(r'^edit/$',usersviews.edit,name="selfadmin_edit"),
    url(r'^insert/$',usersviews.insert,name="selfadmin_insert"),
    url(r'^type/list/$', typesviews.list,name="selfadmin_list")
]