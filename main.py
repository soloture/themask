

from tts import downloadFile, getGoogleSpeechURL, downloadSpeechFromText, playText
from speech_rec import speech_recognition, save_speech, speech_to_text, openAudioStream, readAudioStream, stopAudioStream
from text_analysis import text_analysis
from pygame.locals import *
import pygame, pyaudio, sys
import nltk
WAVE_OUTPUT_FILENAME = "output"
fileName = "mask.mp3"

CHUNK = 4098
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5



if __name__ == "__main__":
	
	pygame.init()
	pygame.display.set_mode((100,100))
	State = "False"
	stream = ''
	frames = []
	final_text = ''
	p = pyaudio.PyAudio()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT: sys.exit()
			if event.type == KEYDOWN and event.dict['key'] == 50:
				print "Button"
				if State == "False":
					State = "Ready"
					print "Truing.."
				if State == "Recording":
					State = "Saving"
					print "Savinging.."
					
		if State == "Ready":
			p = pyaudio.PyAudio()
			stream = openAudioStream(p)
			frames = []
			State = "Recording"

		if State == "Recording":
			frames = readAudioStream(stream,frames,CHUNK)
		
		if State == "Saving":
			stopAudioStream(stream,p,frames,WAVE_OUTPUT_FILENAME)
			State = "STT"
			frames = []
		
		if State == "STT":
			text = speech_to_text(WAVE_OUTPUT_FILENAME)
			final_text = text_analysis(text)
			print "Input : " + text
			print "Output : " + final_text
			downloadSpeechFromText(final_text,fileName)
			playText(fileName)
			State = "False"
	'''
	speech_recognition(WAVE_OUTPUT_FILENAME)
	p = speech_to_text(WAVE_OUTPUT_FILENAME)
	final_text = text_analysis(p)
	print "Input : " + p
	print "Output : " + final_text
	downloadSpeechFromText(final_text,fileName)
	playText(fileName)
	'''