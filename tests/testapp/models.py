from django.db import models

STATUS_DRAFT = 0
STATUS_PUBLISHED = 1

STATUSES = (
    (STATUS_DRAFT, 'Draft'),
    (STATUS_PUBLISHED, 'Published'),
)

class Article(models.Model):

    title = models.CharField(max_length=200)
    status = models.IntegerField(default=STATUS_DRAFT, choices=STATUSES, blank=True)

    def __str__(self):
        return self.title
