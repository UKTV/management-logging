from django.db import models


class Logging(models.Model):
    name = models.CharField(
        max_length=150
    )
    class_name = models.CharField(
        max_length=150
    )
    stdout_output = models.TextField(verbose_name="Output")
    stderr_output = models.TextField(verbose_name="Error output")
    status = models.CharField(max_length=10)
    start_datetime = models.DateTimeField(auto_now_add=True)
    finish_datetime = models.DateTimeField(blank=True, null=True)
    site = models.CharField(blank=True, null=True, max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
