from wachat import WAChat


def main():
    myChat = WAChat("whatsapp.txt")
    for key, value in myChat.members.iteritems():
        print key + ": " + str(value)


if __name__ == "__main__":
    main()
