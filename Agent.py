# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.

from PIL import Image
from PIL import ImageChops
from PIL import ImageOps
from decimal import Decimal

import numpy
import math
import collections
import operator

ptype = ""
q = []
a = ['1', '2', '3', '4', '5', '6']
probA = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
questions = collections.OrderedDict()
answers = collections.OrderedDict()
qna = collections.OrderedDict()
problem = collections.OrderedDict()


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, p):
        global q
        global ptype
        global questions
        global problem
        global answers

        pname = p.name
        ptype = p.problemType
        figures = p.figures

        if "Basic Problem B-12" in pname:
            print(pname + "\n" + ptype)

            if "2x2" in ptype:
                q = ['A', 'B', 'C']
                row = [['A', 'B']]
                col = [['A', 'C']]
                r = ['C']
                c = ['B']
            else:
                q = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                row = [['A', 'B', 'C'], ['D', 'E', 'F']]
                col = [['A', 'D', 'G'], ['B', 'E', 'H']]
                r = ['G', 'H']
                c = ['C', 'F']

            # traverse through each object in problem and save it in a dictionary called problem
            self.getObjects(figures)

            # traverse through problem dictionary and order questions and answers in different dictionaries
            self.fillQA(problem, q, a)

            print(questions)
            print(answers)
            # search for patterns in images
            # img1 = Image.open(questions['A'])
            # img2 = Image.open(questions['B'])

            horizontaltrans = self.findPatterns(row)
            verticaltrans = self.findPatterns(col)

            hans = self.findAnswers(horizontaltrans, r)
            vans = self.findAnswers(verticaltrans, c)

            hansorder = self.rankAnswers(hans)
            vansorder = self.rankAnswers(vans)

            print("------------- Answers for horizontal trans -------------")
            print(hansorder)

            print("------------- Answers for vertical trans -------------")
            print(vansorder)

            finalans = self.findBestAnswer(hansorder, vansorder)

            print("------------- Answers found in order of probability -------------")
            print(finalans)
            #img1 = Image.open("Problems/Basic Problems B/Basic Problem B-12/A.png")
            #img2 = Image.open("Problems/Basic Problems B/Basic Problem B-12/B.png")

            #img1.save('1.png')
            #img2.save('2.png')

            #img1 = ImageChops.invert(img1)
            #img2 = ImageChops.invert(img2)
            #print(img1.getbbox())
            #print(img2.getbbox())

            #img1 = img1.convert("1")
            #img2 = img2.convert("1")



            #diff = Image.add(img1, img2)
            #diff = ImageChops.invert(diff)

            # DARKER == returns all black pixels from two images [both images combined]
            # LIGHTER == returns what is common between two [common between two images]
            # MULTIPLY == similar effect to darker (for now) [both images combined]
            # ADD == similar effect to lighter (for now) [common between two images]
            # BLEND with alpha 1 == returns second image, with alpha 0 == returns first image [one of two images]
            # SUBTRACT == returns empty image
            # DIFFERENCE == similar to subtract (for now)

            #diff.save('3.png')

        return 1

    # initial setup function
    def getObjects(self, figurelist):
        for f in figurelist:
            fileuri = figurelist[f].visualFilename
            '''
            #h1 = Image.open(fileuri).histogram()
            #print(h1)
            #break
            # here open file and analyze
            #print(f)
            #print(fileuri)
            '''
            problem[f] = fileuri

    # initial setup function
    def fillQA(self, p, orderQ, orderA):
        for i in orderQ:
            questions[i] = p[i]
            qna[i] = p[i]

        for j in orderA:
            answers[j] = p[j]
            qna[j] = p[j]

    def findPatterns(self, cmpList):
        transformations = {'fill': '', 'difference': '', 'flip': '', 'mirror': ''}
        print('------------------------ FINDING PATTERNS ....... --------------------------')
        for a in cmpList:
            imglist = []
            for b in a:
                print("img name" + b)
                imgpath = qna[b]
                print(imgpath)
                img = Image.open(imgpath)
                imglist.append(img)

            # end of inner loop we have list of images in imglist for a given row/col
            # now we can find different transformations for given images
            print('finished getting all images in row/col .........')

            # FILL TRANSFORMATION
            if transformations['fill'] != 'na':
                fill = self.getFillRatio(imglist, transformations['fill'])
                transformations['fill'] = fill

            if transformations['difference'] != 'na':
                diff = self.getDifference(imglist, transformations['difference'])
                # print("DIFF IS BEING SET TO ---------- %.2f" % (diff))
                transformations['difference'] = diff

            if transformations['flip'] != 'na':
                flip = self.getFlipDiff(imglist, transformations['flip'])
                transformations['flip'] = flip

            if transformations['mirror'] != 'na':
                mirror = self.getMirrorDiff(imglist, transformations['mirror'])
                transformations['mirror'] = mirror

        print("--------- PATTERNS FOUND ------------")
        print(transformations)
        return transformations

    def findAnswers(self, transformations, rc):
        global ptype
        global questions
        global answers
        global a
        probableanswers = {}
        print('finding answers .......')
        '''
        for t in transformations:
            if transformations[t] != 'na':
                if t == 'fill':
                    target = transformations[t]
                    if ptype == '3x3':
                        # print("finding answer for 3x3")
                        img1 = Image.open(questions['G'])
                        img2 = Image.open(questions['H'])
                        img1ratio = self.getFillRatio(img1)
                        img2ratio = self.getFillRatio(img2)
                        newratio = img2ratio/img1ratio
        '''
        for i in a:
            imglist = list(rc)
            imglist.append(i)
            '''
            for j in rc:
                #qimg = Image.open(questions[j])
                imglist.append(qimg)
            '''
            il = [imglist]
            p = self.findPatterns(il)
            prob = self.comparePatterns(transformations, p)
            probableanswers[i] = prob

        return probableanswers

    def comparePatterns(self, giventrans, predictedtrans):
        keylist = giventrans.keys()
        percentdiff = 0.0

        for k in keylist:
            givenvalue = giventrans[k]
            predictedvalue = predictedtrans[k]
            if givenvalue != 'na' and predictedvalue != 'na':
                if givenvalue + predictedvalue != 0:
                    # percentdiff += (abs((givenvalue - predictedvalue)) / ((givenvalue + predictedvalue) / 2)) * 100
                    percentdiff += self.getPercentageDiff(givenvalue, predictedvalue)
            else:
                percentdiff += 100000

        # print("PROBABILITY OF ANSWER")
        # print(percentdiff)
        return percentdiff

    def rankAnswers(self, dict):
        sortedlist = sorted(dict.items(), key=operator.itemgetter(1))
        anslist = []

        for i in sortedlist:
            anslist.append(i[0])

        print("----- SORTED ANSWER LIST -----")
        print(sortedlist)
        return anslist

    def findBestAnswer(self, a, b):
        finalansdict = {}
        for i in range(0, len(a)):
            for j in range(0, len(b)):
                if a[i] == b[j]:
                    finalansdict[a[i]] = i+j
                    break
        finalanslist = self.rankAnswers(finalansdict)
        return finalanslist

    # transformation function
    def getFillRatio(self, imglist, target):
        # getting black pixel ratio from image list that is passed in
        fillratiolist = []
        for img in imglist:
            blackCount = 0
            totalCount = 0
            img = img.convert('RGB')
            pixels = list(img.getdata())

            for p in pixels:
                #print(p)
                if p == (0, 0, 0):
                    blackCount += 1
                totalCount += 1
            fillratio = blackCount / totalCount
            fillratiolist.append(fillratio)

        print("FILL RATIO LIST: ")
        print(fillratiolist)

        # finding geometric progression between ratios
        if len(fillratiolist) == 2:
            # print("2x2")
            value1 = fillratiolist[0]*1000
            value2 = fillratiolist[1]*1000
            # fr = (abs((value2 - value1))/((value2 + value1)/2))*100
            fr = self.getPercentageDiff(value2, value1)

        else:
            # finding percentage difference
            value1 = fillratiolist[0]*1000
            value2 = fillratiolist[1]*1000
            value3 = fillratiolist[2]*1000
            # print(value1)

            if value1 + value2 != 0:
                # fr1 = (abs((value2 - value1))/((value2 + value1)/2))*100
                fr1 = self.getPercentageDiff(value2, value1)
            else:
                fr1 = 0

            if value2 + value3 != 0:
                # fr2 = (abs((value3 - value2))/((value3 + value2)/2))*100
                fr2 = self.getPercentageDiff(value3, value2)

            else:
                fr2 = 0

            perdiff = fr2 - fr1

            # print(fr2)
            # print(fr1)

            # if percentage difference between img1, img2 and img2, img3 is greater than 10% then return na
            # which means get fill ratio does not count
            # else return the average of percentage differences

            if perdiff > 10:
                fr = 'na'

            else:
                fr = ((fr2+fr1)/2)
                if target != '':
                    if target + fr != 0:
                        # perdiff = (abs((target - fr)) / ((target + fr) / 2)) * 100
                        perdiff = self.getPercentageDiff(target, fr)
                    else:
                        perdiff = 0

                    if perdiff > 5:
                        fr = 'na'
                    else:
                        fr = (target + fr) / 2
        # print("FILL RATIO FOUND TO BE ----- %.2f" % (perdiff))
        return fr

    # transformation function
    def getDifference(self, imglist, target):
        # finding pixel difference between images using the get distance function
        # get distance function finds euclidean distance for each RGB pixel value
        if len(imglist) == 2:
            img1 = imglist[0]
            img2 = imglist[1]
            dist = self.getDistance(img1, img2)
            print("<><><><><> dist1 -------- %.2f" % (dist))
            return dist

        # if 3x3 matrix then find percentage difference between img1, img2 difference and
        # img2, img3 difference
        else:
            img1 = imglist[0]
            img2 = imglist[1]
            img3 = imglist[2]
            dist1 = self.getDistance(img1, img2)
            dist2 = self.getDistance(img2, img3)

            print("<><><><><> dist1 -------- %.2f" % (dist1))
            print("<><><><><> dist2 -------- %.2f" % (dist2))

            if dist1 + dist2 != 0:
                print("FINDING --- PERCENT DIFFERENCE FOR IMG DIFF VALUES")
                # diff = (abs(dist1-dist2)/((dist1+dist2)/2))*100
                diff = self.getPercentageDiff(dist1, dist2)
                print(diff)
            else:
                diff = 0

            # dist = (dist1+dist2)/2
            # print("-------- AVG DIST FOUND TO BE %.2f" % (dist))
            if diff > 10:
                return 'na'
            else:
                if target != '':
                    print(target)
                    if target != 0:
                        if target + diff != 0:
                            # print("%.2f" % (dist))
                            # perdiff = (abs((target - diff)) / ((target + diff) / 2)) * 100
                            perdiff = self.getPercentageDiff(target, diff)
                        else:
                            perdiff = 0

                        print("PER DIFF %0.2f" % (perdiff))
                        print(target)
                    else:
                        perdiff = diff
                    if perdiff > 5:
                        return 'na'
                    else:
                        diff = (target + diff)/2
                return diff

            # h = ImageChops.difference(imglist[0], imglist[1]).histogram()

    # generic function
    def getDistance(self, img1, img2):
        # given two images find euclidean distance between each pixel value (RGB)
        # returns total distance between two images
        img1 = img1.convert('1')
        img2 = img2.convert('1')
        imgd1 = list(img1.getdata())
        imgd2 = list(img2.getdata())

        if len(imgd1) == len(imgd2):
            d = 0
            for i in range(0, len(imgd1)):
                p1 = imgd1[i]
                p2 = imgd2[i]
                # below formula for RGB
                #distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)+((p1[2]-p2[2])**2))

                distance = abs(p1-p2)
                d += distance
            return d

        else:
            print('ERROR: IN getDistance function ---  images do not have same number of pixels')

    # generic function
    def getPercentageDiff(self, x, y):
        percentdiff = (abs(x - y) / ((x + y) / 2))*100
        return percentdiff

    # transformation function
    def getFlipDiff(self, imglist, target):
        if len(imglist) == 2:
            img1 = imglist[0]
            img2 = imglist[1]
            newimg1 = img1.convert("1")
            newimg2 = img2.convert("1")
            flipimg1 = ImageOps.flip(newimg1)
            dist = self.getDistance(flipimg1, newimg2)
            return dist

        else:
            return 'na'
        # for now flip is not required in 3x3 problems
        '''
        else:
            img1 = imglist[0]
            img2 = imglist[1]
            img3 = imglist[2]
            flipimg1 = ImageOps.flip(img1)
            dist1 = self.getDistance(flipimg1, img2)

            flipimg2 = ImageOps.flip(img2)
            dist2 = self.getDistance(flipimg2, img3)
        '''

    # transformation function
    def getMirrorDiff(self, imglist, target):
        if len(imglist) == 2:
            img1 = imglist[0]
            img2 = imglist[1]
            newimg1 = img1.convert("1")
            newimg2 = img2.convert("1")
            invertimg1 = ImageOps.mirror(newimg1)
            dist = self.getDistance(invertimg1, newimg2)
            return dist

        # for now invert is not required in 3x3 problems
        else:
            return 'na'

    # transformation function
    def getSizeDiff(self, imglist, target):
        if len(imglist) == 2:
            # not really applicable for 2x2 matrix but might add logic
            print("2x2")
        else:
            img1 = imglist[0]
            img2 = imglist[1]
            img3 = imglist[2]
