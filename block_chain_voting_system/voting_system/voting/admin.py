from django.contrib import admin
from .models import Candidate, VoteBlock

admin.site.register(Candidate)
admin.site.register(VoteBlock)