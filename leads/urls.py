from django.urls import path
from .views import (
    LeadListView,
    LeadDetailView,

    LeadUpdateView,
    LeadDeleteView,
    AssignAgentView,
    CategoryListView,
    CategoryDetailView,
    LeadCategoryUpdateView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    LeadRegisterView,

    )
app_name="leads"

urlpatterns=[

path('',LeadListView.as_view(), name='lead-list'),
path('<int:pk>/',LeadDetailView.as_view(), name='lead-detail'),
path('<int:pk>/register/',LeadRegisterView.as_view(), name='lead-register'),
path('<int:pk>/update',LeadUpdateView.as_view(), name='lead-update'),
path('<int:pk>/delete',LeadDeleteView.as_view(), name='lead-delete'),

path('<int:pk>/assign-agent/',AssignAgentView.as_view(),name='assign-agent'),



path('categories/',CategoryListView.as_view(),name='category-list'),
path('categories/<int:pk>/',CategoryDetailView.as_view(),name='category-detail'),
path('<int:pk>/category/',LeadCategoryUpdateView.as_view(),name='lead-category-update'),
path('creategories/<int:pk>/update',CategoryUpdateView.as_view(), name='category-update'),
path('create-category/',CategoryCreateView.as_view(), name='category-create'),
path('categories/<int:pk>/delete',CategoryDeleteView.as_view(), name='category-delete'),


]

# using name - its like name given to the url. so where we need to mention this url we can use the name in place of the url.
# /leads/create = lead_create -> without this if we did any change in url we need to chamge the url in every place.
# /leads-YT/create now we need to change this url every where because /leads/create is not same as /leads-YT/create,
# with using name we can just udate at one place and the name value will get updated in every palce.9