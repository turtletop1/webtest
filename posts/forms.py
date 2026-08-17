from django import forms 
from .models import Post
from .models import Stuff

class PostForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            
            super(PostForm, self).__init__(*args, **kwargs)

            if user:
                self.fields['stuff'].queryset = Stuff.objects.filter(user=user) 


    class Meta:                     # Meta 類別用於設定這個表單的元數據（組態設定）

        model = Post             # 指定這個表單對應的資料庫模型是 Contact

        fields = '__all__'

        widgets = {                             # 自訂 HTML 元件（Widgets）的樣式與屬性
            'user': forms.HiddenInput(attrs={'name':'user' ,'class': 'form-control'}),
            'stuff': forms.Select(attrs={'name':'stuff' ,'id':'stuff','class': 'form-control'}),
            'title': forms.TextInput(attrs={'name':'title' ,'class': 'form-control'}),
            'status': forms.Select(attrs={'name':'status' ,'class': 'form-control'}),
            'type': forms.Select(attrs={'name':'type' ,'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'name':'due_date' ,'class': 'form-control' , 'type':"datetime-local"}),
            'content': forms.Textarea(attrs={'name':'content' ,'class': 'form-control'}),
            'reward': forms.CheckboxInput(attrs={'name':'reward' ,'class': 'form-control'}),
        }