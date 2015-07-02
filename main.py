from wachat import WAChat


def main():
    myChat = WAChat("whatsapp3.txt")
    print myChat.getMembers().keys()
    myChat.plotMembersSpokenLines("p")
if __name__ == "__main__":
    main()
