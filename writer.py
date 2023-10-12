import xlsxwriter
from queue import Queue

def write_to_xlsx(filename: str, titles: list, data: Queue):
    workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
    worksheet = workbook.add_worksheet(filename)
    row = 0
    column = 0
    for item in titles:
        worksheet.write(row, column, item)
        column += 1

    while not data.empty():
        car = data.get()
        row += 1
        column = 0
        for value in car:
            worksheet.write(row, column, value)
            column += 1
    print("finish")
    workbook.close()