from django.test import TestCase
from yeager_ai.users.models import User
from django.urls import reverse
from ..models import Tag, AgentClass
from yeager_ai.world.models import Memory, ObjectClass

'''
1. create agent items
2. check the existence of created agent
4. delete an agent
'''
class AgentTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.object_class = ObjectClass.objects.create(name="Microphone", description="audio booster", 
                                                       interactions = {'speak_to_agent':"am working on test"},
                                                                       is_public=True,)
        self.object_class1 = ObjectClass.objects.create(name="Board", description="write discussion", 
                                                       interactions = {'speak_to_agent':"writing test cases"},
                                                                       is_public=True,)
        self.memories = Memory.objects.create(name = "agent mem", description="agent memories store the activities memories")
        self.tag = Tag.objects.create(creator=self.user, name="Tag1", description="A tag description")
        self.tag2 = Tag.objects.create(creator=self.user, name="Tag2", description="A tag2 description")
        self.agent_classes =  AgentClass.objects.create(name="Oakyln Tunner", description="Agent Oakyln Description", is_public=True)
        self.agent_classes.tags.set([self.tag, self.tag2]) 
        self.agent_classes.tools.set([self.object_class, self.object_class1])
        
    
    def test_agent_created(self):
        self.assertTrue(AgentClass.objects.filter(name='Oakyln Tunner').exists())

    
    def test_agent_delete_view(self):
        response = self.client.post(reverse('agents:agent_delete', kwargs={'uuid': self.agent_classes.uuid}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('agents:agent_user'))
        self.assertFalse(AgentClass.objects.filter(uuid=self.agent_classes.uuid).exists())
