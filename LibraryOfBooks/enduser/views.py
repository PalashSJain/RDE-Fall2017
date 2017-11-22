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
    book = Book.objects.get(id=book_id)
    book.current_page = int(page_number)
    book.last_page_number = book.get_last_page_number()
    content = book.get_content(page_number)
    request.session[book.title] = page_number
    return render_to_response('book_page.html', {'content': content, 'book': book})
