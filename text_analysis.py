import nltk

Subject_list = ["I","this","that","these","those","it","my","mine"]
Negative_list = ["not","n't"]
VBP_list = ["get","buy","like","want","need","love"]
VBP_alt_list = ["obtain","acquire","incline toward","require","hanker","admire"]
JJ_list = ["beautiful", "awesome","pretty","nice","good","great","broken","lost"]
JJ_alt_list = ["exquisite", "statuesque", "pulchritudinous", "prepossessing", "stupendous", "fractured", "mislaid"]
VBP_alt_list_melody = [(("c*",4),("e*",4),("f*",4))]


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
	
def text_analysis_split(text):
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	