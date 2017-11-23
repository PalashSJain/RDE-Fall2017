import math
from django.shortcuts import render_to_response, redirect

from enduser.models import Book


def home(request):
    books = Book.objects.all()
    for book in books:
        try:
            book.current_page = int(request.session.get(book.title))
        except TypeError:
            book.current_page = 1
    return render_to_response('home.html', {'books': books})


def show_page(request, book_id, page_number):
    if request.session.__contains__('page_size'):
        page_size = int(request.session.get('page_size'))
    else:
        page_size = 50
        request.session['page_size'] = 50
    book = Book.objects.get(id=book_id)
    book.current_page = int(page_number)
    book.last_page_number = book.get_last_page_number(page_size)
    content = book.get_content(page_number, page_size)
    request.session[book.title] = page_number
    return render_to_response('book_page.html', {'content': content, 'book': book, 'current_page_size': page_size})


def change_page_size(request, book_id, new_page_size):
    current_page_size = int(request.session.get('page_size'))
    new_page_size = int(new_page_size)
    book = Book.objects.get(id=book_id)
    current_page = int(request.session.get(book.title))
    current_first_line = (current_page - 1) * current_page_size

    print("current_first_line %s" % current_first_line)
    print("new_page_size %s" % new_page_size)
    print("current_page_size %s" % current_page_size)

    page_number = math.floor(current_first_line / new_page_size) + 1
    request.session['page_size'] = new_page_size
    return redirect('show_page', book_id=book_id, page_number=page_number)
