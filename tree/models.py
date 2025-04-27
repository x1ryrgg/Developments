from django.db import models



class TreeStore(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, default=None)

    def __str__(self):
        return 'type %s' % self.type
