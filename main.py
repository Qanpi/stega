from cv2 import cv2
import numpy as np

import stega as st
import timeit as tt
import time

text = open("input/example.txt").read()
img = cv2.imread("images/lena.png")

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