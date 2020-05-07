import os
import uuid

from django.conf import settings
from django.db import models


class Project(models.Model):
    codename = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='owned_projects')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Membership',
        through_fields=['project', 'user'])
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__, self.codename)

    def is_maintainer(self, user):
        return self.members.filter(type='maintainer', user=user).exists()


def doc_directort_path(obj, filename):
    ext = os.path.splitext(filename)[-1].lstrip('.')
    filename = uuid.uuid4().hex
    return 'doc/{}/{}.{}'.format(
        obj.project.codename, filename, ext)


class Doc(models.Model):
    version = models.CharField(max_length=100)
    path = models.FileField(
        upload_to=doc_directort_path, max_length=255)
    project = models.ForeignKey(
        Project, on_delete=models.DO_NOTHING, related_name='doc')
    update_at = models.DateTimeField(auto_now=True)


class Membership(models.Model):
    MEMBER_TYPE_CHOICES = [
        ('maintainer', 'maintainer'),
        ('guest', 'guest')
    ]
    project = models.ForeignKey(
        Project, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=32, choices=MEMBER_TYPE_CHOICES)


class GitHook(models.Model):
    slug = models.CharField(max_length=100, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    git_repo = models.CharField(max_length=255)
    doc_path = models.CharField(max_length=255)
