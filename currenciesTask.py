from currenciesParser import CurrenciesParser
from Splitter import Splitter

fileName = "vacancies_dif_currencies.csv"
# fileName = "TestFile.csv"
#splitter = Splitter(fileName, "CsvFilesCurrencyByYear", "CurrencyByYear")
currenciesParser = CurrenciesParser(fileName)
convertedCurrencies = currenciesParser.ConverToRub()