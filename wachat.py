from collections import defaultdict, namedtuple
from datetime import datetime
import unicodedata
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches

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

    def getMessagesSeperatedByUsers(self, fromHour=0, untilHour=23, fromDay=1,
                                    untilDay=31, fromMonth=1, untilMonth=12,
                                    fromYear=2009, untilYear=2020):
        messageSeparated = defaultdict(str)
        for message in self.messageList:
            if (isMessageInFrame(message, fromHour, untilHour, fromDay,
                                 untilDay, fromMonth, untilMonth, fromYear,
                                 untilYear)):
                messageSeparated[message.user] += ' ' + message.text
        return dict(messageSeparated)


    def getMembers(self, fromHour=0, untilHour=23, fromDay=1, untilDay=31,
                   fromMonth=1, untilMonth=12, fromYear=2009, untilYear=2020):
        members = defaultdict(int)
        for message in self.messageList:
            if (isMessageInFrame(message, fromHour, untilHour, fromDay,
                                 untilDay, fromMonth, untilMonth, fromYear,
                                 untilYear)):
                members[message.user] += 1
        return dict(members)

    def plotMembersSpokenLines(self, fromHour=0, untilHour=23, fromDay=1,
                               untilDay=31, fromMonth=1, untilMonth=12,
                               fromYear=2009, untilYear=2020,
                               dataRepresntIn="total",
                               yAxisTitle='Number of messages',
                               plotTitle='Number of messages sent by each \
                               member'):
        peopleList = self.getMembers(fromHour, untilHour, fromDay, untilDay,
                                     fromMonth, untilMonth, fromYear,
                                     untilYear).keys()
        linesList = self.getMembers(fromHour, untilHour, fromDay, untilDay,
                                    fromMonth, untilMonth, fromYear,
                                    untilYear).values()
        sumlinesList = sum(linesList)
        if dataRepresntIn == "p":
            linesList = [float(i)/sumlinesList for i in linesList]
        ind = np.arange(len(peopleList))
        width = 0.75
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind+width/2.0, linesList, width, color='r')
        ax.set_ylabel(yAxisTitle)
        ax.set_title(plotTitle)
        ax.set_xticks(ind+width)
        ax.set_xticklabels(peopleList, rotation="vertical")
        axes = plt.gca()
        axes.set_ylim([0, 1.1 * max(linesList)])

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                if dataRepresntIn == "p":
                    ax.text(rect.get_x()+rect.get_width()/2.,
                            height + 0.01 * max(linesList), '%.1f%%'
                            % (height * 100.0), ha='center', va='bottom')
                else:
                    ax.text(rect.get_x()+rect.get_width()/2.,
                            height + 0.01 * max(linesList), '%d' % int(height),
                            ha='center', va='bottom')

        autolabel(rects1)
        plt.subplots_adjust(bottom=0.25)
        plt.show()

    def getMemberDailyFrequencies(self, keyword=None):
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

    def getMemberHourlyFrequencies(self):
        # A dictionary of arrays (each sized number of hours
        # in a day) gets created. For each hour it simply counts
        # the number of messages sent by user and add it to the corresponding
        # hour.
        # So in the end for each member we have a list of
        # number of messages in each hour

        memberHour = dict()
        numberOfHoursPerDay = 24

        for key in self.getMembers():
            memberHour[key] = [0] * numberOfHoursPerDay

        for i in range(numberOfHoursPerDay):
            hourTalk = self.getMembers(fromHour=i, untilHour=i)
            for key in hourTalk:
                memberHour[key][i] = hourTalk[key]
        return memberHour

    def getMemberMonthlyFrequencies(self):
        # A dictionary of arrays (each sized number of month
        # in a year) gets created. For each month it simply counts
        # the number of messages sent by user and add it to the corresponding
        # month.
        # So in the end for each member we have a list of
        # number of messages in each month

        memberMonth = dict()
        numberOfMonthPerYear = 12

        for key in self.getMembers():
            memberMonth[key] = [0] * numberOfMonthPerYear

        for i in range(1, numberOfMonthPerYear + 1):
            monthTalk = self.getMembers(fromMonth=i, untilMonth=i)
            for key in monthTalk:
                memberMonth[key][i - 1] = monthTalk[key]
        return memberMonth

    def statisticalGroupInfo(self, statInfo):
        # Get some statistical numbers regarding data
        # statInfo can be avg for average and ... (room for improvement)
        # This func is currently working for entire group

        if statInfo == "avg":
            talks = self.getMembers().values()
            peopleList = self.getMembers().keys()
            sumTalks = sum(talks)
            return sumTalks / float(len(peopleList))

    def plotOverHoursMemberSpokenLines(self, memberName=None):
        # if memberName is specified, for the given member it plots
        # the spoken lines vs hours. If the member is not specified
        # it plots the same thing for the entire group.

        if memberName:
            memberHourInfo = self.getMemberHourlyFrequencies()[memberName]
            N = len(memberHourInfo)
            toPlotData = memberHourInfo
            plotTitle = "What hour does %s talk? [Seattle Time]" % memberName

        else:
            peopleList = self.getMembers().keys()
            groupHourInfo = np.array([0] * 24)
            for memberName in peopleList:
                memberHourInfo = self.getMemberHourlyFrequencies()[memberName]
                groupHourInfo += np.array(memberHourInfo)
            toPlotData = groupHourInfo
            N = len(groupHourInfo)
            plotTitle = "What hour our group talk? [Seattle Time]"

        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        avg = sum(toPlotData)/float(len(toPlotData))
        radii = [x / avg for x in toPlotData]
        width = [(2-0.75)*np.pi/float(N)]*N
        fig = plt.figure(1, figsize=(8, 8), dpi=90)
        # Polar Plot
        ax = fig.add_subplot(211, polar=True)
        bars = ax.bar(theta, radii, width=width, bottom=0)
        ax.set_rmax(1.1 * max(radii))
        # Set the major tick locations to create a clock
        ax.xaxis.set_major_locator(ticker.MultipleLocator(np.pi/12))
        # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
        ax.set_xticklabels(['This does not get printed']+range(24))
        ax.set_yticklabels([])

        for i, r, bar in zip(range(N), radii, bars):
            if i/12 == 0:
                bar.set_facecolor("yellow")
                bar.set_alpha(0.5)
            else:
                bar.set_facecolor("black")
                bar.set_alpha(0.5)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        classes = ['AM', 'PM']
        class_colours = ['yellow', 'gray']
        recs = []
        for i in range(0, len(class_colours)):
            recs.append(mpatches.Rectangle((0, 0), 1, 1,
                        fc=class_colours[i]))
        plt.legend(recs, classes, bbox_to_anchor=(1.4, 1.15))

        # Regular Histagram Plot on the side
        ax = fig.add_subplot(212)

        hourList = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8',
                    '8-9', '9-10', '10-11', '11-12', '12-13', '13-14',
                    '14-15', '15-16', '16-17', '17-18', '18-19', '19-20',
                    '20-21', '21-22', '22-23', '23-0']

        ind = np.arange(len(hourList))
        width = 0.85
        rectsbars = ax.bar(ind+width/2.0, toPlotData, width)
        for i, bar in zip(range(24), rectsbars):
            if i/12 == 0:
                bar.set_facecolor("yellow")
                bar.set_alpha(0.5)
            else:
                bar.set_facecolor("black")
                bar.set_alpha(0.5)
        # ax.set_ylabel(yAxisTitle)
        # ax.set_title(plotTitle)
        ax.set_xticks(ind+width)
        ax.set_xticklabels(hourList, rotation="vertical")
        axes = plt.gca()
        axes.set_ylim([0, 1.1 * max(toPlotData)])

        def autolabel(rects, toPlotData):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2.0,
                        height + 0.02 * max(toPlotData),
                        '%d' % int(height),
                        ha='center', va='bottom')
        autolabel(rectsbars, toPlotData)
        plt.subplots_adjust(bottom=0.25)

        fig.suptitle(plotTitle, fontsize=20, y=1)

        plt.show()

    def getMemberAllYearsOverMonthFrequencies(self, memberName=None):
        # For each existing year (startDate to endDate) for given
        # member finds the number of spoken lines for each month.
        # If MemberName is not specified it provides information for
        # all members of the group

        firstMessageDate = self.messageList[0].date
        lastMessageDate = self.messageList[-1].date

        if memberName:
            peopleList = [memberName]
        else:
            peopleList = self.getMembers().keys()

        infoDic = dict()
        for memberName in peopleList:
            infoDic[memberName] = dict()
            for year in range(firstMessageDate.year + 1, lastMessageDate.year):
                infoDic[memberName][year] = dict()
                for month in range(1, 12 + 1):
                    infoDic[memberName][year][month] = self.getMembers(
                        fromMonth=month,
                        untilMonth=month,
                        fromYear=year,
                        untilYear=year).get(memberName, 0)
            # Dealing with first year
            infoDic[memberName][firstMessageDate.year] = dict()
            for month in range(firstMessageDate.month, 12 + 1):
                infoDic[memberName][firstMessageDate.year][month] = self.getMembers(
                    fromMonth=month,
                    untilMonth=month,
                    fromYear=firstMessageDate.year,
                    untilYear=firstMessageDate.year).get(memberName, 0)
            # Dealing with last year
            infoDic[memberName][lastMessageDate.year] = dict()
            for month in range(1, lastMessageDate.month + 1):
                infoDic[memberName][lastMessageDate.year][month] = self.getMembers(
                    fromMonth=month,
                    untilMonth=month,
                    fromYear=lastMessageDate.year,
                    untilYear=lastMessageDate.year).get(memberName, 0)

        return infoDic

    def getMembers_givenYear_monthlyInfo(self, year, memberName=None):
        # Give this function a specific year
        # and it gives
        # you how many line each member spoke in each month of that year
        if memberName:
            peopleList = [memberName]
        else:
            peopleList = self.getMembers().keys()
        firstMessageDate = self.messageList[0].date
        lastMessageDate = self.messageList[-1].date

        # Not accounting for the leap years
        firstMonth = 1
        finalMonth = 12

        if year > lastMessageDate.year or year < firstMessageDate.year:
            print "Please enter a valid year which the group data provides!\n"
            print "Something between %r and %r!" % (firstMessageDate.year,
                                                    lastMessageDate.year)
            return
        elif year == lastMessageDate.year and lastMessageDate.month != 12:
            print "Note: The year you are asking is right-incomplete"
            finalMonth = lastMessageDate.month
        elif year == firstMessageDate.year and firstMessageDate.month != 1:
            print "Note: The month you are asking for is left-incomplete"
            firstMonth = firstMessageDate.month
        infoDic = dict()
        for memberName in peopleList:
            infoDic[memberName] = dict()
            for month in range(firstMonth, finalMonth + 1):
                infoDic[memberName][month] = self.getMembers(
                    fromMonth=month,
                    untilMonth=month,
                    fromYear=year,
                    untilYear=year).get(memberName, 0)
        return infoDic

    def getMembers_givenYearAndMonth_dailyInfo(self, year, month,
                                               memberName=None):
        # Give this function a specific month (1-12) of a specific year
        # and it gives
        # you how many line each member spoke in each day of that month
        if memberName:
            peopleList = [memberName]
        else:
            peopleList = self.getMembers().keys()
        firstMessageDate = self.messageList[0].date
        lastMessageDate = self.messageList[-1].date

        monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # Not accounting for the leap years
        firstDay = 1
        finalDay = monthDays[month-1]

        if year > lastMessageDate.year or year < firstMessageDate.year:
            print "Please enter a valid year which the group data provides!\n"
            print "Something between %r and %r!" % (firstMessageDate.year,
                                                    lastMessageDate.year)
            return
        elif year == lastMessageDate.year and month > lastMessageDate.month:
            print "Please enter a valid month which the group data provides!"
            print "Something <= than %r!" % lastMessageDate.month
            return
        elif year == firstMessageDate.year and month < firstMessageDate.month:
            print "Please enter a valid month which the group data provides!"
            print "Something >= than %r!" % firstMessageDate.month
            return
        elif year == lastMessageDate.year and month == lastMessageDate.month:
            print "Note: The month you are asking might be right-incomplete"
            finalDay = lastMessageDate.day
        elif year == firstMessageDate.year and month == firstMessageDate.month:
            print "Note: The month you are asking might be left-incomplete"
            firstDay = firstMessageDate.day
        infoDic = dict()
        for memberName in peopleList:
            infoDic[memberName] = dict()
            for day in range(firstDay, finalDay + 1):
                infoDic[memberName][day] = self.getMembers(
                    fromMonth=month,
                    untilMonth=month,
                    fromYear=year,
                    untilYear=year,
                    fromDay=day,
                    untilDay=day).get(memberName, 0)
        return infoDic

    def getMembers_givenYearAndMonthAndDay_hourlyInfo(self, year, month, day,
                                                      memberName=None):
        # Give this function a specific day of a specific month (1-12) of a
        #specific year
        # and it gives
        # you how many line each member spoke in each hour of that day
        if memberName:
            peopleList = [memberName]
        else:
            peopleList = self.getMembers().keys()
        firstMessageDate = self.messageList[0].date
        lastMessageDate = self.messageList[-1].date
        print "We do not deal with leap days so no result for Feb 29!!! sorry\n"
        print "Note: The results are based on the timezone of the downloader"
        #
        monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if day < 1 or day > monthDays[month-1]:
            print 'Your date is not a valid Date pffff'
            return

        # Not accounting for the leap years
        firstHour = 0
        finalHour = 24

        if year > lastMessageDate.year or year < firstMessageDate.year:
            print "Please enter a valid year which the group data provides!\n"
            print "Something between %r and %r!" % (firstMessageDate.year,
                                                    lastMessageDate.year)
            return
        elif year == lastMessageDate.year and month > lastMessageDate.month:
            print "Please enter a valid month which the group data provides!"
            print "Something <= than %r!" % lastMessageDate.month
            return
        elif year == firstMessageDate.year and month < firstMessageDate.month:
            print "Please enter a valid month which the group data provides!"
            print "Something >= than %r!" % firstMessageDate.month
            return
        elif year == lastMessageDate.year and month == lastMessageDate.month:
            if day > lastMessageDate.day:
                print "Please enter a valid day which the group data provides!"
                print "The last day recorded for this year-month is %r" % lastMessageDate.day
                return
            if day == lastMessageDate.day:
                print "Note: The day you are asking might be right-incomplete"
                finalHour = lastMessageDate.hour
        #
        elif year == firstMessageDate.year and month == firstMessageDate.month:
            if day < firstMessageDate.day:
                print "Please enter a valid day which the group data provides!"
                print "The first day recorded for this year-month is %r" % firstMessageDate.day
                return
            if day == firstMessageDate.day:
                print "Note: The day you are asking might be left-incomplete"
                firstHour = firstMessageDate.hour

        infoDic = dict()
        for memberName in peopleList:
            infoDic[memberName] = dict()
            for hour in range(firstHour, finalHour):
                infoDic[memberName][hour] = self.getMembers(
                    fromMonth=month,
                    untilMonth=month,
                    fromYear=year,
                    untilYear=year,
                    fromDay=day,
                    untilDay=day,
                    fromHour=hour,
                    untilHour=hour).get(memberName, 0)
        return infoDic

    def plotGivenYearOverMonthFrequencies(self, memberName=None):

        monthNames = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
                      'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                      'Nov': 11, 'Dec': 12}
        toPlotData = self.getMemberAllYearsOverMonthFrequencies(
            memberName)[memberName]
        fig, ax = plt.subplots()
        numColors = 0
        for year in toPlotData:
            numColors += 1
            monthList = toPlotData[year].keys()
            monthValues = toPlotData[year].values()
            ax.plot(np.array(monthList), np.array(monthValues), label=year,
                    linewidth=3)
        cm = plt.get_cmap('gist_rainbow')
        ax.set_color_cycle([cm(1. * i / numColors) for i in range(numColors)])
        plt.xticks(monthNames.values(), monthNames.keys(),
                   rotation='vertical', fontsize=18)
        plt.yticks(fontsize=18)
        ax.margins(0.1)
        ax.grid(b=True, which='both', color='r', linestyle='--')
        # plt.subplots_adjust(bottom=0.15)
        plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
        plotTitle = "%s" % memberName
        fig.suptitle(plotTitle, fontsize=20, y=1)

        plt.show()
