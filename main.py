from wachat import WAChat
import os


def main():
    fileName = "whatsapp.txt" if len(os.sys.argv) < 2 else os.sys.argv[1]
    myChat = WAChat(fileName)
    myChat.plotMembersSpokenLines(plotTitle="July 2015", fromMonth=7,
                                  fromYear=2015)
    # print myChat.getMemberFrequencies()["Nick Zeynal"]


if __name__ == "__main__":
    main()
