from cv2 import cv2
import numpy as np

import stega as st
import timeit as tt

#Prerequisites
text = open("input/example.txt").read()
img = cv2.imread("images/lena.png")

e_binary = st.encode_message(text)
e_result = st.put_binary(img, e_binary)

d_binary = st.get_binary(e_result)
d_result = st.decode_message(d_binary)

cv2.imwrite("images/lena_encoded.png", e_result)

with open("output/example.txt", "w") as output_txt:
    output_txt.write(d_result)



