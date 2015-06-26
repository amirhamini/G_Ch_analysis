from wachat import WAChat


def main():
    myChat = WAChat("whatsapp.txt")
    print myChat.messageList[0].text


if __name__ == "__main__":
    main()
