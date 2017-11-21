import fnmatch
import os
import re

from django.core.management.commands.runserver import BaseRunserverCommand

import Books
from enduser.models import Book, Author, Language, Settings


def read_book(file):
    content = open(os.path.join(os.path.dirname(Books.__file__), file), encoding="utf-8").read()
    try:
        title = re.search('Title: (.+?)\n', content).group(1)
        author = re.search('Author: (.+?)\n', content).group(1)
    except AttributeError:
        title = ''
        author = ''

    language = re.search('Language: (.+?)\n', content)
    if language:
        language = language.group(1)
        language, created = Language.objects.get_or_create(language=language)
    else:
        language = None

    release_date = re.search('Release Date: (.+?)\n', content)
    if release_date:
        release_date = release_date.group(1)
        release_date = re.sub("(\s\[.+)", "", release_date)
    else:
        release_date = None

    posting_date = re.search('Posting Date: (.+?)\n', content)
    if posting_date:
        posting_date = posting_date.group(1)
        posting_date = re.sub("(\s\[.+)", "", posting_date)
    else:
        posting_date = None

    first_posted = re.search('First Posted: (.+?)\n', content)
    if first_posted:
        first_posted = first_posted.group(1)
        first_posted = re.sub("(\s\[.+)", "", first_posted)
    else:
        first_posted = None

    last_updated = re.search('Last Updated: (.+?)\n', content)
    if last_updated:
        last_updated = last_updated.group(1)
        last_updated = re.sub("(\s\[.+)", "", last_updated)
    else:
        last_updated = None

    author, created = Author.objects.get_or_create(name=author)

    Book.objects.update_or_create(
        title=title,
        author=author,
        content=content,
        language=language,
        file_path=file,
        release_date=release_date,
        posting_date=posting_date,
        first_posted=first_posted,
        last_updated=last_updated
    )


def read_books():
    print("Starting to read books...")
    files = os.listdir(os.path.dirname(Books.__file__))
    for file in files:
        if fnmatch.fnmatch(file, '*.txt'):
            read_book(file)
    print("All books have been read...")


def setup():
    Settings.objects.update_or_create(page_size=50)


class Command(BaseRunserverCommand):
    def inner_run(self, *args, **options):
        read_books()
        setup()
        super(Command, self).inner_run(*args, **options)
