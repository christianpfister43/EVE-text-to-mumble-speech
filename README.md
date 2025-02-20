# EVE-text-to-mumble-speech

A python application that takes you EVE online chat and speaks in mumble for you

## Setup

## Windows:

Installing a virtual audio device: Download from https://vb-audio.com/Cable/ and install in locally on your pc.
Extract the zip file and run this .exe:
![Install the virtual audio device](https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/Install_virtual_audio_device.PNG)

Linux: coming soon.

Make sure to set the new virtual deive as the standard:
![Set standard device](https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/set_standard.PNG)
Check with system sounds or music that the virtual audio device is working!

Set the sound output to the virtual device:
![Set output device](https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/set_output_device.PNG)
You might only want to do that while you use this app.

## Mumble

Start the Audio assistant in mumble
![Start Audio Assistant](https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/mumble_start_audio_assistant.PNG)

Select the virtual device as input for mumble (Yes the device called "output" is the input device).
![Select input device](Screenshots/https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/mumble_select_input_device.PNG)

When you play a system sound (or test this app), make sure that mumble recognizes the virtual input device. You will likely not hear anything through your speakers/headset.
![Check if mumble recognizes the device](https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/mumble_device_working.PNG)

## Usage

Execute 'main.exe'

![App UI Overview](https://github.com/christianpfister43/EVE-text-to-mumble-speech/blob/main/Screenshots/App_UI_startup.PNG)
Create an ingame chat in EVE that you use for speaking on coms. You should be the only one writing in that channel. The app will monitor this chat channel when you press Start. Everything you type there, will be converted into voice. Select the language you want to talk in. For most this will be English. It currently only supports German and English, if more languages are needed, I might add them. You want to select the right language, otherwise the voice will sound horrible.
I assume that everyone is using push to talk on mumble, so put your push to talk in the respective field.^
The Text window will show you, what chat messages get converted into voice.

## Remarks

Currently the app is using Microsofts text to spech engine native in windows. The voice is a horrible computer voice. I plan on using something more sophisticated while trying to keep it free to use locally on every pc.

## Knows Issues

You need to select English as language once to set it.
