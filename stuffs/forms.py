from django import forms 
from .models import Stuff

class StuffForm(forms.ModelForm):

    class Meta:                     # Meta 類別用於設定這個表單的元數據（組態設定）

        model = Stuff             # 指定這個表單對應的資料庫模型是 Contact
        fields = '__all__'

        widgets = {                             # 自訂 HTML 元件（Widgets）的樣式與屬性
            'user': forms.HiddenInput(attrs={'name':'user' ,'class': 'form-control'}),
            'name': forms.TextInput(attrs={'name':'name' ,'class': 'form-control'}),
            'type': forms.Select(attrs={'name':'type' ,'class': 'form-control'}),
            'district': forms.Select(attrs={'name':'district' ,'class': 'form-control'}),
            'location': forms.TextInput(attrs={'name':'location' ,'class': 'form-control'}),
            'description': forms.Textarea(attrs={'name':'description' ,'class': 'form-control','row':5}),
            'missing_date': forms.DateTimeInput(attrs={'name':'missing_date' ,'class': 'form-control' , 'type':"datetime-local"}),
            'photo_main': forms.FileInput(attrs={'name':'photo_main' ,'class': 'form-control' }),
        }