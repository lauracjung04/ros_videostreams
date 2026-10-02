# Source - https://stackoverflow.com/a/63410126
# Posted by Niraj
# Retrieved 2026-10-02, License - CC BY-SA 4.0

#pip install SpeechRecognition
# sudo apt install portaudio19-dev python3-pyaudio
#pip install pyaudio

#surpress ALSA messages
import ctypes
ERROR_HANDLER = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                    ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
def _silent(filename, line, function, err, fmt):
       pass
c_handler = ERROR_HANDLER(_silent)
ctypes.cdll.LoadLibrary("libasound.so.2").snd_lib_error_set_handler(c_handler)

import speech_recognition as sr
import pyaudio

init_rec = sr.Recognizer()
print("Let's speak!!")
with sr.Microphone() as source:
    audio_data = init_rec.listen(source)
    print("Recognizing your text.............")
    text = init_rec.recognize_google(audio_data)
    print(text)
