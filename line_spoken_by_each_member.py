# Goals:
#      2. Provide the number of line spoken by each member

# Assuming whatsapp.txt is in the same directory
whatsappFileName = "whatsapp.txt"

chatList = []

with open(whatsappFileName, 'r') as infile:
    chatList = [line.strip() for line in infile]

for line in chatList:
    print line
