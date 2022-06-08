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
                        insert.append(jAux[2].strip().replace("'", ""))

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
                        read.append(jAux[2].strip().replace("'", ""))

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
                        readHybrid.append(jAux[2].strip().replace("'", ""))

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
                        updateHybrid.append(jAux[2].strip().replace("'", ""))

    return updateHybrid


def LoadAndTreatData(dbName):
    insert = getInsertFromRawData(dbName)
    read = getReadFromRawData(dbName)
    insertHybrid = getReadHybridFromRawData(dbName)
    updateHybrid = getUpdateHybridFromRawData(dbName)

    return insert, read, insertHybrid, updateHybrid


def numpyMatrixToListMatrix(numpyMatrix):
    listMatrix = []

    for i in range(len(numpyMatrix)):
        listMatrix.append(numpyMatrix[i].tolist())

    return listMatrix


def updateSheet(sheet, data, startLine, endLine, columnLabel):
    metricRows = numpyMatrixToListMatrix(np.array_split(data, 21))

    startLineIndex = 4
    endLineIndex = 7
    metricCount = 0

    for i in range(len(metricRows)):
        cellList = sheet.range(f'{columnLabel}{startLineIndex}:{columnLabel}{endLineIndex}')

        for j in range(len(cellList)):
            cellList[j].value = float(metricRows[i][j])

        sheet.update_cells(cellList)

        if metricCount < 2:
            startLineIndex += 7
            endLineIndex += 7
            metricCount += 1
        else:
            startLineIndex += 8
            endLineIndex += 8
            metricCount = 0


def loadResultsTxt(fileName):
    fileName = fileName + ".txt"

    with open(fileName, 'r') as file:
        return file.readlines()


def getAllInserts(databasesData):
    inserts = []

    for i in range(0, 7):
        for j in range(0, len(databasesData[0][0]), 7):
            inserts.append(databasesData[0][0][j+i])
            inserts.append(databasesData[1][0][j+i])
            inserts.append(databasesData[2][0][j+i])
            inserts.append(databasesData[3][0][j+i])

    return inserts


def getAllReads(databasesData):
    read = []

    for i in range(0, 7):
        for j in range(0, len(databasesData[0][1]), 7):
            read.append(databasesData[0][1][j + i])
            read.append(databasesData[1][1][j + i])
            read.append(databasesData[2][1][j + i])
            read.append(databasesData[3][1][j + i])

    return read


def getAllInsertsHybrid(databasesData):
    insertsHybrid = []

    for i in range(0, 7):
        for j in range(0, len(databasesData[0][2]), 7):
            insertsHybrid.append(databasesData[0][2][j + i])
            insertsHybrid.append(databasesData[1][2][j + i])
            insertsHybrid.append(databasesData[2][2][j + i])
            insertsHybrid.append(databasesData[3][2][j + i])

    return insertsHybrid


def getAllUpdatesHybrid(databasesData):
    updatesHybrid = []

    for i in range(0, 7):
        for j in range(0, len(databasesData[0][3]), 7):
            updatesHybrid.append(databasesData[0][3][j + i])
            updatesHybrid.append(databasesData[1][3][j + i])
            updatesHybrid.append(databasesData[2][3][j + i])
            updatesHybrid.append(databasesData[3][3][j + i])

    return updatesHybrid


if __name__ == '__main__':
    mariaDBData = LoadAndTreatData("mariadb")
    mongoDB = LoadAndTreatData("mongodb")
    postGreSql = LoadAndTreatData("postgresql")
    redis = LoadAndTreatData("redis")

    databasesData = [mariaDBData, mongoDB, postGreSql, redis]

    insert = getAllInserts(databasesData)
    read = getAllReads(databasesData)
    insertHybrid = getAllInsertsHybrid(databasesData)
    updateHybrid = getAllUpdatesHybrid(databasesData)

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('eth-vs-ton-b8e005fda44c.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open_by_key("142EyP1_sl6gJszKFme9MABFU_yDuJlJLaUJgVAqIMYU").sheet1

    #updateSheet(sheet, insert, 4, 153, "B")
    #updateSheet(sheet, read, 4, 153, "C")
    #updateSheet(sheet, insertHybrid, 4, 153, "D")
    updateSheet(sheet, updateHybrid, 4, 153, "E")

    # cellList = sheet.range(f'k{10}:k{15}')
    #
    # for j in range(len(cellList)):
    #     cellList[j].value = 10
    #
    # sheet.update_cells(cellList)
