from django import forms

class FileForm(forms.Form):
    upFile = forms.FileField(
        label='上传需要抽样的excel文档'
    )


class SelectColForm(forms.Form):
    useSize = forms.BooleanField(required=False, label='固定数量抽样：')
    size = forms.IntegerField(initial=10, min_value=0, max_value=5000)
    useRate = forms.BooleanField(required=False, label='固定比例抽样：')
    rate = forms.IntegerField(initial=10, min_value=0, max_value=100)
    dropDown = forms.ChoiceField(required=True,
                                 label='选择需要抽样的列',
                                 choices=[])
