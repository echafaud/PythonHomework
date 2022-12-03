import os

outputParameter = input("Что вы хотите вывести?")
if (outputParameter == "Вакансии"):
    os.system('TableTask.py')
elif (outputParameter == "Статистика"):
    os.system('PdfTask.py')