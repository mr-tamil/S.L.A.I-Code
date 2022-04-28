import pyaudio
import wave
import speech_recognition as sr


# convert continuous audio (live microphone source) to text
def speech2text():
    r = sr.Recognizer()
    while (1):
        try:

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Started")
                audio2 = r.listen(source, timeout= 5)

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
    
                print(MyText)
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occured")

# record the audio
def recordAudio(filename):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 5

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


# convert audio file to text
def audioFile2text(file):
    r = sr.Recognizer()

    file_audio = sr.AudioFile(file)

    with file_audio as source:
        audio_text = r.record(source)

    # print(type(audio_text))
    print(r.recognize_google(audio_text))


def TextFromRAFile(filename, seconds= 5):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = seconds

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


    r = sr.Recognizer()
    file_audio = sr.AudioFile(filename)

    try:
        with file_audio as source:
            audio_text = r.record(source)

        text = r.recognize_google(audio_text)
        print(text)
        return text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None  # e
            
    except sr.UnknownValueError:
        print("unknown error occured")
        return None  # "unknown error occured"


if __name__ == "__main__":
    pass
    # path = 'C:\\Users\\ELCOT\\Python\\output.wav'
    # path = "C:\\Users\\ELCOT\\Python\\S.L.A.I Code\\AudioData01.wav" # From Phone 

    # speech2text()
    # audioFile2text(path)
    # recordAudio(path)

    # TextFromRAFile(path)
