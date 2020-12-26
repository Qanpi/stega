# This a demo file showing how the stega.py package can be used, it is not a part of the said package
#
#

from PIL import Image
import numpy as np
import argparse
import ntpath

import stega as st

# INITIALIZING PARSER CLASS FOR CMD LINE ARGUMENTS
parser = argparse.ArgumentParser(description="Decode a message from an image")
parser.add_argument("image",          metavar="I",  type=str, help="a path to an image")
parser.add_argument("-o", "--output", metavar="p",  type=str, help="a path for the decoded text or image (default: 'messages_decoded')", default="messages_decoded",)

args = parser.parse_args()

# Creating a Decoder class
decoder = st.Decoder()

# Opening the image and commencing the dejection process
image = np.asarray(Image.open(args.image))

binary = decoder.extract_binary(image)
message_decoded, ext = decoder.convert_binary_to_arr(binary, all=True)

st.write_file(message_decoded, args.output + "/" + ntpath.splitext(ntpath.basename(args.image))[0], ext)

if ext == ".png":
    Image.fromarray(image).show("original")
    Image.fromarray(message_decoded).show("decoded")

