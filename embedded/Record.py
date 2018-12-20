import wave  # Python 3 module for reading / writing simple .wav files

import pyaudio  # Soundcard audio I/O access library


class Record:
    def __init__(self, **kwargs):
        """
        :param window_record: duration (ms)
        :param output_dir:
        :param kwargs:
        """
        self.record_seconds = kwargs.get('record_seconds', 5)  # Record time
        self.format = kwargs.get('format', pyaudio.paInt16)  # data type formate
        self.channels = kwargs.get('channels', 2)  # Adjust to your number of channels
        self.rate = kwargs.get('rate', 44100)  # Sample Rate
        self.chunk = kwargs.get('chunk', 1024)  # Block Size

        # Startup pyaudio instance
        self.audio = pyaudio.PyAudio()

    def record(self, output_file):
        # start Recording
        stream = self.audio.open(format=self.format, channels=self.channels,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        print("recording...")
        frames = []

        # Record for RECORD_SECONDS
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        print
        "finished recording"

        # Stop Recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        # Write your new .wav file with built in Python 3 Wave module
        waveFile = wave.open(output_file, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

