import uuid
from django.db import models
from django.conf import settings
from yeager_ai.api_key.models import ApiKey
from django.contrib.auth import get_user_model
from yeager_ai.agent.models import AgentClass, Tag
from yeager_ai.users.models import TimeStampedModel
from django.db.models import BooleanField, JSONField, CharField, ForeignKey,\
    URLField, ManyToManyField, DecimalField, FilePathField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
User = get_user_model()

""" Models defined under the world app.
1. Memory Model
2. Category
3. InstanceStatusChoices Model
4. ObjectClass
5. Event
6. WorldClass
7. WorldInstance
8. Object Instances
"""


class Memory(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Memory : {self.name}"


'''
Category model
'''
Category = [
    ('RS', 'Research'),
    ('SD', 'Software Development'),
    ('MK', 'Marketing'),
    ('AC', 'Accounting'),
    ('BP', 'Business Process'),
]

''' world instances choice '''


class InstanceStatusChoices(models.TextChoices):
    STARTING = 'STARTING', _('Starting')
    BLOCKED = 'BLOCKED', _('Blocked')
    PAUSED = 'PAUSED', _('Paused')
    STOPPED = 'STOPPED', _('Stopped')
    PROCESSING = 'PROCESSING', _('Processing')
    IDLE = 'IDLE', _('Idle')
    ERROR = 'ERROR', _('Error')
    DELETED = 'DELETED', _('Deleted')
    TERMINATED = 'TERMINATED', _('Terminated')


""" Object Class Section """
class ObjectClass(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    avatar = models.ImageField(upload_to='object-avatar/')
    interactions = models.JSONField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


'''
Event Stream
'''


class Event(TimeStampedModel):
    event_type = models.CharField(max_length=255)
    description = models.TextField()
    data = JSONField()

    def __str__(self):
        return self.event_type

'''
world rating
'''
class WorldRatings(models.Model):
    world = models.ForeignKey("world.WorldClass", on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['world', 'user']

class WorldClass(TimeStampedModel):
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='world-thumbnails/')
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    category = CharField(choices=Category, max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)

    agent_classes = models.ManyToManyField(AgentClass)
    object_classes = models.ManyToManyField(ObjectClass)
    docker_path = FilePathField(path=settings.WORLD_AGENT_PATH, max_length=500)

    user_interactions = models.ManyToManyField(
        "world.Event", related_name="interaction", blank=True)
    world_outputs = models.ManyToManyField(
        "world.Event", blank=True, related_name="output")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse("worlds:world_detail", kwargs={"slug": self.slug})
        return url


    def delete_world(self):
        return reverse("worlds:world_delete", args=[self.uuid])
    
    # rating a world is based on users
    def rate_world(self, user):
        # check that user have not rated an agent before incrementing 
        
        try:
            rated = self.ratings.filter(user=user)
            if not rated.exists():
                self.rating += 1
                self.save()
                WorldRatings.objects.create(world=self, user=user)
            else:
                self.rating -= 1
                rated.delete()
                self.save()
        except WorldRatings.DoesNotExist:
            pass


# Instances Section
'''
World Instance 
'''


class WorldInstance(TimeStampedModel):
    slug = models.SlugField(unique=True)
    uuid = models.CharField(max_length=100, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    world_class = models.ForeignKey(WorldClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    description = models.TextField()
    status = models.CharField(
        max_length=50, choices=InstanceStatusChoices.choices, default=InstanceStatusChoices.STARTING)
    is_running = BooleanField(default=False)
    is_test = BooleanField(default=False)
    tags = ManyToManyField(Tag, blank=True)

    bit16_url = URLField(blank=True, null=True)
    default_preview_file = FilePathField(path=settings.WORLD_AGENT_PATH, max_length=500)
    default_preview_urls = URLField(blank=True, null=True)
    socket_url = CharField(blank=True, null=True, max_length=200)
    api_key = ForeignKey(ApiKey, on_delete=models.SET_NULL,
                         null=True, blank=True)

    total_ml_cost = DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cloud_cost = DecimalField(max_digits=10, decimal_places=2, default=0)
    total_memory_cost = DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_external_tool_cost = DecimalField(
        max_digits=10, decimal_places=2, default=0)
    shutdown_cost = DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        url = reverse("worlds:world_instance_detail", kwargs={"slug": self.slug})
        return url

    def total_cost(self):
        return self.total_ml_cost + self.total_cloud_cost + self.total_memory_cost + self.total_external_tool_cost

    def user_performs_action(self, request):
        # execute when a user perform an action on the world
        # for instance reduce users tokens
        try:
            # ws.send(socket_event)
            pass
        except Exception as e:
            print(f"Error: {e}")
            return False
        token_cost = 1
        # to be discuss
        self.user.balance -= token_cost
        
        



''' 
Object Instance
'''


class ObjectInstance(TimeStampedModel):
    # meant to come from the socket
    uuid = models.CharField(max_length=100, default=uuid.uuid4)
    world = models.ForeignKey(WorldInstance, on_delete=models.CASCADE)
    object_class = models.ForeignKey(ObjectClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.object_class} - {self.world}"
