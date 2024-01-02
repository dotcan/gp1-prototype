from io import BytesIO

from gtts import gTTS


def convert(text: str):
    b = BytesIO()
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(b)
    # bs = b.getvalue()
    # add wav file format header
    # b = (bytes(b'RIFF') + (len(bs) + 38).to_bytes(4, byteorder='little')
    #      + b'WAVEfmt\x20\x12\x00\x00'b'\x00\x01\x00\x01\x00'b'\x22\x56\x00\x00\x44\xac\x00\x00' +
    #      b'\x02\x00\x10\x00\x00\x00data' + (len(bs)).to_bytes(4, byteorder='little') + bs)
    # b = BytesIO(b)
    return b
