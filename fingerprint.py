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
from Database import Database
import sys


warnings.filterwarnings('ignore')

class Fingerprint():
    
    def __init__(self,path):
        
       # print('reached')
        self.path = path
        self.from_mp3_to_wav()
        self.fo = self.fingerprint_operation()
        
        
    def from_mp3_to_wav(self):
        
        #https://github.com/jiaaro/pydub
        #print(self.path + '\\fingerprinted_songs')
        if not os.path.exists(self.path + '\\fingerprinted_songs'):            
            os.makedirs(self.path + '\\fingerprinted_songs')

        count = 0
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
        
    def fingerprint_operation(self):
        
        # https://github.com/worldveil/dejavu/blob/master/dejavu/fingerprint.py
        print('\nfingerprinted_songs folder created\n')
        dict = {}
        index = 0
        local_maxima_list = []
        for _,_,file in os.walk(self.path + '\\fingerprinted_songs'):
            for filename in file:   
                sampling_frequency,signal_data = wavfile.read(self.path + '\\fingerprinted_songs\\' +  filename)
                #table_name = os.path.splitext(filename)
                index += 1
                dict[os.path.splitext(filename)[0]] = index
                #a = list(signal_Data[:,0])
                #arr = np.array(a)
                a = list(signal_data[:,0])
                arr = np.array(a)
                plt.ioff()
                arr2D = plt.specgram(arr,Fs=sampling_frequency)[0]
                arr2D = 10 * np.log10(arr2D)
                #plt.specgram(arr2D,Fs=sampling_frequency)
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
                local_maxima = list(local_maxima)
                local_maxima_list.append(sorted(local_maxima,key=itemgetter(1)))             
                
        
        return (dict,local_maxima_list)   
                
   

