# Baird Encoder - A small tool to convert images to mechanical TV audio signals.
Converts images into mechanical TV audio signals. Pretty much the opposite of the [Baird Decoder](https://github.com/RegisCasey/Baird-Decoder).
It does this by reading each pixel vertically, and assigns each pixel an audio value based on brightness.

# REQUIREMENTS
**THIS IS A PYTHON SCRIPT, AND AS SUCH, IT IS ASSUMED THAT YOU HAVE AT LEAST PYTHON 3.6.X INSTALLED.**

To use this program, you will need to have the [Pillow/PIL](https://pypi.org/project/Pillow/) and [PySoundFile](https://pypi.org/project/PySoundFile/) libraries,  and a Python code editor (Visual Studio Code, [Thonny](https://thonny.org/), etc. installed (all not included).

You will also need a small image file (ideally under 128x128), which has been provided in this repository to serve as an example.

# HOW TO USE
Open the `BairdEncoder-v0.2-RegisC.py` script in a code editor, and modify the values listed in **MAIN CONFIGURATIONS**. Once you are done, run the script, and once the script is done, it will save the audio file. It really is that simple!

# MAIN CONFIGURATIONS
`inName` - Your source image, please include extension (i.e. SampleImage.png).

`outName` - Your output audio file, saved as .wav. Audio files are saved as "`[NAME]`_`[x resolution]`x`[y resolution]`.wav"

# NOTES
- This only works on individual images, a batch version is in development.
- The only image processing this program does is converting color to B&W,
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
