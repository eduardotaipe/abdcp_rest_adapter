# -*- coding: utf-8 -*-

from django.db import models
from operators import strings

# Operators

class Operator(models.Model):

    name = models.CharField(
        verbose_name=strings.OPERATOR_NAME,
        max_length=128,
        unique=True
    )

    code = models.CharField(
        verbose_name=strings.OPERATOR_CODE,
        max_length=128,
        unique=True
    )

    uri = models.URLField(
        verbose_name=strings.OPERATOR_URI,
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        verbose_name=strings.OPERATOR_CREATED,
        auto_now_add=True
    )

    updated = models.DateTimeField(
        verbose_name=strings.OPERATOR_UPDATED,
        auto_now=True
    )

    class Meta:
        verbose_name = strings.OPERATOR_MODEL_NAME
        verbose_name_plural = strings.OPERATOR_MODEL_NAME_PLURAL

    def __unicode__(self):
        return self.name

