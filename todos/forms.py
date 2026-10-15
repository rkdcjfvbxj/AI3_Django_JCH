from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "content", "is_completed"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "무엇을 해야 하나요?", "maxlength": 200}),
            "content": forms.Textarea(attrs={"rows": 5, "placeholder": "세부 내용을 입력하세요 (선택)"}),
        }
        error_messages = {"title": {
            "required": "할 일 제목을 입력해주세요.",
            "max_length": "제목은 200자 이하로 입력해주세요.",
        }}
