import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, requests, cv2, numpy, pyodbc

def connectSQLDatabase():
    server = 'univision.database.windows.net'
    database = 'UniVision'
    username = 'adminunivision'
    password = '!univision19012019'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

cursor = connectSQLDatabase()

class FaceID(object):
    """The FaceID Class"""

    conn = http.client.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
    cam = cv2.VideoCapture(0)
    personScanned = ''

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'INSERT_API_KEY',
    }

    def createGroup(self, groupId, groupName):

        params = urllib.parse.urlencode({})

        body = {
            "name" : '{}'.format(groupName),
        }

        try:
            self.conn.request("PUT", "/face/v1.0/persongroups/" + groupId + "?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("GROUP CREATED")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def addPerson(self, name, targetGroup):

        params = urllib.parse.urlencode({})

        body = {
            "name": '{}'.format(name),
        }

        try:
            self.conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/persons?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("PERSON ADDED: ", name)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def addFace(self, targetName, targetGroup, URL):

        # WARNING: going off the assumption that there are no duplicate names
        listOfPersons = json.loads(self.listPersonsInGroup(targetGroup))
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
            self.conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/persons/" + personId + "/persistedFaces?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("FACE ADDED TO", targetName)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # returns a json list of people in a group
    def listPersonsInGroup(self, targetGroup):

        params = urllib.parse.urlencode({})

        try:
            self.conn.request("GET", "/face/v1.0/persongroups/" + targetGroup + "/persons?%s" % params, "{body}", self.headers)
            response = self.conn.getresponse()
            data = response.read()
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def trainGroup(self, targetGroup):

        params = urllib.parse.urlencode({})

        try:
            self.conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/train?%s" % params, "{body}", self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("GROUP TRAINED")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def takeFrame(self):
        s, img = self.cam.read()
        return img, cv2.imencode(".jpg",img)[1].tostring()

    # Returns faceId to be fed into identifyFace, returns -1 (integer) if no face found
    def detectFace(self, imgData):

        detectHeaders = {'Content-Type': 'application/octet-stream', 
                   'Ocp-Apim-Subscription-Key': 'INSERT_API_KEY'}

        url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect'

        params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            # 'returnFaceAttributes': '{string}',
        })

        try:
            # response = requests.post(url, data=imgData, headers=headers, params=params)
            response = requests.post(url, headers=detectHeaders, data=imgData)
            return response.json()[0]["faceId"]
        except IndexError:
            print("NO FACE DETECTED")
            return -1
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def identifyFace(self, faceId, targetGroup):

        params = urllib.parse.urlencode({})

        body = {
            'faceIds' : [faceId],
            'personGroupId' : targetGroup
        }

        try:
            self.conn.request("POST", "/face/v1.0/identify?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = json.loads(response.read())

            if not data or not data[0]["candidates"]:
                raise IndexError()

            candidatePersonId = data[0]["candidates"][0]["personId"]
            listOfPersons = json.loads(self.listPersonsInGroup(targetGroup))
            for person in listOfPersons:
                if person["personId"] == candidatePersonId:
                    print("PERSON IDENTIFIED: " + person["name"])
                    return person["name"]

        except IndexError:
            print("***** Idk something went wrong *****")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def addStudentToDatabase(self, id, name, programme):
        query = "INSERT INTO students (studentID, studentName, studentProgramme) VALUES ('" + id + "', '" + name + "', '" + programme + "');"
        cursor.execute(query)
        cursor.commit()

    def takeAttendance(self, timetableKey):
        try:
            while True:
                img, imgData = self.takeFrame()
                detectedFaceId = self.detectFace(imgData)
                if detectedFaceId != -1:
                    studentId = self.identifyFace(detectedFaceId, "testgroup")
                    if studentId:
                        checkPresentQuery = "SELECT * FROM attendance WHERE (studentID = '" + studentId + "' AND timetableKey = '" + timetableKey + "');"
                        cursor.execute(checkPresentQuery)
                        data = cursor.fetchone()
                        if not data:
                            print('Not in database, add:')
                            addQuery = "INSERT INTO attendance (studentID, timetableKey) VALUES ('" + studentId + "', '" + timetableKey + "');"
                            cursor.execute(addQuery)
                            cursor.commit()
                            self.personScanned = studentId
                        else:
                            print('Attendance already taken')
        except KeyboardInterrupt:
            self.conn.close()

    def getLastPersonScanned(self):
        return self.personScanned

    def getStudentDetails(self, studentId):
        try:
            retrieveDetailsQuery = "SELECT * FROM students WHERE (studentID = '" + studentId + "');"
            cursor.execute(retrieveDetailsQuery)
            return cursor.fetchone()
        except Exception as e:
            print(e)

    def getCourseDetails(self, courseId):
        try:
            retrieveCourseQuery = "SELECT * FROM courses WHERE (courseID = '" + courseId + "');"
            cursor.execute(retrieveCourseQuery)
            return cursor.fetchone()
        except Exception as e:
            print(e)

    def getCourseAttendanceScore(self, studentId, courseId):
        try:
            retrieveTotalNoLecturesQuery = "SELECT timetableKey FROM timetable WHERE (courseID = '" + courseId + "');"
            cursor.execute(retrieveTotalNoLecturesQuery)
            totalNoLectures = len(cursor.fetchall())

            retrieveAllAttendancesQuery = "SELECT * FROM attendance WHERE (studentID = '" + studentId + "');"
            cursor.execute(retrieveAllAttendancesQuery)
            allAttendances = cursor.fetchall()

            totalNoAttendances = 0
            for attendance in allAttendances:
                attendanceQuery = "SELECT courseID FROM timetable WHERE timetableKey = '" + str(attendance[2]) + "';"
                cursor.execute(attendanceQuery)
                lectureCourseId = cursor.fetchone()
                if lectureCourseId:
                  if lectureCourseId[0] == courseId:
                      totalNoAttendances += 1

            score = round((totalNoAttendances/totalNoLectures)*100,1)
            return score, totalNoAttendances, totalNoLectures
        except Exception as e:
            print(e)


    def getOverallAttendanceScore(self, studentId):
        try:
            retrieveStudentCourseChoicesQuery = "SELECT courseID FROM studentsCourseChoices WHERE studentID = '" + studentId + "';"
            cursor.execute(retrieveStudentCourseChoicesQuery)
            studentChoices = cursor.fetchall()

            attendanceSum = 0
            lectureSum = 0

            for course in studentChoices:
                _, attendanceNo, lectureNo = self.getCourseAttendanceScore(studentId, course[0])
                attendanceSum += attendanceNo
                lectureSum += lectureNo

            totalScore = round((attendanceSum / lectureSum) * 100, 1)
            return totalScore

        except Exception as e:
            print(e)  

    def wipeAttendanceLog(self, timetableKey):
        try:
            wipeAttendanceQuery = "DELETE FROM attendance WHERE timetableKey = '" + timetableKey + "';"
            cursor.execute(wipeAttendanceQuery)
            cursor.commit()
        except Exception as e:
            print(e)  

    def getLectureAttendance(self, timetableKey):
        try:
            getAttendedStudents = "SELECT * FROM attendance WHERE timetableKey = '" + timetableKey + "';"
            cursor.execute(getAttendedStudents)
            attendedStudents = cursor.fetchall()

            getCourseId = "SELECT courseID FROM timetable WHERE timetableKey = '" + timetableKey + "';"
            cursor.execute(getCourseId)
            courseId = cursor.fetchone()

            getRegisteredStudents = "SELECT * FROM studentsCourseChoices WHERE courseID = '" + courseId[0] + "';"
            cursor.execute(getRegisteredStudents)
            registeredStudents = cursor.fetchall()

            score = round(len(attendedStudents)/len(registeredStudents)*100,2)
            return score

        except Exception as e:
            print(e)

    def getCourseAttendance(self, courseId):
        try:
            timetableKeys = self.getTimetableKeysFromCourseId(courseId)

            totalAttendees = 0
            for event in timetableKeys:
                getNoAttendees = "SELECT * FROM attendance WHERE timetableKey = '" + str(event) + "';"
                cursor.execute(getNoAttendees)
                attendeesNo = len(cursor.fetchall())
                totalAttendees += attendeesNo
            
            getRegisteredStudents = "SELECT * FROM studentsCourseChoices where courseID = '" + courseId + "';"
            cursor.execute(getRegisteredStudents)
            registeredStudents = len(cursor.fetchall())

            score = round(totalAttendees/(registeredStudents*len(timetableKeys)) * 100, 1)

            return score

        except Exception as e:
            print(e)

    def getTimetableKeysFromCourseId(self, courseId):
        try:
            getTimetableQuery = "SELECT timetableKey FROM timetable WHERE courseID = '" + courseId + "';"
            cursor.execute(getTimetableQuery)
            timetable = cursor.fetchall()

            timetableKeys = []
            for event in timetable:
                timetableKeys.append(event[0])

            return timetableKeys

        except Exception as e:
            print(e)  

    def hackCambridgeTrainInit(self):
        self.createGroup("testgroup", "hello group")
        self.addPerson("0000000", "testgroup")
        self.addPerson("1111111", "testgroup")
        self.addPerson("2222222", "testgroup")
        self.addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/46854334_1320054438135017_7272253035202478080_o.jpg")
        self.addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/40646988_1267616973378764_4509956788853932032_n.jpg")
        self.addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/50425886_1359944970812630_2846946035958284288_o.jpg")
        self.addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/47173225_1322186427921818_2925789588129579008_o.jpg")
        self.addFace("0000000", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Matt/LRM_EXPORT_471358170522868_20181228_220101328-2.jpeg")
        self.addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_3102.JPG")
        self.addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_9449.PNG")
        self.addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/vsco5a9442a42aaee.JPG")
        self.addFace("1111111", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Neil/IMG_1818.JPG")
        self.addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf1.png")
        self.addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf2.jpg")
        self.addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf3.png")
        self.addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf4.png")
        self.addFace("2222222", "testgroup", "https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Faces/Raf/raf5.png")
        self.trainGroup("testgroup")
        time.sleep(2) # Give a second to train database

    def hackCambridgeDatabaseInit(self):
        self.addStudentToDatabase("0000000", "Matt Timmons-Brown", "BEng Computer Science & Electronics")
        self.addStudentToDatabase("1111111", "Neil Weidinger", "BSc Computer Science & Artificial Intelligence")
        self.addStudentToDatabase("2222222", "Rafael Anderka", "BSc Computer Science")

    def getStudentJson(self, studentId):
        studentDetails = self.getStudentDetails(studentId)

        studentDetailsDict = {
            "name" : studentDetails[2],
            "id" : "s" + studentDetails[1],
            "degree" : studentDetails[3]
        }

        return json.dumps(studentDetailsDict)

    def getCoursesJson(self):
        try:
            getCoursesQuery = "SELECT * FROM courses"
            cursor.execute(getCoursesQuery)
            courses = cursor.fetchall()

            jsonObjects = []
            for course in courses:
                
                attendance = self.getCourseAttendance(course[1])

                courseDict = {
                "courseID" : course[1],
                "courseName" : course[2],
                "school" : course[3],
                "courseAbbreviation" : course[4],
                "attendance" : attendance
                }
            
                jsonObjects.append(json.dumps(courseDict))
            
            return jsonObjects

        except Exception as e:
            print(e)

    def getEventsJson(self,courseId):
        try:
            courseDetails = self.getCourseDetails(courseId)

            getTimetable = "SELECT * FROM timetable WHERE courseID = '" + courseId + "';"
            cursor.execute(getTimetable)
            timetable = cursor.fetchall()

            jsonObjects = []
            for event in timetable:
                attendance = self.getLectureAttendance(str(event[0]))

                eventDict = {
                "eventName" : event[4] + " - " + courseDetails[2],
                "start" : event[2],
                "end" : event[3],
                "attendance" : attendance
                }

                jsonObjects.append(json.dumps(eventDict))

            return jsonObjects

        except Exception as e:
            print(e)

    def main(self):
        #self.hackCambridgeTrainInit() # Init only once
        #self.hackCambridgeDatabaseInit() # Also init only once
        #self.listPersonsInGroup("testgroup")
        #print(self.getStudentDetails("0000000"))
        #print(self.getCourseDetails("MATH08057"))
        #print(self.getCourseAttendanceScore("0000000" ,"MATH08057"))
        #print(self.getOverallAttendanceScore("0000000"))
        #self.getStudentJson("0000000")
        #print(self.getLectureAttendance("8"))
        #print(self.getCourseAttendance("MATH08057"))
        #print(self.getTimetableKeysFromCourseId("MATH08057"))
        #self.getCoursesJson()
        #self.getEventsJson("MATH08057")
        self.wipeAttendanceLog("1")
        print('--------------------------')
        self.takeAttendance("1")

if __name__ == "__main__":
    app = FaceID()
    app.main()
