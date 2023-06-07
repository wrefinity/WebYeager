import uuid
from yeager_ai.users.models import TimeStampedModel
# import yeager_ai.world.models as world_model
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField,  CharField, ForeignKey, ManyToManyField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
User = get_user_model()
'''
Tag model for agents
'''
class Tag(TimeStampedModel):
    creator = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = CharField(_("Tag Name"), blank=True, max_length=255)
    description = TextField(null=False, blank=True)

    def __str__(self):
        return f"Tag: {self.name}"

    def get_absolute_url(self):
        return reverse("worlds:tag_detail", kwargs={"uuid": self.uuid})

'''
AgentRating Model
'''
class AgentRatings(models.Model):
    world = models.ForeignKey("agent.AgentClass", on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['world', 'user']

class AgentClass(TimeStampedModel):
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    description = models.TextField()
    avatar = models.ImageField(upload_to='agent-avatars/')
    tags = ManyToManyField(Tag, blank=True)
    memories = ManyToManyField(to="world.Memory", blank=True, related_name="agent_memory")
    tools = ManyToManyField(to="world.ObjectClass", blank=True, related_name="world_object_tool")
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def get_agents_created_by_user(self):
        return AgentClass.objects.filter(creator=self.creator)

    def get_absolute_url(self):
        return reverse("agents:agent_detail", kwargs={"uuid": self.uuid})

    def delete_agent(self):
        return reverse("agents:agent_delete", kwargs={"uuid": self.uuid})
    
    # rating an agent is based on users
    def rate_agent(self, user):
        # check that user have not rated an agent before incrementing 
        
        try:
            rated = self.ratings.filter(user=user)
            if not rated.exists():
                self.rating += 1
                self.save()
                AgentRatings.objects.create(world=self, user=user)
            else:
                self.rating -= 1
                rated.delete()
                self.save()
        except AgentClass.DoesNotExist:
            pass
'''
Agent Instance
'''


class AgentInstance(TimeStampedModel):
    slug = models.SlugField(unique=True)
    uuid = models.CharField(max_length=100)
    world = models.ForeignKey("world.WorldInstance", on_delete=models.CASCADE, related_name="world_instance_name")
    agent_class = models.ForeignKey(AgentClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uuid} - {self.agent_class.name} - {self.world}"
