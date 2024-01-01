from io import BytesIO

import pyttsx4


class TextToSpeech:
    def __init__(self, voice: int = 0):
        self.engine = pyttsx4.init()
        self.engine.setProperty('rate', 125)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice].id)

    def convert(self, text: str):
        b = BytesIO()
        self.engine.save_to_file(text, b)
        self.engine.runAndWait()
        bs = b.getvalue()

        # add wav file format header
        b = (bytes(b'RIFF') + (len(bs) + 38).to_bytes(4, byteorder='little')
             + b'WAVEfmt\x20\x12\x00\x00'b'\x00\x01\x00\x01\x00'b'\x22\x56\x00\x00\x44\xac\x00\x00' +
             b'\x02\x00\x10\x00\x00\x00data' + (len(bs)).to_bytes(4, byteorder='little') + bs)
        b = BytesIO(b)
        return b
