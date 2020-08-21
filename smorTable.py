import re
import copy


class course:
    def __init__(self, name, startHour, startMin, endHour, endMin):
        self.name = name
        self.startHour = startHour
        self.startMin = startMin
        self.endHour = endHour
        self.endMin = endMin


class CourseClass:
    def __init__(self, name):
        self.name = name
        self.sList = []  #section list

    def getName(self):
        return self.name

    def isSame(self, course):
        if self.name == course.name:
            return True
        return False

    def checkSection(self, sectionName):
        for s.name in self.sList:
            if s == sectionName:
                return 1
        return 0

    def addSection(self, Section):
        self.sList.append(Section)


class DegCourseList:
    def __init__(self, degree):
        self.cList = []
        self.degree = degree

    #takes class course
    def addCourse(self, course):
        self.cList.append(course)

    #takes string course
    def courseExists(self, course):
        for c in self.cList:
            if c.name == course:
                return 1
        return False


class Section:
    def __init__(self, name, startHour, startMin, endHour, endMin):
        self.name = name
        self.startHour = startHour
        self.startMin = startMin
        self.endHour = endHour
        self.endMin = endMin

    def isSame(self, section):
        if self.name == section.name:
            return True
        return False


def compareTimes(prevEndHour, startHour):
    if (prevEndMin < 0):
        return False
    if prevEndHour < 8:
        prevEndHour += 12
    if startHour < 8:
        startHour += 12
    return prevEndHour > startHour


def getSectionFromCourse(cName):
    degree = re.search(r'\((.*?)\)',cName).group(1)
    degree = degree.strip('()')
    return re.split('-', degree)[1]

def addSection2Course(course, cName ):
    #get section of course
    section = getSectionFromCourse(cName)

    #see if section exists
    found = 0
    for s in course.sList:
        if section == s:
            found = 1
            break

    if found == 0:
        course.sList.append(section)


def getNameFromCourse(cName):
    m = re.split('\(', cName)
    return m[0]

def addCourse2cList(degree, cName):
    #get name of the course
    name = getNameFromCourse(cName)

    #see if course already in list
    found = 0
    for n in degree.cList:
        if name == n.name:
            found = 1
            break

    if found == 0:
        degree.cList.append(CourseClass(name))
        addSection2Course(degree.cList[len(degree.cList) - 1], cName)
    else:
        addSection2Course(n, cName)


def getDegFromCourse(cName):
    degree = re.search(r'(.*?)', cName)
    degree = degree.strip('()')
    return re.split('-', degree)[0]

def addCourse(cName, courseList):
    #get degree name of the course
    degree = getDegFromCourse(cName)

    #see if degree already added
    found = 0
    for d in courseList:
        if degree == d.degree:
            found = 1
            break

    if found == 0:
        courseList.append(DegCourseList(degree))
        addCourse2cList(courseList[len(courseList) - 1], cName)
    else:
        addCourse2cList(d, cName)


def processRows(list, dayOfTheWeek, table, courseList):
    hrCount = 0
    count = 0
    startHour = 8
    startMin = 0
    endHour = 0
    endMin = 0
    for j in range(6, len(list)):

        #check if course
        if list[j] != "" and not list[j].isdigit() and not list[j].isspace():
            cName = list[j][:]
            cName = re.sub('[ ]', '', cName)
            cName = cName.lower()
            if cName not in courseList:
                courseList.append(cName)
            duration = 0
            if cName.find("lab") != -1 or cName.find("(m") != -1:
                endMin = startMin
                endHour = (startHour + 3) % 12
                #duration += 180

            elif cName.find("english") != -1:
                endMin = startMin
                endHour = (startHour + 2) % 12
                #duration += 120

            else:
                # duration += 90
                endMin = (startMin + 30) % 60
                if endMin == 0:
                    endHour = startHour + 2
                else:
                    endHour = startHour + 1

                if endHour > 12:
                    endHour -= 12

            c = course(cName, startHour, startMin, endHour, endMin)
            if (table[dayOfTheWeek][count] == None):
                table[dayOfTheWeek][count] = []
                table[dayOfTheWeek][count].append(c)
            else:
                table[dayOfTheWeek][count].append(c)
        count += 1
        if hrCount == 5:
            startHour += 1
            if startHour > 12:
                startHour -= 12
            startMin = 0
            hrCount = 0
        else:
            startMin = (startMin + 10) % 60
            hrCount += 1


def getDegreeName(degreePlusSection):
    tempList = degreePlusSection.split("-")
    degName = tempList[0]
    if len(tempList) > 2:
        sectionName = tempList[2][:2]

    else:
        if len(tempList[1]) > 2:
            sectionName = tempList[1][:2]
        else:
            sectionName = tempList[1]
    return [degName, sectionName]


