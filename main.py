import sys
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QTimer
from ChatParser import ChatParser
import sounddevice as sd
from pynput.keyboard import Controller, Key
import soundfile as sf

class TextToSpeechMumble(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 170)  # Set speech rate to a slower value
        self.parser = None
        self.first_chat_call = True
        self.keyboard = Controller()  # Initialize keyboard controller
        self.print_available_voices()  # Print available voices for debugging

    def print_available_voices(self):
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            print(f"Available Voice: {voice.name}, ID: {voice.id}, Languages: {voice.languages}")

    def initUI(self):
        self.setWindowTitle('Eve Chat to Mumble Speech')
        layout = QVBoxLayout()

        self.chat_name_input = QLineEdit(self)
        self.chat_name_input.setPlaceholderText('Enter Chat Name')
        layout.addWidget(self.chat_name_input)

        self.language_selector = QComboBox(self)  # Add language selector
        self.language_selector.addItems(['English', 'German'])
        self.language_selector.setCurrentText('English')  # Set English as the default language
        self.language_selector.currentIndexChanged.connect(self.update_language)
        layout.addWidget(self.language_selector)

        self.push_to_talk_input = QLineEdit(self)
        self.push_to_talk_input.setPlaceholderText('Enter Push-to-Talk Key')
        layout.addWidget(self.push_to_talk_input)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop', self)  # Add stop button
        self.stop_button.clicked.connect(self.stop)  # Connect to stop method
        layout.addWidget(self.stop_button)

        self.status_label = QLabel('Status: Inactive', self)  # Add status label
        layout.addWidget(self.status_label)

        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        self.setLayout(layout)

    def start(self):
        chat_name = self.chat_name_input.text()
        if not chat_name:
            self.log_display.append("Please enter a chat name.")
            return

        try:
            self.parser = ChatParser(chat_name)
            self.parser.reset_to_ignore_old_messages()  # Reset parser to ignore old messages
            self.status_label.setText('Status: Listening')  # Update status to listening

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.process_chat)
            self.timer.start(5000)  # Poll every 5 seconds
        except Exception as e:
            self.log_display.append(f"Error: {e}")  # Display error in the text window

    def stop(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()  # Stop the timer
            self.status_label.setText('Status: Inactive')  # Update status to inactive
            self.log_display.append("Monitoring stopped.")  # Log the stop action^
            self.first_chat_call = True

    def update_language(self):
        language_map = {
            'English': 'Zira',
            'German': 'Hedda',
            # Add other languages and their corresponding voice names if available
        }
        selected_language = self.language_selector.currentText()
        language_name = language_map.get(selected_language, 'Zira')
        self.set_tts_language(language_name)

    def set_tts_language(self, language_name):
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if language_name in voice.name:
                self.tts_engine.setProperty('voice', voice.id)
                print(f"Selected voice: {voice.name}")
                return
        print(f"No voice found for language: {language_name}, using default.")

    def process_chat(self):
        latest_chat = self.parser.get_latest_chat_element(self.first_chat_call)
        
        if latest_chat:
            self.first_chat_call = False
            self.log_display.append(f"Converting: {latest_chat}")
            self.text_to_speech(latest_chat)
            self.inject_audio_to_virtual_device('output.wav')
        else:
            pass
            #self.status_label.setText('Status: Inactive')  # Update status to inactive if no chat


    def text_to_speech(self, text):
        self.tts_engine.setProperty('volume', 0.99)  # Set volume to 80%
        self.tts_engine.save_to_file(text, 'output.wav')
        self.tts_engine.runAndWait()

    def inject_audio_to_virtual_device(self, audio_file):
        try:
            data, samplerate = sf.read(audio_file)

            push_to_talk_key = self.push_to_talk_input.text()
            if push_to_talk_key:
                self.keyboard.press(push_to_talk_key)  # Press the push-to-talk key

            sd.play(data, samplerate)
            sd.wait()  # Wait until file is done playing

            if push_to_talk_key:
                self.keyboard.release(push_to_talk_key)  # Release the push-to-talk key

        except Exception as e:
            self.log_display.append(f"Error playing audio: {e}")
            print(f"Error playing audio: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextToSpeechMumble()
    ex.show()
    sys.exit(app.exec_())