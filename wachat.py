from collections import defaultdict, namedtuple
from datetime import datetime
import unicodedata
import re
import numpy as np
import matplotlib.pyplot as plt

Message = namedtuple("Message", ["date", "user", "text"])
WADateFormat = '%m/%d/%y, %I:%M:%S %p'


def isMessageInFrame(message, fromHour, untilHour, fromDay, untilDay,
                     fromMonth, untilMonth, fromYear, untilYear):
    return (message.date.hour >= fromHour and message.date.hour <= untilHour and
            message.date.day >= fromDay and message.date.day <= untilDay and
            message.date.month >= fromMonth and
            message.date.month <= untilMonth and
            message.date.year >= fromYear and message.date.year <= untilYear)


class WAChat(object):

    def __init__(self, whatsappFileName):
        self.messageList = []
        with open(whatsappFileName, 'r') as infile:
            pattern = re.compile("([0-9]+)/([0-9]+)/([0-9]+)")
            for line in infile:
                line = line.decode("utf-8-sig").encode("utf-8")
                if not pattern.match(line):
                    continue
                splitLine = line.strip().split(": ")
                if len(splitLine) >= 3:
                    date = datetime.strptime(splitLine[0], WADateFormat)
                    user = (unicodedata
                            .normalize('NFKD', unicode(splitLine[1], "utf-8"))
                            .encode("ascii", "ignore"))
                    if user == "ERROR":
                        continue
                    text = (unicodedata
                            .normalize('NFKD', unicode("".join(splitLine[2:]),
                                       "utf-8"))
                            .encode("ascii", "ignore"))
                    self.messageList.append(Message(date, user, text))

    def getMembers(self, fromHour=0, untilHour=23, fromDay=1, untilDay=31,
                   fromMonth=1, untilMonth=12, fromYear=2009, untilYear=2020):
        members = defaultdict(int)
        for message in self.messageList:
            if (isMessageInFrame(message, fromHour, untilHour, fromDay,
                                 untilDay, fromMonth, untilMonth, fromYear,
                                 untilYear)):
                members[message.user] += 1
        return dict(members)

    def plotMembersSpokenLines(self, dataRepresntIn = "total"):
        peopleList = self.getMembers().keys()
        linesList = self.getMembers().values()
        sumlinesList = sum(linesList)
        if dataRepresntIn == "p":
            linesList = [float(i)/sumlinesList for i in linesList]
        ind = np.arange(len(peopleList))
        width = 0.75
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind+width/2.0, linesList, width, color='r')
        ax.set_ylabel('Number of messages')
        ax.set_title('Number of messages sent by each member')
        if dataRepresntIn == "p":
            ax.set_title(("Number of messages sent by each member"
                          " divided by total number of messages"))
        ax.set_xticks(ind+width)
        ax.set_xticklabels(peopleList, rotation="vertical")
        axes = plt.gca()
        axes.set_ylim([0, 1.05 * max(linesList)])

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                if dataRepresntIn == "p":
                    ax.text(rect.get_x()+rect.get_width()/2.,
                        height + 0.01 * max(linesList), '%.1f%%'
                        % (height * 100.0), ha='center', va='bottom')
                else:
                    ax.text(rect.get_x()+rect.get_width()/2.,
                        height + 0.01 * max(linesList), '%d'%int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        plt.subplots_adjust(bottom=0.25)
        plt.show()

    def getMemberFrequencies(self, keyword=None):
        # starting from first day messages was sent until the last day,
        # for each member, a dictionary of arrays (each sized number of days)
        # gets created. if keyword is specified, when it is seen in a message
        # by a member, 1 is added to the member of the array that represents
        # that day, if keyword is not specified, it simply counts the number
        # of messages sent by user on the timeline from start until end of the
        # chat

        firstMessageDate = self.messageList[0].date
        lastMessageDate = self.messageList[-1].date
        numberOfDays = (lastMessageDate - firstMessageDate).days + 1
        membersByWord = dict()

        for key in self.getMembers():
            membersByWord[key] = [0]*numberOfDays

        if keyword:
            keyword = keyword.lower()

        for message in self.messageList:
            saidWord = 0
            if keyword:
                saidWord = message.text.lower().count(keyword)

            if saidWord or not keyword:
                messageDay = (message.date - firstMessageDate).days
                membersByWord[message.user][messageDay] += 1

        return membersByWord
