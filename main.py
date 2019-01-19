import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, requests, cv2, numpy, pyodbc

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '700bad17d5d6443bad2fd69b0da27cdc',
}

conn = http.client.HTTPSConnection('northeurope.api.cognitive.microsoft.com')

def connectSQLDatabase():
    server = 'univision.database.windows.net'
    database = 'UniVision'
    username = 'adminunivision'
    password = '!univision19012019'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def createGroup(groupId, groupName):

    params = urllib.parse.urlencode({})

    body = {
        "name" : '{}'.format(groupName),
    }

    try:
        conn.request("PUT", "/face/v1.0/persongroups/" + groupId + "?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print("GROUP CREATED")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def addPerson(name, targetGroup):

    params = urllib.parse.urlencode({})

    body = {
        "name": '{}'.format(name),
    }

    try:
        conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/persons?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print("PERSON ADDED: ", name)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def addFace(targetName, targetGroup, URL):

    # WARNING: going off the assumption that there are no duplicate names
    listOfPersons = json.loads(listPersonsInGroup(targetGroup))
    personId = ""
    for person in listOfPersons:
        if person["name"] == targetName:
            personId = person["personId"]
            break

    params = urllib.parse.urlencode({})

    body = {
        "url" : '{}'.format(URL)
    }

    try:
        conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/persons/" + personId + "/persistedFaces?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print("FACE ADDED TO", targetName)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# returns a json list of people in a group
def listPersonsInGroup(targetGroup):

    params = urllib.parse.urlencode({})

    try:
        conn.request("GET", "/face/v1.0/persongroups/" + targetGroup + "/persons?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def trainGroup(targetGroup):

    params = urllib.parse.urlencode({})

    try:
        conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/train?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print("GROUP TRAINED")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

cam = cv2.VideoCapture(0)

def takeFrame():
    s, img = cam.read()
    return cv2.imencode(".jpg",img)[1].tostring()

# Returns faceId to be fed into identifyFace, returns -1 (integer) if no face found
def detectFace(imgData):

    headers = {'Content-Type': 'application/octet-stream', 
               'Ocp-Apim-Subscription-Key': '700bad17d5d6443bad2fd69b0da27cdc'}

    url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect'

    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        # 'returnFaceAttributes': '{string}',
    })

    try:
        # response = requests.post(url, data=imgData, headers=headers, params=params)
        response = requests.post(url, headers=headers, data=imgData)
        print(response)
        return response.json()[0]["faceId"]
    except IndexError:
        print("NO FACE DETECTED")
        return -1
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def identifyFace(faceId, targetGroup):

    params = urllib.parse.urlencode({})

    body = {
        'faceIds' : [faceId],
        'personGroupId' : targetGroup
    }

    try:
        conn.request("POST", "/face/v1.0/identify?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())

        if not data or not data[0]["candidates"]:
            raise IndexError()

        candidatePersonId = data[0]["candidates"][0]["personId"]
        listOfPersons = json.loads(listPersonsInGroup(targetGroup))
        for person in listOfPersons:
            if person["personId"] == candidatePersonId:
                print("PERSON IDENTIFIED: " + person["name"])
                break

    except IndexError:
        print("***** Idk something went wrong *****")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def addStudentToDatabase(id, name, programme, faceId, cursor):
    query = "INSERT INTO students (studentID, studentName, studentProgramme, studentFaceID) VALUES ('" + id + "', '" + name + "', '" + programme + "', '" + faceId + "');"
    cursor.execute(query)

def hackCambridgeDataSet():
    createGroup("testgroup", "hello group")
    addPerson("0000000", "testgroup")
    addPerson("1111111", "testgroup")
    addPerson("2222222", "testgroup")
    addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/46854334_1320054438135017_7272253035202478080_o.jpg")
    addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/40646988_1267616973378764_4509956788853932032_n.jpg")
    addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/50425886_1359944970812630_2846946035958284288_o.jpg")
    addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/47173225_1322186427921818_2925789588129579008_o.jpg")
    addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/LRM_EXPORT_471358170522868_20181228_220101328-2.jpeg")
    addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_3102.JPG")
    addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_9449.PNG")
    addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/vsco5a9442a42aaee.JPG")
    addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_1818.JPG")
    addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf1.png")
    addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf2.jpg")
    addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf3.png")
    addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf4.png")
    addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf5.png")
    trainGroup("testgroup")

def hackCambridgeDatabaseSetup():
    addStudentToDatabase("0000000", "Matt", "G400", "1234", cursor)


if __name__ == "__main__":
    cursor = connectSQLDatabase()
    addStudentToDatabase("1234567", "Matt", "G400", "1234", cursor)
    # hackCambridgeDataSet() # Init only once
    listPersonsInGroup("testgroup")
    time.sleep(2) # should replace this with some method that used the gettrainingstatus api
    print('--------------------------')

    try:
        while True:
            imgData = takeFrame()
            detectedFaceId = detectFace(imgData)
            if detectedFaceId != -1:
                identifyFace(detectedFaceId, "testgroup")

    except KeyboardInterrupt:
        conn.close()