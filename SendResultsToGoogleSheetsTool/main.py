import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np


def getInsertFromRawData(dbName):
    insert = []

    for i in range(2, 10, 3):
        insertAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in insertAux:
            if j.startswith("["):
                jAux = j.split(",")

                keywords = ["[INSERT]", "RunTime(ms)", "Throughput(ops/sec)"]

                if jAux[0].strip() in keywords or jAux[1].strip() in keywords:
                    if "Operations" not in jAux[1].strip() and "Return" not in jAux[1].strip():
                        insert.append(jAux[2].strip())

    return insert


def getReadFromRawData(dbName):
    read = []

    for i in range(1, 10, 3):
        readAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in readAux:
            if j.startswith("["):
                jAux = j.split(",")

                keywords = ["[READ]", "RunTime(ms)", "Throughput(ops/sec)"]

                if jAux[0].strip() in keywords or jAux[1].strip() in keywords:
                    if "Operations" not in jAux[1].strip() and "Return" not in jAux[1].strip():
                        read.append(jAux[2].strip())

    return read


def getReadHybridFromRawData(dbName):
    readHybrid = []

    for i in range(3, 10, 3):
        readHybridAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in readHybridAux:
            if j.startswith("["):
                jAux = j.split(",")

                keywords = ["[READ]", "RunTime(ms)", "Throughput(ops/sec)"]

                if jAux[0].strip() in keywords or jAux[1].strip() in keywords:
                    if "Operations" not in jAux[1].strip() and "Return" not in jAux[1].strip():
                        readHybrid.append(jAux[2].strip())

    return readHybrid


def getUpdateHybridFromRawData(dbName):
    updateHybrid = []

    for i in range(3, 10, 3):
        updateHybridAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in updateHybridAux:
            if j.startswith("["):
                jAux = j.split(",")

                keywords = ["[UPDATE]", "RunTime(ms)", "Throughput(ops/sec)"]

                if jAux[0].strip() in keywords or jAux[1].strip() in keywords:
                    if "Operations" not in jAux[1].strip() and "Return" not in jAux[1].strip():
                        updateHybrid.append(jAux[2].strip())

    return updateHybrid


def LoadAndTreatData(dbName):
    insert = getInsertFromRawData(dbName)
    read = getReadFromRawData(dbName)
    insertHybrid = getReadHybridFromRawData(dbName)
    updateHybrid = getUpdateHybridFromRawData(dbName)

    return insert, read, insertHybrid, updateHybrid


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
    mariaDBData = LoadAndTreatData("mariadb")
    mongoDB = LoadAndTreatData("mongodb")
    #postGreSql = LoadAndTreatData("postgresql")
    redis = LoadAndTreatData("redis")

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('eth-vs-ton-b8e005fda44c.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open_by_key("1_nZLaWe0RleL9vHWVRra3ltOy37VnQJy5SRqrdJNw9c").sheet1

    # updateSheet(sheet, metricsK6, 3, 17)
