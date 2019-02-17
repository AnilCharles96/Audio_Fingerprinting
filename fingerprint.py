from scipy.io import wavfile
import os
import numpy as np
from pydub import AudioSegment
from shutil import copy2
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import iterate_structure,generate_binary_structure,binary_erosion
from scipy.ndimage import maximum_filter
from operator import itemgetter
import hashlib
import warnings
#from Database import Database
import sys
import progressbar
import time

warnings.filterwarnings('ignore')

class Fingerprint():
    
    def __init__(self,path):
        
        
        self.path = path
        self.local_maxima_list = []
        
        if path:
            
            self.from_mp3_to_wav()
            self.fo = self.fingerprint_folder()
        
        
    def from_mp3_to_wav(self):
        
        #https://github.com/jiaaro/pydub
        #print(self.path + '\\fingerprinted_songs')
        print('\nfingerprinted_songs folder created')
        if not os.path.exists(self.path + '\\fingerprinted_songs'):            
            os.makedirs(self.path + '\\fingerprinted_songs')

        count = 0
        print('\nconverting to wav please wait')
        for _,_,file in os.walk(self.path):
            for filename in file:
                if filename.endswith('.mp3'): 
                    count += 1
                    AudioSegment.from_mp3(self.path + '\\' + filename).export(self.path+'\\fingerprinted_songs\\'+os.path.splitext(filename)[0]+'.wav',format='wav')
                if filename.endswith('.wav'):
                    count += 1
                    copy2(self.path+'\\'+filename,self.path+'\\fingerprinted_songs')            
            break
        if count == 0:
            print('\nplease enter the directory which contains songs')
            sys.exit(0)
        print('\nconverted successfully')
            
    def produce_hashes(self,local_maxima):   
        for i in range(len(local_maxima)):
            for j in range(1,20):
                if (i+j) < len(local_maxima):
                    freq1 = local_maxima[i][0]
                    freq2 = local_maxima[i+j][0]
                    t1 = local_maxima[i][1]
                    t2 = local_maxima[i+j][1]
                    t_delta = t2 - t1
                    if t_delta >= 0 and t_delta <= 240:
                        encode = '%s|%s|%s' %(str(freq1),str(freq2),str(t_delta))
                        h = hashlib.sha1(encode.encode('utf-8'))
                        yield(h.hexdigest()[0:20])
                        
                        
    def ungenerate(self,hashes):
        
        iter = []
        for hash in hashes:
            iter.append(hash)       
        return iter
        
    def fingerprint_folder(self):
        
        # https://github.com/worldveil/dejavu/blob/master/dejavu/fingerprint.py
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        print('\nproducing fingerprints please wait')
        dict = {}
        index = 0
        self.local_maxima_list = []
        for _,_,file in os.walk(self.path + '\\fingerprinted_songs'):
            for filename in file: 
                time.sleep(0.1)
                bar.update(index)
                sampling_frequency,signal_data = wavfile.read(self.path + '\\fingerprinted_songs\\' +  filename)
                #table_name = os.path.splitext(filename)
                index += 1               
                dict[os.path.splitext(filename)[0]] = index
                self.fingerprint_operation(signal_data,sampling_frequency)
        
        
        return (dict,self.local_maxima_list)
                
    def fingerprint_operation(self,signal_data,sampling_frequency):

        a = signal_data[:,0]
        arr = np.array(a)
        plt.ioff()
        arr2D = plt.specgram(arr,Fs=sampling_frequency)[0]
        arr2D = 10 * np.log10(arr2D)
        #plt.specgram(arr2D,Fs=sampling_frequency)
        arr2D[arr2D == -np.inf] = 0
        peak_neighbourhood_size = 50
        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct, peak_neighbourhood_size)
        local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
        background = (arr2D == 0)
        eroded_background = binary_erosion(background, structure=neighborhood,border_value=1)                                      
        local_max = local_max.astype(np.float32)
        eroded_background = eroded_background.astype(np.float32)
        detected_peaks = local_max - eroded_background
        detected_peaks = detected_peaks.astype(np.bool)
        amps = arr2D[detected_peaks]
        j, i = np.where(detected_peaks)
        amps = amps.flatten()
        peaks = zip(i, j, amps)
        min_amplitude = 1
        peaks_filtered = [x for x in peaks if x[2] > min_amplitude]
        frequency_idx = [x[1] for x in peaks_filtered]
        time_idx = [x[0] for x in peaks_filtered]
        '''
                fig, ax = plt.subplots()
                ax.imshow(arr2D)
                ax.scatter(time_idx, frequency_idx,color='red')
                ax.set_xlabel('Time')
                ax.set_ylabel('Frequency')
                ax.set_title("Spectrogram")
                plt.gca().invert_yaxis()
                plt.show()
        '''
        local_maxima = zip(frequency_idx,time_idx)
        #local_maxima = list(local_maxima)
        self.local_maxima_list.append(sorted(local_maxima,key=itemgetter(1)))             
                
        

