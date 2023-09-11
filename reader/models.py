from django.contrib.postgres.indexes import GinIndex
from django.db import models
from languages.fields import LanguageField
from parler.models import TranslatedFields
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=200)
    )
    codename = models.CharField(max_length=64, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ["parent", "order"]


class Keyword(models.Model):
    title = models.CharField(max_length=128, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]


class SourceEngine(models.Model):
    title = models.CharField(max_length=128, db_index=True, unique=True)
    codename = models.CharField(max_length=64, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]


class Article(models.Model):
    title = models.TextField(db_index=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    original_id = models.CharField(max_length=255, db_index=True, unique=True)
    original_url = models.URLField(max_length=4096, db_index=True, unique=True)
    language = LanguageField()
    is_premium = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    first_related = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
    source_engine = models.ForeignKey(SourceEngine, on_delete=models.SET_NULL, blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            GinIndex(fields=["title", "summary"], name="article_gin_idx"),
        ]
