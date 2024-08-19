from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import ChatSession, Message
from .rag import RAG

rag = RAG(settings.OPENAI_API_KEY)

def chat_view(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        user_message = request.POST.get('message')
        
        session, created = ChatSession.objects.get_or_create(id=session_id)
        Message.objects.create(session=session, content=user_message, is_user=True)
        
        response = rag.generate_response(user_message)
        Message.objects.create(session=session, content=response, is_user=False)
        
        return JsonResponse({'response': response, 'session_id': session.id})
    
    return render(request, 'chat/chat.html')