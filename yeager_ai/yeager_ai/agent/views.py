from django.http import JsonResponse
from yeager_ai.agent.models import AgentClass
from django.contrib import auth, messages
from yeager_ai.agent.forms import AgentForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, DeleteView, View, ListView, TemplateView


def agent_navbar(request):
    # Retrieve the queryset
    
    queryset = AgentClass.objects.all()
    
    agent_data = []

    for item in queryset:
   
        result = {
            'slug': item.slug,
            'name': item.name,
            'created_at': item.created_at,
            'avatar': item.avatar.url,
        }
        
        agent_data.append(result)
    
    return JsonResponse(agent_data, safe=False)


'''
rating update
'''
class RateAgentView(View):
    def get(self, request, slug):
        agent = get_object_or_404(AgentClass, slug=slug)
        agent.rate_agent(request.user)
        return redirect('agents:agent_list')

rate_agent_view = RateAgentView.as_view()

'''
agent create view
'''
class AgentCreateView(LoginRequiredMixin, TemplateView):
    model = AgentClass
    template_name = "agents/create_agents.html"
    form_class = AgentForm
    success_url = reverse_lazy('agents:agent_list')
    login_url = "/accounts/login"

    def form_valid(self, form):
        form.save()
        return super(AgentCreateView).form_valid(form)


agents_create_view = AgentCreateView.as_view()
'''
agent tab
'''
class AgentTabView(LoginRequiredMixin, TemplateView):
    template_name = "pages/Agent/agent_tab.html"


agents_tab_view = AgentTabView.as_view()

'''
a class to get all the agents
'''


class AgentListView(ListView):
    model = AgentClass
    template_name = "pages/Agent/agent.html"
    context_object_name = 'agents'


agents_list_view = AgentListView.as_view()


'''
get the details of an agent
'''
class AgentDetailView(DetailView):
    model = AgentClass
    template_name = "pages/Agent/agent_details.html"

        
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug') 
        return get_object_or_404(queryset, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        context['agent'] = get_object_or_404(AgentClass, slug=self.kwargs['slug'])
        context["all_objects"] = AgentClass.objects.all()   
        
        return context


agents_detail_view = AgentDetailView.as_view()


'''
deleting an agent
'''


class AgentDeleteView(DeleteView):
    model = AgentClass
    success_url = reverse_lazy("agents:agent_user")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        return get_object_or_404(queryset, slug=slug)
    
agent_delete_view = AgentDeleteView.as_view()

'''
get agents current logged-in user
'''


class MyAgentView(LoginRequiredMixin, TemplateView):
    template_name = "pages/agents/agent_list.html"
    login_url = login_url = "/accounts/login"
    context_object_name = "agent_list"

    def get_context_data(self, **kwargs):
        context = super(MyAgentView, self).get_context_data(**kwargs)
        context["agents"] = get_object_or_404(
            MyAgentView, user=self.request.user)
        return context


api_my__agent_view = MyAgentView.as_view()