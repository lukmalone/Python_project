from django.contrib.auth.models import User
from main.models import Profile

for u in User.objects.all():
    try:
        profile = Profile(user=u)
        profile.save()
    except:
        pass