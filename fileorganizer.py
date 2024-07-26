import os
import re
from datetime import datetime

class FileOrganizer:
    def __init__(self, directory):
        self.directory = directory
        self.keywords = ["camera", "imu", "current", "referenceWave"]

    def organize_files(self):
        pattern_dirs = self.organize_by_patterns()
        self.organize_by_keywords()
        return pattern_dirs

    def organize_by_patterns(self):
        patterns = {
            'amp': r'amp_(\d+)',
            'f': r'f_(\d+)',
            'p': r'p_(\d+)',
            'a': r'a_(\d+)',
            'datetime': r'\d{4}-\d{2}-\d{2}'  
        }
        pattern_dirs = []

        for key in patterns:
            pattern_dir = os.path.join(self.directory, key)
            os.makedirs(pattern_dir, exist_ok=True)
            pattern_dirs.append(pattern_dir)

        for filename in os.listdir(self.directory):
            for key, pattern in patterns.items():
                match = re.search(pattern, filename)
                if match:
                    self.move_file(filename, key, match.group(1))
                    break

        return pattern_dirs

    def organize_by_keywords(self):
        for filename in os.listdir(self.directory):
            for keyword in self.keywords:
                if keyword in filename:
                    self.move_file(filename, 'keywords', keyword)
                    break

    def move_file(self, filename, category, value):
        target_dir = os.path.join(self.directory, category, value)
        os.makedirs(target_dir, exist_ok=True)
        os.rename(
            os.path.join(self.directory, filename),
            os.path.join(target_dir, filename)
        )

    def preview_organization(self):
        preview = []
        patterns = {
            'amp': r'amp_(\d+)',
            'f': r'f_(\d+)',
            'p': r'p_(\d+)',
            'a': r'a_(\d+)',
            'datetime': r'\d{4}-\d{2}-\d{2}'  
        }

        for filename in os.listdir(self.directory):
            for key, pattern in patterns.items():
                match = re.search(pattern, filename)
                if match:
                    target_dir = os.path.join(self.directory, key, match.group(1))
                    preview.append(f"{filename} -> {target_dir}")
                    break
            else:
                for keyword in self.keywords:
                    if keyword in filename:
                        target_dir = os.path.join(self.directory, 'keywords', keyword)
                        preview.append(f"{filename} -> {target_dir}")
                        break
        return preview