from django import forms
from django.core import validators


# # 1.10 方法二
# def must_be_empty(value):
#     if value:
#         raise forms.ValidationError('is not empty')


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Please verify your email address')  # 1.12 方法三
    suggestion = forms.CharField(widget=forms.Textarea)  # 一个自定义widget, **widget是事情是如何被表现到html的
    
    # 1.8 自定义一个field验证, 将cleaning看成一个field处理
    # honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label='Leave empty')

    # def clean_honeypot(self):
    #     honeypot = self.cleaned_data['honeypot']    # 因为我们想要里面的数据
    #     if len(honeypot):                           # 如果honeypot有length, 即里面有东西,
    #         raise forms.ValidationError(            # 那么我们想要引发一个ValidationError
    #             'honeypot should be left empty. Bad bot!')
    #     return honeypot                             # 最后不管怎样,返回honeypot, 我们要将数据发回去,
    #                                                 # 实际上我们发送的是form自身, 但是我们肯定???, 我们要将全部发送回去

    # 1.10 方法一, 用MaxLengthValidator()
    # honeypot = forms.CharField(required=False,
    #                            widget=forms.HiddenInput,
    #                            label='Leave empty',
    #                            validators=[validators.MaxLengthValidator(0)])

    # 1.10 方法二, 自定义validators
    # honeypot = forms.CharField(required=False,
    #                            widget=forms.HiddenInput,
    #                            label='Leave empty',
    #                            validators=[must_be_empty])

    # 1.12 方法三
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')  # 因为.get('email')就像一个字典,所以可以做email = cleaned_email['email']
        verify = cleaned_data.get('verify_email')

        if email != verify:
            raise forms.ValidationError(
                'You need to enter the same email in both fields')
