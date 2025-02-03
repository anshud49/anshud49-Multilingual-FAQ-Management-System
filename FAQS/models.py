from django.db import models
from ckeditor.fields import RichTextField
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    
    question_en = models.TextField(blank=True, null=True)
    question_hi = models.TextField(blank=True, null=True)  
    question_bn = models.TextField(blank=True, null=True)  
    question_fr = models.TextField(blank=True, null=True)  
    question_ar = models.TextField(blank=True, null=True)  
    question_ru = models.TextField(blank=True, null=True)  
    question_ur = models.TextField(blank=True, null=True)  

    answer_en = RichTextField(blank=True, null=True)  
    answer_hi = RichTextField(blank=True, null=True)  
    answer_bn = RichTextField(blank=True, null=True)  
    answer_fr = RichTextField(blank=True, null=True)  
    answer_ar = RichTextField(blank=True, null=True)  
    answer_ru = RichTextField(blank=True, null=True)  
    answer_ur = RichTextField(blank=True, null=True)  

    def save(self, *args, **kwargs):
        language_codes = ['hi', 'bn', 'fr', 'ar', 'ru', 'ur']
        
        try:
            detected_lang_question = detect(self.question) if self.question else 'en'
        except:
            detected_lang_question = 'en'

        try:
            detected_lang_answer = detect(self.answer) if self.answer else 'en'
        except:
            detected_lang_answer = 'en'

        self.question_en = GoogleTranslator(source=detected_lang_question, target='en').translate(self.question)
        for lang in language_codes:
            setattr(self, f'question_{lang}', GoogleTranslator(source=detected_lang_question, target=lang).translate(self.question))

        self.answer_en = GoogleTranslator(source=detected_lang_answer, target='en').translate(self.answer)
        for lang in language_codes:
            setattr(self, f'answer_{lang}', GoogleTranslator(source=detected_lang_answer, target=lang).translate(self.answer))

        super().save(*args, **kwargs)

    def get_translated_text(self, lang_code='en'):
        translations = {
            'en': {'question': self.question_en, 'answer': self.answer_en},
            'hi': {'question': self.question_hi, 'answer': self.answer_hi},
            'bn': {'question': self.question_bn, 'answer': self.answer_bn},
            'fr': {'question': self.question_fr, 'answer': self.answer_fr},
            'ar': {'question': self.question_ar, 'answer': self.answer_ar},
            'ru': {'question': self.question_ru, 'answer': self.answer_ru},
            'ur': {'question': self.question_ur, 'answer': self.answer_ur},
        }

        return translations.get(lang_code, {}).get('question', self.question), translations.get(lang_code, {}).get('answer', self.answer)

    def __str__(self):
        return f'FAQ {self.id}'
