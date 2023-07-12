# Baird Encoder - A small tool to convert images to mechanical TV audio signals.

![image](https://github.com/RegisCasey/Baird-Encoder/assets/138264475/ff77ab97-46eb-4550-ae44-1da7f9cb5250)

**NOW ON VERSION 1!**

Converts images into mechanical TV audio signals. Pretty much the opposite of the [Baird Decoder](https://github.com/RegisCasey/Baird-Decoder).
It does this by reading each pixel vertically, and assigns each pixel an audio value based on brightness.

# REQUIREMENTS
**THIS IS A PYTHON SCRIPT, AND AS SUCH, IT IS ASSUMED THAT YOU HAVE AT LEAST PYTHON 3.6.X INSTALLED.**

To use this program, you will need to have the [Pillow/PIL](https://pypi.org/project/Pillow/) and [PySoundFile](https://pypi.org/project/PySoundFile/) libraries,  and a Python code editor (Visual Studio Code, [Thonny](https://thonny.org/), etc. installed (all not included).

You will also need a small image file (ideally under 128x128), which has been provided in this repository to serve as an example. **As of v1, this program can also work with batch folders.**

# HOW TO USE
Open the `BairdEncoder-v1-RegisC.py` script in a code editor, and modify the values listed in **MAIN CONFIGURATIONS**. Once you are done, run the script, and once the script is done, it will save the audio file. It really is that simple!

# MAIN CONFIGURATIONS
`inFile` - Your source image or batch directory, please include extension if single image (i.e. SampleImage.png), or a "/" if it's a directory (i.e. home/myfile/photos/).

`outName` - Your output audio file, saved as .wav. Audio files are saved as "`[NAME]`_`[x resolution]`x`[y resolution]`.wav"

`outDir` - Fill this out if you wish to save your outputs to a specific directory, again ending the directory with "/".

`FPS` - *Only activates if `Combine` is set to `True`.* Saves the audio batch as one file, playing back at the specified "frame rate".

`Batch` - Set true if your inFile is set to a folder with multiple images.

`Combine` - If False, saves every frame as an individual audio file. Setting it to True combines all the frames to one audio.
**IMAGES MUST BE IN THE SAME RESOLUTION AS EACH OTHER!**

`sld_mode` - The *Baird Encoder* saves your conversions as `.wav` by default, but if your image resolution and/or frame rate is too high for the `.wav` format (you can calculate this by multiplying the x and y values of your image size, 
that will tell you how many audio samples are required for one frame. Multiply that number by your frame rate, and that will tell you how many audio samples are required to store one second of that. If the value is greater than 48000 (or 96000),
then it won't fit in the `.wav` format.), you may need to save your file under the `.sld` container instead. 

*See dictionary for more documentaion*

## .sld File Format
`.sld` is a label based on .txt and audio, which allows you to convert images that are too big, or has too high of a framerate, for a .wav file to support, thus extending the limits on the videos you can convert.

For instance, a 44100hz .wav file can hold approx...
- 40fps of 32x34 footage (1088 samples per frame)
- 10fps of 64x68 footage (4352 samples per frame)
- 2fps of 128x136 footage (17408 samples per frame)

A .sld file can support all three sizes at a full 30, or even 60fps!
This format also allows for color support.
Currently, only the "Baird Decorder" starting on v1.1 can open these .sld files.


# NOTES
- The only image processing this program does is converting images to audio,
so please resize, crop, and process your image before feeding it to this
program.
- To view the images after the conversion, you'll need to use a
mechanical TV unit, Regis' "[Baird Decoder](https://github.com/RegisCasey/Baird-Decoder)" program, or aizquier's "[VoyagerImb](https://github.com/aizquier/voyagerimb)"
program.

It it advised that you only use images sized to mechanincal TV specs, such as
32x34, 64x68, 128x136, etc. We cannot promise functionality for values that are 
large (i.e. 640x480), outrageous (i.e. 10000x9000), or values that do not comply
with standard image sizes (i.e. 5x300). Please note that larger images may take
longer to convert.

Please do NOT report bugs if you modify the code past basic configurations or
use images we warned you about.

# Changelog

## v1
- Added batch file support
- Added the ability to combine frames into one file
- Added frame rate support
- Added the ability to save conversions as an `.sld` file, which allows for images to have higher resolutions and/or higher framerates.
- Added color support and a basic compression algorithm (`.sld` mode only)

## v0.2
- Fixed bug which prevented the program from drawing images correctly (the image ended up looking "deep-fried").

## v0.1
- Proof of concept.