r'''


current_path = os.getcwd() 
sampling_frequency,signal_data = wavfile.read(current_path + '\\output.wav')
fobject = Fingerprint(path=None)
fobject.fingerprint_operation(signal_data,sampling_frequency)
a = fobject.local_maxima_list
store_hash = []   
for i in range(1):    
    store_hash.append(fobject.ungenerate(fobject.produce_hashes(a[0])))
    


fobject = Fingerprint('C:\\Users\\Anil\\Desktop\\tick')


from collections import Counter
showcount = Counter()
dbobject = Database(hostname='localhost',user='root',passwd='helloworld')

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



       
  




      
for i in value:
    print(i)
        
        
dict[2] += 1   
    
dbobject.insert_values_into_song_table(1,'linkin park')
dbobject.insert_values_into_hash_table(1,'t6575756765')
    



a[0][0]

def produce_hashes(local_maxima):   
        for i in range(len(local_maxima)):
            for j in range(1,20):
                if (i+j) < len(local_maxima):
                    print(local_maxima)
                    freq1 = local_maxima[i][0]
                    freq2 = local_maxima[i+j][0]
                    t1 = local_maxima[i][1]
                    t2 = local_maxima[i+j][1]
                    t_delta = t2 - t1
                    if t_delta >= 0 and t_delta <= 240:
                        encode = '%s|%s|%s' %(str(freq1),str(freq2),str(t_delta))
                        h = hashlib.sha1(encode.encode('utf-8'))
                        yield(h.hexdigest()[0:20])



s = produce_hashes(a)
for i in s:
    print(s)
   

path_name = 'C:\Users\Anil\Desktop'


dbobject = Database(hostname='localhost',user='root',passwd='helloworld')
os.path.defpath
fobject = Fingerprint('C:\\Users\\Anil\\Desktop\\audio fingerprinting finished\\songs')

a = fobject.fo
a = list(a)
a[1][0]
count = 0
for name,index in a[0].items():
    count += 1
    dbobject.insert_values_into_song_table(index,name)
    
if not os.path.exists('C:\\Users\\Anil\\Desktop\\audio fingerprinting final' + '\\fingerprinted_songs'):
            os.makedirs('C:\\Users\\Anil\\Desktop\\audio fingerprinting final\fingerprinted_songs')

insert into song_table values(index,name)

path = 'C:\\Users\\Anil\\Desktop\\audio fingerprinting finished\\songs\\fingerprinted_songs\\maybe-next-time.wav'
sampling_frequency,signal_data = wavfile.read(path)
a = signal_data[:,0]
list(a)
a = np.array(a)
%matplotlib qt
arr2D = plt.specgram(a,Fs=sampling_frequency)[0]
    
a = signal_data[:,0]
arr = np.array(a)
plt.ioff()
arr2D = plt.specgram(arr,Fs=sampling_frequency)[0]
arr2D = 10 * np.log10(arr2D)
arr2D[arr2D == -np.inf] = 0
        peak_neighbourhood_size = 20
        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct, peak_neighbourhood_size)
        local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
        background = (arr2D == 0)
        eroded_background = binary_erosion(background, structure=neighborhood,border_value=1)                                      
        local_max = local_max.astype(np.float32)
        eroded_background = eroded_background.astype(np.float32)
        detected_peaks = local_max - eroded_background
        detected_peaks = detected_peaks.astype(np.bool)
        amps = arr2D[detected_peaks]
        j, i = np.where(detected_peaks)
        amps = amps.flatten()
        peaks = zip(i, j, amps)
        min_amplitude = 1
        peaks_filtered = [x for x in peaks if x[2] > min_amplitude]
        frequency_idx = [x[1] for x in peaks_filtered]

                fig, ax = plt.subplots()
                ax.imshow(arr2D)
                ax.scatter(time_idx, frequency_idx,color='red')
                ax.set_xlabel('Time')
                ax.set_ylabel('Frequency')
                ax.set_title("Spectrogram")
                plt.gca().invert_yaxis()
                plt.show()
  
        local_maxima = zip(frequency_idx,time_idx)
        local_maxima = list(local_maxima)
        self.local_maxima_list.append(sorted(local_maxima,key=itemgetter(1)))    

import os
os.getcwd() +'\\output.wav'




obj = Fingerprint('C:\\Users\\Anil\\Desktop\\audio fingerprinting final\\songs')

sampling_frequency,signal_data = wavfile.read('file.wav')

a = list(signal_data[:,0])
arr = np.array(a)
plt.ioff()
arr2D = plt.specgram(arr,Fs=sampling_frequency)[0]
arr2D = 10 * np.log10(arr2D)
#plt.specgram(arr2D,Fs=sampling_frequency)
arr2D[arr2D == -np.inf] = 0
peak_neighbourhood_size = 5
struct = generate_binary_structure(2, 1)
neighborhood = iterate_structure(struct, peak_neighbourhood_size)
local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
background = (arr2D == 0)
eroded_background = binary_erosion(background, structure=neighborhood,border_value=1)                                      
local_max = local_max.astype(np.float32)
eroded_background = eroded_background.astype(np.float32)
detected_peaks = local_max - eroded_background
detected_peaks = detected_peaks.astype(np.bool)
amps = arr2D[detected_peaks]
j, i = np.where(detected_peaks)
amps = amps.flatten()
peaks = zip(i, j, amps)
DEFAULT_AMP_MIN = 1
peaks_filtered = [x for x in peaks if x[2] > DEFAULT_AMP_MIN]
frequency_idx = [x[1] for x in peaks_filtered]
time_idx = [x[0] for x in peaks_filtered]


fig, ax = plt.subplots()
ax.imshow(arr2D)
ax.scatter(time_idx, frequency_idx,color='red')
ax.set_xlabel('Time')
ax.set_ylabel('Frequency')
ax.set_title("Spectrogram")
plt.gca().invert_yaxis()
plt.show()

local_maxima = zip(frequency_idx,time_idx)
local_maxima = list(local_maxima)
local_maxima = sorted(local_maxima,key=itemgetter(1))


def hashes(local_maxima):
    
    for i in range(len(local_maxima)):
        for j in range(1,20):
            
             if (i+j) < len(local_maxima):
                 
                 freq1 = local_maxima[i][0]
                 freq2 = local_maxima[i+j][0]
                 t1 = local_maxima[i][1]
                 t2 = local_maxima[i+j][1]
                 t_delta = t2 - t1
            
                 if t_delta >= 0 and t_delta <= 240:

                     encode = '%s|%s|%s' %(str(freq1),str(freq2),str(t_delta))
                     h = hashlib.sha1(encode.encode('utf-8'))
                     yield(h.hexdigest()[0:20],t1)


def mapper(hashes):
    
    mapper = {}
    for hash,offset in hashes:
        mapper[hash.upper()] = offset   
        
    return mapper

mic = mapper(hashes(local_maxima))


count =0
new_count=0

for i in not_mic:
    for j in mic:
        if i == j:
            count += 1
            


import pyaudio
import wave

 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "file.wav"

 
audio = pyaudio.PyAudio()
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

print("recording...")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print ("finished recording")


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()


'''


