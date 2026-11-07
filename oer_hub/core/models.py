from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="дата обновления",
        auto_now=True,
    )

    class Meta:
        abstract = True


class NamedModel(TimeStampedModel):
    name = models.CharField(
        verbose_name="название",
        max_length=255,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
