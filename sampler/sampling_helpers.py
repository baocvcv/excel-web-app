import xlrd
import xlwt

# helper
def get_headers(filePath):
    ' Get excel headers '
    workSheet = xlrd.open_workbook(filePath).sheet_by_index(0)
    headers = workSheet.row_values(0)
    return headers

def do_sampling(sourceFile, config):
    ' Sample sourcefile according to config '
    ' config = {"size":3, "useSize":True, "rate":4, "useRate":False} '
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
    targetSheet = result.add_sheet('Sheet1')
    # formats
    formatDate = xlwt.easyxf(num_format_str='yyyy.mm.dd')
    formatNum = xlwt.easyxf(num_format_str='0')
    # write
    targetSheet.write(0, 0, '序号')
    for i in range(workSheet.ncols):
        targetSheet.row(0).write(i+1, workSheet.cell(0,i).value)
    targetRow = 1
    for i in indices:
        targetSheet.row(targetRow).write(0, targetRow)
        for j in range(workSheet.ncols):
            sourceCell = workSheet.cell(i, j)
            if sourceCell.ctype == 2:
                targetSheet.row(targetRow).write(j+1, sourceCell.value, formatNum)
            elif sourceCell.ctype == 3:
                targetSheet.row(targetRow).write(j+1, sourceCell.value, formatDate)
            else:
                targetSheet.row(targetRow).write(j+1, sourceCell.value)
        targetRow += 1
    return result

