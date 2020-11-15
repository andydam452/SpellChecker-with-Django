# SpellChecker-with-Django
<img src="/image/en_pic.png"> 

<img src="/image/vn_pic.png">

## About
Use Django to build website.

BKTree is used to store words in dictionary to reduce exuction time.

Damerau-Levenshtein algorithm is used to calculate the edit distance between words.

This app is available for both Vietnamese and English.

You can change either Damerau-Levenshtein algorithm or Levenshtein algorithm in views.py.

Change search range is also avaiable in views.py. Default value of search range is 1.

## Library

```sh
pip install requirements.txt
```

## Usage

```sh
python manage.py runserver
```

Access http://localhost:8000/spellcheckapp to use.

Enjoy :pray: :pray: :pray:
