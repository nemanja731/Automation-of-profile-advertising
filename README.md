# Automation-of-profile-advertising

## Project content

The project is divided into 4 folders. Certain operations are performed in each folder, which are logically divided into scripts. The scripts are not connected to each other, they are called individually because some of them exchange data with other, licensed programs, which are not included in the project. **The goal of each script** is to significantly speed up the work that is done manually through **automation**, which saves both human energy and time.

<img align='center' alt = 'Automation' width = '400' src = 'https://www.learninglinksindia.org/public/images/screen-manages.gif'>

## 1. Folder - _Prepare data_

This folder is responsible for the initial preparation of files and images. Check if there is a sufficient number of files and redistribute them to the appropriate places in the appropriate formats.

There are 3 scripts inside this folder:

- _cleanImages.py_ :arrow_right: contains functions for all kinds of image processing
- _prepareFiles.py_ :arrow_right: checks if there are enough files for the Snapchat account
- _showCurrentAmountOfData.py_ -> checks if there are enough files for the licensed program to prevent account deletion by Snapchat

## 2. Folder - _Make promotion_

This folder contains two scripts:

- _mainPyQt5.py_ :arrow_right: first it redistributes the files, and then, depending on the selected promotion, it creates the promotion, 
- _mainTkinter.py_ :arrow_right: same as above function, without some functionalities

Both scripts are GUIs used to create promotions and have exactly the same purpose. One script contains a GUI made using the PyQt5 library, and the other GUI is made using the tkinter library. A GUI created using the tkinter library does not have all the functionality as a GUI created using the PyQt5 library. The second GUI was created because there was a desire to rearrange the first GUI, but the idea was not finished. The main goal of this folder is to create a promotion that will be added to Snapchat on the picture or description of the profile that wants to be advertised.

## 3. Folder - _Make promotion_

This folder contains four scripts:

- _commands.py_ :arrow_right: contains various commands used when working with emulators
- _setupEmulators.py_ :arrow_right: creates and configures emulators to run
- _run.py_ :arrow_right: run emulators, create a Snapchat account and accept adds
- _ocr.py_ :arrow_right: contains functions for OCR

This folder is responsible for running emulators on the computer that simulate the mobile device. First, emulators are built and tuned. Then the emulators are started, each emulator downloads the snapchat application, registers the user, adjusts his profile and uploads promotions, all with the help of OCR. At the end of the day, the number of people who added a user is collected so that the emulator enters snapchat, goes to the list of new adds and accepts each add in turn, counting how many there were

## 4. Folder - _Export results_

This folder contains only one script:

- _export.py_- :arrow_right: extracts the result of promoting

When the entire job is done, this script is called to extract the promotion results.
