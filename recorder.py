import pyaudio
import wave
import threading
import logging
import os

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
    
    def set_save_directory(self, directory):
        self.save_directory = directory
        logging.info(f"Save directory set to: {self.save_directory}")

    def start_recording(self):
        self.frames = []
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
        )
        self.recording = True
        self.thread = threading.Thread(target=self.record)
        self.thread.start()
        logging.info("Recording started")

    def record(self):
        while self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.recording = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.save_recording()
        logging.info("Recording stopped and saved to output.wav")

    def save_recording(self):
        # Ensure save_directory is set, otherwise default to the current directory
        if hasattr(self, "save_directory"):
            self.filepath = os.path.join(self.save_directory, "output.wav")
        else:
            self.filepath = "output.wav"

        wf = wave.open(self.filepath, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        logging.info(f"Recording saved to {self.filepath}")