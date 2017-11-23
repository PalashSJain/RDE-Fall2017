import math
from django.shortcuts import render_to_response, redirect

from enduser.models import Book


def home(request):
    books = Book.objects.all()
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
    return render_to_response('home.html', {'books': books})


def show_page(request, book_id, page_number):
    if request.session.__contains__('page_size'):
        current_page_size = int(request.session.get('page_size'))
    else:
        current_page_size = 50
        request.session['page_size'] = 50
    book = Book.objects.get(id=book_id)
    book.current_page = int(page_number)
    book.last_page_number = book.get_last_page_number(current_page_size)
    content = book.get_content(book.current_page, current_page_size)
    request.session[book.title] = (book.current_page - 1) * current_page_size
    return render_to_response('book_page.html', {'content': content, 'book': book, 'current_page_size': current_page_size})


def change_page_size(request, book_id, new_page_size):
    new_page_size = int(new_page_size)
    book = Book.objects.get(id=book_id)
    current_first_line = int(request.session.get(book.title))
    page_number = math.floor(current_first_line / new_page_size) + 1
    request.session['page_size'] = new_page_size
    return redirect('show_page', book_id=book_id, page_number=page_number)
