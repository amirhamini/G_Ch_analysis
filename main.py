from wachat import WAChat
import os


def main():
    fileName = "whatsapp.txt" if len(os.sys.argv) < 2 else os.sys.argv[1]
    myChat = WAChat(fileName)
    # myChat.plotMembersSpokenLines(plotTitle="July 2015", fromMonth=7,
                                  # fromYear=2015)

    # print myChat.getMemberMonthlyFrequencies()
    # names = myChat.getMembers().keys()
    # for name in names:
    #     myChat.plotOverHoursMemberSpokenLines(name)
    # for name in names:
    #     myChat.plotGivenYearOverMonthFrequencies(name)
    print myChat.getMembers()
    # print myChat.getMemberGivenYearOverMonthFrequencies('Varahram')
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
