from PIL import Image
import numpy as np
import argparse
import ntpath

import stega as st

# INITIALIZING PARSES CLASS FOR CMD LINE ARGUMENTS
parser = argparse.ArgumentParser(description="Encode a message into an image.")
parser.add_argument("image",          metavar="I",  type=str, help="a path to an image")
parser.add_argument("message",        metavar="M",  type=str, help="a path to the message file")
parser.add_argument("-o", "--output", metavar="p",  type=str, help="a path for the encoded image (default: 'images_encoded')", default="images_encoded")

args = parser.parse_args()

# Opening the image that will be injected the message into ---
image = np.asarray(Image.open(args.image))

# Creating an Encoder class and injecting the message
encoder = st.Encoder(image)
message = encoder.read_message(args.message)

binary = encoder.convert_msg_to_binary(message)
image_encoded = encoder.insert_binary(image, binary)

# Saving the output
st.write_file(image_encoded, args.output + "/" + ntpath.splitext(ntpath.basename(args.image))[0], ".png")

# Demonstrating the difference
Image.fromarray(image).show("original")
Image.fromarray(image_encoded).show("encoded")