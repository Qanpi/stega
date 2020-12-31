# This a demo file showing how the stega.py package can be used, it is not a part of the said package
#
#

import stega

def encode():
    #Open the message file and convert it to binary
    message = stega.Message.fromimagefile("example/lenna.png", c1=0, c2=1)
    binary = message.to_binary()
    
    #Open the host image and inject binary into it, then save the modified image file
    host = stega.Host.fromimagefile("example/lenna.png")
    host.inject_binary(binary, c2=3)
    host.save("images_encoded/")

def decode():
    #Open the modified host file and extract binary from it
    host = stega.Host.fromimagefile("images_encoded/host_encoded.png")    
    binary = host.extract_binary(c2=3)

    #Create a message class from the extracted binary and convert it back to the original message, then save the decoded file
    message = stega.Message.frombinary(binary)
    message.decode(all=True)
    message.save("messages_decoded/")

encode()
decode()

