from cv2 import cv2
import numpy as np

import stega as st

#Prerequisites
text = open("messages/test.txt").read()
img = cv2.imread("images/img.png")


e_binary = st.encode_message(text)
e_result = st.put_binary(img, e_binary)

d_binary = st.get_binary(e_result)
d_result = st.decode_message(d_binary)

with open("output/decoded.txt", "w") as output_txt:
    output_txt.write(d_result)

cv2.imshow("test", e_result)
cv2.waitKey(0)


#For review later
# b, g, r = cv2.split(img)

# bits.resize(img.shape[:2])
# b = st.inject_bits(b, bits).astype(np.uint8)
# g = st.inject_bits(g, bits).astype(np.uint8)
# r = st.inject_bits(r, bits).astype(np.uint8)
# result = cv2.merge((b, g, r))

# cv2.imshow("Encoded image", result)
# cv2.imshow("Original image", img)
# cv2.imshow("Difference", np.subtract(result, img) * 255)
# cv2.waitKey(0)

# bits = st.scrape_bits(b)
# msg = st.decode_message(bits)


