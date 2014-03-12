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
MIN_VOLUME = 600
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output"
fileName = "mask.mp3"
INPUT_DEVICE = 0
OUTPUT_DEVICE = 7

def main():
	p = pyaudio.PyAudio()
	stream = p.open(
		input_device_index = INPUT_DEVICE,
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		frames_per_buffer=CHUNK_SIZE,
	)
	noisecounter = 0
	silencecounter = 0
	r = array('h')
	r_buffer = array('h')
	vol = 0
	dump = True
	stream_status = True
	try:
		while True:
			if stream_status == False:
				print "Stream off. Starting a new stream.."
				p = pyaudio.PyAudio()
				stream = p.open(
					
					format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK_SIZE,
				)
				stream_status = True
			try :
				chunk = array('h', stream.read(CHUNK_SIZE))
				vol = max(chunk)
				if vol <= MIN_VOLUME:
					blank = []
					for i in range(CHUNK_SIZE):
						blank.append(0)
					chunk = array('h', blank)
				r_buffer.extend(chunk)
				while len(r_buffer) > 44100:
					r_buffer.pop(0)
			except IOError :
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
				if dump:
					print "Buffer dumped"
					r.extend(r_buffer)
					dump = False
				if vol <= MIN_VOLUME:
					blank = []
					for i in range(CHUNK_SIZE):
						blank.append(0)
					chunk = array('h', blank)
				r.extend(chunk)
				
			if silencecounter >= 20 and noisecounter >=6:
				stream.stop_stream()
				stream.close()
				p.terminate()
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
				dump = True
				print "Terminating the stream."
				stream.stop_stream()
				stream.close()
				p.terminate()
				stream_status = False
			
	except KeyboardInterrupt:
		print "Keyboard Interrupt..Terminating the stream."
		stream.stop_stream()
		stream.close()
		p.terminate()


			
	
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