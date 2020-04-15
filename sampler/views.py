from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.urls import reverse

from os.path import join
from datetime import datetime
from mimetypes import guess_type

import xlrd
import xlwt

from .forms import FileForm, SelectColForm
from .models import ExcelDocument

# TODO: move these somewhere else
# helper
def get_headers(filePath):
    workSheet = xlrd.open_workbook(filePath).sheet_by_index(0)
    headers = workSheet.row_values(0)
    return headers

def do_sampling(sourceFile, config):
    workSheet = xlrd.open_workbook(sourceFile).sheet_by_index(0)
    # sampling
    dpts = workSheet.col_values(int(config['dropDown']))
    indices = []
    sampleSize = config['size'] if config['useSize'] else 0
    sampleRate = config['rate'] if config['useRate'] else 0

    nEntry = workSheet.nrows
    start = 1
    while start < nEntry:
        end = start
        while end < nEntry and dpts[start] == dpts[end]:
            end += 1

        size = end - start
        realSampleSize = max(sampleSize, sampleRate*size/100)
        step = max(size / realSampleSize, 1)
        for i in range(int(realSampleSize)):
            val = int(start + i * step)
            if val >= end:
                break
            indices.append(val)
        start = end
    
    # create workbook
    result = xlwt.Workbook()
    sheet1 = result.add_sheet('Sheet1')
    # formats
    formatDate = xlwt.easyxf(num_format_str='yyyy.mm.dd')
    formatNum = xlwt.easyxf(num_format_str='0')
    # write
    sheet1.write(0, 0, '序号')
    for i in range(workSheet.ncols):
        sheet1.row(0).write(i+1, workSheet.cell(0,i).value)
    targetRow = 1
    for i in indices:
        for j in range(workSheet.ncols):
            sheet1.row(targetRow).write(j, workSheet.cell(i,j).value)
        targetRow += 1
    saveTo = join(settings.MEDIA_ROOT, 'result.xlsx')
    result.save(saveTo)
    return saveTo

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
            filename = do_sampling(sourceFile, form.cleaned_data)
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