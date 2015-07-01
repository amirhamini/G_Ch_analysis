from collections import defaultdict, namedtuple
from datetime import datetime
import unicodedata
import re

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
