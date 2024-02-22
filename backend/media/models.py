#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from commons.models import BaseModel
from config.settings import MEDIA_UPLOAD

# from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Media(BaseModel):
    """Common shared Media model with metadata fields

    Abstract class: all specific Media classes will inherit from this class.
    This class describes media with related informations.
    """

    # "upload_to" defined through config param
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    storage = models.ImageField(upload_to=MEDIA_UPLOAD)
    date = models.DateField(_("Date"))
    author = models.CharField(
        _("Author"), null=True, blank=True, max_length=200
    )
    source = models.CharField(
        _("Source of data"), null=True, blank=True, max_length=200
    )
    remark = models.TextField(_("Remark"), null=True, blank=True)
    # TMP See if this field is required
    # added_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     null=True,
    #     blank=True,
    #     related_name="media_author",
    #     verbose_name=_("Author of the media condition"),
    #     help_text=_("Author of the media condition"),
    #     on_delete=models.SET_NULL,
    # )
