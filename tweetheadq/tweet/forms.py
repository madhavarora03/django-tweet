from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'thumbnail']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'textarea textarea-bordered h-48 block mb-4',
                                          'placeholder': 'Your tweet message here...'}),
            'thumbnail': forms.ClearableFileInput(
                attrs={'class': 'block file-input file-input-bordered w-full max-w-xs mb-4'})
        }
