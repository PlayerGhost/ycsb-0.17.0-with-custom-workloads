import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

def getInsertFromRawData(rawData):
    pass

def getReadFromRawData(rawData):
    pass

def getReadAndUpdateFromRawData(rawData):
    pass


def mariadbLoadData():
    insert = []
    for i in range(9):
        rawData = getInsertFromRawData(f"./results/mariadb/outputRun_{i+1}")

    for i in range(9):
        rawData = getReadFromRawData(f"./results/mariadb/outputRun_{i+1}")

    for i in range(9):
        rawData = getReadAndUpdateFromRawData(f"./results/mariadb/outputRun_{i+1}")


def mariadbLoadData():
    pass

def postgresqlLoadData():
    pass

def redisLoadData():
    pass

def updateSheet(sheet, metrics, startLine, endLine, isNewMetric=False):
    minValues = []
    maxValues = []
    meanValues = []
    medianValues = []
    percentileValues = []

    for i in metrics:
        minValues.append(i['min'])
        maxValues.append(i['max'])
        meanValues.append(i['avg'])
        medianValues.append(i['med'])
        percentileValues.append(i['p(95)'])

    minValues = np.array_split(minValues, 3)
    maxValues = np.array_split(maxValues, 3)
    meanValues = np.array_split(meanValues, 3)
    medianValues = np.array_split(medianValues, 3)
    percentileValues = np.array_split(percentileValues, 3)

    columnsValues = []

    for i in range(3):
        columnValues = []

        columnValues += minValues[i].tolist()
        columnValues += maxValues[i].tolist()
        columnValues += meanValues[i].tolist()
        columnValues += medianValues[i].tolist()
        columnValues += percentileValues[i].tolist()

        columnsValues.append(columnValues)

    columnsLabels = ["C", "D", "E"]

    for i in range(len(columnsLabels)):
        cellList = sheet.range(f'{columnsLabels[i]}{startLine}:{columnsLabels[i]}{endLine}')

        for j in range(len(cellList)):
            cellList[j].value = columnsValues[i][j]

        sheet.update_cells(cellList)

def loadResultsTxt(fileName):
    fileName = fileName + ".txt"

    with open(fileName, 'r') as file:
        return file.readlines()

if __name__ == '__main__':

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('eth-vs-ton-b8e005fda44c.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open_by_key("1_nZLaWe0RleL9vHWVRra3ltOy37VnQJy5SRqrdJNw9c").sheet1

    #updateSheet(sheet, metricsK6, 3, 17)