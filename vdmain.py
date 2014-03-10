import threading
from array import array
from Queue import Queue, Full
import time
import sys, os, wave
import pyaudio
from struct import pack
from speech_rec import speech_recognition, speech_to_text
from tts import downloadFile, getGoogleSpeechURL, downloadSpeechFromText, playText
from text_analysis import text_analysis, text_analysis_stutter
import nltk


CHUNK_SIZE = 4098
MIN_VOLUME = 500
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output"
fileName = "mask.mp3"


def main():
	stopped = threading.Event()
	q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
	listen_t = threading.Thread(target=listen, args=(stopped, q))
	listen_t.start()
	record_t = threading.Thread(target=record, args=(stopped, q))
	record_t.start()
	try:
		while True:
			listen_t.join(0.1)
			record_t.join(0.1)
	except KeyboardInterrupt:
		stopped.set()

	listen_t.join()
	record_t.join()


def record(stopped, q):
	noisecounter = 0
	silencecounter = 0
	r = array('h')
	while True:
		if stopped.wait(timeout=0):
			break
		chunk = q.get()
		vol = max(chunk)
		"""
		for i in chunk:
			framebuffer.append(i)
		
		
		if len(framebuffer) > 10:
			framebuffer = framebuffer[len(framebuffer)-10:]
		"""
		if vol >= MIN_VOLUME:
			# TODO: write to file
			print "O",
			noisecounter += 1
			silencecounter = 0
		else:
			print "-",
			silencecounter += 1
			
		if noisecounter >= 10:
			print "start recording!"
			r.extend(chunk)
			
		if silencecounter >= 20 and noisecounter >=6:
			print "Saving!"
			save_speech(r,WAVE_OUTPUT_FILENAME)
			text = speech_to_text(WAVE_OUTPUT_FILENAME)
			print "text : " + text
			final_text = text_analysis_stutter(text)
			print "output : " + final_text
			downloadSpeechFromText(final_text,fileName)
			playText(fileName)
			"""speechOutput_t = threading.Thread(target=speechOutput, args=(text))
			speechOutput_t.start()
			speechOutput_t.join()"""
			r = array('h')
			text = ""
			final_text = ""
			silencecounter = 0
			noisecounter = 0 
			
			
def listen(stopped, q):
	p = pyaudio.PyAudio()
	stream = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		frames_per_buffer=CHUNK_SIZE,
	)

	while True:
		if stopped.wait(timeout=0):
			break
		try:
			q.put(array('h', stream.read(CHUNK_SIZE)))	
		except Full:
			pass  # discard
		except IOError:
			print "IOError -- resetting the stream"
			stream.stop_stream()
			stream.close()
			p.terminate()
			stream = p.open(
				format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK_SIZE,
			)
	
	
def speechOutput(text):
	final_text = text_analysis_stutter(text)
	print "output : " + final_text
	downloadSpeechFromText(final_text,fileName)
	playText(fileName)
	
	
	
def save_speech(data,WAVE_OUTPUT_FILENAME):
	frames = pack('<' + ('h'*len(data)), *data)
	wf = wave.open(WAVE_OUTPUT_FILENAME+".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(frames)
	print WAVE_OUTPUT_FILENAME
	wf.close()

if __name__ == '__main__':
	main()