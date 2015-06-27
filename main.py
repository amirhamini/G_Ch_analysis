from wachat import WAChat


def main():
    myChat = WAChat("whatsapp3.txt")
    print myChat.messageList

if __name__ == "__main__":
    main()
