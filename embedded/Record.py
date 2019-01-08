import wave  # Python 3 module for reading / writing simple .wav files

import pyaudio  # Soundcard audio I/O access library


class Record:
    def __init__(self, **kwargs):
        """
        :param window_record: duration (ms)
        :param output_dir:
        :param kwargs:
        """
        self.record_seconds = int(kwargs.get('record_seconds', 5))  # Record time
        self.format = kwargs.get('format', pyaudio.paInt16)  # data type formate
        self.channels = int(kwargs.get('channels', 2))  # Adjust to your number of channels
        self.rate = int(kwargs.get('rate', 44100))  # Sample Rate
        self.chunk = int(kwargs.get('chunk', 1024))  # Block Size
        self.input_device_index = int(kwargs.get('input_device_index', 2))
        # Startup pyaudio instance
        self.audio = pyaudio.PyAudio()
        # start Recording
        print()
        print("record_seconds: {}".format(self.record_seconds))
        print("format: {}".format(self.format))
        print("channels: {}".format(self.channels))
        print("rate: {}".format(self.rate))
        print("chunk: {}".format(self.chunk))

        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                 rate=self.rate, input=True,
                                 frames_per_buffer=self.chunk,
                                 input_device_index=self.input_device_index)

    def record(self, output_file):
        print("recording...")
        frames = []

        # Record for RECORD_SECONDS
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = self.stream.read(self.chunk)
            frames.append(data)
        print("finished recording")

        # Write your new .wav file with built in Python 3 Wave module
        waveFile = wave.open(output_file, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def terminate(self):
        print("Record: terminated")

        # Stop Recording
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
