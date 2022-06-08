import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np


def getRunTimeFromRawData(dbName):
    runTime = []

    for i in range(1, 10):
        runTimeAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in runTimeAux:
            if j.startswith("["):
                jAux = j.split(",")

                if "RunTime" in jAux[1]:
                    runTime.append(jAux[2].strip())

    return runTime


def getThroughputFromRawData(dbName):
    throughput = []

    for i in range(1, 10):
        throughputAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in throughputAux:
            if j.startswith("["):
                jAux = j.split(",")

                if "Throughput" in jAux[1]:
                    throughput.append(jAux[2].strip())

    return throughput

def getAverageLatencyFromRawData(dbName):
    averageLatency = []
    keywords = ["[READ]", "[INSERT]", "[UPDATE]"]

    for i in range(1, 10):
        averageLatencyAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in averageLatencyAux:
            if j.startswith("["):
                jAux = j.split(",")

                if jAux[0] in keywords:
                    if "AverageLatency" in jAux[1]:
                        averageLatency.append(jAux[2].strip())

    return averageLatency


def getMinLatencyFromRawData(dbName):
    minLatency = []
    keywords = ["[READ]", "[INSERT]", "[UPDATE]"]

    for i in range(1, 10):
        minLatencyAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in minLatencyAux:
            if j.startswith("["):
                jAux = j.split(",")

                if jAux[0] in keywords:
                    if "MinLatency" in jAux[1]:
                        minLatency.append(jAux[2].strip())

    return minLatency


def getMaxLatencyFromRawData(dbName):
    maxLatency = []
    keywords = ["[READ]", "[INSERT]", "[UPDATE]"]

    for i in range(1, 10):
        maxLatencyAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in maxLatencyAux:
            if j.startswith("["):
                jAux = j.split(",")

                if jAux[0] in keywords:
                    if "MaxLatency" in jAux[1]:
                        maxLatency.append(jAux[2].strip())

    return maxLatency

def get95thPercentileLatencyFromRawData(dbName):
    percentileLatency = []
    keywords = ["[READ]", "[INSERT]", "[UPDATE]"]

    for i in range(1, 10):
        percentileLatencyAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in percentileLatencyAux:
            if j.startswith("["):
                jAux = j.split(",")

                if jAux[0] in keywords:
                    if "95thPercentileLatency" in jAux[1]:
                        percentileLatency.append(jAux[2].strip())

    return percentileLatency

def get99thPercentileLatencyFromRawData(dbName):
    percentileLatency = []
    keywords = ["[READ]", "[INSERT]", "[UPDATE]"]

    for i in range(1, 10):
        percentileLatencyAux = loadResultsTxt(f"./results/{dbName}/outputRun_{i}")

        for j in percentileLatencyAux:
            if j.startswith("["):
                jAux = j.split(",")

                if jAux[0] in keywords:
                    if "99thPercentileLatency" in jAux[1]:
                        percentileLatency.append(jAux[2].strip())

    return percentileLatency


def LoadAndTreatData(dbName):
    runTime = getRunTimeFromRawData(dbName)
    throughput = getThroughputFromRawData(dbName)
    averageLatency = getAverageLatencyFromRawData(dbName)
    minLatency = getMinLatencyFromRawData(dbName)
    maxLatency = getMaxLatencyFromRawData(dbName)
    ninetyFivethPercentileLatency = get95thPercentileLatencyFromRawData(dbName)
    ninetyNinethPercentileLatency = get99thPercentileLatencyFromRawData(dbName)

    return runTime, throughput, averageLatency, minLatency, maxLatency, ninetyFivethPercentileLatency, ninetyNinethPercentileLatency


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

    columnsLabels = ["B", "C", "D", "E"]

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
    postGreSql = LoadAndTreatData("postgresql")
    redis = LoadAndTreatData("redis")

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('eth-vs-ton-b8e005fda44c.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open_by_key("1_nZLaWe0RleL9vHWVRra3ltOy37VnQJy5SRqrdJNw9c").sheet1

    #updateSheet(sheet, metricsK6, 3, 17)