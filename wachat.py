from collections import defaultdict, namedtuple
from datetime import datetime

Message = namedtuple("Message", ["date", "user", "text"])
WADateFormat = '%m/%d/%y, %I:%M:%S %p'


class WAChat(object):

    def __init__(self, whatsappFileName):
        self.messageList = []
        self.members = defaultdict(int)
        with open(whatsappFileName, 'r') as infile:
            for line in infile:
                splitLine = line.strip().split(": ")
                if len(splitLine) >= 3:
                    date = datetime.strptime(splitLine[0], WADateFormat)
                    user = splitLine[1]
                    text = "".join(splitLine[2:])
                    self.messageList.append(Message(date, user, text))
        for message in self.messageList:
            self.members[message.user] += 1
