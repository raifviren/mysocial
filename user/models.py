from __future__ import unicode_literals, absolute_import

import uuid

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class BaseClass(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, name="id")

    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def get_obj(cls, primary_key):
        """
        Get object by primary_key and return this object

        Params: cls, class object
                 primary_key
        Return: models object
        """
        try:
            return cls.objects.get(id=primary_key)
        except (cls.DoesNotExist, ValueError):
            return None
        except Exception:
            return None

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # print(self.id)
        # if not self.id:
        #     self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BaseClass, self).save(*args, **kwargs)

    class Meta(object):
        abstract = True


class User(AbstractUser, BaseClass):
    mobile = models.CharField(_('mobile number'),
                              max_length=15,
                              help_text=_('Enter mobile number'),
                              )
    country_code = models.CharField(_('country code'),
                                    max_length=5,
                                    help_text=_('Enter country code'),
                                    default='+91'
                                    )
    twitter_oauth_token = models.CharField(max_length=100, null=True, blank=True)
    twitter_oauth_token_secret = models.CharField(max_length=100, null=True, blank=True)
    twitter_user_id = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True)
    twitter_screen_name = models.CharField(max_length=100, null=True, blank=True)
