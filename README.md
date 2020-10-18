# Django Files Archive

Accept multiple URLs in a POST request and return a ZIP archive including all downloaded files

## Get started

```bash
python -m venv env
source env/bin/activate # Windows .\env\Scripts\activate
pip install -r requirements.txt
python manage.py runserver --settings=django_files_archive.settings.dev
```

## Test
```
python manage.py test --settings=django_files_archive.settings.dev
```

## Local functional testing

[http://127.0.0.1:8000/test_archive/](http://127.0.0.1:8000/test_archive/)

## Roadmap
* bump Django version