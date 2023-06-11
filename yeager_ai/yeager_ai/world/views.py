from django.http import HttpResponse
from django.http import HttpResponse
from django.conf import settings
from .tasks import fetch_data_from_api, run_socket_task, get_data_from_api
from .forms import WorldInstanceForm
from websockets.server import serve
from .models import WorldClass, WorldInstance, Tag
from django.db.models import Q
from django.shortcuts import redirect,  get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, DeleteView, View, FormView, ListView
from asgiref.sync import sync_to_async




'''
 a search view
'''   
def search_view(request):
    # Retrieve the queryset
    query = request.GET.get('search')
    queryset = WorldClass.objects.filter(name__icontains=query)
    
    results = []

    for item in queryset:
   
        result = {
            'slug': item.slug,
            'name': item.name,
            'creator': {
                'first_name': item.creator.first_name,
                'last_name': item.creator.last_name,
                },
            'created_at': item.created_at,
            'thumbnail': item.thumbnail.url,
        }
        
        results.append(result)
 
    
    return JsonResponse(results, safe=False)

def world_navabr(request):
    # Retrieve the queryset
    
    queryset = WorldClass.objects.all()
    
    data = []

    for item in queryset:
   
        result = {
            'slug': item.slug,
            'name': item.name,
            'creator': {
                'first_name': item.creator.first_name,
                'last_name': item.creator.last_name,
                },
            'created_at': item.created_at,
            'thumbnail': item.thumbnail.url,
        }
        
        data.append(result) 
    
    return JsonResponse(data, safe=False)

        
class WorldDetailView(LoginRequiredMixin, DetailView):
    model = WorldClass
    login_url = "/accounts/login"
    template_name = "pages/World/world_details.html"
    context_object_name = 'worlds'
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        return get_object_or_404(queryset, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['worlds'] = self.get_object()
        context["all_objects"] = WorldClass.objects.all()   
        obj = get_object_or_404(WorldClass, slug=self.kwargs.get('slug'))
        context['world_instances'] = WorldInstance.objects.filter(world_class=obj.uuid)
        return context

world_detail_view = WorldDetailView.as_view()


class WorldListView(ListView):
    model = WorldClass
    login_url = "/accounts/login"
    template_name = "pages/World/world.html"
    context_object_name = 'worlds'
    # paginate_by = 10

world_list_view = WorldListView.as_view()

''' get some list of worlds to feature'''
class WorldFeatured(ListView, LoginRequiredMixin):
    model = WorldClass
    context_object_name = 'worlds'
    template_name = "pages/Worlds/featured.html"
    login_url = "/accounts/login"
    queryset = WorldClass.objects.filter(is_public=True)[:5]

world_featured = WorldFeatured.as_view()


'''
rating update
'''
class RateWorldView(View, LoginRequiredMixin):
    def get(self, request, slug):
        world = get_object_or_404(WorldClass, slug=slug)
        world.rate_world(request.user)
        return redirect('worlds:world_list')

rate_world_view = RateWorldView.as_view()

'''
WorldDeleteView: delete a world if only is 
created by the current user
'''
class WorldDeleteView(LoginRequiredMixin, DeleteView):
    model = WorldClass
    success_url = None
    login_url = "/accounts/login"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.creator != request.user:
            messages.error(request, "User Not Permitted")
            return reverse_lazy("world_list")
        self.object.delete()
        messages.success(request, "World Deleted")
        return redirect(reverse_lazy("world_list"))


world_delete_view = WorldDeleteView.as_view()

'''
World Instance Section
'''
def get_data(request):
    socket_url = request.GET.get('socket_url')
    result = fetch_data_from_api.delay(socket_url)
    data = result.get()  # Get the task result
    return HttpResponse(data)

class WorldInstanceFormView(LoginRequiredMixin, FormView):
    form_class = WorldInstanceForm
    success_url = reverse_lazy('worlds:world_plan_list')
    login_url = "/accounts/login"
    template_name = 'pages/world/world_instances.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

'''
World Instance View Details
'''
def get_data(request):
    result = fetch_data_from_api.delay("ws://external-api.com/stream")
    data = result.get()  # Get the task result

    return HttpResponse(data)



class WorldInstanceDetail(LoginRequiredMixin, View):
    template_name = "pages/World/world_instance_event.html"
    login_url = "/accounts/login"
    
    
    def get(self, request, slug):
        world = get_object_or_404(WorldInstance, slug=slug)
        file_path = world.default_preview_file
        '''
        default preview url instance: http://localhost:7456/send-mocked-world-event-stream
        '''
        default_preview_urls = str(world.default_preview_urls)
        socket_urls = str(world.socket_url)
        get_data_from_api.delay(socket_urls)
        with open(file_path, "r") as f:
            mocked_world_event_stream = {"data": f.read()}
        run_socket_task.delay(mocked_event_file=mocked_world_event_stream, default_preview_urls=default_preview_urls)

        context = {
            "world_instance": world,
        }
        return render(request, self.template_name, context)

world_instance_detail_view = WorldInstanceDetail.as_view()


class WorldInstanceListView(LoginRequiredMixin, ListView):
    model = WorldInstance
    template_name = "pages/world/world_instance_lists.html"
    context_object_name = 'world_instances'
    login_url = "/accounts/login"
    paginate_by = 50
    queryset = WorldInstance.objects.filter(is_public=True)


world_instance_list_view = WorldInstanceListView.as_view()

'''
A class world instance to delete a world
Note: deletion is restricted to the user that created the world
'''
class WorldInstanceDeleteView(LoginRequiredMixin, DeleteView):
    model = WorldInstance
    login_url = "/accounts/login"
    success_url = reverse_lazy("worlds:world_instance_list")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(queryset, uuid=uuid)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.creator != request.user:
            messages.error(request, "User Not Permitted")
            return reverse_lazy("worlds:world_instance_list")
        self.object.delete()
        messages.success(request, "Instance Deleted")
        return redirect(reverse_lazy("worlds:world_instance_list"))
    
world_instance_delete_view = WorldInstanceDeleteView.as_view()

'''
Tag Modules
'''
class TagCreateView(LoginRequiredMixin, View):
    template_name = "agents/create_agents.html"
    login_url = "/accounts/login"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        tag = Tag.objects.create(name=name, description=description)
        if tag:
            messages.success(request, "Tag created")
            return redirect("tag_list")
        else:
            messages.error(request, "Something Went Wrong")
            return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


tag_create_view = TagCreateView.as_view()

""" 
Tag details view
"""
class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = "pages/Tag/tag_detail.html"
    login_url = "/accounts/login"

tag_detail_view = TagDetail.as_view()

""" 
Tag get all tag
"""
class TagListView(ListView):
    model = Tag
    template_name = "pages/Tag/tag_lists.html"
    context_object_name = 'tag_list'
    paginate_by = 50

tag_list_view = TagListView.as_view()

""" 
Tag deletion class based view
"""
class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy("tag_list")
    login_url = "/accounts/login"
    
tag_delete_view = TagDeleteView.as_view()