import nltk
import random

Subject_list = ["I","this","that","these","those","it","my","mine"]
Negative_list = ["not","n't"]
VBP_list = ["get","buy","like","want","need","love"]
VBP_alt_list = ["obtain","acquire","incline toward","require","hanker","admire"]
JJ_list = ["beautiful", "awesome","pretty","nice","good","great","broken","lost"]
JJ_alt_list = ["exquisite", "statuesque", "pulchritudinous", "prepossessing", "stupendous", "fractured", "mislaid"]
VBP_alt_list_melody = [(("c*",4),("e*",4),("f*",4))]
consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','r','s','t','v','w','x','z']
vowels = ['a','e','i','o','u','y']


def text_analysis(text):
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	PRP_check = False
	#PRP check
	print tagged
	for x in tagged:
		if x[1] == "PRP" or "DT" or "PRP$":
			for y in Subject_list:
				if x[0] == y:
					PRP_check = True
					print "PRP checked"
	#verb replacement				
	for x in tagged:
		for y in Negative_list:
			if x[0] == y:
				PRP_check = False
				print "Negative checked"
	for x in tagged:
		if PRP_check:
			for z in VBP_list:
				if x[0] == z:
					tokens[tagged.index((x[0],x[1]))] = VBP_alt_list[VBP_list.index(z)]
					print x[0] + " is replaced with " + VBP_alt_list[VBP_list.index(z)]
	#adj replacement
	for x in tagged:
		if PRP_check:
			for z in JJ_list:
				if x[0] == z:
					tokens[tagged.index((x[0],x[1]))] = JJ_alt_list[JJ_list.index(z)]
					print x[0] + " is replaced with " + JJ_alt_list[JJ_list.index(z)]
	final_text = " ".join(tokens)
	return final_text
	
def text_analysis_stutter(text):
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	for x in tokens:
		two_cons = False
		if len(x) >= 3:
			#Checking if the word is two consonants+vowel
			cons_counter = 0
			for y in list(x):
				if len(x) == 3 and y in consonants:
					cons_counter += 1
			if cons_counter >= 2:
				two_cons = True
			
			if two_cons is not True:
				temp = random.triangular()
				print "random number : " + str(temp)
				repeat = 1
				word = ""
				if temp >= 0 and temp <= 0.5:
					repeat = 1
				if temp > 0.5 and temp <= 0.7:
					repeat = 2
				if temp > 0.7 and temp <= 0.8:
					repeat = 4
				if temp > 0.8 and temp <= 0.9:
					repeat = 8
				if temp > 0.9 and temp <= 1:
					repeat = 12
				for i in range(repeat):
					word = list(x)[0] + list(x)[1] + word
				word = word + x
				tokens[tokens.index(x)] = word
	new_tokens =[]
	for z in tokens:
		k = tokens.pop()
		word = k
		if word == "n't":
			word = tokens.pop() + k
		new_tokens.append(word)
	for i in reversed(new_tokens):
		tokens.append(i)
	final_text = " ".join(tokens)
	return final_text
			
			
			
				
			
			
			
			
			
			
			
			
			
	