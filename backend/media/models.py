#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

# from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from commons.models import BaseModel
from config.settings import MEDIA_UPLOAD


class Media(BaseModel):
    """Common shared Media model with metadata fields

    Abstract class: all specific Media classes will inherit from this class.
    This class describes media with related informations.
    """

    # "upload_to" defined through config param
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(_("label"), null=True, blank=True)
    storage = models.ImageField(upload_to=MEDIA_UPLOAD)
    date = models.DateField(_("Date"))
    author = models.CharField(
        _("Author"), null=True, blank=True, max_length=200
    )
    source = models.CharField(
        _("Source of data"), null=True, blank=True, max_length=200
    )
    remark = models.TextField(_("Remark"), null=True, blank=True)

    def __str__(self):
        return f"{self.date} | {self.label} by {self.created_by}"
