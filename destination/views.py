

from typing import Any
from django.shortcuts import reverse
from django.views.generic import (
   ListView,
   CreateView,
   DetailView,
   UpdateView,
   DeleteView)
from agents.mixins import OragniserLoginRequiredMixin

from .models import Destination
from .forms import DestinationForm
from django.conf import settings


# Create your views here.
class DashboardView(ListView):
   template_name="dashboard.html"
   context_object_name="destinations"
   queryset=Destination.objects.all()


class DestinationAddView(OragniserLoginRequiredMixin,CreateView):
   template_name="destination/add_destination.html"
   form_class=DestinationForm
   
   def get_success_url(self):
      return reverse("dashboard")



class DestinationDetail(DetailView):
   template_name="destination/detination_detail.html"
   context_object_name="destination"

   def get_queryset(self):
         pk=self.kwargs["pk"]
         return Destination.objects.filter(pk=pk)


class DestinationUpdate(OragniserLoginRequiredMixin,UpdateView):
      template_name="destination/destination_update.html"
      form_class=DestinationForm

      def get_success_url(self):
         return reverse("dashboard")
      
      def get_queryset(self):
         pk=self.kwargs["pk"]
         return Destination.objects.filter(pk=pk)
   
class DestinationDelete(OragniserLoginRequiredMixin,DeleteView):
   template_name="destination/destination_delete.html"
   
   def get_success_url(self):
      return reverse("dashboard")
   
   def get_queryset(self):
      pk=self.kwargs["pk"]
      return Destination.objects.filter(pk=pk)
   

