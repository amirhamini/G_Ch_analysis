from wachat import WAChat
import os


def main():
    fileName = "whatsapp3.txt" if len(os.sys.argv) < 2 else os.sys.argv[1]
    myChat = WAChat(fileName)
    # myChat.plotMembersSpokenLines(plotTitle="July 2015", fromMonth=7,
                                  # fromYear=2015)

    # print myChat.getMemberMonthlyFrequencies()
    # names = myChat.getMembers().keys()
    # for name in names:
    #     myChat.plotOverHoursMemberSpokenLines(name)
    # for name in names:
    #     myChat.plotGivenYearOverMonthFrequencies(name)
    # print myChat.getMembers()
    # print myChat.getMembers_givenYearAndMonth_dailyInfo(2015, 6)
    # print myChat.getMembers_givenYear_monthlyInfo(2012)
    print myChat.getMembers_givenYearAndMonthAndDay_hourlyInfo(2013, 7, 20)
    # print myChat.getMemberAllYearsOverMonthFrequencies()
    # txtSeparated = myChat.getMessagesSeperatedByUsers()
    # import csv
    # writer = csv.writer(open('txtSeparated.csv', 'wb'))
    # writer.writerow(['name', 'text'])
    # for key, value in txtSeparated.items():
    #     writer.writerow([key, value])
        # print key
    # import json
    # with open('txtSeparated.json', 'w') as fp:
    #     for
    #     json.dump(txtSeparated, fp)


if __name__ == "__main__":
    main()
