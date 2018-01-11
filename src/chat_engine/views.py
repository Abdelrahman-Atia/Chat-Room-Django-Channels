from django.shortcuts import render

#render the html view
def chat(request):
    return render(request, 'chat/chat.html')
