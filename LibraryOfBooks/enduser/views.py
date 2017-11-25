import math
from django.shortcuts import render_to_response, redirect, render
from django.db.models import Q

from enduser.forms import FilterForm
from enduser.models import Book


def home(request):
    title = ''
    author = ''

    if request.method == 'POST':
        query = Q()
        if 'submit' in request.POST:
            form = FilterForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                if title:
                    query_title = Q(title__contains=title)
                    query.add(query_title, Q.AND)

                author = form.cleaned_data['author']
                if author:
                    query_author = Q(author__name__contains=author)
                    query.add(query_author, Q.AND)
        books = Book.objects.filter(query)
    else:
        books = Book.objects.all()

    if len(books) == 0:
        return render(request, 'no-book-found.html', {'title': title, 'author': author})

    if request.session.__contains__('page_size'):
        current_page_size = int(request.session.get('page_size'))
    else:
        current_page_size = 50
        request.session['page_size'] = 50

    for book in books:
        try:
            current_line_number = int(request.session.get(book.title))
            book.current_page = math.floor(current_line_number / current_page_size) + 1
        except TypeError:
            book.current_page = 1
            request.session[book.title] = 0
    return render(request, 'home.html', {'books': books, 'title': title, 'author': author})


def show_page(request, book_id, page_number):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return render(request, 'non-existant-book.html')

    if request.session.__contains__('page_size'):
        current_page_size = int(request.session.get('page_size'))
    else:
        current_page_size = 50
        request.session['page_size'] = 50

    book.current_page = int(page_number)
    book.last_page_number = book.get_last_page_number(current_page_size)
    if book.current_page > book.last_page_number:
        return redirect('show_page', book_id=book_id, page_number=book.last_page_number)

    content = book.get_content(book.current_page, current_page_size)
    request.session[book.title] = (book.current_page - 1) * current_page_size
    return render_to_response('book_page.html',
                              {'content': content, 'book': book, 'current_page_size': current_page_size})


def change_page_size(request, book_id, new_page_size):
    new_page_size = int(new_page_size)
    book = Book.objects.get(id=book_id)
    current_first_line = int(request.session.get(book.title))
    page_number = math.floor(current_first_line / new_page_size) + 1
    request.session['page_size'] = new_page_size
    return redirect('show_page', book_id=book_id, page_number=page_number)
