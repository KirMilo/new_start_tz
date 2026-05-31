from django.shortcuts import render


def items_list_view(request):
    return render(request, "items/items_list.html")
