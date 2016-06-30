#coding: utf-8
from web import form

CreditForm = form.Form(
    form.Textbox('amount', form.notnull, 
        form.regexp(r'[+-]?([0-9]*[.])?[0-9]+', "Le montant entré n'est pas un chiffre valide"),
        size=5,
        post=" €",
        description="Montant :"),

    form.Button('Envoyer'),
)

ConsumeForm = form.Form(
    form.Dropdown('units', [(x,x) for x in range(1,11)], description="Nombre de consommations"),
    form.Button('Envoyer'),
)

ConsumeInlineForm = form.Form(
    form.Textbox('units', size=5),
)

UserForm = form.Form(
    form.Textbox('firstname', form.notnull, 
        size=30, 
        description="Prénom :"),
    form.Textbox('lastname', form.notnull, 
        size=30,
        description="Nom :"),
    form.Textbox('email', form.notnull, 
        form.regexp(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', 'Adresse mail incorrecte'),
        rows=30,
        description="Adresse mail:"),
    form.Textbox('fgs', form.notnull, 
        form.regexp(r'\d{8}', 'Numéro FGS incorrect'),
        rows=8,
        description="Numéro FGS:"),
    form.Textbox('rfid',
        size=8,
        description="Numéro RFID :", post=" Non obligatoire"),

    form.Button('Envoyer'),

)

TemplateForm = form.Form(
    form.Textarea('template', form.notnull,
        cols=50,
        rows=10,
        description="Template mail",
    ),

    form.Button('Envoyer'),
)
