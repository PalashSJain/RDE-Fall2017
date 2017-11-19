import os

from django.db import models

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


class Book(models.Model):
    title = models.TextField(blank=False, null=False)
    author = models.ForeignKey('Author')
    file_path = models.TextField(blank=True, null=True)
    language = models.ForeignKey('Language')
    release_date = models.DateField(blank=True, null=True)
    posting_date = models.DateField(blank=True, null=True)
    first_posted = models.DateField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    current_page = models.IntegerField(default=0, blank=False, null=False)
    content = models.TextField(blank=True, null=True)
    next_page = models.TextField(blank=True, null=True)

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def set_page_number(self, page_number=0):
        self.current_page = page_number

    def get_content(self):
        if self.content is None:
            file = open(os.path.join(PROJECT_ROOT, self.file_path))
            self.content = file.read()
        print(self.content)
        return ""


class Author(models.Model):
    name = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.TextField(blank=True, null=True)


class Settings(models.Model):
    page_size = models.IntegerField(default=0, blank=False, null=False)

    def set_page_size(self, page_size=50):
        self.page_size = page_size

    def get_page_size(self):
        return self.page_size
