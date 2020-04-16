from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.urls import reverse

from os.path import join
from datetime import datetime
from mimetypes import guess_type

from .forms import FileForm, SelectColForm
from .models import ExcelDocument
from .sampling_helpers import get_headers, do_sampling

# Create your views here.
def index(request):
    ' View for uploading the document '
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['upFile'])
            newFile = ExcelDocument(docFile=request.FILES['upFile'])
            newFile.save()
            return HttpResponseRedirect(reverse('sampler:do-sampling',
                                                args=(newFile.id,)))
    form = FileForm()
    return render(
        request=request,
        template_name='sampler/index.html',
        context={'form': form},
    )

def SetParam(request, doc_id):
    ' Sets the sampling parameters and do sampling '
    sourceFile = join(
        settings.MEDIA_ROOT,
        ExcelDocument.objects.get(pk=doc_id).docFile.name
    )
    params = get_headers(sourceFile)
    params = [(i, h) for i, h in enumerate(params)]
    if request.method == 'POST':
        form = SelectColForm(request.POST, request.FILES)
        form.fields['dropDown'].choices = params
        if form.is_valid():
            # save the sampling result
            result = do_sampling(sourceFile, form.cleaned_data)
            filename = join(settings.MEDIA_ROOT, 'result_tmp.xlsx')
            result.save(filename)
            # let user download the result
            response = FileResponse(open(filename, 'rb'))
            response['content_type'] = guess_type(filename)
            response['Content-Disposition'] = 'attachment;'\
                'filename=result_%d.xlsx' % datetime.now().microsecond
            return response
    form = SelectColForm()
    form.fields['dropDown'].choices = params
    return render(
        request,
        template_name='sampler/set_param.html',
        context={'form': form, 'doc_id': doc_id}
    )