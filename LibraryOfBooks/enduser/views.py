from django.shortcuts import render_to_response

from enduser.models import Book


def home(request):
    books = Book.objects.all()
    return render_to_response('home.html', {'books': books})
    # return render(request, 'home.html')

