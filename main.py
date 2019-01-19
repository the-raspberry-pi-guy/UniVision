import http.client, urllib.request, urllib.parse, urllib.error, base64, json

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '700bad17d5d6443bad2fd69b0da27cdc',
}

conn = http.client.HTTPSConnection('northeurope.api.cognitive.microsoft.com')

def createGroup(groupID, groupName):

    params = urllib.parse.urlencode({})

    body = {
            "name" : '{}'.format(groupName),
            }

    try:
        conn.request("PUT", "/face/v1.0/persongroups/" + groupID + "?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
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
        print(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def addFaces(targetName, targetGroup, URL):


if __name__ == "__main__":
#    createGroup("testgroup", "hello group")
    addPerson("Matt", "testgroup")
