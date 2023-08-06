# GDV WiSe 2022 - Assignment #01 - Image riddle

## Task
Implement a tool to generate image riddles using Python and OpenCV. The tool should change an image of an everyday object or a VIP or an animal until it is not recognizable any more. This should happen in steps. These images need to be recorded and played back in reverse order. The resulting video can be used in a game like image riddle, where participants shall recognize the object in the image as fast as possible.
Hand in the code for the video generation tool and an exemplary video. Also write a readme file that states the authors and explains how to run the code (including all needed modules and their version) and how to use it (about 200 words, German or English).

## Hints
Those image riddles are used in television shows like "Frag doch mal die Maus". You can find exemplary videos in the example folder.

You can either shift pixels or blocks of pixels around or you can merge pixel blocks into one single color pixel.

Check out [this project](https://github.com/othneildrew/Best-README-Template) to get an impression about a good readme file.

## Rating
- Load an image with an everyday object or a VIP or an animal. (1 point) XX
- Find at least one way to change the image so that recognizability is reduced (up to 3 points)  
- Store several steps of the changed image. (1 point)   xx
- Record a video of the backward transformation process. Start with the unrecognizable image and end with the original one. (2 point)
- Code is well readable, structured and documented. And it can be well explained in the consultation. (up to 2 points)
- Readme is well written and helpful. It contains all used modules and their version. (1 point)
- BONUS: Code fullfils the [PEP8 styleguide](https://peps.python.org/pep-0008/). (1 point)
- BONUS: Producing at least three riddles that are fun to play. (1 point)

## Acceptance criteria
- Commit and push the code including resulting video(s) (in some appropriate file format and obey the file size) and a short explanation (edit this readme.md file).
- Resulting video alters some object.
- From the source code, it is clearly visible how the pixel values are altered.
- The code is written mainly on your own and any other source is mentioned in the code. If two groups hand in the same or extremely similar solution, both groups do not pass the assignment.

## Pass criteria
- The assignment is passed, if 5 or more points are reached.

## Solution
<add your readme here>


## Image Riddles by Nils Bergmann and Leon Gobbert

## What is the Project about?
- the file riddler.py modifies images in the data folder in several ways and each way with several steps
- Out of the resulting images that show the modified image in steps, a video is generated which works as a riddle to guess the original image
- The function 'change_pixel_random' copies small pixel chunks from  it's original position to new positions in the image 
- The function 'blurr_image' blurrs the image more on more at each step 
- The function 'hide_part_of_image' paints an incresingly bigger part of the image in black at each step

## How to run the code?
- First make sure you have python installed on your computer
- type 'python --version' in a terminal, if you get the version number 3.10.8, you are all set
- if not, download the python installer for version 3.10.8 from the official python website https://www.python.org/downloads/ and run it to install or update
- next, install opencv version 4.6.0 or update your existing install. To do that, type 'pip install opencv-python' in your terminal window or to update, type 'pip install --upgrade    opencv-python==4.6.0'
- We recommend using visual studio code with the python extension for the following steps:
- open the folder 'ImageRiddle' in visual studio code and run it by clicking the play-button on the top right corner of the editor window
- now an .mp4 file, named random_pixel should appear in the same folder as this README
- scroll down in the code file and comment out line 102 by placing a '#' in front of the text
- now remove the hashtag in line 104 and run the code again -> you will get another video as output next to the first video
- comment out line 104 and uncomment line 106 to generate the last video
- and you are finished! Have fun guessing the three riddles by running the videos in a video reader (open the 'ImageRiddle' folder in a file explorer and double click on the videos)