# Baird Encoder - Image to Mechanical TV Signal Converter v1.10 - July 15, 2023
# By Regis "Casey" C., opimized by "Sylvia".

# REQUIRES THE PIL/PILLOW AND PYSOUNDFILE PYTHON LIBRARIES (NOT INCLUDED)

# Credits to Stack Overflow and related Python resources for my research.

"""
NOTES:
- The only image processing this program does is converting images to sound,
so please resize, crop, and process your image before feeding it to this
program.
- To view the images after the conversion, you'll need to use a
mechanical TV unit, Regis' "Baird Decoder" program, or aizquier's "VoyagerImb"
program.

This program features an ".sld mode", which saves your converted images in a 
format under the ".sld" extension (based on audio and .txt), which allows you to 
convert images that are too big, or has too high of a framerate, for a .wav file
to support, thus extending the limits on the videos you can convert.
For instance, a 44100hz .wav file can hold approx...
- 40fps of 32x34 footage (1088 samples per frame)
- 10fps of 64x68 footage (4352 samples per frame)
- 2fps of 128x136 footage (17408 samples per frame)
A .sld file can support all three sizes at a full 30, or even 60fps!
This format also allows for color support.
Currently, only the "Baird Decorder" starting on v1.1 can open these .sld files.

This program currently only works vertically, as in the program scans the images
starting from (0,0), goes down to the max Y value, and moves on to (1,0), and
repeats the process until all pixels are scanned.

It it advised that you only use images sized to mechanincal TV specs, such as
32x34, 64x68, 128x136, etc. We cannot promise functionality for values that are 
large (i.e. 640x480), outrageous (i.e. 10000x9000), or values that do not comply
with standard image sizes (i.e. 5x300). Please note that larger images may take
longer to convert.

Please do NOT report bugs if you modify the code past basic configurations or
use images we warned you about.
"""

# FILE SETTINGS


inFile = "" # Your input file.
# Please include the extension. If you are doing batch processing, then list only
# the directory, ending it with "/".
outName = "" # Your output audio file, saved as .wav
outDir = "" # Directory to output image rips to.
# Audio files are saved as "[NAME]_[x resolution]x[y resolution]_[frameNo].wav"

# PARAMETERS
FPS = 1 # Only activates if "Combine" is set to True - resizes the audio to a
# specific frame rate

# CONFIGURATIONS
Batch = False # Set true if your inFile is set to a folder with multiple images
Combine = False # If False, saves every frame as an individual audio file.
# Setting it to True combines all the frames to one audio.
# IMAGES MUST BE IN THE SAME RESOLUTION AS EACH OTHER!
allow_mega_conversions = False # If True, the program will be able to convert large
# image to audio (such as 1080p pics), but the audio will be larger than 1 second.
# *SLD_MODE* AND *COMBINE* MUST BE SET TO FALSE!
sld_mode = False # Scanline data (.sld), file format container.

# .SLD SETTINGS - sld_mode MUST BE SET TO "TRUE" TO USE THESE SETTINGS>
comp_mode = 0 # Compression mode, 0 - None, 1 - tenths, 2 - hundredths, 3 - Trim 
binary_comp = False # Binary conversion developed by Sylvee, converts .sld to a binary
# .slb (scanline binary) file. (NOT YET SCRIPTED!)
ColorMode = False # Saves your images as 3-channel color data instead of
# B&W. Takes up 3x file space as a B&W file, and compression is NOT supported.
# (Color data is trimmed at best.)


from PIL import Image
import soundfile as sf
import os
import sys
import time

MediaPerameters = {'FPS': 30, # LEAVE DICTIONARY AS IS! The script will correct 
                'ColorVid': False, # the values for you!
                'SoundVid': False, 
                'SlantCorrection': True,
                'Compression': 'Trim'}

backlog = []

if Batch == True:
    batchPic = os.listdir(inFile)
    print(batchPic)
    batchPic.sort()
    for pic in batchPic:
        backlog.append(pic)
else:
    backlog.append(inFile)

loopnum = 0
collectSamples = []
collectSamples2 = []
collectSamples3 = []
collectSamples4 = []

