import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '700bad17d5d6443bad2fd69b0da27cdc',
}

conn = http.client.HTTPSConnection('northeurope.api.cognitive.microsoft.com')

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

# Returns faceId to be fed into identifyFace
def detectFace(URL):

    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        # 'returnFaceAttributes': '{string}',
    })

    body = {
        'url' : URL
    }

    try:
        conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        faceInfo = json.loads(response.read())
        print("FACE DETECTED")

        return [faceInfo[0]["faceId"]] # assumes only one face in image to detect
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def identifyFace(faceId, targetGroup):

    params = urllib.parse.urlencode({})

    body = {
        'faceIds' : faceId,
        'personGroupId' : targetGroup
    }

    try:
        conn.request("POST", "/face/v1.0/identify?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())

        candidatePersonId = data[0]["candidates"][0]["personId"]
        listOfPersons = json.loads(listPersonsInGroup(targetGroup))
        for person in listOfPersons:
            if person["personId"] == candidatePersonId:
                print("PERSON IDENTIFIED: " + person["name"])
                break

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == "__main__":
    createGroup("testgroup", "hello group")
    addPerson("Matt", "testgroup")
    addPerson("Neil", "testgroup")
    addFace("Matt", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/46854334_1320054438135017_7272253035202478080_o.jpg")
    addFace("Matt", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/50425886_1359944970812630_2846946035958284288_o.jpg")
    addFace("Matt", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/LRM_EXPORT_471358170522868_20181228_220101328-2.jpeg")
    addFace("Neil", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_3102.JPG")
    addFace("Neil", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_9449.PNG")
    addFace("Neil", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/vsco5a9442a42aaee.JPG")
    addFace("Neil", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_1818.JPG")

    listPersonsInGroup("testgroup")
    trainGroup("testgroup")
    time.sleep(2)
    print('--------------------------')
    trialFaceId = detectFace("https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/40763831_1267081676765627_1908500290282192896_o.jpg?_nc_cat=111&_nc_ht=scontent-lht6-1.xx&oh=06827214331cb73cd071b45ff628c088&oe=5CB82C5C")
    identifyFace(trialFaceId, "testgroup")
    
    conn.close()

