import httplib
import json
import sys, os
import pyaudio
import wave
import urllib2
import urllib
import json
from array import array

THRESHOLD = 500
CHUNK = 4098
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

def openAudioStream(p):
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)
	frames = []
	return stream

def readAudioStream(stream,frames,CHUNK):
	data = stream.read(CHUNK)
	frames.append(data)
	return frames

def stopAudioStream(stream,p,frames,WAVE_OUTPUT_FILENAME):
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	save_speech(frames, p, WAVE_OUTPUT_FILENAME)
	

def speech_recognition(WAVE_OUTPUT_FILENAME):	 
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)
	print("* recording")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	save_speech(frames, p, WAVE_OUTPUT_FILENAME)



def save_speech(frames, p, WAVE_OUTPUT_FILENAME):
	wf = wave.open(WAVE_OUTPUT_FILENAME+".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


def speech_to_text(filename):
	#Convert to flac
	os.system("flac -f "+ filename+'.wav')
	f = open(filename+'.flac','rb')
	flac_cont = f.read()
	f.close()
	"""
	lang_code='en-US'
	googl_speech_url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=%s&maxresults=6'%(lang_code)
	hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",'Content-type': 'audio/x-flac; rate=16000'}
	req = urllib2.Request(googl_speech_url, data=flac_cont, headers=hrs)
	p = urllib2.urlopen(req)

	res = eval(p.read())['hypotheses']
	print res
	map(os.remove, (filename+'.flac', filename+'.wav'))
	return res
	"""
	url = "www.google.com"
	path = "/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en"
	headers = { "Content-type": "audio/x-flac; rate=44100" };
	params = {"xjerr": "1", "client": "chromium"}
	conn = httplib.HTTPSConnection(url)
	conn.request("POST", path, flac_cont, headers)
	response = conn.getresponse()
	data = response.read()
	splitdata = data.split("\n")
	splitdata.pop()
	print splitdata
	k = []
	for i in splitdata:
		jsdata = json.loads(i)
		try:
			k.append(jsdata["hypotheses"][0]["utterance"])
		except IndexError:
			k.append(" ")
	jsdataoutput = " ".join(k)
	return jsdataoutput

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r
