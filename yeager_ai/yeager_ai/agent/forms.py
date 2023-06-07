from django import forms
from .models import AgentClass


class AgentForm(forms.ModelForm):
    class Meta:
        model = AgentClass
        fields = (
            'name',
            'description',
            'avatar',
            'tags',
            'memories',
            'tools',
            'is_public',
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        if AgentClass.objects.filter(name=name).exists():
            raise forms.ValidationError('agent exists')
        return name
