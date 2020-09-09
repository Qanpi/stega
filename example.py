from cv2 import cv2
import argparse
import ntpath

import numpy as np

import stega as st

# INITIALIZING PARSES CLASS FOR CMD LINE ARGUMENTS
parser = argparse.ArgumentParser(description="Encode a message into an image and decode it back.")
parser.add_argument("image",          metavar="I",  type=str, help="a path to an image")
parser.add_argument("message",        metavar="M",  type=str, help="a path to the message file")
parser.add_argument("-o", "--output", metavar="p",  type=str, help="a path for the output text and image (default: 'output')", default="output",)

args = parser.parse_args()

# CREATING BASIC VARIABLES ---
image = cv2.imread(args.image)
message = st.read_message(args.message, (0,3))

# EXAMPLE CODE ---
e_binary = st.convert_arr_to_binary(message, 8)
e_result = st.insert_binary(image, e_binary, (0,3))

d_binary = st.extract_binary(e_result, (0,3))
d_result = st.convert_binary_to_arr(d_binary, 8, True)

st.write_message(d_result, "output/" + ntpath.basename(args.message))

cv2.imshow("original", image)
cv2.imshow("encoded", e_result)

cv2.imshow("decoded", d_result.astype(np.uint8))
cv2.waitKey(0)