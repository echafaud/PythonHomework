from concurrent.futures import ThreadPoolExecutor
from Splitter import Splitter
from DynamicsCalculator import Calculator
from PdfReport import Report
import os

if __name__ == "__main__":
    fileName = input("Введите название файла: ")
    vacancyName = input("Введите название профессии: ")
    splitter = Splitter(fileName, "CsvFilesByYear", "DataByYear")
    dynamicsCalculator = Calculator(vacancyName)
    with ThreadPoolExecutor(os.cpu_count() * 3) as ex:
        res = ex.map(dynamicsCalculator.GetDynamicsByYear,
                     [f'CsvFilesByYear\\DataByYear{year}.csv' for year in splitter.years], splitter.years)
    generalSalaries, generalCount, vacancySalaries, vacancyCount = dynamicsCalculator.HandleResults(res)
    citiesSalaryData, citiesRatioData = dynamicsCalculator.GetDynamicsByCity(fileName)
    data = [generalSalaries, generalCount, vacancySalaries, vacancyCount, citiesSalaryData, citiesRatioData]
    report = Report(vacancyName)
    report.GeneratePDF(data)
