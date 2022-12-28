import pandas as pd


class Calculator:
    def __init__(self, vacancyName, areaName):
        self.vacancyName = vacancyName
        self.areaName = areaName

    def GetDynamicsByYear(self, fileName, year):
        # fileName, year = data
        generalDf = self.GetDataByYear(fileName, areaName=self.areaName)
        dfByParameters = self.GetDataByYear(fileName, self.vacancyName, self.areaName)
        res = (year, self.GetSalariesData(generalDf), self.GetDataCount(generalDf),
               self.GetSalariesData(dfByParameters), self.GetDataCount(dfByParameters))
        # print(multiprocessing.current_process().name, fileName, res)
        # , areaName = self.areaName
        return res

    def GetDataByYear(self, fileName, vacancyName=None, areaName=None):
        df = pd.read_csv(fileName)
        if areaName is not None:
            df = df[df["area_name"] == areaName]
        if vacancyName is not None:
            df = df[df["name"].str.contains(vacancyName)]
        x = len(df)
        return df

    def GetSalariesData(self, df):
        # df["salary"] = df[['salary_from', 'salary_to']].mean(axis=1)
        return int(df["salary"].mean()) if len(df) > 0 else 0

    def GetDataCount(self, df):
        return len(df)

    def GetDynamicsByCity(self, fileName):
        df = pd.read_csv(fileName)
        df['count'] = df.groupby('area_name')['area_name'].transform('count')
        vacanciesCount = len(df)
        tempDf = df[df['count'] / vacanciesCount >= 0.01]
        return self.GetCitySalariesData(tempDf), self.GetCityRatioData(tempDf, vacanciesCount)

    def GetCitySalariesData(self, df):
        tempDf = df.copy()
        # tempDf["salary"] = tempDf[['salary_from', 'salary_to']].mean(axis=1)
        tempDf = tempDf.groupby('area_name')['salary'].mean().sort_values(ascending=False)
        tempDf = tempDf.head(10).apply(lambda x: int(x)).to_dict()
        return tempDf

    def GetCityRatioData(self, df, vacanciesCount):
        tempDf = df.copy()
        tempDf["ratio"] = (tempDf["count"] / vacanciesCount)
        tempDf = tempDf.groupby('area_name')['ratio'].mean().sort_values(ascending=False)
        tempDf = tempDf.head(10).apply(lambda x: round(x, 4)).to_dict()
        return tempDf

    def HandleResults(self, result):
        generalSalaries, generalCount, vacancySalaries, vacancyCount = {}, {}, {}, {}
        for dataYear in result:
            generalSalaries[dataYear[0]] = dataYear[1]
            generalCount[dataYear[0]] = dataYear[2]
            vacancySalaries[dataYear[0]] = dataYear[3]
            vacancyCount[dataYear[0]] = dataYear[4]
        print("Динамика уровня зарплат по годам и региону:", generalSalaries)
        print("Динамика количества вакансий по годам и региону:", generalCount)
        print("Динамика уровня зарплат по годам для выбранной профессии:", vacancySalaries)
        print("Динамика количества вакансий по годам для выбранной профессии:", vacancyCount)
        return generalSalaries, generalCount, vacancySalaries, vacancyCount
