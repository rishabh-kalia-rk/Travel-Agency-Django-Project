from django.urls import path
from .views import (
    DestinationAddView,
    DestinationDetail,
    DestinationUpdate,
    DestinationDelete,
    )


app_name="destination"

urlpatterns=[

    path("create/",DestinationAddView.as_view(),name="destination-create"),
    path("<int:pk>/",DestinationDetail.as_view(),name="destination-detail"),
    path("<int:pk>/update/",DestinationUpdate.as_view(),name="destination-update"),
    path("<int:pk>/delete/",DestinationDelete.as_view(),name="destination-delete")
]