def measureResizeCheck(ImgArea, FPS, Samplerate):
    FrameMax = Samplerate/ImgArea
    FrameMax = round(FrameMax)
    if FrameMax < 1 and allow_mega_conversions == True:
        print(f'I can do this conversion, but the final audio will be {ImgArea/Samplerate} seconds long.')
        possibleAction = True
        return possibleAction
    elif Batch == True and Combine == True or allow_mega_conversions == False:
        HypoMax = round(94000/ImgArea,1)
        SampRequire = ImgArea * FPS
        print(f'This sample rate of {Samplerate} can only support a max of about {round(FrameMax)} frames at this resolution.')
        if FPS > FrameMax:
            print(f'I am unable to create an audio with the current sample rate of {Samplerate}hz.')
            print(f'You will at least need a sample rate of {round(SampRequire)}hz to create this video...')
            if SampRequire > 96000: # Typical max sample rate for PCM recorders.
                print('...which is not possible seeing how large the sample rate would need to be.')
                print(f'The most that could be done with this image is {HypoMax} frames per second at 96000hz.')
                time.sleep(10)
                possibleAction = False
                return possibleAction
        elif FrameMax < 1:
            print('...which is not possible seeing how large the sample rate would need to be.')
            print(f'You will need to set the *allow_mega_conversions* to True to convert this image,')
            print ('or switch to .sld mode.')
            time.sleep(10)
            possibleAction = False
            return possibleAction


# Code to create an .sld file.
def CreateFile(mediaPerams, xnum, ynum, mediaSamples,addSamp2=None, addSamp3=None):
    filename = outDir+outName
    with open(filename, 'w') as media_container:
        media_container.write(f'>framesize ({xnum},{ynum})\n')
        media_container.write(f'>framearea {xnum*ynum}\n')
        for param,vals in mediaPerams.items():
            media_container.write(f'>{param} {vals}\n')
        media_container.write('\n')
        loopCount = 0
        for pixel in mediaSamples:
            media_container.write(f'{str(pixel)}')
            if ColorMode == True:
                if addSamp2 != None:
                    media_container.write(f' {str(addSamp2[loopCount])}')
                if addSamp3 != None:
                    media_container.write(f' {str(addSamp3[loopCount])}')
            media_container.write('\n')
            loopCount+=1
    media_container.close()


MainSize = 0
MainSizeFlag = False
PossibleAction = True
PossibleActionFlag = False

compName = ''
MediaPerameters['FPS'] = FPS
MediaPerameters['ColorVid'] = ColorMode
if comp_mode == 0:
    compName = 'None'
elif comp_mode == 1:
    compName = 'Ultra'
elif comp_mode == 2:
    compName = 'Super'
elif comp_mode == 3:
    compName = 'Trim'
elif comp_mode > 3:
    comp_mode = 3
MediaPerameters['Compression'] = compName

if allow_mega_conversions == True and Combine == True:
    Combine == False
    print('*allow_mega_conversions* is enabled, *Combine* is now disabled.')
    time.sleep(5)


