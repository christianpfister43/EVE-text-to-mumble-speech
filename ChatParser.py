import os
import glob
from datetime import datetime
import chardet

class ChatParser:
    def __init__(self, chat_name):
        self.chat_name = chat_name
        self.chat_directory = os.path.join(os.path.expanduser("~"), "Documents", "EVE", "logs", "Chatlogs")
        self.current_date = datetime.now().strftime("%Y%m%d")
        self.memory = set()
        self.latest_file = self._find_latest_file()
        self.start_time = None  # Add a start time attribute

    def reset_to_ignore_old_messages(self):
        self.start_time = datetime.now()  # Set start time to current time

    def _find_latest_file(self):
        pattern = f"{self.chat_name}_{self.current_date}_*.txt"
        files = glob.glob(os.path.join(self.chat_directory, pattern))
        if not files:
            raise FileNotFoundError("No chat log files found for this chat for today.")
        latest_file = max(files, key=os.path.getctime)
        return latest_file

    def _detect_encoding(self, file_path):
        with open(file_path, 'rb') as file:
            raw_data = file.read(10000)  # Read a portion of the file
        result = chardet.detect(raw_data)
        return result['encoding']

    def _read_file(self):
        encoding = self._detect_encoding(self.latest_file)
        with open(self.latest_file, 'r', encoding=encoding) as file:
            lines = file.readlines()
        
        # Skip the first 12 lines
        start_index = 12
        # The first 12 lines are just the head of the chat file
        
        # Return lines after the first 12 lines
        return lines[start_index:]

    def get_latest_chat_element(self, first_call=False):
        if first_call:
            return None
        else:
            lines = self._read_file()
            # Filter out empty lines
            non_empty_lines = [line for line in lines if line.strip()]
            if not non_empty_lines:
                return None
            
            # Get the last non-empty line
            new_element = non_empty_lines[-1]
            new_element = new_element.split('>')[-1].strip()
            if new_element not in self.memory:
                self.memory.add(new_element)
                return new_element
            return None

