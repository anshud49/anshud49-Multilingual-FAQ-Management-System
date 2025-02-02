from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer
from .forms import FAQForms
from googletrans import Translator
import asyncio
from django.core.cache import cache

# View for rendering HTML page
def FAQSViews(request):
    lang = request.GET.get('lang', 'en')  
    faqs = FAQ.objects.all()

    for faq in faqs:
        
        translated_question = None
        translated_answer = None
        
        if getattr(faq, f'question_{lang}', None):
           translated_question = getattr(faq, f'question_{lang}')
        if getattr(faq, f'answer_{lang}', None):
           translated_answer = getattr(faq, f'answer_{lang}')

        
        cache_key_q=None
        cache_key_a=None
        if not translated_question:    
         cache_key_q = f"translate:{faq.question}:{lang}"
        if not translated_answer:
         cache_key_a = f"translate:{faq.answer}:{lang}"

        translated_question = cache.get(cache_key_q)
        translated_answer = cache.get(cache_key_a)

        if not translated_question:
            translated_question = sync_detect_and_translate(faq.question, lang)
            cache.set(cache_key_q, translated_question, timeout=60 * 60 * 24)  

        if not translated_answer:
            translated_answer = sync_detect_and_translate(faq.answer, lang)
            cache.set(cache_key_a, translated_answer, timeout=60 * 60 * 24)
        
        setattr(faq, f'question_{lang}', translated_question)
        setattr(faq, f'answer_{lang}', translated_answer)
        faq.translated_question = translated_question
        faq.translated_answer = translated_answer

    return render(request, 'faqs.html', {'faqs': faqs, 'selected_lang': lang})


def sync_detect_and_translate(text, target_language):
    if not text.strip():
        return text  

    translator = Translator()
    
    try:
        detected_lang = translator.detect(text).lang
        if detected_lang != target_language:
            return translator.translate(text, dest=target_language).text
        return text  
    except Exception as e:
        return text 


async def detect_and_translate(translator, text, target_language):
   
    cache_key = f"translate:{text}:{target_language}"  

    cached_translation = cache.get(cache_key)
    if cached_translation:
        return cached_translation  
    
    try:
        detected_lang = await translator.detect(text)
        
        if detected_lang.lang != target_language:
            translated = await translator.translate(text, dest=target_language)
            cache.set(cache_key, translated.text, timeout=60*60*24)  
            return translated.text
        
        return text  
    except Exception as e:
        return text  


async def translate_faqs_async(faqs, target_language):
    translator = Translator()
    tasks = []

    for faq in faqs:
        tasks.append(detect_and_translate(translator, faq['question'], target_language))
        tasks.append(detect_and_translate(translator, faq['answer'], target_language))

    translated_questions_answers = await asyncio.gather(*tasks)

    for i, faq in enumerate(faqs):
        faq['question'] = translated_questions_answers[i * 2]
        faq['answer'] = translated_questions_answers[i * 2 + 1]

    return faqs

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')  
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = asyncio.run(translate_faqs_async(serializer.data, lang))
        return Response(data)

def FaqsEditViews(request):
    faq_id = request.GET.get('faq_id') 
    faq = None
    form = FAQForms()
    
    if faq_id:
        faq = get_object_or_404(FAQ, id=faq_id)

    if request.method == 'POST':
        form = FAQForms(request.POST, instance=faq)  
        if form.is_valid():
            form.save()  
            return redirect('/faqs/')  
    else:
        form = FAQForms(instance=faq)  

    return render(request, 'faqs-edit.html', {'form': form, 'faq_id': faq_id})
