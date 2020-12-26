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

# CREATING BASIC VARIABLES ---
image = np.asarray(Image.open(args.image))

# EXAMPLE CODE ---
binary = st.extract_binary(image, (0,3))
decoded_message = st.convert_binary_to_arr(binary, all=True)

st.write_file(decoded_message, args.output + "/" + ntpath.splitext(ntpath.basename(args.image))[0], ".png")

Image.fromarray(image).show("original")
Image.fromarray(decoded_message).show("decoded")