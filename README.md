# Django-vod
Use Django to create a vod(video on demand) manage system
Based on Bootstrap3

# Useful 3rd-party app
1. Django Crispy Forms
`pip install django-crispy-forms`
>*.html
```
{% load crispy_forms_tags %}

<form method='POST' action='' >{%csrf_token%}
{{form|crispy}}
<input class='btn btn-primary' type='submit' value='Sign Up'/>
</form>
```
2. Django Registration Redux
