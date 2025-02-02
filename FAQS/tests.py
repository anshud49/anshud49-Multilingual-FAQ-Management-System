from django.test import TestCase
from .models import FAQ
from .serializers import FAQSerializer

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(question="<b>What is Django?</b>", answer="<li>Django is a web framework.</li>")

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "<b>What is Django?</b>")
        self.assertEqual(self.faq.answer, "<li>Django is a web framework.</li>")

    def test_faq_str_method(self):
        self.assertEqual(str(self.faq), str(self.faq.id))

class FAQViewsTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(question="<b>Test Question</b>", answer="<li>Test Answer</li>")

class FAQSerializerTest(TestCase):
    def test_faq_serializer(self):
        faq = FAQ.objects.create(question="<b>What is Django?</b>", answer="<li>Django is a web framework.</li>")
        serializer = FAQSerializer(faq)
        expected_data = {
            'id': faq.id,
            'question': "<b>What is Django?</b>",
            'answer': "<li>Django is a web framework.</li>"
        }
        self.assertEqual(serializer.data, expected_data)