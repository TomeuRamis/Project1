from django import forms


class ProcessType(forms.Form):

    TYPE_OF_PROCESS = (
        ('fibonacci', 'fibonacci'),
        ('wait', 'wait')
    )
    type_of_process = forms.ChoiceField(choices=TYPE_OF_PROCESS)


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

