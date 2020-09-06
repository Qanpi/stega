from cv2 import cv2
import argparse

import stega as st

# INITIALIZING PARSES CLASS FOR CMD LINE ARGUMENTS
parser = argparse.ArgumentParser(description="Encode a message into an image and decode it back.")
parser.add_argument("image",   metavar="I", type=str, help="a path to an image")
parser.add_argument("message", metavar="M", type=str, help="a path to the text file (message)")

args = parser.parse_args()

# CREATING BASIC VARIABLES ---
img = cv2.imread(args.image)
text = open(args.message).read()

# EXAMPLE CODE ---
e_binary = st.msg_to_binary(text)
e_result = st.insert_binary(img, e_binary, 2)

d_binary = st.extract_binary(e_result, 2)
d_result = st.binary_to_msg(d_binary)

with open("output/example.txt", "w") as output_txt:
    output_txt.write(d_result)

cv2.imwrite("output/lena.png", e_result)
cv2.imshow("test", e_result)
cv2.waitKey(0)