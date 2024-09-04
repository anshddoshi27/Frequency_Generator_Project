import numpy as np 
import scipy.io.wavfile as wav



def interpolate_linearly(wave_table,index):
    truncated_index=int(np.floor(index)) # regular rounded down index
    next_index=(truncated_index+1)%wave_table.shape[0]  # in case the index is out of range again
    next_index_weight=index-truncated_index#distance of rounded index to actual index
    truncated_index_weight=1-next_index_weight #
    return truncated_index_weight*wave_table[truncated_index]+next_index_weight*wave_table[next_index] 

def fade_in_out(signal,fade_length=1000):
    fade_in=(1-np.cos(np.linspace(0,np.pi,fade_length)))*0.5 #creates an array of 1000 values that go to pi from 0 in the x manner. 1- this makes it go from 0 to 1 in a cosine manner                          
    fade_out=np.flip(fade_in)
    signal[:fade_length]=np.multiply(fade_in,signal[:fade_length])
    signal[-fade_length:]=np.multiply(fade_out,signal[-fade_length:])
    return signal
    
def sawtooth(x):
    x=(x+np.pi)/np.pi %2 -1
    return x





    
    
    

    
    
    
  
            
    
f1=int(input("Frequency for sawtooth: "))     
f2=int(input("Frequency for sine: ")) 
name=str(input("Enter File Name:"))
t=3
sample_rate=48000
    
    
    
def main(): #creates wavetable and populates it with the audio data. Captures the data in "output"  
    
    def sine(f2,t):
        sample_rate=48000#sample rate is amount of sampples produced per second; t is length of audio f is frequency
        f=f2
        t=3
        #waveform=sawtooth#sine waveform or sawtooth 
        waveform=np.sin
        wavetable_length=64 #length of the wavetable
        wave_table=np.zeros(wavetable_length) #initializes the wavetable as a vector of 64 elements that are zeroes. This allows for data to be populated 
        for n in range(wavetable_length):
            wave_table[n]= waveform(2*np.pi*n/wavetable_length) # each sample is sin(2*pi*ratio of period for sample), assigns voltage levels for each sample that outputs a sine wave
        output=np.zeros((t*sample_rate,)) # this makes a vector of the number of samples that will be produced in 3 sec.
        
        index=0
        index_increment=f*wavetable_length/sample_rate
        

        for n in range(output.shape[0]): #creates all the correct voltage values for each sample that correspond to a sine waveform with the right frequency!
            #output[n]=wave_table[int(np.floor(index))]
            output[n]=interpolate_linearly(wave_table,index)
            index+=index_increment # to get the next index for generating a certain frequency
            index%=wavetable_length # bring index back to the wavetable range as the waveform is periodic so we don't have to extend the wavetable.
        
        gain=-10
        amplitude=10**(gain/20) #inverse of 20*log(amplitude or v1/v2) gain is the actual db change we are creating to the output
        output*=amplitude
        output=fade_in_out(output)
        return output
    def make_sawtooth(f1,t):
        sample_rate=48000#sample rate is amount of sampples produced per second; t is length of audio f is frequency
        f=f1
        t=3
        #waveform=sawtooth#sine waveform or sawtooth 
        waveform=sawtooth
        wavetable_length=64 #length of the wavetable
        wave_table=np.zeros(wavetable_length) #initializes the wavetable as a vector of 64 elements that are zeroes. This allows for data to be populated 
        for n in range(wavetable_length):
            wave_table[n]= waveform(2*np.pi*n/wavetable_length) # each sample is sin(2*pi*ratio of period for sample), assigns voltage levels for each sample that outputs a sine wave
        output=np.zeros((t*sample_rate,)) # this makes a vector of the number of samples that will be produced in 3 sec.
        
        index=0
        index_increment=f*wavetable_length/sample_rate
        

        for n in range(output.shape[0]): #creates all the correct voltage values for each sample that correspond to a sine waveform with the right frequency!
            #output[n]=wave_table[int(np.floor(index))]
            output[n]=interpolate_linearly(wave_table,index)
            index+=index_increment # to get the next index for generating a certain frequency
            index%=wavetable_length # bring index back to the wavetable range as the waveform is periodic so we don't have to extend the wavetable.
        
        gain=-30
        amplitude=10**(gain/20) #inverse of 20*log(amplitude or v1/v2) gain is the actual db change we are creating to the output
        output*=amplitude
        output=fade_in_out(output)
        return output
    
    if f1==0:
        final_output=sine(f2,t)
    elif f2==0:
        final_output=make_sawtooth(f1,t)
    else:
        final_output=(make_sawtooth(f1,t)*sine(f2,t))
    wav_name=name+".wav"
    #wav.write(wav_name,sample_rate,final_output.astype(np.float32))
    print(final_output)
 
if __name__=='__main__':
    main()