for nextPic in backlog:
    if Batch == True:
        inName = inFile + nextPic  # Your source image, please include extentsion.
    else:
        inName = inFile

    debugMode = False
    # If True, displays the image that is being written to the audio.
    # For debugging use only. Will open up a TON of tabs if you're doing
    # batch processing.

    ToConvert = Image.open(inName)
    #ToConvert = ToConvert.convert ('L')
    # For some reason, any attempt to convert RGB to luminance via math kept making
    # black images, so this was the only way to make the image B&W.
    OutSample = (ToConvert.size[0] * ToConvert.size[1])
    if MainSize == 0:
        MainSize = (ToConvert.size[0] * ToConvert.size[1])
    if OutSample != MainSize and Combine == True and MainSizeFlag == False:
        print (f'Image resoltuions between {backlog[0]} and {nextPic} do not match.')
        print (f'Setting Combine mode to false.')
        Combine = False
        MainSizeFlag == True
    Xnum = ToConvert.size[0]
    Ynum = ToConvert.size[1]

    if sld_mode == False and PossibleActionFlag == False:
        PossibleAction = measureResizeCheck(OutSample,FPS,44100)
        if PossibleAction == False:
            sys.exit()
            break
        PossibleActionFlag = True

    ToConvert = ToConvert.convert('RGB')

    loopnot = 0

    Shades = []
    GreenSound = []
    Blue = []
    if ColorMode == False:
        ReadPix = ToConvert.convert('L')
    for pix1 in range(ToConvert.size[0]): # Reads each pixel, vertically.
        for pix2 in range(ToConvert.size[1]):
            #Vert += 1\
            ReadPix = ToConvert.getpixel((pix1,pix2))
        
            R,G,B = ReadPix
            #print(pix1,pix2)
            Shades.append(R)
            if ColorMode == True:
                GreenSound.append(G)
                Blue.append(B)
        loopnot += 1
        print(loopnot)

    # DO NOT MODIFY VALUES BELOW UNLESS YOU KNOW WHAT YOU'RE DOING!
    # These configurations were specifically callibrated so the image would display
    # correctly with the Baird Decoder program.
    # If any anomalies occur because of the modification of these values, do NOT
    # report them as bugs.
    AmpVals = []
    GreenVals = []
    BlueVals = []
    patternSamp = []
    hold2 = []
    patternCount = 0
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
        if ColorMode == True or comp_mode == 3:
            pixval = round(pixval,3)
        AmpVals.append(pixval)
    if comp_mode > 0:
        AmpVals.append(0.0) # Dummy value needed to fix appending bug in the compression function.
    if ColorMode == True:
        for pixval2 in GreenSound:
            pixval2 += 128 # Brightness adjustment
            pixval2 -= 255 # Lowers value to be easily converted to audio.
            pixval2 = pixval2/255 + 0.2 # Convert to linear + Center line positioning
            if pixval2 > 1: # Audio wave scales go from -1 to 1
                pixval2 = 1
            elif pixval2 < -1:
                pixval2 = -1
            else:
                pass
            GreenVals.append(round(pixval2,3))
        for pixval3 in Blue:
            pixval3 += 128 # Brightness adjustment
            pixval3 -= 255 # Lowers value to be easily converted to audio.
            pixval3 = pixval3/255 + 0.2 # Convert to linear + Center line positioning
            if pixval3 > 1: # Audio wave scales go from -1 to 1
                pixval3 = 1
            elif pixval3 < -1:
                pixval3 = -1
            else:
                pass
            BlueVals.append(round(pixval3,3))
    print('hi')

# Regis' compression algorithm. 

    if comp_mode > 0 and comp_mode < 3 and ColorMode == False and sld_mode == True:
        lastAmp = 0
        repeatCount = 0
        totalLoop = 0
        toAdd = []
        NewAmp = []
        for valH in AmpVals:
            if toAdd: # If a value is present in "toAdd"
                if toAdd[0] == lastAmp: # if what's in there is equal to what we had last...
                    repeatCount+= 1 # only make a note of it, and do not append.
                    toAdd=[]
                else: # If this value is new...
                    NewAmp.append(toAdd[0]) # add it to the new compressed list. 
                    toAdd=[]
            simpH = round(valH,comp_mode) # Round the sound values down!
            if simpH == lastAmp: # If what we have is equal to what we had...
                repeatCount += 1 # only make a note of it, and do not append.
                continue # Go back and repeat the loop until the cycle is broken.
            else:
                if repeatCount > 0: # If the last x values have been repeated...
                    zerocount = 4-len(str(repeatCount))
                    zerocount = '0'*zerocount
                    NewAmp.append(f'^{zerocount}{repeatCount}x{lastAmp}') # Say "This value has appeared x times in a row."
                    repeatCount = 0
                    toAdd.append(simpH)
                    lastAmp = simpH
                    continue
                else:
                    NewAmp.append(simpH)
                    lastAmp = simpH
                    repeatCount = 0
            lastAmp = simpH
            totalLoop +=1
        AmpVals = NewAmp[:]
    if Combine == False and sld_mode == False:
        if allow_mega_conversions == True:
            OutSample == 44100
        outAud = sf.write(f"{outDir}{outName}_{Xnum}x{Ynum}_{loopnum}.wav", AmpVals, OutSample, 'PCM_24')
    elif Combine == True:
        collectSamples += AmpVals[:]
        collectSamples2 += GreenVals[:]
        collectSamples3 += BlueVals[:]


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
        #FrameConvert.show()



if Combine == True and sld_mode == True:
    if ColorMode == True:
        CreateFile(MediaPerameters, Xnum, Ynum, collectSamples,collectSamples2,collectSamples3)
    else:
        CreateFile(MediaPerameters, Xnum, Ynum, collectSamples)
elif Combine == True and sld_mode == False:
    OutSample = OutSample * FPS
    outAud = sf.write(f"{outDir}{outName}_{Xnum}x{Ynum}_{loopnum}.wav", collectSamples, OutSample, 'PCM_24')