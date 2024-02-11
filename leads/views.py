from typing import Any

from django.shortcuts import render, redirect,reverse
from django.core.mail import send_mail

from .models import Lead, Agent,Category
from .forms import ( LeadModelForm,
                    LeadCategoryUpdateForm,
                    CustomUserCreationForm,
                    AssignAgentForm,
                    CategoryModelForm,                           
)
from django import forms

from django.db.models import Q

from django.contrib import messages
from django.views.generic import (TemplateView,ListView,
UpdateView,DeleteView,DetailView,CreateView,FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OragniserLoginRequiredMixin

from destination.models import Destination

import datetime

# Create your views here.

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")



class LandingPageView(TemplateView):
   template_name="landing.html"

   def dispatch(self, request,*args,**kwargs):
      if request.user.is_authenticated:
         return redirect("dashboard")
      return super().dispatch(request,*args,**kwargs)

def landing_page(request):
#    return render(request,'landing.html')
   return render(request,'landing.html')

def home_page(request):    
    return render (request,"leads/home_page.html")




class LeadListView(LoginRequiredMixin,ListView):
   template_name="leads/lead_list.html"
   context_object_name="leads"

   def get_queryset(self):
      user=self.request.user
     
      if user.is_organisor:
            queryset = Lead.objects.all()
            
      else:
            queryset = Lead.objects.filter(
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
      return queryset
   
   def get_context_data(self,**kwargs):
      context=super(LeadListView,self).get_context_data(**kwargs)
      user=self.request.user
      if user.is_organisor:
         queryset=Lead.objects.filter( agent__isnull=True)
         context.update({
            "unassigned_leads":queryset, 
         })
      else:
         finag=Agent.objects.filter(user_id=user.id).first()
         usid=finag.id
   
         context.update({
            "usid":usid 
         })
  
      return context
   

class LeadDetailView(LoginRequiredMixin,DetailView):
   template_name="leads/lead_detail.html"
   context_object_name="lead"
   #it will autometically pickup the obectt for id=pk.

   def get_queryset(self):
      destination_pk = self.kwargs['pk']
      # Filter the Destination queryset based on the destination_pk
      queryset = Lead.objects.filter(id=destination_pk)
      return queryset




class LeadRegisterView(CreateView):
   template_name="leads/lead_register.html"
   form_class=LeadModelForm
   context_object_name="destination"


   def get_success_url(self):
        return reverse("dashboard")
   
   def form_valid(self,form):
      lead = form.save(commit=False)
      # Get the destination_pk from the URL
      destination_pk = self.kwargs['pk']
      # Filter the Destination queryset based on the destination_pk
      destination = Destination.objects.get(id=destination_pk)

      lead.destination = destination.place_name
      lead.save()
      message = "You are now registered for {} trip destination".format(destination.place_name)


      send_mail(
         subject="Registration completed",
          message=message,
         from_email="test@test.com",
         recipient_list=["test2@test2.com"]
      )
      return super(LeadRegisterView, self).form_valid(form)

   def get_context_data(self, **kwargs):
      context = super(LeadRegisterView, self).get_context_data(**kwargs)
      destination_pk = self.kwargs['pk']
      # Retrieve data from the database, for example
      destination = Destination.objects.get(id=destination_pk)
      queryset_data= destination.place_name
      context.update({'curr_destination':queryset_data})
      return context
   
   def get_form_kwargs(self):
      kwargs = super(LeadRegisterView, self).get_form_kwargs()
      kwargs['curr_destination_id'] = self.kwargs['pk']  # Pass the curr_destination to the form
      return kwargs

class LeadUpdateView(LoginRequiredMixin
,UpdateView):
   template_name="leads/lead_update.html"
   form_class=LeadModelForm
   model=Lead

   def get_success_url(self):
      return reverse("leads:lead-list")

   def get_queryset(self):
      lead_pk = self.kwargs['pk']
      return Lead.objects.filter(id=lead_pk)
   
   def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)

   
   def get_form(self, form_class=None):
      form = super(LeadUpdateView, self).get_form(form_class) 
      # if 'agent' in self.fields:

      previous_instance = self.get_object()

      # Access the value of a specific field from the previous instance
      find_category = previous_instance.category_id

      check_Category=Category.objects.filter(id=find_category).values('name').first()
      if check_Category and check_Category["name"] == "Completed":
         form.fields['first_name'].widget.attrs['disabled'] = True
         form.fields['last_name'].widget.attrs['disabled'] = True
         form.fields['phone_number'].widget.attrs['disabled'] = True


      form.fields['agent'].widget.attrs['disabled'] = True
      form.fields['agent'].help_text = 'This field is not editable.'

      form.fields['destination'].widget.attrs['readonly'] = True
      form.fields['destination'].help_text = 'This field is not editable.'

      return form





class LeadDeleteView(OragniserLoginRequiredMixin
,DeleteView):
   template_name="leads/lead_delete.html"

  
   def get_success_url(self):
      return reverse("leads:lead-list")
   def get_queryset(self):
      lead_delete_pk = self.kwargs['pk']
      return Lead.objects.filter(id=lead_delete_pk)
   
    

   



class AssignAgentView(OragniserLoginRequiredMixin,FormView):
   template_name="leads/assign_agent.html"
   form_class=AssignAgentForm
   
   def get_form_kwargs(self,**kwargs):
      kwargs=super(AssignAgentView,self).get_form_kwargs(**kwargs)
      pk = self.kwargs.get('pk')
      kwargs.update({
         # "request":self.request,
         "pk":pk
      })
      return kwargs
  

   def get_success_url(self):
      return reverse("leads:lead-list")

   def form_valid(self,form):
      agent=form.cleaned_data["agent"]
      lead=Lead.objects.get(id=self.kwargs["pk"])
      lead.agent=agent
      lead.save()
      return super(AssignAgentView,self).form_valid(form)



class CategoryListView(LoginRequiredMixin,ListView):
   template_name ="leads/category_list.html"
   context_object_name="category_list"
   def get_queryset(self):
      user=self.request.user
      if user.is_organisor:
         queryset=Category.objects.filter(organisation=user.userprofile)
      else:
         queryset=Category.objects.filter(organisation=user.agent.organisation)
      return queryset
   
   
   
   def get_context_data(self, **kwargs: Any):
      context=super(CategoryListView,self).get_context_data(**kwargs)
      queryset=Lead.objects.all()
   
      context.update({
         "Completed":queryset.filter(category__name='Completed').count(),
         "NotCompleted":queryset.filter(Q(category_id=2) | Q(category__isnull=True)).count()

      })
      return context
      


class CategoryDetailView(LoginRequiredMixin,DetailView):
   template_name="leads/category_detail.html"
   content_object_name="category"


   def get_queryset(self):
      user=self.request.user
      if user.is_organisor:
         queryset=Category.objects.filter(organisation=user.userprofile)
      else:
         queryset=Category.objects.filter(organisation=user.agent.organisation)
      return queryset
  

class LeadCategoryUpdateView(LoginRequiredMixin,UpdateView):
   template_name="leads/lead_category_update.html"
   form_class=LeadCategoryUpdateForm

   def get_success_url(self):
      return reverse("leads:lead-detail", kwargs={"pk":self.get_object().id})

   def get_queryset(self):
      user=self.request.user
      pk = self.kwargs.get('pk')
      if user.is_organisor:
         queryset=Lead.objects.filter(id=pk)
      else:
         queryset=Lead.objects.filter(id=pk)
      return queryset
   
   def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Completed")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)


   def get_form(self, form_class=None):
      form = super(LeadCategoryUpdateView, self).get_form(form_class) 
      previous_instance = self.get_object()

      # Access the value of a specific field from the previous instance
      find_category = previous_instance.category_id
    
      check_Category=Category.objects.filter(id=find_category).values('name').first()
      if check_Category and check_Category["name"] == "Completed":
         form.fields['category'].widget.attrs['disabled'] = True
      return form
         

class CategoryCreateView(LoginRequiredMixin,CreateView):
   template_name="leads/category_create.html"
   form_class=CategoryModelForm


   def get_success_url(self):
        return reverse("leads:category-list")

   def form_valid(self,form):
      category=form.save(commit=False)
      category.organisation=self.request.user.userprofile
      category.save()
      return super(CategoryCreateView,self).form_valid(form)

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
   template_name="leads/category_update.html"
   form_class=CategoryModelForm


   def get_success_url(self):
        return reverse("leads:category-list")


   
   def get_queryset(self):
      user=self.request.user
      if user.is_organisor:
         queryset=Category.objects.filter(organisation=user.userprofile)
      else:
         queryset=Category.objects.filter(organisation=user.agent.organisation)
      return queryset
   
    
  
  

class CategoryDeleteView(OragniserLoginRequiredMixin
,DeleteView):
   template_name="leads/category_delete.html"

  
   def get_success_url(self):
      return reverse("leads:category-list")
   
   def get_queryset(self):
      user=self.request.user
      if user.is_organisor:
         queryset=Category.objects.filter(organisation=user.userprofile)
      else:
         queryset=Category.objects.filter(organisation=user.agent.organisation)
      return queryset
   