def createDegreeCourseStructure(table, completeCourseList):
    megaList = []
    count = 0
    for courseName in completeCourseList:
        count += 1
        i = len(courseName) - 2
        degreePlusSection = ""
        while courseName[i] != "(" and i >= 0:
            degreePlusSection = courseName[i] + degreePlusSection
            i -= 1
        cName = ""
        for x in range(i):
            cName += courseName[x]

        tempResult = getDegreeName(copy.deepcopy(degreePlusSection))
        degName = tempResult[0]
        sectionName = tempResult[1]

        newDegreeCourseObject = DegCourseList(degName)
        newCourseObject = CourseClass(cName)
        newSectionObject = Section(sectionName, -1, -1, -1, -1)
        newCourseObject.addSection(newSectionObject)
        uniqueDegree = True
        if len(megaList) > 0:
            for degreecourse in megaList:
                #if the degree exists
                if degName == degreecourse.degree:
                    uniqueDegree = False
                    if degreecourse.courseExists(
                            newCourseObject.name) == False:
                        degreecourse.addCourse(newCourseObject)
                    else:
                        for c in degreecourse.cList:
                            if c.getName() == newCourseObject.getName():
                                exists = False
                                for secName in c.sList:
                                    if newSectionObject.name == secName.name:
                                        exists = True
                                if exists == False:
                                    c.addSection(newSectionObject)

            if uniqueDegree == True:
                newDegreeCourseObject.addCourse(newCourseObject)
                megaList.append(newDegreeCourseObject)
        else:
            newDegreeCourseObject.addCourse(newCourseObject)
            megaList.append(newDegreeCourseObject)
    return megaList


def createTable(table, file, courseList):
    file = open(file, "r")
    line = file.readlines()
    dayOfTheWeek = ""

    for i in range(4, len(line)):
        list = line[i].split(";")

        #set next day
        if list[0] != "":
            days = list[0].split(" ")
            dayOfTheWeek = days[0]
        processRows(list, dayOfTheWeek, table, courseList)


table = {
    "Monday": [None] * 100,
    "Tuesday": [None] * 100,
    "Wednesday": [None] * 100,
    "Thursday": [None] * 100,
    "Friday": [None] * 100,
}
completeCourseList = []

# filename = "timeTable.csv"  #input("Enter the csv file's name or path: ")
# outputFile = open("OutputTimeTable.txt", "a+")
# separator = "#####################################\n#####################################\n#####################################\n"
# # print("\nComplete Courses List:\n\n")
# createTable(table, filename, completeCourseList)
# completeCourseList.sort()
# modifiedList = createDegreeCourseStructure(table, completeCourseList)
# print(modifiedList)

if __name__ == "__main__":
    table = {
        "Monday": [None] * 100,
        "Tuesday": [None] * 100,
        "Wednesday": [None] * 100,
        "Thursday": [None] * 100,
        "Friday": [None] * 100,
    }
    completeCourseList = []

    filename = "timeTable.csv"  #input("Enter the csv file's name or path: ")
    outputFile = open("OutputTimeTable.txt", "a+")
    separator = "#####################################\n#####################################\n#####################################\n"
    # print("\nComplete Courses List:\n\n")
    createTable(table, filename, completeCourseList)
    completeCourseList.sort()

    #creating the structure that stores all courses alongwith degrees
    megaList = createDegreeCourseStructure(table, completeCourseList)

    input("MegaList is ready but section's timings and days are not")

    while True:
        print("\nComplete Courses List:\n\n")

        x = 1
        for courseName in completeCourseList:
            print(str(x) + ". " + courseName)
            x += 1

        prevEndHour = -1
        prevEndMin = -1
        coursesStr = str(
            input(
                "Enter the numbers corresponding to the courses you want separated by a comma(Type 'exit' to close the program): "
            ))
        #coursesStr = "Theory of Automata (BCS-5C)/Software Design & Analysis (BCS-5C)/Numerical Computing (BCS-5C)/Computer Networks (BCS-5C)/Computer Networks Lab  (BCS-5C1, BCS-5C2)"
        if coursesStr == "exit": break

        #outputFile.write(coursesStr + '\n\n')
        print('\n\n')
        coursesList = coursesStr.split(",")
        selectedCourses = []
        for index in coursesList:
            ind = int(index)
            selectedCourses.append(completeCourseList[ind - 1])
            outputFile.write(completeCourseList[ind - 1] + "; ")
        outputFile.write("\n")

        i = 0
        days = 0
        courses = [""] * 5
        for key in table:
            print("####################################\n")
            print(key + ":\n")
            outputFile.write("####################################\n")
            outputFile.write(key + ":\n")

            prevEndMin = prevEndHour = -1
            for i in range(len(table[key])):
                if table[key][i] != None:
                    clashCount = 0
                    for j in range(len(table[key][i])):
                        if table[key][i][j].name in selectedCourses:
                            tempCourse = table[key][i][j]
                            clashCount += 1
                            if (compareTimes(
                                    prevEndHour + float(prevEndMin / 60),
                                    tempCourse.startHour +
                                    float(tempCourse.startMin / 60))):
                                clashCount += 1

                            prevEndHour = tempCourse.endHour
                            prevEndMin = tempCourse.endMin

                            courses[days] += str(
                                tempCourse.name) + '\nStart: ' + str(
                                    tempCourse.startHour) + ":" + str(
                                        tempCourse.startMin) + '\nEnd: ' + str(
                                            tempCourse.endHour) + ":" + str(
                                                tempCourse.endMin) + '\n'
                    if clashCount > 1:
                        courses[days] += "<<<CLASH EXISTS>>>\n\n"

            if courses[days] != "":
                print(courses[days] + '\n')
                outputFile.write(courses[days] + '\n')
            days += 1
        print(separator)
        outputFile.write(separator)

        while True:
            cont = input("Continue? y/n:")
            if cont == "n" or cont == "N":
                exit()
            elif cont == "y" or cont == "Y":
                break
