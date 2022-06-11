from PIL import Image
import pytesseract
import numpy as np
import json

class GetTxt():
    def __init__(self, path):
        self.image_path = path
        self.languages = None
        self.languages_str = ''
        self.image = np.array(Image.open(self.image_path))
        self.text = None
        self.read_langs()

    def read_langs(self):
        
        langs = json.load(f)
        self.languages = json.loads(json.dumps(langs))
        self.languages = self.languages["langs"]

        for s in self.languages:
            self.languages_str += s + "+"

        self.custom_config = f"-l {self.languages_str} --psm 6"

    def read_text(self):
        self.text = pytesseract.image_to_string(self.image)

    def get_text(self):
        return self.text
