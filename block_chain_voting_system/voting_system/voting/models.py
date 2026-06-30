from django.db import models
from django.contrib.auth.models import User
import hashlib
import json
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    party_logo = models.ImageField(upload_to='logos/', blank=True, null=True) # சின்னம்
    candidate_photo = models.ImageField(upload_to='photos/', blank=True, null=True) # புகைப்படம்
    votes_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.party})"

class VoteBlock(models.Model):
    prev_hash = models.CharField(max_length=64)
    voter_id = models.IntegerField()
    candidate_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    block_hash = models.CharField(max_length=64)

    def save(self, *args, **kwargs):

        block_content = f"{self.prev_hash}{self.voter_id}{self.candidate_id}{self.timestamp}"
        self.block_hash = hashlib.sha256(block_content.encode()).hexdigest()
        super().save(*args, **kwargs)
class ElectionSettings(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Election Schedule"        