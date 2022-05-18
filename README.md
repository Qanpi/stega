# stega

So... I'm a little ashamed to admit this, but being in my YouTuber phase, I actually made a video about this project of mine. There I provide a detailed, animated explanation of what steganography is and how I put to it to use in Reddit memes: https://www.youtube.com/watch?v=9JwKDBPkWqI. 

![image](https://user-images.githubusercontent.com/61239034/169135966-09fac13c-a4d2-4e8e-9c7e-e512764ab8d9.png)



## Introduction
Anyways, I will still provide documentation for the project here. However, a deeper dive into steganography can be better grasped from the video.

### What & Why?
Steganography is, as defined by [Wikipedia](https://en.wikipedia.org/wiki/Steganography), "the practice of concealing a message within another message". After watching a Computerphile [video](https://www.youtube.com/watch?v=TWEXCYQKyDc) about this topic, I became quite excited about steganography. In this project, I dabble with the very basic idea of hiding messages (text, images) within the binary code of other images.

### Technological components
- Numpy for binary and image array operations
  - optimized efficiency through vectorized binary operations
- PIL Image library for reading and writing image files
- Python library structure

## Documentation
The Stega Python library consists of two classes: Host and Message. The Message class represents the message (text, image, binary) we are trying to sneak by. The Host class is the host of that message, i.e. the medium into which that message will be injected. Hosts are typically in the form of images, since they are lossy (some binary information can be sacrificed for the sake of transporting the message).

### Example
1. Clone the repository from Github; don't bother with the releases - they are not well maintained. 
    - Note: The `stega.py` file is the actual library with full-fledged support for image steganography. `Encoder.py` provides an example of using that library.
2. Run the `encoder.py` file.

#### What happens?

The code comes with two starting images: `lenna.png` and `lennalight.png` (one-fourth the size of the former image). The former will become our Host image whilst the latter will become the Message. 

After running, the newly-created `host_encoded.png` now contains the injected binary data of the message (`lennalight.png`):

![image](https://user-images.githubusercontent.com/61239034/169138212-85f3d5a1-1691-4cc6-89d2-f745b5d0c23b.png)

Compare this with the original, starting file of the Host (`lenna.png`):

![image](https://user-images.githubusercontent.com/61239034/169138231-bb109bb2-0d01-47ab-82e8-1bb8d21aefdf.png)

The difference is unnoticable to the human eye. However, the computer is able to distinguish the modifications to the original image and from that reconstruct the message. The reconstructed message will be saved as `message_decoded.png`:

![image](https://user-images.githubusercontent.com/61239034/169138343-351925b5-d5ea-466e-9505-085189c2dae0.png)

You will notice that the image repeats twice - this is because it was able to fit twice into the Host file! Take a moment to consider how incredible it is that you are able to virtually store two whole images within another image. And all that without it being visually apparent. In fact, if we choose to inject only one color channel (out of the three RGB channels), we can fit six images (3x as much):

![image](https://user-images.githubusercontent.com/61239034/169138638-f4326716-d450-4cc4-bbe8-17a6d12ec46e.png)

Feel free to play around with the number of channels in the Host and the Message, the Message binary itself (text is also supported) and build on top of the library.
