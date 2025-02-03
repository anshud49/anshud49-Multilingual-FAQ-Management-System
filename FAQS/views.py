from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer
from .forms import FAQForms
from googletrans import Translator
import asyncio
from django.core.cache import cache
from deep_translator import GoogleTranslator
from langdetect import detect


def update_faq_translations():
    language_codes = ['en','hi', 'bn', 'fr', 'ar', 'ru', 'ur'] 
    faqs = FAQ.objects.all()

    for faq in faqs:
        updated_fields = {}  

        try:
            detected_lang = detect(faq.question)
        except:
            detected_lang = 'en'  

        try:
            detected_lang_answer = detect(faq.answer)
        except:
            detected_lang_answer = 'en' 

        for lang in language_codes:
            question_field = f'question_{lang}'
            answer_field = f'answer_{lang}'

            updated_fields[question_field] = GoogleTranslator(source=detected_lang, target=lang).translate(faq.question)

            updated_fields[answer_field] = GoogleTranslator(source=detected_lang_answer, target=lang).translate(faq.answer)

        FAQ.objects.filter(id=faq.id).update(**updated_fields)
        print(f"Updated FAQ ID: {faq.id}")

    print("Translation update completed!")
    
import threading
    
def FAQSViews(request):
    lang = request.GET.get('lang', 'en')  
    # thread = threading.Thread(target=update_faq_translations)
    # thread.start()
    faqs = FAQ.objects.all()
    for faq in faqs:
        
        translated_question = None
        translated_answer = None
        
        if getattr(faq, f'question_{lang}', None):
           translated_question = getattr(faq, f'question_{lang}')
        if getattr(faq, f'answer_{lang}', None):
           translated_answer = getattr(faq, f'answer_{lang}')

        faq.translated_question = translated_question
        faq.translated_answer = translated_answer
    return render(request, 'faqs.html', {'faqs': faqs, 'selected_lang': lang})



async def detect_and_translate(text, target_language, faq_id):
    cache_key = f"translate:{faq_id}:{target_language}"  

    cached_translation = cache.get(cache_key)
    if cached_translation:
        return cached_translation 

    try:
        detected_lang = detect(text)

        if detected_lang != target_language:
            translated_text = GoogleTranslator(source=detected_lang, target=target_language).translate(text)
            cache.set(cache_key, translated_text, timeout=60*60*24) 
            return translated_text
        else:
            return text  
    except Exception as e:
        return text


async def translate_faqs_async(faqs, target_language):
    tasks = []

    for faq in faqs:
        tasks.append(detect_and_translate(faq['question'], target_language, faq['id'])) 
        tasks.append(detect_and_translate(faq['answer'], target_language, faq['id']))   

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
    lang = request.GET.get('lang', 'en') 
    faq = get_object_or_404(FAQ, id=faq_id) if faq_id else None
    
   
    question = getattr(faq, f'question_{lang}', None)
    answer = getattr(faq, f'answer_{lang}', None)

    class DynamicFAQForm(FAQForms):
        def __init__(self, *args, **kwargs):
            initial_values = {
                'question': question,
                'answer': answer
            }
            
            super().__init__(*args, **kwargs)
            
            allowed_fields = ['question', 'answer']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    del self.fields[field_name]
            
            for field_name, value in initial_values.items():
                if field_name in self.fields:
                    self.fields[field_name].initial = value

    if request.method == 'POST':
        form = DynamicFAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect(f'/faqs/?lang={lang}')
    else:
        form = DynamicFAQForm(instance=faq)

    return render(request, 'faqs-edit.html', {'form': form, 'faq_id': faq_id, 'selected_lang': lang})
