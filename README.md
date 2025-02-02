
# Multilingual FAQ Management System

## Overview
This is a Django-based FAQ (Frequently Asked Questions) Management System that supports multilingual FAQs using **CKEditor** for rich text answers and hence adding the functionality WYSIWYG. It also includes **automatic translation** using Google Translate and supports **language-based filtering**.

Live link - https://anshud49-multilingual-faq.onrender.com/

#### Use the following credentials to log in to the admin site
- username-Anshu
- password-Anshu@123


## Features
- Manage FAQs with **rich text answers** using CKEditor.
- CKEditor integrated both in the **admin panel** and **frontend** to edit the answers.
- Supports multiple languages (English, Hindi, Bengali, French, Arabic, Russian, Urdu).
- Auto-translation using Google Translate.
- Django Rest Framework (DRF) API for retrieving FAQs.
- Admin panel support for CRUD operations.
- Caching(Redis) for translated content to improve performance.
- Followed PEP8 conventions and best practices using flake8.
- Unit tests performed successfully.

## Technologies Used
- **Django** (Backend Framework)
- **HTML ,CSS, Javascript** (Frontend Framework)
- **Django REST Framework** (API)
- **CKEditor** (Rich Text Editor for answers)
- **Google Translate API** (for automatic translation)
- **SQLite / PostgreSQL** (Database)
- **asyncio** (Asynchronous tasks for translations)
- **Redis** (Caching translations)

## FAQ Model
- **question = models.TextField()** 
- **answer = RichTextField()**
- **question_hi = models.TextField()**
- **answer_hi = RichTextField()** 
- .
- .
- .
- .
- **question_fr = models.TextField()**
- **answer_fr = RichTextField()** 


## Installation
### 1. Clone the Repository
```sh
 git clone https://github.com/yourusername/django-faq-system.git
 cd BharatFD
```

### 2. Create and Activate Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  
# On Windows use 
venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Setup `.env` file
Create a `.env` file in the root directory with the following content:
```env
REDIS_HOST=<your-hostname>
REDIS_PORT=<your-redis-port-number>
REDIS_PASSWORD=<your-redis-password>
REDIS_DB=<your-database-number>
```

### 5. Apply Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```sh
python manage.py createsuperuser
```

### 7. Run Development Server
```sh
python manage.py runserver
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/faqs/` | Get all FAQs in English Language|
| GET | `/api/faqs/?lang=fr` | Get FAQs in French |
| POST | `/api/faqs/` | Create a new FAQ |
| PUT | `/api/faqs/{faq_id}/` | Update an FAQ |
| DELETE | `/api/faqs/{faq_id}/` | Delete an FAQ |

## Usage
- Navigate to `https://anshud49-multilingual-faq.onrender.com/admin/` to manage FAQs.
- Access `https://anshud49-multilingual-faq.onrender.com/api/faqs/` for API responses.
- Add `?lang=fr` or any supported language code to get translations.
- For viewing all FAQs, visit `https://anshud49-multilingual-faq.onrender.com/faqs/`.
- By clicking on any FAQ answer, you will be redirected to `https://anshud49-multilingual-faq.onrender.com/faqs/edit/?faq_id={faq_id}` to edit the question and the answer using **CKEditor**.

### Example languages:
- `en` (default)
- `hi` (Hindi)
- `bn` (Bengali)
- `ar` (Arabic)
- `fr` (French)
- `ur` (Urdu)
- `ru` (Russian)

## Testing
Run unit tests using pytest:
```sh
python3 manage.py test
```

## Caching
- FAQs are cached for 1 hour to improve performance.
## Contributing

1. Fork the repo
2. Create a new branch (`feature/new-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Author
[Anshu Dwivedi](https://github.com/anshud49) 

##### anshudwivedi135@gmail.com
##### https://www.linkedin.com/in/anshudwivedi49/

