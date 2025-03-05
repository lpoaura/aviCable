#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _

from media.models import Media


class Species(models.Model):
    """Species model describing a species."""

    code = models.CharField(_("Species code"), unique=True, max_length=100)
    scientific_name = models.CharField(_("Scientific name"), max_length=200)
    vernacular_name = models.CharField(_("Vernacular name"), max_length=200)
    active = models.BooleanField(_("Active"), default=True)
    photo = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        verbose_name=_("Photo"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = _("Species")
