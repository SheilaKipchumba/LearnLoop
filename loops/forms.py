from django import forms
from .models import Loop, Comment

class LoopForm(forms.ModelForm):
    class Meta:
        model = Loop
        fields = ['title', 'category', 'difficulty', 'description', 'content', 
                  'video_url', 'attachment', 'is_premium', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a catchy title for your loop'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Briefly describe what this loop is about'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control', 'placeholder': 'Write your micro-lesson here. Keep it concise and focused.'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/... (optional)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }
        help_texts = {
            'content': 'Try to keep your micro-lesson under 500 words for best readability.',
            'video_url': 'Add a video to supplement your lesson (optional).',
            'price': 'Set price in Ksh. Free loops are accessible to everyone.',
        }

    def clean(self):
        cleaned_data = super().clean()
        is_premium = cleaned_data.get('is_premium')
        price = cleaned_data.get('price')

        if is_premium and (price is None or price <= 0):
            self.add_error('price', 'Price must be set for premium loops.')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Share your thoughts or ask a question...',
                'style': 'resize: none;'
            })
        }
