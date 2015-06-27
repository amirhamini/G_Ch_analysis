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
                    user = splitLine[1]
                    if user == "ERROR":
                        continue
                    text = "".join(splitLine[2:])
                    self.messageList.append(Message(date, user, text))

    def getMembers(self, fromHour=0, untilHour=23, fromDay=1, untilDay=31,
                   fromMonth=1, untilMonth=12, fromYear=2009, untilYear=2020):
        members = defaultdict(int)
        for message in self.messageList:
            if (isMessageInFrame(message, fromHour, untilHour, fromDay,
                                 untilDay, fromMonth, untilMonth, fromYear,
                                 untilYear)):
                name = (unicodedata
                        .normalize('NFKD', unicode(message.user, "utf-8"))
                        .encode("ascii", "ignore"))
                members[name] += 1
        return dict(members)
