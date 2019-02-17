import pyaudio
import wave
from collections import Counter
from Database import Database
from fingerprint import Fingerprint
import os
from scipy.io import wavfile

class Recognize():
    
    def __init__(self):
        
        self.record()
        
    def record(self):
        
        format = pyaudio.paInt16
        channels = 2
        sample_rate = 44100
        chunk = 1024
        record_sec = 6
        output_file = 'output.wav'
        audio = pyaudio.PyAudio()
        stream = audio.open(format = format,channels = channels,
                            rate = sample_rate, input = True, frames_per_buffer = chunk)
        
        print('\nrecording\n')
        frames = []
        for i in range(0,int(sample_rate / chunk * record_sec)):
            data = stream.read(chunk)
            frames.append(data)
        
        print('recording stopped\n')
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        wavefile = wave.open(output_file,'wb')
        wavefile.setnchannels(channels)
        wavefile.setsampwidth(audio.get_sample_size(format))
        wavefile.setframerate(sample_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()
        
    def identify(self,dbobject):
        
        current_path = os.getcwd() 
        sampling_frequency,signal_data = wavfile.read(current_path + '\\output.wav')
        fobject = Fingerprint(path=None)
        fobject.fingerprint_operation(signal_data,sampling_frequency)
        a = fobject.local_maxima_list
        store_hash = []   
        for i in range(1):    
            store_hash.append(fobject.ungenerate(fobject.produce_hashes(a[0])))
            
        
        showcount = Counter()

        store_hash[0]

        for i in store_hash[0]:
            s = dbobject.select_hash_table(i)
            for item in s:
                showcount.update(item)
        


        max_value = max(showcount, key=showcount.get)
        v = dbobject.select_song_table(max_value)
        for value in list(v):
            for j in value:        
                print(j)
        
    
