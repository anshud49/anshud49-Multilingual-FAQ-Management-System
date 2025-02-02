from django.db import models
from ckeditor.fields import RichTextField

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    
    
    question_hi = models.TextField(blank=True, null=True)  # Hindi 
    question_bn = models.TextField(blank=True, null=True)  # Bengali translation
    question_fr = models.TextField(blank=True, null=True)  # French translation
    question_ar = models.TextField(blank=True, null=True)  # Arabic
    question_ru = models.TextField(blank=True, null=True)  # Russian 
    question_ur = models.TextField(blank=True, null=True)  # Urdu 

    answer_hi = RichTextField(blank=True, null=True)       # Hindi 
    answer_bn = RichTextField(blank=True, null=True)       # Bengali 
    answer_fr = RichTextField(blank=True, null=True)       # French 
    answer_ar = RichTextField(blank=True, null=True)       # Arabic 
    answer_ru = RichTextField(blank=True, null=True)       # Russian 
    answer_ur = RichTextField(blank=True, null=True)       # Urdu 


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def get_translated_text(self, lang_code='en'):

        translations = {
            'en': {'question': self.question, 'answer': self.answer},
            'hi': {'question': self.question_hi, 'answer': self.answer_hi},
            'bn': {'question': self.question_bn, 'answer': self.answer_bn},
            'fr': {'question': self.question_fr, 'answer': self.answer_fr},
            'ar': {'question': self.question_ar, 'answer': self.answer_ar},
            'ru': {'question': self.question_ru, 'answer': self.answer_ru},
            'ur': {'question': self.question_ur, 'answer': self.answer_ur},
        }

        translated_question = translations.get(lang_code, {}).get('question', self.question)
        translated_answer = translations.get(lang_code, {}).get('answer', self.answer)

        return translated_question, translated_answer

    
    def __str__(self):
        return f'{self.id}'
