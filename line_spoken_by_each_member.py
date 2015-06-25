from collections import defaultdict, namedtuple

# Source file emailed from Whatsapp
whatsappFileName = "whatsapp.txt"

# Create a namedtuple called Message to store in a list
Message = namedtuple("Message", ["date", "user", "text"])

# A list to hold messages
messageList = []

# Iterate over the Whatsapp file, filter only real messages, split them to
# date, user, and text, convert to "Message" and store in message list
with open(whatsappFileName, 'r') as infile:
    for line in infile:
        splitLine = line.strip().split(": ")
        if len(splitLine) >= 3:
            date = splitLine[0]
            user = splitLine[1]
            text = "".join(splitLine[2:])
            messageList.append(Message(date, user, text))

# Store members of the chat in a dict which returns 0 when member not found
members = defaultdict(int)

# Iterate through the messages, add how many times each member spoke
for message in messageList:
    members[message.user] += 1

# Print the members dictionary
for key, value in members.iteritems():
    print key + ": " + str(value)
