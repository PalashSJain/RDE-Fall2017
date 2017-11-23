import os
import math
from django.db import models

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


class Book(models.Model):
    class Meta:
        unique_together = ('title', 'author')

    title = models.TextField(blank=False, null=False)
    author = models.ForeignKey('Author')
    file_path = models.TextField(blank=True, null=True, unique=True)
    language = models.ForeignKey('Language')
    release_date = models.TextField(blank=True, null=True)
    posting_date = models.TextField(blank=True, null=True)
    first_posted = models.TextField(blank=True, null=True)
    last_updated = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    no_of_lines = models.IntegerField(default=1, blank=False, null=False)

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_content(self, page_number=1, page_size=50):
        content = self.content.split("\n")
        text = ""
        start = (page_number - 1) * page_size
        end = page_number * page_size
        if end > self.no_of_lines:
            end = self.no_of_lines
        for line_number in range(start, end):
            text += content[line_number] + "\n"
        return text

    def get_last_page_number(self, page_size=50):
        return math.ceil(int(self.no_of_lines) / page_size)


class Author(models.Model):
    name = models.TextField(default='N/A', blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.TextField(default='N/A', blank=False, null=False, unique=True)

    def __str__(self):
        return self.language


