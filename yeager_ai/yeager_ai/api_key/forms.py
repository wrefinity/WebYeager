from django import forms
from .models import ApiKey


class ApiKeyForm(forms.ModelForm):
    class Meta:
        model = ApiKey
        fields = ('user',
                  'key',
                  'description',
                  'is_active')

    def clean_key(self):
        # - generate the key
        key = self.cleaned_data['key']
        if ApiKey.objects.filter(key=key).exists():
            raise forms.ValidationError('api key exists')
        return key
