from django import forms
from .models import WorldClass, WorldInstance, Category


class SearchForm(forms.ModelForm):
    class Meta:
        model = WorldClass
        fields= ('name',)
        
        

class WorldForm(forms.ModelForm):
    class Meta:
        model = WorldClass
        fields = ("creator",
                  "name",
                  "description",
                  "thumbnail",
                  "is_public",
                  "is_active",
                  "category",
                  "tags",
                  "agent_classes",
                  "object_classes",
                  "docker_path",
                  "user_interactions",
                  "world_outputs",)

    def clean_name(self):
        name = self.cleaned_data['name']
        if WorldClass.objects.filter(name=name).exists():
            raise forms.ValidationError('world exists')
        return name


class WorldInstanceForm(forms.ModelForm):
    class Meta:
        model = WorldInstance
        fields = (
            'user',
            'world_class',
            'name',
            'is_public',
            'description',
            'status',
            'is_running',
            'is_test',
            'tags',
            'bit16_url',
            'default_preview_urls',
            'default_preview_file',
            'socket_url',
            'api_key',
            'total_ml_cost',
            'total_cloud_cost',
            'total_memory_cost',
            'total_external_tool_cost',
            'shutdown_cost',)

    def clean_name(self):
        name = self.cleaned_data['name']
        if WorldClass.objects.filter(name=name).exists():
            raise forms.ValidationError(
                f'world exists under the category {name} exist')
        return name
