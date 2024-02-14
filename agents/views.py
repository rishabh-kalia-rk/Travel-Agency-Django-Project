
from django.shortcuts import reverse,redirect
from django.views import generic

from leads.models import Agent
from .forms import AgentModelForm
from django.core.mail import send_mail
from .mixins import OragniserLoginRequiredMixin

import random 




from leads.models import Lead
from datetime import datetime
import datetime


# Create your views here.
class AgentListView(OragniserLoginRequiredMixin,generic.ListView):
    template_name="agents/agent_list.html"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        # userprofile: Accesses the related UserProfile instance of the currently logged-in user.
       
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OragniserLoginRequiredMixin,generic.CreateView):
    template_name="agents/agent_create.html"
    form_class=AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f"{random.randint(0,1000000)}")
        user.agent_full_name=f"{user.first_name} {user.last_name}"
        user.save()

        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        # create and save the instance to database.
        send_mail(
            subject="you are invited to be an agent",
            message="you were added as an agent on RK World site. Please come and login to satrt.",
            from_email="admin@test.com",
            recipient_list=[user.email]

        )
        return super(AgentCreateView,self).form_valid(form)
    
class AgentDetailView(OragniserLoginRequiredMixin,generic.DetailView):
    template_name="agents/agent_detail.html"
    context_object_name="agent"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    
       
    

class AgentUpdateView(OragniserLoginRequiredMixin,generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    model=Agent
        
    
    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_object(self, queryset=None):
        # Retrieve the instance of Model1 based on the URL parameter
        return Agent.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent_instance = self.object

        # Initialize the form with the instance of the User model
        form = AgentModelForm(instance=agent_instance.user)

        # Add the form to the context
        context['form'] = form

        return context
    
    def form_valid(self, form):
  
        agent_instance = form.save(commit=False)

        # Get the associated User instance
        user_instance = agent_instance.user

        # Update only the fields mentioned in the form data
        for field, value in form.cleaned_data.items():
            setattr(user_instance, field, value)
        
        user_instance.agent_full_name=f"{user_instance.first_name} {user_instance.last_name}"

        # Save the updated User instance
        user_instance.save()
        
        agent_instance.save()

        return redirect(reverse("agents:agent-list"))
    


class AgentDeleteView(OragniserLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        return Agent.objects.filter(id=pk)


class AgentHistoryView(OragniserLoginRequiredMixin,generic.TemplateView):
    template_name="agents/agent_history.html"
 
    def get_context_data(self, **kwargs):
        context=super(AgentHistoryView,self).get_context_data(**kwargs)
  
        pk = self.kwargs.get('pk')
        Total_leads=Lead.objects.filter(agent_id=pk).count()


        thirty_days_ago=datetime.date.today()-datetime.timedelta(days=30)
        total_in_past30=Lead.objects.filter(agent_id=pk,date_added__gte=thirty_days_ago).count()

        context.update({
            "total_lead_count": Total_leads,
            "total_in_past30": total_in_past30,
            "agentref":pk
        })
        return context
    def get_success_url(self):
        return reverse("agents:agent-list")

    
   