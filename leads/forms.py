
from django import forms
from .models import Lead,Agent,Category

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UsernameField


from destination.models import Destination

User=get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model=Lead
        fields= (
        'first_name',
        'last_name',
        'age',
        'agent',
        'destination',
        'phone_number',
        'email',
        'profile_picture'
                )
    def __init__(self, *args, **kwargs):
       
        if 'curr_destination_id' in kwargs:
            curr_destination_id2 = kwargs.pop('curr_destination_id')
            super(LeadModelForm, self).__init__(*args, **kwargs)

            # To assign the destination
            destination_instance = Destination.objects.filter(id=curr_destination_id2).first()
            self.fields['destination'].initial = destination_instance.place_name if destination_instance else None

            # dynamically add the choice filed.
            filtered_users = User.objects.filter(destination_assign_id=curr_destination_id2)
            filtered_agents = [user.agent for user in filtered_users if user.agent]

            self.fields['agent'].queryset = Agent.objects.filter(pk__in=[agent.pk for agent in filtered_agents])
        else:
            super(LeadModelForm, self).__init__(*args, **kwargs)
        
      

class LeadForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    age=forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username",)
        field_Classes={'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent=forms.ModelChoiceField(queryset=Lead.objects.none())

    def __init__(self, *args, **kwargs):
    
      
        # this is to find the lead and its destination
        pk=kwargs.pop("pk")
        desti_check=Lead.objects.filter(id=pk).first()
        name=desti_check.destination

        # now we have the name of the destination and dron destination table i will get the id of the destination

        desti_id_check=Destination.objects.filter(place_name=name).first()
        id_check=desti_id_check

        # now i will filter out the agents to which above specific destination was assigned.

                

        super(AssignAgentForm, self).__init__(*args, **kwargs)
        filtered_users = User.objects.filter(destination_assign_id=id_check)
        filtered_agents = [user.agent for user in filtered_users if user.agent]

        self.fields['agent'].queryset = Agent.objects.filter(pk__in=[agent.pk for agent in filtered_agents])


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields={
            'category'
        }

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=(
            'name',

        )
