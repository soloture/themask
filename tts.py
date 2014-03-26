#!/usr/bin/python

import urllib, urllib2, pycurl, subprocess, sys, os

def downloadFile(url, fileName):
	fp = open(fileName, "wb")
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEDATA, fp)
	curl.perform()
	curl.close()
	fp.close()

def getGoogleSpeechURL(phrase):
	googleTranslateURL = "http://translate.google.com/translate_tts?tl=en&"
	parameters = {'q': phrase}
	data = urllib.urlencode(parameters)
	googleTranslateURL = "%s%s" % (googleTranslateURL,data)
	return googleTranslateURL

def getGoogleSpeechURL_fr(phrase):
	googleTranslateURL = "http://translate.google.com/translate_tts?tl=fr&"
	parameters = {'q': phrase}
	data = urllib.urlencode(parameters)
	googleTranslateURL = "%s%s" % (googleTranslateURL,data)
	return googleTranslateURL

def downloadSpeechFromText(phrase, fileName):
	googleSpeechURL = getGoogleSpeechURL(phrase)
	print googleSpeechURL
	downloadFile(googleSpeechURL, fileName)

def downloadSpeechFromText_fr(phrase, fileName):
	googleSpeechURL = getGoogleSpeechURL_fr(phrase)
	print googleSpeechURL
	downloadFile(googleSpeechURL, fileName)	


def getGoogleSpeechURL_es(phrase):
	googleTranslateURL = "http://translate.google.com/translate_tts?tl=sp&"
	parameters = {'q': phrase}
	data = urllib.urlencode(parameters)
	googleTranslateURL = "%s%s" % (googleTranslateURL,data)
	return googleTranslateURL


def downloadSpeechFromText_es(phrase, fileName):
	googleSpeechURL = getGoogleSpeechURL_es(phrase)
	print googleSpeechURL
	downloadFile(googleSpeechURL, fileName)

def playText(fileName):
	command = "play " + fileName
	os.system(command)

