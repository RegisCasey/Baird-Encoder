# Baird Encoder - Image to Mechanical TV Signal Converter v0.2 - July 3, 2023
# By Regis "Casey" C.

# REQUIRES THE PIL/PILLOW AND PYSOUNDFILE PYTHON LIBRARIES (NOT INCLUDED)

# Credits to Stack Overflow and related Python resources for my research.

"""
NOTES:
- This only works on individual images, a batch version is in development.
- The only image processing this program does is converting color to B&W,
so please resize, crop, and process your image before feeding it to this
program.
- To view the images after the conversion, you'll need to use a
mechanical TV unit, Regis' "Baird Decoder" program, or aizquier's "VoyagerImb"
program.

It it advised that you only use images sized to mechanincal TV specs, such as
32x34, 64x68, 128x136, etc. We cannot promise functionality for values that are 
large (i.e. 640x480), outrageous (i.e. 10000x9000), or values that do not comply
with standard image sizes (i.e. 5x300). Please note that larger images may take
longer to convert.

Please do NOT report bugs if you modify the code past basic configurations or
use images we warned you about.
"""

# CONFIGURATIONS

inName = "SampleImage.png" # Your source image, please include extentsion.
outName = "SampleExport" # Your output audio file, saved as .wav
# Audio files are saved as "[NAME]_[x resolution]x[y resolution].wav"

from PIL import Image
import soundfile as sf

debugMode = False 
# If True, displays the image that is being written to the audio.
# For debugging use only.

ToConvert = Image.open(inName)
ToConvert = ToConvert.convert ('L')
# For some reason, any attempt to convert RGB to luminance via math kept making
# black images, so this was the only way to make the image B&W.
OutSample = (ToConvert.size[0] * ToConvert.size[1])
Xnum = ToConvert.size[0]
Ynum = ToConvert.size[1]

ToConvert = ToConvert.convert('RGB')

Shades = []
for pix1 in range(ToConvert.size[0]): # Reads each pixel, vertically.
    for pix2 in range(ToConvert.size[1]):
        #Vert += 1\
        ReadPix = ToConvert.getpixel((pix1,pix2))
        R,G,B = ReadPix
        print(pix1,pix2)
        Shades.append(G)

# DO NOT MODIFY VALUES BELOW UNLESS YOU KNOW WHAT YOU'RE DOING!
# These configurations were specifically callibrated so the image would display
# correctly with the Baird Decoder program.
# If any anomalies occur because of the modification of these values, do NOT
# report them as bugs.
AmpVals = []
for pixval in Shades:
    pixval += 128 # Brightness adjustment
    pixval -= 255 # Lowers value to be easily converted to audio.
    pixval = pixval/255 + 0.2 # Convert to linear + Center line positioning
    if pixval > 1: # Audio wave scales go from -1 to 1
        pixval = 1
    elif pixval < -1:
        pixval = -1
    else:
        pass
    AmpVals.append(pixval)

if debugMode == True: # Displays the converted image
    FrameConvert = Image.new('RGB',(ToConvert.size[0], ToConvert.size[1]))
    PixColor = FrameConvert.load()
    Pixie = PixColor

    PixelVal = Shades
    horizCount = 0 
    vertCount = -1
    for n in range(ToConvert.size[0]):
        horizCount += 1
        for m in range(ToConvert.size[1]-1):
            vertCount += 1
            try:
                PixColor[n,m] = (PixelVal[horizCount+vertCount], PixelVal[horizCount+vertCount], PixelVal[horizCount+vertCount])
            except:
                pass
                
    FrameConvert.show()

sf.write(f"{outName}_{Xnum}x{Ynum}.wav", AmpVals, OutSample, 'PCM_24')
