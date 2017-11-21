from django.shortcuts import render_to_response

from enduser.models import Book


def home(request):
    books = Book.objects.all()
    return render_to_response('home.html', {'books': books})
    # return render(request, 'home.html')


def show_page_number(request, book_id, page_number):
    book = Book.objects.get(id=book_id)
    content = book.get_content(page_number)
    return render_to_response('book_page.html', {'content': content, 'book': book})

