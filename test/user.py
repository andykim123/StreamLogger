from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk # this needs to be pip installed

# need the following nltk package for properly handle SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# Not really necessary but I figured maybe it's best to access these with separate class
# rather than have dictionary and access with get function
# because it'll take care of a lot of them in real time later on.
class SentimentIntensity:
	def __init__(self, compound, neg, neu, pos):
		self.compound = compound
		self.neg = neg
		self.neu = neu
		self.pos = pos

# class about a single comment
# current timestamp is off
class Comment:
	def __init__(self, content, timestamp = "000000", sentiment = 0):
		self.content = content
		self.timestamp = timestamp
		self.sentiment = sentiment

	def calculateSentimentIntensity(self):
		ss = sid.polarity_scores(self.content)
		newSentiment = SentimentIntensity(compound = ss.get("compound"), neg = ss.get("neg"), neu = ss.get("neu"), pos = ss.get("pos"))
		self.sentiment = newSentiment

# class about a single user
class User:
	def __init__(self, inputName, inputComments = [], sentiment = 0.0):
		self.name = inputName
		self.comments = inputComments
		self.sentiment = sentiment

	# add comments in a proper way
	# with regards to the class of inputComments
	def addComments(self, inputComments):
		if(isinstance(inputComments, list)):
			self.__addComments(inputComments)
		else:
			self.__addComment(inputComments)

	def __addComment(self, inputComment):
		self.comments.append(inputComment)

	def __addComments(self, inputComments):
		self.comments.extend(inputComments)

	# calculateCommentSentiments and getUserSentiment
	# are separated because "getUserSentiment" is our bread and butter for now
	# so I just wanted to separate out as we experiment with regards to
	# diverse papers about public opinions and other things if there's any.

	def calculateCommentSentiments(self):
		for comment in self.comments:
			comment.calculateSentimentIntensity()

	def getUserSentiment(self):
		sum = 0
		for comment in self.comments:
			sum = sum + comment.sentiment.compound
		self.sentiment = sum / len(self.comments)


# class which creates dictionary of users from 
# we keep dictionary in the form of hashtable
# because we want to have optimal access time of O(1)
# probably will change after some design experiments
class UserFactory:

	# public function that will be used to get dictionary of users
	def getUsers(self, fileName):
		return self.__buildUserDicts(self.__getRawComments(fileName))

	# private function to build user dictionary
	# out of list of tuples, (username, comment)
	def __buildUserDicts(self, inputList):
		userDict = dict()
		for comment in inputList:
			if(userDict.get(comment[0])==None):
				userDict[comment[0]] = User(inputName = comment[0], inputComments = [comment[1]])
			else:
				userDict[comment[0]].addComments(Comment(content = comment[1].content))
		return userDict


	# private function to build list of tuples, (username, comment)
	# from the given csv file path, if the path is a proper one.
	def __getRawComments(self, fileName):
		sentences = list()
		try:
			file = open(fileName, 'rb') # Python 2 version
			# file = open(fileName, 'r') # Python 3 version
			with file as csvfile:
				reader = csv.reader(csvfile, delimiter="\n") # read per line
				for row in reader:
					if(len(row)!=1): # only one full comment per line in csv file --> may change later on.
						raise ValueError('input csv file is not formatted correctly')
					line = row[0].split("\t")
					comment = (line[0], Comment(content = line[1]))
					sentences.append(comment)
			file.close()
		except EnvironmentError: # in python3, use FileNotFoundError
			print(fileName + " does not exist.")
		return sentences