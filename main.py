from wachat import WAChat
import os


def main():
    fileName = "whatsapp.txt" if len(os.sys.argv) < 2 else os.sys.argv[1]
    myChat = WAChat(fileName)
    print myChat.messageList

if __name__ == "__main__":
    main()
