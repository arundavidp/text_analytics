import os
import re
import pickle
import pandas as pd
import numpy as np
import cytoolz as ct
from collections import defaultdict
from gensim.parsing import preprocessing
from gensim.corpora import Dictionary
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from gensim.models.ldamodel import LdaModel
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import classification_report
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from scipy.sparse import isspmatrix
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import tensorflow as tf
import spacy


# ---------------------------------
def load(file):
    file = os.path.join(file)
    with open(file, "rb") as fo:
        ai = pickle.load(fo)

    return ai

print(load('tests/AI.State.Twitter.tfidf.pickle'))
# ---------------------------------

# ---------------------------------------------------------------------
# Class to centralize the functions used in the course
# ---------------------------------------------------------------------
class text_analytics(object):

    def __init__(self):

        # Define word lists
        self.max_size = 200
        self.function_words_single = ["the", "of", "and", "to", "a", "in", "i", "he", "that", "was", "it", "his", "you",
                                      "with", "as", "for", "had", "is", "her", "not", "but", "at", "on", "she", "be",
                                      "have", "by", "which", "him", "they", "this", "from", "all", "were", "my", "we",
                                      "one", "so", "said", "me", "there", "or", "an", "are", "no", "would", "their",
                                      "if", "been", "when", "do", "who", "what", "them", "will", "out", "up", "then",
                                      "more", "could", "into", "man", "now", "some", "your", "very", "did", "has",
                                      "about", "time", "can", "little", "than", "only", "upon", "its", "any", "other",
                                      "see", "our", "before", "two", "know", "over", "after", "down", "made", "should",
                                      "these", "must", "such", "much", "us", "old", "how", "come", "here", "never",
                                      "may", "first", "where", "go", "s", "came", "men", "way", "back", "himself",
                                      "own", "again", "say", "day", "long", "even", "too", "think", "might", "most",
                                      "through", "those", "am", "just", "make", "while", "went", "away", "still",
                                      "every", "without", "many", "being", "take", "last", "shall", "yet", "though",
                                      "nothing", "get", "once", "under", "same", "off", "another", "let", "tell", "why",
                                      "left", "ever", "saw", "look", "seemed", "against", "always", "going", "few",
                                      "got", "something", "between", "sir", "thing", "also", "because", "yes", "each",
                                      "oh", "quite", "both", "almost", "soon", "however", "having", "t", "whom", "does",
                                      "among", "perhaps", "until", "began", "rather", "herself", "next", "since",
                                      "anything", "myself", "nor", "indeed", "whose", "thus", "along", "others", "till",
                                      "near", "certain", "behind", "during", "alone", "already", "above", "often",
                                      "really", "within", "used", "use", "itself", "whether", "around", "second",
                                      "across", "either", "towards", "became", "therefore", "able", "sometimes",
                                      "later", "else", "seems", "ten", "thousand", "don", "certainly", "ought",
                                      "beyond", "toward", "nearly", "although", "past", "seem", "mr", "mrs", "dr",
                                      "thou", "except", "none", "probably", "neither", "saying", "ago", "ye",
                                      "yourself", "getting", "below", "quickly", "beside", "besides", "especially",
                                      "thy", "thee", "d", "unless", "three", "four", "five", "six", "seven", "eight",
                                      "nine", "hundred", "million", "billion", "third", "fourth", "fifth", "sixth",
                                      "seventh", "eighth", "ninth", "tenth", "amp", "m", "re", "u", "via", "ve", "ll",
                                      "th", "lol", "pm", "things", "w", "didn", "doing", "doesn", "r", "gt", "n", "st",
                                      "lot", "y", "im", "k", "isn", "ur", "hey", "yeah", "using", "vs", "dont", "ok",
                                      "v", "goes", "gone", "lmao", "happen", "wasn", "gotta", "nd", "okay", "aren",
                                      "wouldn", "couldn", "cannot", "omg", "non", "inside", "iv", "de", "anymore",
                                      "happening", "including", "shouldn", "yours", ]
        self.function_words = ["the", "of", "and", "to", "a", "in", "i", "he", "that", "was", "it", "his", "you",
                               "with", "as", "for", "had", "is", "her", "not", "but", "at", "on", "she", "be", "have",
                               "by", "which", "him", "they", "this", "from", "all", "were", "my", "we", "one", "so",
                               "said", "me", "there", "or", "an", "are", "no", "would", "their", "if", "been", "when",
                               "do", "who", "what", "them", "will", "out", "up", "then", "more", "could", "into", "man",
                               "now", "some", "your", "very", "did", "has", "about", "time", "can", "little", "than",
                               "only", "upon", "its", "any", "other", "see", "our", "before", "two", "know", "over",
                               "after", "down", "made", "should", "these", "must", "such", "much", "us", "old", "how",
                               "come", "here", "never", "may", "first", "where", "go", "s", "came", "men", "way",
                               "back", "himself", "own", "again", "say", "day", "long", "even", "too", "think", "might",
                               "most", "through", "those", "am", "just", "make", "while", "went", "away", "still",
                               "every", "without", "many", "being", "take", "last", "shall", "yet", "though", "nothing",
                               "get", "once", "under", "same", "off", "another", "let", "tell", "why", "left", "ever",
                               "saw", "look", "seemed", "against", "always", "going", "few", "got", "something",
                               "between", "sir", "thing", "also", "because", "yes", "each", "oh", "quite", "both",
                               "almost", "soon", "however", "having", "t", "whom", "does", "among", "perhaps", "until",
                               "began", "rather", "herself", "next", "since", "anything", "myself", "nor", "indeed",
                               "whose", "thus", "along", "others", "till", "near", "certain", "behind", "during",
                               "alone", "already", "above", "often", "really", "within", "used", "use", "itself",
                               "whether", "around", "second", "across", "either", "towards", "became", "therefore",
                               "able", "sometimes", "later", "else", "seems", "ten", "thousand", "don", "certainly",
                               "ought", "beyond", "toward", "nearly", "although", "past", "seem", "mr", "mrs", "dr",
                               "thou", "except", "none", "probably", "neither", "saying", "ago", "ye", "yourself",
                               "getting", "below", "quickly", "beside", "besides", "especially", "thy", "thee", "d",
                               "unless", "three", "four", "five", "six", "seven", "eight", "nine", "hundred", "million",
                               "billion", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
                               "amp", "m", "re", "u", "via", "ve", "ll", "th", "lol", "pm", "things", "w", "didn",
                               "doing", "doesn", "r", "gt", "n", "st", "lot", "y", "im", "k", "isn", "ur", "hey",
                               "yeah", "using", "vs", "dont", "ok", "v", "goes", "gone", "lmao", "happen", "wasn",
                               "gotta", "nd", "okay", "aren", "wouldn", "couldn", "cannot", "omg", "non", "inside",
                               "iv", "de", "anymore", "happening", "including", "shouldn", "yours", "lets", "in the",
                               "and ten", "others for", "to the", "from the", "by way", "way of", "at that",
                               "that time", "time we", "it the", "to some", "was not", "and would", "of our", "for the",
                               "of the", "who were", "were too", "through the", "with the", "we shall", "shall not",
                               "them the", "of this", "will probably", "one for", "for some", "to come", "is they",
                               "they know", "know that", "that there", "there is", "is very", "very little", "in it",
                               "it and", "and that", "that at", "at the", "the first", "they must", "must be",
                               "away it", "it is", "is as", "to your", "is all", "all the", "was the", "upon which",
                               "which we", "for our", "but we", "we have", "have been", "of it", "upon the", "by the",
                               "which our", "are once", "once more", "into that", "has already", "already been",
                               "will be", "on the", "the th", "out of", "of two", "by their", "both the", "are in",
                               "the two", "and their", "have already", "before the", "first and", "of at", "is so",
                               "as to", "as the", "to be", "in that", "and at", "last three", "three of", "and an",
                               "was made", "made to", "that the", "was then", "and the", "of five", "since they",
                               "they have", "or on", "has been", "with which", "which to", "has gone", "gone to",
                               "to day", "day to", "and will", "the next", "next day", "day he", "he is", "that his",
                               "is the", "the most", "first that", "that only", "only five", "can be", "for all",
                               "all that", "which was", "day was", "and its", "from an", "the day", "day has",
                               "been very", "more than", "than at", "at any", "but the", "is still", "it in",
                               "for their", "at st", "at this", "th of", "are to", "to dr", "after all", "all to",
                               "neither the", "there are", "to make", "make the", "probably in", "but there", "to go",
                               "one or", "or two", "two others", "however have", "have also", "of whom", "have not",
                               "not yet", "yet been", "day the", "and we", "it every", "for an", "in this", "of its",
                               "as its", "here this", "having on", "by mr", "of that", "to in", "and is", "the ten",
                               "until the", "and in", "th and", "th the", "was at", "when the", "now in", "there and",
                               "at five", "and made", "made the", "is about", "and to", "from our", "the and", "in an",
                               "we had", "had some", "with every", "will to", "to our", "we cannot", "to all",
                               "men whose", "if they", "their way", "way in", "in with", "that would", "would be",
                               "be on", "on your", "for it", "ten to", "to one", "one that", "is going", "going on",
                               "this has", "been the", "day of", "before this", "were on", "on their", "way to",
                               "and during", "during the", "it seemed", "seemed as", "as if", "if all", "out its",
                               "which came", "came from", "again at", "when after", "after the", "of some",
                               "through its", "of all", "men and", "than that", "that with", "or that", "the one",
                               "one at", "the other", "other at", "we never", "to what", "what the", "been more",
                               "more or", "why should", "should the", "be so", "while the", "of his", "were also",
                               "which had", "had the", "what is", "to they", "they were", "through many", "and this",
                               "this to", "to such", "such an", "them against", "against the", "and others",
                               "others was", "but for", "are probably", "probably not", "the three", "who got",
                               "got up", "up the", "are quite", "in their", "of having", "that on", "being on",
                               "they are", "from them", "them last", "after long", "it was", "men at", "it with",
                               "already made", "who are", "have no", "of their", "of an", "under this", "which is",
                               "is now", "the use", "use of", "to her", "she can", "can now", "is of", "who have",
                               "been most", "that dr", "here in", "us that", "and other", "down the", "at about",
                               "which were", "over the", "on by", "on to", "is always", "always an", "to it",
                               "and there", "is no", "is more", "have just", "of for", "for this", "them their",
                               "the last", "and men", "men on", "and was", "on her", "of one", "one of", "not long",
                               "long ago", "and two", "about seven", "long after", "of her", "soon the", "in some",
                               "some of", "to get", "get up", "the st", "in another", "of mr", "who is", "and man",
                               "man of", "left the", "he has", "to his", "man by", "while at", "under the", "where it",
                               "is being", "away to", "upon him", "him it", "both of", "him he", "he was", "in very",
                               "he had", "time with", "with its", "than any", "any other", "other man", "we are",
                               "are now", "at which", "which the", "things which", "have to", "ever since", "since the",
                               "by which", "make things", "for more", "used to", "be the", "of men", "men who",
                               "who had", "two thousand", "had come", "has had", "more of", "than of", "than the",
                               "of whether", "whether it", "is just", "just what", "what it", "it should",
                               "should have", "been in", "in all", "all its", "will not", "not say", "say but",
                               "but it", "is what", "is and", "and cannot", "it be", "be made", "was to", "for few",
                               "with your", "and my", "of over", "day in", "seven in", "all and", "and are", "as an",
                               "and mr", "whether the", "be of", "the long", "between them", "them and", "is not",
                               "such is", "with it", "but now", "say of", "in these", "or the", "the hundred", "me and",
                               "and when", "you my", "of things", "things that", "that were", "st of", "with him",
                               "him from", "from st", "in our", "in every", "every way", "been made", "made during",
                               "last few", "we take", "our most", "is made", "made up", "up of", "upon its", "and and",
                               "already in", "is one", "after some", "from which", "the more", "to say", "say nothing",
                               "nothing of", "of which", "which will", "be very", "at its", "those of", "of any",
                               "by about", "about the", "from this", "in ten", "and one", "in about", "this is",
                               "ever made", "made between", "between the", "while mr", "from here", "here who",
                               "who at", "at first", "for which", "among them", "in which", "which they", "about two",
                               "having left", "anything of", "for three", "three or", "or four", "that many",
                               "going to", "is indeed", "day at", "at an", "were being", "they say", "say the",
                               "have all", "there was", "him not", "down to", "as yet", "yet not", "in others",
                               "men is", "is to", "next to", "and long", "from two", "to five", "to those", "has just",
                               "this man", "man has", "with four", "have made", "made some", "because the", "has only",
                               "out from", "all over", "the may", "may three", "had been", "which has", "so much",
                               "much to", "was after", "of what", "ought to", "two hundred", "and little", "has always",
                               "always had", "and he", "he seems", "who has", "has never", "never been", "beyond his",
                               "past has", "if the", "been an", "and all", "they could", "has made", "between these",
                               "it because", "having been", "the time", "time and", "we think", "be able", "able to",
                               "that has", "and don", "towards the", "you for", "of your", "every other", "the just",
                               "which you", "you have", "to that", "the old", "old as", "we see", "see it", "by no",
                               "than eight", "at one", "the third", "man about", "just inside", "inside the",
                               "with both", "just above", "above the", "only been", "some three", "and from",
                               "have every", "it already", "to about", "about and", "every day", "day and", "it has",
                               "this day", "day on", "made in", "until next", "not in", "in time", "time however",
                               "however for", "for many", "many who", "had gone", "to re", "was never", "never in",
                               "in more", "never more", "man in", "to take", "now the", "the men", "are men", "in any",
                               "which do", "do not", "and then", "then they", "their most", "of them", "upon their",
                               "from his", "one day", "day later", "there were", "were about", "about to", "to their",
                               "it seems", "with his", "and can", "that he", "he now", "from mr", "and upon", "with mr",
                               "who was", "the fourth", "and who", "which have", "not been", "six hundred",
                               "hundred and", "one thousand", "where some", "come from", "be this", "at their",
                               "is under", "of last", "that some", "of those", "the man", "is upon", "by these",
                               "from their", "almost at", "at it", "nothing but", "up to", "seven hundred", "than two",
                               "while many", "among others", "than hundred", "as many", "of six", "three hundred",
                               "and six", "down at", "the of", "of three", "which shall", "to every", "to any",
                               "has not", "made and", "are not", "not so", "st to", "should be", "no more", "more to",
                               "than it", "is in", "or in", "be and", "and no", "men can", "only to", "on every",
                               "have the", "their own", "on this", "and it", "as we", "the an", "the re", "the same",
                               "and which", "and both", "and out", "do in", "with some", "some other", "nothing to",
                               "to which", "all on", "it would", "the it", "which more", "more and", "and more",
                               "where they", "any of", "at by", "and with", "such as", "was in", "re in", "that of",
                               "with more", "or if", "in most", "most of", "that is", "to have", "was such", "was it",
                               "in few", "said that", "that it", "and four", "among the", "were of", "and of",
                               "we must", "than is", "is either", "in his", "if we", "we did", "did not", "not know",
                               "know him", "him to", "we should", "should take", "take him", "him for", "never to",
                               "something that", "that seems", "and his", "he will", "will soon", "his old",
                               "time when", "when that", "if it", "the to", "the in", "from first", "first to",
                               "to last", "than once", "been as", "as his", "time will", "at is", "is already",
                               "never made", "still the", "she is", "off the", "every man", "man the", "to use",
                               "use it", "are no", "that are", "always to", "but at", "just as", "as she", "she was",
                               "been able", "are as", "off on", "on next", "go before", "before their", "man he",
                               "he too", "as they", "if he", "day it", "one thing", "however is", "is with",
                               "unless there", "we in", "how you", "in so", "are really", "to think", "think there",
                               "there must", "be some", "that by", "by and", "and by", "by your", "will come",
                               "upon us", "up is", "is there", "there any", "upon this", "many of", "of were", "as can",
                               "but from", "they did", "did nothing", "the were", "could not", "not have", "have for",
                               "what seems", "through them", "to other", "by our", "if such", "as there", "in and",
                               "for were", "some way", "be used", "used as", "not to", "to to", "but by", "them from",
                               "them under", "but to", "to and", "them to", "from all", "is time", "about this",
                               "of and", "that under", "the was", "to nothing", "nothing on", "was left", "those who",
                               "was too", "too and", "into the", "that such", "upon by", "in those", "with being",
                               "before and", "and they", "him in", "is that", "with an", "can the", "was with",
                               "him on", "day be", "was just", "while was", "man and", "going up", "up and", "had got",
                               "were and", "said when", "went down", "it he", "he went", "down and", "said it",
                               "ought not", "be going", "on so", "was on", "were at", "just at", "to do", "went into",
                               "and went", "went out", "was and", "and her", "her to", "go and", "she did", "went up",
                               "to my", "my own", "saw the", "across the", "came up", "came out", "out with",
                               "had very", "it might", "it his", "this time", "of my", "and me", "me to", "to down",
                               "and did", "did so", "so after", "after this", "down with", "not go", "go up",
                               "in going", "up but", "had he", "of him", "up by", "the few", "came down", "only eight",
                               "it as", "up it", "of of", "we used", "down on", "near the", "as now", "on it", "of to",
                               "in up", "to him", "him the", "man that", "that came", "was said", "them no",
                               "until they", "said nothing", "the left", "left was", "see him", "him as", "get for",
                               "been to", "the now", "it may", "may be", "be it", "beside the", "have way", "of these",
                               "these things", "which does", "in your", "day upon", "you are", "it does", "does not",
                               "himself from", "him by", "that out", "has ever", "us and", "since his", "toward his",
                               "and our", "might be", "others were", "up before", "is much", "but within", "within the",
                               "itself to", "who shall", "has this", "are that", "and for", "upon it", "made very",
                               "and after", "after their", "nor was", "of either", "quite as", "as at", "probably be",
                               "is said", "other the", "on with", "have always", "always been", "have had", "had to",
                               "the all", "the four", "have gone", "so that", "and dr", "before he", "with all",
                               "of very", "seems to", "is nothing", "for but", "and few", "but only", "that to",
                               "that one", "beyond all", "him during", "the five", "and three", "been said", "said in",
                               "that mr", "and ever", "ever has", "am not", "not an", "an up", "to its", "and as",
                               "by an", "the up", "it some", "some time", "time in", "the down", "came along",
                               "but was", "the second", "in its", "at from", "from to", "which in", "should not",
                               "not be", "first is", "is this", "this in", "to certain", "now about", "she will",
                               "before her", "alone on", "her own", "and she", "and though", "still there", "as little",
                               "with our", "from that", "that about", "said to", "there for", "after which", "was that",
                               "second day", "very much", "there have", "been some", "which are", "are at", "been at",
                               "at some", "of going", "under which", "which he", "to these", "we now", "has all",
                               "from its", "in other", "as already", "while their", "has in", "of time", "time been",
                               "and while", "while most", "almost every", "at all", "and under", "has by", "too long",
                               "long for", "however the", "into by", "had her", "away and", "to an", "under that",
                               "for anything", "only have", "have very", "as my", "to us", "us with", "have yet",
                               "very few", "about our", "of st", "went to", "and up", "to this", "time the",
                               "is within", "within two", "of being", "being as", "as it", "is at", "at no", "even in",
                               "at her", "two of", "men of", "many from", "will again", "again be", "that every",
                               "of dr", "and has", "has left", "left behind", "has the", "has of", "other day",
                               "day that", "than was", "as one", "her at", "for one", "here to", "was very", "two or",
                               "or three", "us for", "are all", "upon our", "away from", "was here", "here that",
                               "have so", "so long", "of as", "toward the", "for two", "and if", "them in", "under his",
                               "if that", "which two", "is from", "before they", "with their", "made his", "his first",
                               "but not", "in doing", "doing so", "not seem", "seem to", "in one", "not certain",
                               "he would", "even if", "he should", "should get", "get the", "some were", "were in",
                               "made an", "the past", "that no", "time is", "is some", "day about", "as nearly",
                               "be to", "his little", "too much", "left with", "from some", "time he", "he came",
                               "came in", "and almost", "third day", "other to", "of man", "was indeed", "of long",
                               "than we", "the ninth", "has now", "ten thousand", "if any", "same day", "they will",
                               "there never", "never was", "was more", "my old", "his last", "past and", "rather than",
                               "of so", "be their", "whom they", "has again", "which left", "left off", "at to",
                               "and soon", "to at", "were to", "for of", "take this", "over and", "at very",
                               "and around", "around the", "ago on", "on being", "still another", "by one", "is long",
                               "over three", "is without", "are already", "are the", "here at", "on two", "and before",
                               "could be", "made but", "but none", "have seemed", "just the", "the thing", "of eight",
                               "men in", "the way", "way that", "was there", "all our", "the very", "with them",
                               "which may", "may not", "among all", "make their", "way across", "his men", "of almost",
                               "she left", "on for", "were by", "away with", "about four", "four hundred", "hundred of",
                               "than in", "out in", "to mr", "was quickly", "were not", "might have", "will and",
                               "where he", "that in", "is never", "to no", "since in", "and thus", "that what",
                               "what would", "would also", "also be", "of old", "made at", "one and", "over which",
                               "left here", "with her", "her of", "six others", "left in", "four in", "all for",
                               "on his", "his way", "four or", "or five", "since he", "but after", "down by", "has yet",
                               "yet but", "come to", "have such", "when so", "so many", "by itself", "itself for",
                               "from most", "five hundred", "will on", "first of", "them all", "all three", "three are",
                               "are here", "and some", "we will", "first with", "that we", "is little", "as in",
                               "and among", "them was", "had already", "and had", "she has", "were among", "when all",
                               "all things", "he could", "could get", "was no", "whether that", "of much", "day all",
                               "to ten", "what they", "eight hundred", "of every", "into this", "has for", "past two",
                               "that during", "to many", "this will", "be an", "as that", "is an", "or even",
                               "made under", "under it", "it sometimes", "at other", "me mr", "are its", "much of",
                               "which each", "in seven", "seven and", "in being", "being able", "made all", "was my",
                               "that was", "as is", "is however", "however that", "in no", "and most", "have ever",
                               "there has", "has since", "which man", "has probably", "through his", "and were",
                               "time of", "what may", "be her", "which she", "she goes", "and often", "not only",
                               "every one", "do but", "but few", "know who", "let me", "it will", "last in", "after an",
                               "during which", "made its", "already had", "later than", "than our", "of ten",
                               "being and", "are two", "to two", "two other", "the only", "of sir", "and also",
                               "also made", "it one", "than one", "all his", "long and", "it cannot", "is most",
                               "to know", "will never", "up for", "that she", "in her", "the fifth", "of non",
                               "will ever", "ever be", "as this", "in from", "of many", "here last", "is certainly",
                               "then of", "any such", "only few", "it for", "would make", "make up", "that they",
                               "they would", "from both", "into his", "which so", "do no", "off and", "only one",
                               "the others", "others with", "at for", "an old", "himself for", "were over", "came to",
                               "that their", "was an", "doing the", "from in", "have since", "where the", "to you",
                               "you in", "in much", "you will", "at when", "when you", "his two", "after being",
                               "being out", "out for", "for only", "four others", "against whom", "through our",
                               "last the", "was nearly", "nearly three", "which time", "there in", "would have",
                               "which made", "made so", "of few", "since has", "especially in", "again to", "any one",
                               "one who", "will only", "that among", "the many", "had most", "was one", "out some",
                               "since by", "when it", "that all", "all who", "had left", "of both", "especially the",
                               "upon an", "her with", "of rather", "but when", "up her", "man from", "the the",
                               "before last", "to see", "we also", "the lot", "lot on", "on which", "is by",
                               "on fourth", "fourth and", "what has", "is which", "than even", "even the", "been so",
                               "for us", "say in", "from your", "that you", "although his", "in both", "saying that",
                               "that if", "take into", "first the", "seems that", "it can", "from any", "to another",
                               "day with", "only in", "and mrs", "than by", "we do", "which at", "at last", "last he",
                               "in such", "or without", "on an", "was by", "by last", "him off", "off by",
                               "before been", "this he", "be re", "by her", "were re", "which his", "of another",
                               "another of", "that when", "of nine", "along at", "there being", "on at", "have on",
                               "out but", "but will", "would think", "and make", "have more", "there seems", "each of",
                               "was about", "has long", "with another", "man were", "and nothing", "are over",
                               "over in", "with much", "men or", "for having", "up one", "three other", "make to",
                               "to whom", "that its", "make an", "no other", "that which", "say that", "off in",
                               "be one", "ever had", "had in", "now to", "it had", "rather the", "has few", "few more",
                               "than its", "for his", "last at", "yet to", "day is", "and quite", "never has",
                               "time before", "before in", "you or", "or it", "you with", "upon one", "and against",
                               "all of", "whom are", "in nine", "is on", "on its", "its last", "have but", "think of",
                               "going into", "against those", "in five", "five of", "the six", "from other", "if to",
                               "and therefore", "is such", "here the", "of may", "may last", "is rather", "in mr",
                               "made it", "with many", "by this", "others of", "over those", "of past", "by his",
                               "there mr", "they own", "that as", "that neither", "without even", "about as",
                               "down for", "for to", "but whether", "of not", "there should", "an at", "of four",
                               "is quite", "have it", "it that", "me it", "it another", "because it", "in my",
                               "with eight", "that four", "and very", "little to", "to de", "by me", "in may",
                               "of certain", "made from", "and much", "in too", "which would", "upon them", "be more",
                               "of in", "as their", "the sixth", "to little", "from no", "but rather", "an over",
                               "however was", "by some", "able and", "for at", "it at", "here on", "are made",
                               "out about", "was last", "be that", "much more", "than with", "all others", "three men",
                               "was quite", "now it", "th at", "or as", "be gone", "that sir", "by sir", "and back",
                               "back to", "last as", "are many", "about her", "some that", "seven others", "others who",
                               "day for", "his own", "being made", "have his", "as he", "be but", "at once", "once for",
                               "which if", "day but", "but could", "on that", "anything for", "we make", "up from",
                               "that be", "and again", "again was", "against his", "no man", "man was", "was so",
                               "is nearly", "are we", "way between", "once had", "had no", "and time", "for by",
                               "only had", "all at", "which it", "into our", "or rather", "of no", "had not", "not as",
                               "say it", "men for", "upon that", "among other", "things he", "would get", "get into",
                               "time his", "came on", "by dr", "from it", "by many", "though not", "as on", "on some",
                               "the seventh", "at his", "us the", "now we", "and know", "know the", "he did", "to man",
                               "is its", "for its", "its most", "being the", "before our", "upon his", "without the",
                               "with this", "them as", "this on", "us it", "that an", "had an", "time to", "which no",
                               "either for", "must have", "them or", "or for", "but they", "are first", "second the",
                               "to each", "that your", "from her", "as before", "have few", "of about", "near her",
                               "this can", "yet the", "on our", "as of", "those in", "that after", "and have",
                               "that two", "left her", "but were", "from him", "him some", "there on", "having in",
                               "now than", "than they", "in have", "when we", "may of", "and you", "me that",
                               "though the", "one which", "they had", "not of", "time for", "with that", "it to",
                               "what little", "we could", "been one", "which must", "made more", "but who", "as being",
                               "were made", "made upon", "at on", "where she", "since of", "at certain", "while there",
                               "man whose", "in getting", "getting into", "who seemed", "seemed to", "from eight",
                               "eight to", "since at", "is man", "but of", "it being", "their last", "you that",
                               "way the", "but just", "just now", "that little", "little while", "but my", "that do",
                               "be quite", "be my", "last five", "shall we", "alone for", "first eight", "about three",
                               "especially of", "since my", "my last", "have come", "come down", "off his", "was going",
                               "going out", "out on", "it came", "out to", "after having", "just been", "without any",
                               "are those", "ten or", "say what", "is their", "also that", "other and", "was also",
                               "and be", "be in", "that day", "and think", "think he", "as much", "much as", "with few",
                               "from such", "two long", "one they", "about some", "among its", "goes with", "with you",
                               "you to", "it out", "at your", "our own", "still on", "last two", "all other", "him at",
                               "quite an", "and got", "got into", "into an", "and so", "from these", "along the",
                               "but little", "will go", "go back", "back it", "there will", "be any", "are of",
                               "than ever", "the so", "ago by", "has come", "come within", "been no", "been on",
                               "under an", "our last", "would not", "one may", "that not", "but that", "all those",
                               "those already", "not without", "last and", "made their", "their second", "take back",
                               "back his", "below the", "which an", "saying in", "if these", "these were", "made for",
                               "and just", "day after", "after day", "and not", "not the", "is both", "st and",
                               "between and", "away his", "of has", "in two", "along with", "of others", "ago and",
                               "why the", "especially as", "as those", "for that", "or any", "to six", "long the",
                               "but so", "so it", "it must", "was as", "himself that", "had never", "it have",
                               "and because", "because they", "you the", "are still", "one hundred", "is for",
                               "we might", "not for", "an able", "although there", "been any", "among our", "he goes",
                               "now at", "had his", "his left", "he made", "little of", "is three", "besides the",
                               "in of", "and along", "it also", "how many", "are three", "with himself", "which mr",
                               "that this", "that now", "was of", "and another", "ago are", "of down", "without first",
                               "although not", "are so", "are from", "the back", "back with", "went over", "over to",
                               "how they", "they should", "by very", "were very", "of each", "were you", "you ever",
                               "ever in", "are both", "both in", "that our", "past in", "or other", "getting on",
                               "but have", "saw her", "last ten", "that my", "think that", "last of", "as has",
                               "ago there", "except in", "many more", "nearly all", "whom were", "goes on", "about ten",
                               "who came", "men to", "been long", "who would", "at our", "here during", "during last",
                               "left this", "off long", "her first", "and second", "with those", "are yet", "into and",
                               "out the", "and may", "may come", "come in", "up at", "will all", "all be", "or at",
                               "will it", "in by", "became the", "of most", "of nearly", "nearly every", "himself with",
                               "which many", "out as", "only because", "because of", "not because", "were two",
                               "four and", "and five", "or not", "not by", "the eighth", "eighth and", "and ninth",
                               "think it", "if those", "take more", "them on", "last day", "as having", "only two",
                               "from each", "is our", "our time", "we were", "may that", "for me", "th th", "and st",
                               "have some", "is whether", "shall be", "out or", "take over", "some two", "since there",
                               "seven men", "after they", "they left", "are very", "within their", "where an",
                               "from every", "get in", "where have", "of third", "of fifth", "past few", "us by",
                               "in six", "left at", "they might", "not on", "it ought", "old and", "was still",
                               "of other", "into their", "one was", "and nearly", "nearly in", "at she", "it it",
                               "are sometimes", "but always", "in using", "was all", "all in", "to three", "soon after",
                               "of from", "are on", "on very", "lot of", "time one", "later the", "are more", "have at",
                               "on one", "they came", "came within", "within his", "get through", "through that",
                               "were all", "and many", "of such", "and having", "she also", "of first", "as do",
                               "made by", "for about", "the off", "time had", "if this", "one out", "one in", "but how",
                               "how that", "day or", "perhaps more", "so than", "all their", "have left", "left them",
                               "both at", "he does", "not if", "from at", "is probably", "from nearly", "nearly two",
                               "or out", "have we", "we the", "to by", "were so", "it than", "than has", "even of",
                               "which mrs", "past eight", "that mrs", "to for", "which only", "to he", "by six",
                               "before his", "going the", "time on", "had time", "off from", "and indeed", "think we",
                               "in certain", "came by", "and could", "not make", "on other", "here are", "more in",
                               "when he", "of ninth", "when in", "and since", "in dr", "on th", "two men", "at or",
                               "not get", "get away", "unless the", "last one", "but think", "think the", "except the",
                               "our very", "by other", "were only", "only three", "whom was", "see how", "than their",
                               "not that", "to anything", "anything more", "of more", "at and", "and near", "we still",
                               "up another", "another and", "day will", "than those", "have them", "to with",
                               "which some", "up with", "of is", "in having", "having their", "and every", "one has",
                               "itself by", "be much", "has at", "where my", "on me", "now and", "to me", "me from",
                               "under such", "before that", "that none", "that man", "was his", "her that", "the with",
                               "may about", "were under", "was being", "made on", "was soon", "of with", "although it",
                               "although the", "th st", "between th", "and th", "in last", "down in", "come up",
                               "but her", "had just", "it when", "had on", "when she", "about in", "him that", "in to",
                               "over six", "here from", "than nine", "it over", "is her", "will take", "very soon",
                               "his other", "with any", "although some", "we may", "but all", "all were", "on them",
                               "all six", "six or", "or eight", "but their", "same to", "left on", "having made",
                               "has no", "when they", "are only", "and able", "last to", "has three", "up in",
                               "some one", "one to", "to look", "look after", "no one", "be at", "not however",
                               "but on", "are but", "but one", "who it", "have another", "it from", "from what",
                               "what can", "some men", "and fifth", "was much", "not more", "as when", "have an",
                               "but he", "he still", "that although", "so in", "in either", "either of", "who left",
                               "him of", "thus it", "ago before", "th day", "for mr", "shall have", "it very",
                               "having the", "that any", "by that", "at being", "the things", "and without", "out any",
                               "with one", "behind the", "he cannot", "up on", "will now", "now be", "not how",
                               "though in", "is mrs", "for her", "last was", "probably the", "with nine", "were three",
                               "three in", "from there", "there that", "he may", "is almost", "for now", "was another",
                               "came off", "off at", "by few", "that ever", "having no", "by any", "than to",
                               "from and", "all her", "are being", "them here", "four men", "for any", "do the",
                               "same the", "us to", "is six", "by two", "that have", "us on", "on all", "but with",
                               "has some", "thing is", "and certain", "out and", "we said", "it really", "then we",
                               "it more", "more at", "one is", "other is", "what are", "this as", "and yet",
                               "all about", "or about", "its own", "this very", "to being", "being an", "ago the",
                               "from either", "left that", "for was", "of even", "here few", "ago in", "the above",
                               "have any", "day before", "day an", "make it", "it almost", "almost certain",
                               "certain that", "day by", "since last", "had this", "day there", "whether he", "he or",
                               "would come", "for him", "nothing could", "until she", "they come", "including an",
                               "out this", "been re", "of out", "from long", "them this", "this it", "nor do", "do we",
                               "it if", "if you", "nine and", "that very", "until about", "he been", "she had",
                               "there the", "as some", "and until", "yet have", "at not", "which as", "upon what",
                               "of only", "only about", "and on", "about one", "whom the", "at of", "and non",
                               "in four", "is also", "here there", "but what", "not able", "ninth and", "is again",
                               "among some", "by him", "the tenth", "of she", "against in", "by so", "so doing",
                               "he might", "of doing", "first or", "there can", "be no", "make its", "where for",
                               "his long", "been for", "since was", "men the", "st on", "about six", "down an",
                               "against this", "this the", "here and", "that while", "while this", "are about",
                               "that can", "for you", "for in", "so they", "now before", "who went", "two from",
                               "they can", "can do", "do so", "who cannot", "or will", "the at", "his being", "is ever",
                               "before him", "take an", "out into", "one on", "in what", "am going", "make no",
                               "no such", "as these", "especially to", "us in", "make any", "including the",
                               "it became", "time since", "none is", "ever been", "to th", "others in", "that that",
                               "one man", "us this", "down it", "have before", "before us", "those which", "in each",
                               "gone on", "for six", "without much", "all as", "by mrs", "during my", "came upon",
                               "which also", "the much", "was again", "again the", "with my", "down but", "men have",
                               "that will", "and about", "getting up", "up this", "into it", "over that", "it shall",
                               "do it", "had so", "long been", "lot and", "from one", "not having", "even at",
                               "same time", "all because", "would rather", "go into", "cannot be", "be too", "who get",
                               "were used", "used with", "nothing has", "last for", "only of", "while he", "are under",
                               "it by", "of mrs", "she came", "the non", "as more", "the she", "as just", "to long",
                               "see if", "it on", "being in", "other three", "had with", "also with", "and although",
                               "what he", "her in", "first time", "that even", "have something", "something to",
                               "do with", "too are", "them have", "with about", "through your", "among us",
                               "about that", "now here", "out it", "had ever", "something in", "she made",
                               "against him", "him have", "went for", "also to", "and especially", "for ten",
                               "where there", "eight or", "or ten", "ten men", "can make", "is first", "left many",
                               "they got", "got her", "her back", "and use", "but those", "them will", "made here",
                               "from th", "th to", "get her", "about eight", "what was", "but as", "more so",
                               "at eight", "at four", "near this", "is against", "are against", "by every", "we can",
                               "upon to", "are much", "much too", "that for", "for once", "is behind", "in among",
                               "hundred men", "within ten", "had few", "from out", "her the", "with two", "are said",
                               "but are", "last man", "is thus", "five and", "all he", "and came", "came back",
                               "his second", "all day", "day which", "inside of", "may she", "at little", "to st",
                               "of lot", "one were", "be almost", "were the", "since it", "five thousand", "all last",
                               "already the", "not one", "one other", "had their", "now on", "his will", "at each",
                               "him and", "who did", "not take", "they may", "may see", "we know", "know nothing",
                               "nothing in", "if not", "on as", "toward its", "in them", "with in", "since that",
                               "who take", "did the", "it into", "first ever", "around her", "see the", "said she",
                               "used at", "look of", "is only", "after mr", "under certain", "for other", "it having",
                               "of said", "among whom", "were many", "after many", "come out", "of how", "been under",
                               "including many", "is is", "th from", "go for", "in for", "from you", "you as",
                               "that said", "me as", "day than", "for long", "long time", "time they", "go to",
                               "from five", "five to", "in re", "made this", "after four", "as you", "you on",
                               "day said", "said the", "in old", "which by", "here some", "ago of", "that up",
                               "not made", "that and", "whether they", "will have", "have used", "which every",
                               "are any", "the who", "only after", "but three", "then on", "is over", "here with",
                               "to within", "within four", "me by", "were more", "will you", "none in", "which all",
                               "perhaps you", "you may", "how the", "and now", "soon to", "for such", "got off",
                               "not very", "and only", "off of", "are most", "man who", "take the", "are able",
                               "out at", "were said", "were it", "it not", "an under", "for your", "past have",
                               "have little", "the said", "than there", "is between", "and these", "for them",
                               "them by", "and am", "was little", "but would", "at such", "time as", "by its", "who to",
                               "it something", "something more", "just and", "me the", "do this", "all or", "or of",
                               "said his", "while it", "is it", "the over", "on both", "would seem", "for as",
                               "yet they", "with whom", "whom he", "had had", "him with", "it again", "unless it",
                               "as had", "when our", "else in", "used on", "on any", "go out", "ago an", "this was",
                               "which still", "as near", "as may", "be under", "against all", "under way", "way for",
                               "not come", "one but", "is but", "since our", "only for", "this seems", "by my",
                               "one fourth", "fourth of", "them are", "with seven", "during an", "still in", "out last",
                               "third and", "and fourth", "second and", "and but", "off about", "are just", "not do",
                               "these are", "has one", "by them", "man on", "for not", "not now", "in saying",
                               "that does", "much in", "out her", "may has", "these two", "of th", "make him",
                               "here but", "away by", "and perhaps", "not all", "have nearly", "off to", "its use",
                               "use is", "he seemed", "not always", "day one", "was their", "all such", "so of",
                               "another day", "us but", "so very", "that few", "indeed the", "if one", "one so",
                               "since on", "was something", "something of", "only the", "not much", "is having",
                               "it which", "it much", "have two", "was from", "take my", "and probably", "are among",
                               "but has", "has its", "and never", "nearly as", "it here", "come at", "but she",
                               "than this", "to or", "man they", "himself the", "they all", "in use", "use in",
                               "that may", "as any", "is yet", "about by", "in you", "here by", "take her",
                               "those that", "have almost", "almost always", "with very", "whom we", "many other",
                               "past the", "that more", "up their", "is if", "anything but", "gone by", "by up",
                               "not few", "time was", "is here", "your own", "without having", "were some", "way from",
                               "have probably", "who come", "although he", "with little", "has every", "many to",
                               "fifth time", "time during", "have again", "where is", "is mr", "say is", "to them",
                               "they still", "even for", "for day", "me but", "but said", "upon and", "it were",
                               "yet of", "who should", "not at", "after his", "whether its", "below and", "they cannot",
                               "he said", "said but", "man or", "no use", "them there", "us of", "such was",
                               "that almost", "were mr", "or when", "is too", "and let", "let the", "with no",
                               "other than", "me so", "be mr", "something from", "another the", "his more",
                               "having its", "and each", "within its", "after one", "except for", "are for", "you if",
                               "one now", "though his", "not doing", "doing something", "out what", "should he",
                               "doing it", "some old", "came across", "used by", "are getting", "than for", "any time",
                               "as were", "mr and", "and been", "then by", "what for", "and over", "over again",
                               "again that", "that but", "but four", "will he", "over one", "long of", "about five",
                               "over by", "it said", "said he", "will make", "make way", "beyond the", "than he",
                               "are without", "either in", "why it", "thus the", "before you", "had at", "are such",
                               "against some", "here which", "since to", "two more", "while on", "she went",
                               "since with", "out again", "after her", "is every", "that something", "something was",
                               "which on", "was only", "not had", "had more", "take away", "or mr", "left of",
                               "not over", "but very", "or make", "it first", "first he", "when about", "and should",
                               "he never", "upon all", "that had", "they make", "being no", "few have", "himself as",
                               "fourth day", "day over", "then was", "are again", "are these", "with us", "be when",
                               "others will", "few of", "his many", "use some", "which seems", "only he", "after he",
                               "it but", "time which", "they be", "be just", "from day", "almost from", "almost all",
                               "yet there", "may or", "or may", "is we", "out not", "go the", "though their", "of on",
                               "among men", "perhaps the", "most in", "what one", "one might", "might look", "look for",
                               "next at", "many as", "itself in", "is perhaps", "was first", "these men", "or to",
                               "them at", "any way", "although its", "and seven", "of by", "among his", "being at",
                               "man is", "are especially", "those to", "of under", "both to", "yet it", "and third",
                               "and those", "the really", "those for", "for men", "with long", "you but",
                               "probably will", "be from", "who will", "it all", "own way", "time that", "has also",
                               "not already", "whom you", "you and", "him so", "but is", "out by", "vs the", "had made",
                               "made two", "that certain", "three thousand", "that most", "so to", "us he", "day mr",
                               "has it", "it we", "however we", "himself to", "perhaps it", "whether any", "he himself",
                               "himself has", "made no", "for he", "the while", "he probably", "probably has",
                               "was this", "he can", "could ever", "with ten", "last time", "time by", "what we",
                               "off this", "who after", "off their", "to others", "has an", "and nine", "nothing else",
                               "between seventh", "seventh and", "and eighth", "or seven", "is then", "by five",
                               "each with", "so the", "to third", "to most", "than before", "as long", "is among",
                               "never left", "old he", "there as", "that both", "time past", "on certain", "have said",
                               "with certain", "him last", "more were", "but in", "so as", "has more", "nine other",
                               "since but", "there would", "of anything", "that might", "you think", "about time",
                               "the thousand", "to myself", "not even", "to itself", "came under", "will for",
                               "is doing", "same thing", "no on", "last by", "would take", "only as", "in many",
                               "second of", "than on", "the nd", "do if", "for certain", "at mr", "went off", "off it",
                               "being of", "since mr", "their five", "said if", "from me", "me an", "was almost",
                               "when more", "last four", "their first", "her as", "will certainly", "again and",
                               "to much", "until to", "two to", "to four", "past is", "because there", "is any",
                               "but because", "seven of", "then said", "said is", "do anything", "anything to",
                               "as day", "the inside", "little or", "or no", "for and", "of he", "over all",
                               "about men", "men with", "once and", "that five", "men by", "take them", "with and",
                               "however and", "on my", "both were", "if there", "there had", "was some", "of once",
                               "on five", "and certainly", "by being", "back in", "very long", "and must",
                               "certainly one", "may it", "day as", "to let", "though you", "you about", "off with",
                               "them for", "day this", "this would", "it did", "who does", "is day", "only those",
                               "who know", "know how", "how to", "to is", "and said", "about mr", "of re",
                               "which cannot", "who now", "then to", "time ago", "ago he", "him mr", "during his",
                               "near to", "past five", "until we", "if nothing", "be said", "know if", "two million",
                               "hundred thousand", "during this", "from time", "about their", "time between",
                               "they also", "also for", "not see", "how he", "then in", "were out", "out three",
                               "also on", "is none", "none of", "they go", "six of", "the after", "and left",
                               "little over", "between their", "goes out", "five in", "between mr", "they do", "and do",
                               "this with", "of getting", "way through", "over this", "may have", "let us", "on those",
                               "going over", "left an", "he left", "left and", "some to", "still at", "nearly five",
                               "three to", "your first", "which for", "for time", "which make", "make us", "upon in",
                               "had about", "which most", "has still", "especially on", "the will", "will of",
                               "may and", "to very", "very nearly", "time after", "long but", "nearly so", "long as",
                               "as from", "in not", "not being", "with six", "which her", "now nearly", "made of",
                               "from ten", "for every", "between this", "before it", "having had", "being very",
                               "was for", "of himself", "himself and", "are even", "including mr", "and here",
                               "here we", "men were", "left for", "get off", "off but", "one as", "came at", "but dr",
                               "man to", "by day", "was therefore", "the look", "look out", "and tenth", "which could",
                               "it until", "us at", "that must", "long before", "them up", "than would", "seemed more",
                               "made one", "while we", "let it", "between an", "here it", "out between", "th with",
                               "and through", "any man", "could have", "it could", "before when", "come into",
                               "will we", "will no", "ago to", "both here", "only was", "then the", "up more",
                               "gone out", "out through", "through some", "say on", "indeed be", "on long", "even when",
                               "him has", "among those", "also by", "last is", "day two", "of next", "think this",
                               "are off", "off again", "again in", "said mr", "that am", "but am", "now almost",
                               "am the", "by saying", "be had", "yet made", "made her", "itself the", "now not",
                               "got his", "really is", "about nothing", "nothing the", "have nothing", "nothing is",
                               "day when", "than as", "and does", "certainly not", "between us", "as are", "are and",
                               "one the", "an often", "an almost", "has his", "may we", "him into", "the for",
                               "into two", "the little", "is therefore", "and your", "to but", "me because", "am to",
                               "as for", "now this", "of thousand", "in we", "much we", "because we", "that though",
                               "though this", "was re", "still it", "and why", "ago from", "because in", "now that",
                               "happen to", "could never", "never have", "men was", "was our", "all these", "in or",
                               "or what", "with men", "men one", "gone into", "and de", "each at", "never had",
                               "to either", "it or", "which that", "were five", "no to", "the know", "man with",
                               "it of", "others have", "but can", "can to", "nearly eight", "ago had", "from where",
                               "by of", "had almost", "there be", "now under", "things and", "come for", "said this",
                               "that those", "about it", "could make", "when did", "without their", "than about",
                               "in but", "at with", "do at", "only at", "still be", "re at", "in at", "he and",
                               "through with", "men will", "were never", "past four", "while in", "could see", "see no",
                               "ago that", "in upon", "was when", "within few", "here until", "until this", "away the",
                               "before them", "not his", "and into", "itself with", "him an", "all but", "being that",
                               "with these", "by those", "there to", "with most", "see you", "was mr", "were as",
                               "up his", "but many", "see and", "since we", "have one", "know his", "another has",
                               "used for", "by whom", "them with", "all can", "for being", "all will", "over its",
                               "on last", "four other", "then made", "of you", "certainly have", "for my",
                               "with others", "others are", "its way", "way out", "is really", "had its", "us who",
                               "it there", "be time", "us from", "in after", "among which", "and none", "after that",
                               "first in", "he as", "day from", "take on", "when an", "of would", "would he", "to more",
                               "now with", "against it", "not before", "no the", "way with", "with such", "into which",
                               "but must", "goes to", "has he", "of against", "against their", "perhaps to", "from on",
                               "to eight", "next the", "went on", "as mr", "while to", "this long", "he became",
                               "where his", "take some", "by both", "is another", "be three", "it made", "its first",
                               "be rather", "with three", "two by", "them into", "into all", "them if", "little more",
                               "five or", "up nearly", "after ten", "to still", "said by", "and see", "were really",
                               "day we", "for may", "been quite", "before she", "not its", "also the", "as could",
                               "via the", "to both", "much so", "till the", "no and", "st at", "he ever", "got in",
                               "in during", "having come", "been out", "about at", "went away", "were quite", "who in",
                               "that much", "not any", "up an", "as will", "she may", "may yet", "yet be", "in here",
                               "not it", "about of", "was over", "it mr", "of us", "there with", "around us", "only by",
                               "but once", "were there", "men all", "the then", "after few", "himself in", "was among",
                               "among her", "seventh day", "in is", "three others", "began to", "our first", "and re",
                               "be over", "over there", "be left", "only four", "used their", "with mrs", "upon mr",
                               "with having", "then it", "were first", "just one", "up all", "will do", "against them",
                               "them of", "know something", "which its", "especially at", "day have", "itself is",
                               "at three", "after two", "nearly the", "you by", "than three", "who with", "things in",
                               "however there", "or so", "so ago", "did to", "said as", "as no", "having an", "to none",
                               "were but", "it used", "and sometimes", "of sixth", "sixth and", "we would", "at mrs",
                               "even then", "then as", "only and", "over our", "of something", "each other", "other in",
                               "should do", "do as", "much for", "we get", "get from", "after its", "with other",
                               "it before", "now seems", "will the", "and what", "on mr", "st in", "on sixth",
                               "sixth day", "and still", "you did", "which now", "but about", "about an", "by certain",
                               "if anything", "him all", "soon be", "be as", "as ever", "ago for", "there came",
                               "at my", "only this", "this and", "nothing more", "very many", "will also", "time has",
                               "himself at", "are few", "make his", "on him", "them an", "but also", "also of",
                               "against most", "do nothing", "nothing for", "when at", "him this", "almost to",
                               "though they", "once that", "may take", "when one", "do little", "little and",
                               "would do", "although no", "within an", "again it", "has to", "does so", "so because",
                               "than an", "does in", "which one", "has thus", "is four", "later by", "of but", "as was",
                               "and even", "all through", "one with", "during their", "as made", "now have", "again on",
                               "which with", "four thousand", "around and", "into any", "me this", "him down",
                               "get back", "in will", "for himself", "of little", "which can", "said of", "way here",
                               "here as", "do he", "has used", "used his", "by it", "long to", "another to",
                               "here will", "what mr", "has there", "there been", "first two", "are too", "but while",
                               "day his", "there he", "through all", "in just", "was rather", "little that",
                               "said over", "been almost", "its second", "therefore the", "where does", "does that",
                               "it then", "then and", "over their", "their more", "which after", "old mr", "by what",
                               "as all", "you an", "up mr", "day long", "him we", "others to", "would certainly",
                               "st st", "first day", "probably have", "be out", "their very", "but which",
                               "little else", "each in", "one third", "those whose", "are with", "it any",
                               "do something", "has two", "so little", "which should", "for non", "while another",
                               "let him", "of seven", "tell the", "his th", "again this", "were four", "by by", "at at",
                               "since its", "others he", "is near", "her last", "time but", "man for", "old the",
                               "be or", "will that", "have only", "made few", "just before", "if in", "here about",
                               "goes for", "for nothing", "since for", "some very", "take it", "behind him", "only has",
                               "been with", "long since", "said on", "has said", "but long", "for so", "for saying",
                               "last it", "it under", "by all", "seems in", "way or", "into its", "last but",
                               "nor does", "does she", "with anything", "as soon", "soon as", "to non", "her way",
                               "next in", "made him", "about his", "for quite", "seven or", "as often", "has that",
                               "have never", "be doing", "his re", "look at", "them had", "them but", "was what",
                               "in before", "whether his", "his the", "use the", "away their", "must now", "the seven",
                               "on such", "things as", "much and", "or his", "go with", "with me", "nor has",
                               "little is", "th in", "ago were", "could come", "the that", "take up", "let them",
                               "had yet", "which did", "which there", "while her", "over but", "not until",
                               "until that", "has so", "take his", "it no", "at two", "second was", "that cannot",
                               "to tell", "to fourth", "is off", "no of", "th she", "see who", "on either", "left but",
                               "much that", "cannot do", "all are", "came over", "been left", "were both", "had always",
                               "been their", "or nothing", "could do", "man at", "here is", "that used", "used in",
                               "are also", "also in", "back from", "he even", "time being", "come on", "off as",
                               "as only", "to are", "are nearly", "was out", "fifth and", "has got", "but no",
                               "many and", "which this", "that way", "way but", "in long", "but your", "for mrs",
                               "near st", "to through", "but our", "not quite", "does the", "himself against",
                               "past ten", "am at", "at almost", "almost nothing", "time an", "among these", "these is",
                               "made against", "th after", "such thing", "thing we", "time it", "said for", "quite so",
                               "while that", "himself was", "get an", "once been", "been much", "and eight", "that don",
                               "of don", "third of", "both on", "before or", "some and", "and such", "as would",
                               "up there", "when his", "all this", "make them", "who do", "do now", "are after",
                               "had long", "how much", "and how", "much he", "from another", "with so", "from those",
                               "for whom", "as not", "way it", "can it", "will long", "because he", "should go",
                               "since an", "are certain", "certain to", "one can", "ever the", "them not",
                               "until after", "can get", "from my", "yet in", "we look", "thing in", "was against",
                               "on many", "many were", "were going", "two and", "still and", "get along", "any more",
                               "more that", "be little", "for itself", "the out", "his five", "had two", "both by",
                               "and first", "then with", "to back", "back up", "up our", "perhaps for", "only just",
                               "no later", "than had", "been before", "against such", "did much", "to whether",
                               "five other", "still going", "on there", "against three", "with by", "last may",
                               "made what", "this should", "nor is", "it just", "day she", "its more", "million and",
                               "that her", "ago it", "through long", "went from", "out one", "going and", "after much",
                               "also been", "we went", "see them", "two old", "one being", "or before", "he saw",
                               "saw it", "though it", "now after", "them when", "old when", "not under", "if my",
                               "the has", "does to", "was always", "on again", "first look", "them off", "over eight",
                               "had of", "time at", "or six", "thousand of", "them more", "was its", "but before",
                               "to few", "must take", "left his", "were for", "is through", "that another",
                               "however are", "came through", "through to", "must also", "off without", "but his",
                               "to over", "most to", "does he", "now of", "having his", "are an", "or more",
                               "then came", "came the", "of now", "as so", "himself up", "for what", "against any",
                               "other things", "away when", "have both", "were nearly", "day out", "beyond that",
                               "no way", "between our", "for with", "from three", "me in", "were without", "before any",
                               "million of", "would never", "it my", "by such", "under any", "by man", "seems the",
                               "than others", "last on", "it seem", "even with", "that each", "that from", "does one",
                               "being to", "should make", "himself is", "away of", "had only", "only time",
                               "within five", "long in", "among their", "for on", "how it", "do you", "above all",
                               "was but", "one tenth", "tenth of", "about which", "even after", "he shall", "can not",
                               "all time", "once the", "since been", "him here", "them through", "of before", "on us",
                               "what his", "they and", "for another", "them were", "come of", "from being", "much time",
                               "see that", "or else", "see what", "what this", "where in", "on in", "does and",
                               "is out", "in me", "time next", "seven million", "others the", "to so", "than his",
                               "or has", "including three", "three for", "have got", "got the", "it yet", "them we",
                               "of was", "of while", "both from", "this or", "again next", "by four", "of de",
                               "him were", "by as", "with but", "and doing", "what might", "this we", "who not",
                               "we saw", "have as", "if no", "out an", "it up", "in mrs", "and saw", "being too",
                               "and unless", "he must", "or is", "others and", "upon her", "you make", "make some",
                               "said so", "so we", "are each", "each and", "so his", "be his", "every few",
                               "made about", "being more", "first three", "other men", "in sixth", "between second",
                               "they both", "made as", "since as", "in he", "by us", "be without", "of there",
                               "against an", "who could", "we made", "think in", "for seven", "ever to", "which might",
                               "be there", "but these", "all we", "later at", "from four", "four to", "things have",
                               "and within", "from over", "so did", "her by", "her most", "what she", "old was",
                               "through an", "me was", "in said", "use his", "as under", "why so", "so if", "if mr",
                               "then is", "is his", "same as", "old men", "as our", "where two", "them he", "more for",
                               "away in", "the eight", "time this", "for these", "past to", "or another", "was ever",
                               "ever more", "in as", "there by", "them who", "through their", "the saying",
                               "there nothing", "no for", "went in", "they then", "first man", "go away", "ago we",
                               "had many", "one no", "in second", "were still", "about them", "none the", "behind it",
                               "all have", "which goes", "whose only", "having just", "except to", "one will",
                               "been and", "in almost", "almost any", "around him", "past seven", "would probably",
                               "how long", "are always", "the already", "are almost", "as might", "us we",
                               "was certainly", "when two", "look in", "made with", "at most", "next and", "from six",
                               "are down", "in on", "may the", "during three", "five men", "of fourth", "they get",
                               "old had", "to seven", "about on", "time are", "you can", "can use", "ago when",
                               "when was", "others at", "but its", "also from", "that long", "being used", "ago this",
                               "others by", "time mr", "was often", "to sir", "and rather", "was any", "or she",
                               "along its", "until it", "became so", "even from", "more time", "time than", "than have",
                               "her three", "go over", "fifth day", "over his", "nearly one", "one would", "would only",
                               "in has", "an eighth", "has often", "but last", "be not", "day between", "in st",
                               "should never", "never be", "and used", "used the", "were those", "left one",
                               "come under", "are some", "men had", "me for", "also one", "though no", "other that",
                               "to mrs", "especially those", "which their", "for four", "all was", "or had",
                               "thing for", "of or", "by at", "third the", "that before", "or one", "such that",
                               "have its", "its time", "others on", "rather be", "and last", "with at", "look into",
                               "out two", "no time", "have too", "may also", "time until", "into every", "might seem",
                               "are by", "by men", "each one", "can we", "each to", "us as", "will then", "then be",
                               "down there", "except one", "was he", "would now", "still more", "their third", "as mrs",
                               "her she", "that unless", "to will", "whom it", "time about", "of perhaps", "is up",
                               "day are", "even to", "with just", "the later", "thing as", "is your", "without his",
                               "know of", "made last", "between two", "make of", "whether in", "by more", "have each",
                               "two who", "is especially", "out their", "and sixth", "left by", "which went",
                               "made that", "in whose", "and go", "now going", "or both", "both are", "up what",
                               "within and", "without its", "what you", "you were", "go on", "on and", "and tell",
                               "tell us", "us what", "were probably", "away as", "of back", "little for", "old from",
                               "into another", "them since", "of made", "except by", "had nothing", "but made",
                               "can only", "come through", "own to", "down through", "do they", "only is", "or did",
                               "two for", "perhaps as", "them out", "may with", "made out", "up when", "when mr",
                               "few in", "else and", "over on", "to time", "will at", "of whose", "himself through",
                               "only six", "many others", "though he", "him about", "it they", "long it", "long had",
                               "are having", "above that", "as two", "did it", "it only", "more with", "after it",
                               "even now", "going at", "as man", "to men", "an eight", "her from", "were most",
                               "out there", "did in", "just about", "now as", "was under", "with either", "either the",
                               "by three", "to nine", "their old", "we always", "always have", "and always", "if by",
                               "may do", "for no", "on of", "look upon", "you know", "from certain", "going through",
                               "were already", "first at", "they not", "unless they", "out during", "the nine",
                               "others had", "for we", "should we", "make in", "said has", "since and", "over two",
                               "in still", "way down", "down he", "over five", "because some", "get more",
                               "first thing", "thing that", "but whose", "men are", "though many", "many have",
                               "made before", "into being", "she would", "it so", "say as", "been without",
                               "especially when", "would you", "take your", "eight and", "most other", "indeed in",
                               "yet that", "up as", "at will", "at in", "that so", "since this", "doing in", "it now",
                               "was within", "within three", "may to", "make our", "here again", "there of", "or its",
                               "now is", "seemed so", "of are", "and above", "after my", "three and", "rather more",
                               "ever for", "four the", "or by", "got on", "however were", "them over", "will in",
                               "or over", "as anything", "anything that", "you do", "eight in", "an in", "not whether",
                               "he be", "in us", "when man", "to when", "he used", "so on", "for nearly", "by third",
                               "near his", "make her", "getting out", "cannot get", "there before", "when first",
                               "who made", "much has", "can see", "no little", "at what", "left it", "by to",
                               "and really", "here he", "probably because", "are certainly", "of hundred", "at he",
                               "do that", "might not", "have now", "by just", "than all", "and became", "more from",
                               "eight of", "know what", "into my", "here was", "than four", "get out", "is able",
                               "that same", "we just", "have our", "of yet", "getting in", "them some", "some with",
                               "say whether", "say they", "before its", "say with", "in was", "in little", "they seem",
                               "both his", "was near", "them that", "not think", "no at", "old were", "next six",
                               "see his", "at th", "almost an", "so he", "though there", "the would", "or some",
                               "second time", "gone through", "between him", "it certainly", "take all", "had one",
                               "day during", "and whose", "whose first", "for next", "with only", "the which",
                               "come off", "way at", "and whether", "that three", "after three", "as few", "that over",
                               "that could", "take its", "been two", "other on", "said they", "other for", "four for",
                               "of between", "take that", "may now", "away at", "against one", "in fourth", "for st",
                               "he first", "many that", "that other", "here for", "you very", "at long", "only when",
                               "how do", "it this", "either to", "him or", "left its", "without being", "getting their",
                               "up after", "more by", "men from", "make one", "one more", "old one", "made any",
                               "before at", "one time", "take in", "they see", "are left", "left out", "almost as",
                               "in three", "will last", "gone the", "too that", "even more", "all been", "off more",
                               "for very", "thing about", "about any", "and take", "we don", "don know", "than some",
                               "others that", "for use", "use at", "another for", "of eighth", "about was",
                               "here since", "but still", "not from", "is anything", "with nothing", "nothing can",
                               "had for", "day so", "ago has", "out all", "who said", "those at", "under its",
                               "said you", "you so", "been of", "or an", "alone is", "another million", "was anything",
                               "under one", "each day", "had by", "are doing", "than during", "very near",
                               "under whose", "was however", "so by", "no in", "only be", "on from", "her two",
                               "neither of", "them it", "certain of", "by going", "few who", "in under", "who first",
                               "have much", "this most", "not often", "often that", "but you", "so this", "under no",
                               "be most", "but if", "what will", "do what", "seem that", "around their", "in even",
                               "rather to", "is getting", "getting to", "why is", "can tell", "why they", "this could",
                               "perhaps he", "or he", "or perhaps", "in are", "of have", "was up", "later but",
                               "two the", "them is", "ever before", "before was", "their past", "us now", "then some",
                               "with five", "might come", "come along", "although most", "down as", "in nearly",
                               "way by", "was had", "may mrs", "but neither", "some in", "say there", "since had",
                               "and being", "me of", "still with", "of during", "her past", "into five", "himself an",
                               "or how", "may after", "them mr", "around its", "was perhaps", "than last", "it she",
                               "not tell", "each on", "himself on", "have long", "be here", "against that", "of way",
                               "man but", "has very", "and get", "where are", "of since", "as your", "nor any",
                               "had any", "almost the", "him up", "he ll", "ll be", "may th", "it goes", "for those",
                               "with as", "first it", "including one", "although they", "may is", "this old",
                               "now been", "yet he", "this may", "be all", "me there", "still is", "the saw",
                               "one million", "six other", "way into", "and using", "but without", "against other",
                               "from using", "who goes", "within one", "already has", "has much", "he also",
                               "down this", "her and", "until its", "their time", "the million", "of million",
                               "from dr", "out against", "also had", "just that", "but did", "were then", "to may",
                               "is certain", "as such", "see whether", "whether this", "of had", "had they",
                               "often been", "been my", "lot to", "it went", "who may", "of we", "two ago",
                               "but cannot", "using them", "that left", "it about", "first second", "are mr", "one she",
                               "without them", "however as", "they became", "be about", "off all", "if were",
                               "against its", "may at", "look to", "in eight", "in now", "not too", "always with",
                               "nine of", "in him", "than mr", "little time", "without an", "back the", "others may",
                               "at him", "day may", "last been", "than seven", "if his", "into some", "against mr",
                               "is sometimes", "many are", "may on", "was without", "how this", "day were", "was time",
                               "one from", "again last", "may by", "same in", "perhaps by", "for both", "has almost",
                               "he were", "past six", "first six", "one mr", "her on", "him there", "once it",
                               "which these", "may was", "by only", "and day", "probably never", "often and", "had it",
                               "under what", "by either", "were always", "had and", "its next", "was during",
                               "as among", "they never", "lot more", "if had", "between her", "them only", "if at",
                               "here they", "be for", "time within", "not what", "them than", "was before",
                               "know their", "should it", "himself but", "will they", "them so", "one another",
                               "under their", "the no", "other of", "down upon", "now there", "both for", "others from",
                               "because she", "herself the", "and himself", "must first", "through which", "there but",
                               "that made", "did they", "and seemed", "might make", "there since", "the still",
                               "above is", "that ought", "and where", "still some", "from as", "who seems", "they used",
                               "they made", "from getting", "get on", "men under", "take for", "himself of",
                               "for myself", "some or", "know why", "why we", "who he", "you of", "until two",
                               "myself and", "in quite", "us into", "on time", "time or", "off for", "go there",
                               "between here", "no which", "but do", "think you", "as by", "when this", "no was",
                               "four of", "him out", "too little", "come the", "be between", "on eighth", "where its",
                               "if so", "just so", "much the", "here or", "had such", "nothing was", "come and",
                               "take their", "though we", "come before", "were down", "first was", "but may", "do or",
                               "say anything", "can have", "have their", "after eight", "that probably", "as saying",
                               "saying the", "make out", "which of", "still to", "had something", "however mr",
                               "upon as", "as certain", "he who", "had four", "there one", "take to", "things with",
                               "however to", "on another", "although we", "us have", "than did", "until his", "to of",
                               "who they", "another on", "or we", "on almost", "no second", "that men", "you could",
                               "which first", "it off", "them they", "way and", "on each", "so does", "he not",
                               "were from", "of using", "using it", "way they", "of day", "not with", "with nearly",
                               "up every", "is once", "nothing and", "all it", "get their", "day more", "on most",
                               "is my", "on or", "third time", "it left", "not going", "by ten", "said then",
                               "by another", "said at", "now one", "there from", "were before", "do away", "and old",
                               "said will", "all with", "about such", "for for", "between those", "be nearly",
                               "said not", "up during", "be two", "now being", "at seven", "are one", "certainly be",
                               "it are", "us all", "again for", "saw in", "at between", "have of", "before we",
                               "than what", "nor the", "something as", "ago as", "look back", "were able", "one cannot",
                               "were much", "some said", "even though", "all is", "men he", "first few", "either as",
                               "so and", "the go", "go by", "will see", "see this", "past that", "know and", "to while",
                               "while other", "lot in", "there still", "now are", "been going", "much at",
                               "from second", "than from", "goes the", "some have", "with dr", "one ever", "to on",
                               "us through", "her for", "three million", "than either", "you cannot", "one an",
                               "few men", "than many", "by much", "as have", "say to", "which since", "from whom",
                               "almost too", "much was", "not two", "one by", "but even", "even this", "the once",
                               "them after", "nor did", "might go", "that within", "said would", "man had",
                               "be getting", "by second", "should they", "for each", "and say", "is past", "past for",
                               "only other", "other from", "alone the", "no not", "then went", "these have",
                               "always be", "up its", "do his", "however has", "if its", "so soon", "before there",
                               "what should", "that things", "things are", "has certainly", "from last", "once in",
                               "in while", "go down", "more will", "again been", "use to", "know when", "time last",
                               "until few", "except that", "by eight", "day made", "while they", "made such",
                               "and seems", "seems more", "do all", "at these", "more the", "her an", "say you",
                               "anything in", "will always", "be our", "now even", "away for", "was used", "just after",
                               "his use", "may in", "by most", "as did", "his back", "back by", "also is", "they ought",
                               "each man", "is down", "others it", "happen in", "said was", "three four",
                               "and including", "this being", "doing nothing", "has seemed", "all along", "along that",
                               "than anything", "anything else", "me when", "may for", "ago but", "man mr", "made me",
                               "him before", "at time", "was five", "nearly an", "when its", "to as", "does this",
                               "even without", "during one", "it began", "of near", "nine men", "for getting",
                               "went through", "at every", "would it", "from old", "against which", "might as",
                               "been many", "but had", "was once", "way as", "was off", "past three", "down into",
                               "see an", "out so", "only nine", "as every", "on st", "little but", "but soon",
                               "has many", "other was", "use for", "such way", "been just", "the almost", "who can",
                               "had before", "whom mr", "men as", "can and", "not let", "or should", "him over",
                               "know to", "had my", "out among", "into four", "me on", "with not", "not little",
                               "little if", "over them", "since have", "been all", "all one", "one way", "each the",
                               "should say", "whether mr", "there at", "was now", "by himself", "or be", "time have",
                               "men would", "these the", "was able", "behind them", "two had", "she then", "it since",
                               "you go", "about my", "for while", "ten and", "another in", "time there", "from near",
                               "look and", "say about", "when dr", "me you", "probably no", "than you", "than she",
                               "her up", "do these", "look on", "were again", "where mr", "through this", "only are",
                               "be long", "that nothing", "and sir", "me up", "this for", "only seven", "then there",
                               "say how", "how in", "though its", "will tell", "tell you", "you all", "whether to",
                               "been there", "than five", "his most", "which both", "also at", "last six", "under mr",
                               "come back", "in day", "or later", "to she", "over her", "do much", "since when",
                               "at later", "take two", "each was", "their ninth", "using the", "beyond its", "if she",
                               "went there", "of seventh", "much is", "this one", "in in", "whom she", "go but",
                               "ever have", "was neither", "was most", "second one", "know we", "back for",
                               "of including", "why this", "not since", "at old", "take any", "during her", "while his",
                               "nearly million", "myself in", "see is", "is who", "get it", "and things", "its only",
                               "last have", "from us", "but this", "of when", "has something", "but some", "what does",
                               "any day", "can you", "with what", "just come", "there they", "of saw", "in past",
                               "way there", "all very", "but more", "we left", "one it", "happening to", "things of",
                               "by time", "always in", "although in", "this they", "at many", "to almost", "million in",
                               "except when", "as other", "never saw", "their th", "was having", "look up", "next may",
                               "on much", "seven more", "that others", "about with", "it what", "can they",
                               "never again", "while she", "including all", "now all", "do for", "would say",
                               "those now", "be something", "him is", "are their", "second is", "back some", "are four",
                               "this be", "so would", "ago one", "been his", "his only", "said and", "those not",
                               "before mr", "make every", "some day", "day not", "went about", "his in", "were getting",
                               "or near", "the de", "when their", "those two", "however it", "he then", "for others",
                               "two in", "two on", "unless you", "you should", "should come", "come here", "here you",
                               "he ought", "not and", "over with", "is even", "for has", "perhaps no", "unless we",
                               "us our", "our two", "two most", "over it", "especially by", "have about", "much from",
                               "been getting", "all men", "who for", "yet we", "another way", "are you", "old of",
                               "on when", "on lot", "lot at", "me out", "even before", "came before", "during that",
                               "things they", "by long", "certainly no", "or after", "in third", "as and", "it back",
                               "really the", "such things", "through and", "it an", "left him", "can take",
                               "when three", "nine day", "let not", "not your", "yes he", "of if", "more men",
                               "get under", "time she", "been too", "and too", "now by", "against two", "later it",
                               "over for", "with time", "so have", "while an", "in how", "just made", "their seventh",
                               "which last", "but among", "which seemed", "what in", "where her", "are her", "six and",
                               "nearly to", "out after", "so often", "and seventh", "should know", "things the",
                               "time some", "some things", "too in", "as very", "including in", "by little",
                               "himself out", "of thing", "thing the", "up about", "he began", "have you", "at after",
                               "around at", "get to", "if ever", "than are", "now no", "ever on", "to happen", "you it",
                               "he only", "am an", "went the", "only way", "who use", "is two", "before had", "now has",
                               "which not", "them being", "down or", "again as", "made himself", "we came", "its old",
                               "they now", "there you", "to said", "near and", "not every", "from very", "or just",
                               "just to", "him but", "even among", "his later", "again by", "only were", "you not",
                               "around it", "that make", "who think", "by others", "others but", "thing they",
                               "she got", "got some", "herself and", "their two", "for lot", "see in", "our day",
                               "now for", "why some", "nothing at", "have him", "got out", "out before", "around them",
                               "said there", "left to", "but nothing", "this much", "him was", "know it",
                               "although she", "do some", "is before", "been that", "never before", "for going",
                               "at over", "sometimes the", "sometimes in", "where all", "say he", "by but", "for there",
                               "in later", "who on", "what to", "get him", "again he", "day some", "my way", "too for",
                               "that first", "first came", "down their", "down of", "me is", "whom have", "six to",
                               "old who", "the had", "from man", "it go", "or whether", "another one", "be such",
                               "has another", "do to", "some the", "until her", "man as", "many things", "on little",
                               "where else", "time were", "two at", "them back", "are never", "her was", "where do",
                               "below is", "got their", "day they", "even an", "when on", "the by", "often as",
                               "out his", "but don", "you your", "go as", "he couldn", "not there", "there it",
                               "when some", "were against", "day last", "had also", "by not", "since she", "may he",
                               "again is", "too many", "at another", "she and", "on fifth", "time from", "who she",
                               "be if", "many in", "have time", "and come", "since her", "down his", "tell his",
                               "behind and", "nothing that", "and across", "about being", "been only", "from about",
                               "that old", "on what", "between that", "the he", "since their", "was man",
                               "against time", "be still", "since is", "mr de", "her very", "what other", "the not",
                               "were last", "same for", "in first", "we be", "for either", "from mrs", "while some",
                               "time under", "where their", "between his", "own and", "you say", "thing to",
                               "ago while", "after we", "them one", "him while", "about more", "off until", "from many",
                               "man can", "on three", "ago at", "all by", "than thousand", "know is", "but two",
                               "two are", "now used", "first but", "where we", "where more", "as quickly", "quickly as",
                               "or they", "may go", "than will", "is often", "why not", "but up", "we say", "off last",
                               "where you", "is used", "for from", "one we", "her her", "from going", "take out",
                               "as last", "off that", "as with", "are they", "as her", "men that", "there could",
                               "are used", "always has", "at second", "much about", "they tell", "already at",
                               "but does", "just when", "in there", "himself by", "me at", "long be", "be among",
                               "will get", "what have", "on these", "was really", "make me", "about all", "it down",
                               "does it", "is neither", "he the", "very old", "always there", "you take", "whether we",
                               "that here", "only last", "day since", "my time", "without ever", "that since",
                               "his three", "must not", "rather it", "over as", "this but", "some as", "itself on",
                               "for over", "you come", "at me", "are indeed", "none too", "there who", "that without",
                               "without it", "what do", "do know", "two very", "so now", "up last", "now so",
                               "from above", "been here", "being one", "it little", "know for", "as men", "are up",
                               "can say", "after six", "here she", "in lot", "near by", "none other", "here all",
                               "other two", "just in", "been nearly", "say we", "have in", "little in", "was three",
                               "which dr", "who when", "had first", "tell whether", "quite the", "on between",
                               "both and", "first one", "again with", "little man", "from little", "or from",
                               "have many", "been doing", "see more", "have thus", "gone and", "we got", "too the",
                               "way things", "within our", "think they", "is she", "it ll", "ll take", "take you",
                               "day if", "you be", "things can", "as others", "so can", "be he", "two have",
                               "and might", "day ago", "certainly the", "by will", "thing was", "since then",
                               "been since", "else has", "just where", "you see", "then when", "his very", "you you",
                               "not he", "my first", "using his", "but mr", "from of", "goes through", "often be",
                               "now two", "him she", "for dr", "have with", "alone and", "to who", "while others",
                               "four were", "between fifth", "which until", "until now", "not many", "for little",
                               "even while", "some little", "doing anything", "especially for", "to nearly", "own in",
                               "in itself", "day had", "off some", "were or", "through two", "but where", "at nearly",
                               "have this", "around for", "you at", "of second", "us about", "but an", "had another",
                               "except as", "who also", "for five", "him if", "would go", "for most", "anything and",
                               "been about", "or anything", "can look", "look over", "with each", "to something",
                               "all know", "just out", "there this", "may look", "and later", "between himself",
                               "what were", "would soon", "soon he", "he in", "how and", "for eight", "their little",
                               "that being", "come when", "when these", "is he", "the ever", "next three", "do and",
                               "those from", "other but", "thousand men", "from behind", "here has", "was behind",
                               "many will", "day would", "of ever", "through three", "day no", "than ten", "over mr",
                               "or who", "already there", "at nine", "that having", "though some", "we ll", "ll have",
                               "whether or", "five the", "the mr", "that these", "they ever", "once or", "old saying",
                               "were his", "on more", "got under", "back of", "through my", "perhaps but", "nor are",
                               "few other", "was long", "up again", "only so", "his past", "one whose", "into them",
                               "without some", "me if", "because my", "ten of", "past but", "still very", "now an",
                               "if our", "in something", "something the", "would look", "on day", "away on", "only on",
                               "sixth time", "use as", "perhaps one", "may think", "even that", "up here", "as time",
                               "has about", "two man", "is something", "with over", "of nothing", "all around",
                               "way back", "her next", "to first", "no it", "his time", "from within", "take long",
                               "after next", "have often", "and saying", "but both", "ago now", "but really",
                               "there not", "as am", "she said", "her one", "she must", "she now", "now goes",
                               "during most", "were left", "not after", "against mrs", "during its", "if could",
                               "made another", "and between", "past he", "must come", "until you", "much by",
                               "been few", "once to", "you this", "you is", "indeed it", "nine in", "over of", "of who",
                               "not my", "and getting", "are there", "itself and", "why don", "get little", "out when",
                               "it still", "really was", "say was", "doing all", "could only", "itself of", "you now",
                               "in man", "will was", "not own", "own the", "or and", "is second", "one too",
                               "two things", "there may", "over last", "go in", "men but", "gone from", "himself he",
                               "but then", "alone in", "the or", "is soon", "you from", "by nearly", "that nearly",
                               "on few", "those on", "six in", "had all", "with st", "began in", "has nearly",
                               "been used", "from among", "may as", "here against", "the through", "before but",
                               "first saw", "it through", "men it", "to himself", "became an", "has little",
                               "when such", "but too", "down over", "that should", "way he", "back he", "one after",
                               "after another", "is left", "here not", "now made", "him after", "made since", "up over",
                               "using an", "and gone", "old in", "for man", "things at", "this same", "for third",
                               "only thing", "or with", "him back", "you more", "go about", "there an", "many men",
                               "soon will", "five others", "have your", "said have", "more about", "man will",
                               "only from", "do more", "or too", "used and", "it quite", "other by", "both have",
                               "next four", "you really", "about what", "than if", "on is", "on second", "under two",
                               "these last", "are going", "her time", "was four", "not look", "is gone", "see for",
                               "two were", "here of", "seems almost", "few are", "know but", "even those", "the going",
                               "not their", "is beyond", "over at", "said don", "began that", "know her", "what had",
                               "man we", "me he", "were often", "man could", "and something", "were no", "the under",
                               "that until", "which once", "this that", "be because", "on no", "get at", "certainly is",
                               "than when", "one he", "for or", "gone for", "six men", "will this", "then he",
                               "through it", "men has", "said we", "may seem", "has nothing", "three things",
                               "time may", "about from", "up your", "it away", "back its", "then for", "us are",
                               "say has", "nearly four", "up or", "tell them", "be around", "how is", "is when",
                               "into her", "five million", "or those", "you who", "know all", "for if", "day while",
                               "his all", "may one", "back on", "may say", "into one", "when last", "who during",
                               "them during", "yes the", "way is", "just how", "let her", "do any", "you just",
                               "seems as", "her into", "little after", "old his", "the rather", "just under",
                               "or something", "they said", "for old", "alone to", "us not", "him one", "off her",
                               "let go", "the from", "for they", "her second", "his four", "million or", "saw that",
                               "old man", "was two", "any in", "it never", "ago after", "would just", "us is",
                               "too often", "off an", "more he", "going down", "ago two", "be many", "over long",
                               "other one", "in through", "third was", "here than", "or you", "who really", "were such",
                               "way up", "where one", "for second", "ever there", "only that", "or all", "herself in",
                               "so for", "now his", "how little", "which under", "me my", "there until", "than other",
                               "perhaps they", "is where", "else to", "we go", "but never", "use them", "to next",
                               "in fifth", "that too", "unless he", "time if", "once you", "have three", "later in",
                               "about him", "way on", "had said", "nearly seven", "first they", "would still",
                               "and once", "first by", "had little", "old on", "one must", "say something", "over here",
                               "one else", "up three", "just below", "until he", "another man", "which three",
                               "what on", "two with", "did that", "often the", "whether there", "or their", "or under",
                               "said most", "very first", "although this", "his eight", "said what", "too was",
                               "came and", "from now", "of will", "he soon", "said my", "am in", "up only",
                               "against her", "who by", "see through", "to not", "than six", "by having", "of saying",
                               "the often", "one there", "every four", "something else", "know more", "goes up",
                               "and down", "could tell", "all you", "had used", "we ought", "his third", "ever and",
                               "above it", "ever but", "to having", "take no", "later and", "near th", "also as",
                               "and already", "already under", "besides being", "who since", "did what", "once did",
                               "little has", "go through", "during two", "his fourth", "here now", "now or", "as first",
                               "who so", "both men", "you get", "you would", "just be", "only little", "itself as",
                               "one when", "said many", "its past", "from may", "take time", "who must", "me with",
                               "now what", "nothing about", "old st", "so was", "other more", "know they", "they ll",
                               "here say", "other with", "down all", "said her", "only an", "said before", "up that",
                               "that never", "ago have", "which am", "it without", "me not", "two first", "with last",
                               "thing on", "was past", "way over", "to under", "began his", "at more", "than and",
                               "she could", "come over", "one fifth", "fifth in", "out that", "she does", "by almost",
                               "know as", "one last", "as about", "made mr", "below its", "to there", "more is",
                               "one very", "when her", "for first", "has as", "was because", "because that",
                               "this first", "get over", "will almost", "almost certainly", "both as", "ago about",
                               "here before", "there no", "over seven", "was nothing", "was probably", "he have",
                               "yet when", "re the", "one eighth", "eighth of", "there we", "would ever", "know where",
                               "her th", "with almost", "where no", "about its", "got to", "every time", "me back",
                               "before an", "here under", "by over", "what some", "later to", "however in",
                               "they first", "that did", "are gone", "ago dr", "then have", "although mr", "be nothing",
                               "with something", "could and", "no third", "them what", "what an", "been among",
                               "also an", "and going", "second in", "because its", "what their", "be is", "still have",
                               "why was", "one not", "whom had", "after him", "so quickly", "quickly in", "them while",
                               "of here", "once again", "again we", "are this", "have anything", "things to",
                               "perhaps that", "made much", "about or", "one could", "for last", "did we", "ever was",
                               "him his", "for is", "to during", "between st", "within six", "time while", "what must",
                               "which way", "only their", "in when", "now said", "may day", "getting the", "know about",
                               "use by", "are nothing", "than were", "be near", "take three", "ago with", "has once",
                               "his fifth", "then that", "by on", "sometimes it", "take look", "into such", "to don",
                               "as old", "with for", "still being", "while its", "could it", "so when", "their four",
                               "be by", "except those", "for something", "including those", "left two", "seems so",
                               "out over", "this way", "way we", "be anything", "neither is", "who still", "got it",
                               "next two", "ago mr", "know anything", "he at", "now mr", "first five", "or was",
                               "into three", "being so", "the is", "up between", "became more", "and behind", "on whom",
                               "one such", "goes down", "its very", "from having", "old it", "let you", "of me",
                               "to where", "if some", "them would", "you made", "on third", "said are", "something for",
                               "past as", "man one", "would then", "going from", "than few", "later that", "has any",
                               "with even", "every three", "up was", "her we", "soon on", "are neither", "down its",
                               "to was", "get this", "in over", "is many", "them without", "that went", "tell it",
                               "itself it", "here an", "some are", "two three", "was which", "on mrs", "said their",
                               "up five", "had him", "know whether", "who saw", "him when", "back and", "and beyond",
                               "we all", "after about", "he didn", "didn get", "along in", "had much", "be next",
                               "yet and", "were just", "these will", "go it", "that last", "this little", "be having",
                               "th he", "would in", "how often", "often have", "was dr", "above and", "came here",
                               "or nearly", "so she", "but over", "against last", "its two", "you don", "can all",
                               "which four", "other as", "especially if", "could look", "as four", "be first",
                               "much with", "they take", "seventh in", "past it", "all they", "would no", "said with",
                               "do on", "are little", "little too", "always the", "had but", "so but", "of they",
                               "just such", "day under", "who last", "any and", "so what", "from across", "but under",
                               "she should", "as does", "but such", "did on", "often in", "some will", "and any",
                               "who make", "almost in", "but every", "one here", "else it", "below to", "on whose",
                               "are long", "they really", "many with", "it after", "see one", "because no",
                               "another that", "saying it", "on man", "us an", "was especially", "had that", "long on",
                               "will know", "this last", "or have", "doing some", "make this", "it often", "began this",
                               "this by", "may there", "in th", "whether you", "and away", "as never", "saw him",
                               "now but", "when there", "along this", "to second", "each time", "myself to",
                               "other way", "of itself", "own it", "one two", "else is", "that either", "they went",
                               "after getting", "of say", "or were", "but another", "with on", "look down",
                               "itself into", "these and", "back again", "as though", "it long", "almost without",
                               "back their", "couldn be", "be your", "now more", "was day", "near its", "make such",
                               "another is", "in they", "to near", "me have", "were up", "is after", "it always",
                               "still under", "about were", "look around", "all whose", "same way", "seems at",
                               "in were", "you tell", "for much", "to now", "to own", "be especially", "are five",
                               "but most", "if and", "do their", "no by", "get down", "you must", "on may", "made over",
                               "at there", "was her", "also was", "were an", "up until", "soon in", "man said",
                               "he got", "by in", "three were", "through in", "what its", "way last", "thing of",
                               "or are", "to out", "three the", "if her", "or third", "back at", "was six", "just two",
                               "tell how", "too but", "perhaps in", "later on", "but perhaps", "last eight", "me or",
                               "between what", "are often", "could he", "may soon", "others as", "both its", "by each",
                               "all mr", "which seem", "day against", "already on", "with old", "when will", "same old",
                               "was either", "more are", "and except", "use this", "said from", "probably is",
                               "time now", "been little", "not but", "on nearly", "them because", "to just",
                               "some from", "until at", "which even", "one each", "said think", "on you", "be its",
                               "second for", "there now", "here one", "there so", "some may", "as another", "be either",
                               "by seven", "two that", "soon and", "out under", "him two", "some who", "that come",
                               "come with", "or long", "began last", "going for", "has on", "her out", "out who",
                               "the on", "this once", "own time", "or go", "go at", "yet no", "yet at", "long has",
                               "about last", "is next", "we use", "and goes", "goes into", "for against", "after five",
                               "they even", "say and", "these three", "those most", "among many", "on old", "under her",
                               "her left", "man may", "to from", "all had", "it been", "when as", "so is",
                               "and quickly", "were few", "where to", "of still", "use and", "third in", "been using",
                               "he really", "as second", "think is", "might do", "two such", "else the", "still here",
                               "they don", "one own", "there also", "way she", "before going", "nearly of", "old time",
                               "little as", "at just", "some more", "did and", "man it", "and look", "while and",
                               "over some", "could no", "those were", "if as", "to has", "which said", "at as",
                               "get them", "his and", "can never", "things for", "over into", "their use", "see some",
                               "say this", "made without", "in against", "not later", "some say", "one under",
                               "get his", "the when", "down from", "also were", "as st", "who say", "began at",
                               "be certain", "how things", "us how", "us so", "by st", "after she", "last seven",
                               "ago during", "its eight", "what else", "say at", "until and", "up some", "its fifth",
                               "down her", "it most", "him they", "were almost", "certain the", "another at",
                               "have that", "about other", "ago will", "ago was", "so with", "of use", "but already",
                               "already are", "that often", "often with", "ago his", "left their", "first things",
                               "itself but", "thing and", "up any", "who might", "not here", "left no", "since you",
                               "you might", "she still", "over him", "man made", "had last", "do was", "before being",
                               "seem as", "you he", "in out", "as too", "can ever", "he certainly", "seem more",
                               "is because", "his was", "make all", "but mrs", "against dr", "because an",
                               "although that", "might think", "that just", "things on", "still has", "goes in",
                               "he always", "anything it", "more they", "thing but", "time would", "off into",
                               "once upon", "be up", "gone down", "out they", "him said", "said one", "them both",
                               "beyond their", "because her", "last nine", "next of", "their sixth", "got away",
                               "too soon", "back down", "said about", "it ever", "above their", "that or", "tell of",
                               "up under", "may dr", "can even", "is or", "if an", "did you", "think about", "out he",
                               "here were", "yet another", "take another", "who go", "or down", "down about",
                               "below that", "never see", "yet for", "began with", "three most", "could say",
                               "either by", "made toward", "of just", "perhaps not", "over four", "into your",
                               "use its", "them may", "them even", "could take", "said had", "along to", "both with",
                               "that where", "left over", "know this", "with or", "what made", "between one",
                               "now when", "them until", "something about", "once on", "from third", "it didn",
                               "didn do", "who until", "take off", "old to", "now you", "had six", "if their", "an all",
                               "her he", "back that", "know you", "all four", "but certainly", "from almost",
                               "seem the", "may they", "will still", "against five", "his day", "use their", "as most",
                               "including that", "already have", "it doesn", "see on", "did mr", "little about",
                               "also said", "if only", "it their", "its th", "just over", "things we", "were once",
                               "will look", "at us", "some might", "might say", "say for", "with to", "most often",
                               "out she", "now he", "against another", "has such", "another as", "during those",
                               "those three", "long one", "up he", "of left", "out mr", "his one", "and nd", "much you",
                               "day you", "off two", "it while", "may from", "look as", "were they", "down one",
                               "they look", "tell him", "anything about", "may st", "had three", "other such",
                               "what many", "her four", "while under", "was doing", "each for", "its long", "the as",
                               "while all", "itself has", "so were", "not her", "so at", "may were", "against for",
                               "to against", "up through", "that go", "go off", "oh the", "is saying", "those with",
                               "eighth in", "again before", "into long", "what not", "just because", "had too",
                               "was between", "between now", "it during", "about is", "left before", "can always",
                               "with how", "first made", "made them", "so here", "it last", "that seem", "man his",
                               "first four", "thing he", "before on", "made into", "whom will", "now they", "long day",
                               "their fifth", "over many", "not alone", "their eighth", "from seven", "seven to",
                               "but other", "may when", "over until", "the dr", "along and", "the make", "more this",
                               "would see", "others is", "than being", "tell me", "me how", "the are", "after and",
                               "then go", "are or", "still as", "should also", "also have", "from or", "nothing so",
                               "be with", "have even", "ago my", "at left", "while you", "you still", "or get",
                               "however he", "went by", "left alone", "used an", "own use", "who always", "fourth time",
                               "it you", "day now", "but until", "out here", "its three", "every now", "fourth in",
                               "ve been", "across from", "it two", "for doing", "of myself", "look with", "here next",
                               "own but", "up my", "that seemed", "back but", "three more", "may get", "another long",
                               "tell what", "he once", "yes and", "this does", "where as", "that once", "what more",
                               "in then", "was already", "what with", "long that", "before next", "where can", "all my",
                               "now some", "its third", "not use", "above with", "that six", "for under", "were that",
                               "even its", "why he", "been such", "on who", "no is", "not out", "each from",
                               "been through", "and or", "in rather", "however when", "all so", "on but", "two one",
                               "only did", "who we", "little the", "get your", "out my", "they began", "began on",
                               "began the", "come as", "here have", "were one", "later she", "made three", "and began",
                               "was mrs", "he so", "about when", "it once", "often it", "just got", "against each",
                               "know in", "if your", "out more", "anything the", "because you", "be only", "doing his",
                               "let out", "yes there", "you never", "getting his", "no two", "as third", "tell her",
                               "who look", "who see", "they saw", "first for", "have they", "then again", "off one",
                               "has even", "three out", "about for", "that always", "very often", "it wouldn",
                               "one where", "say when", "so one", "were either", "does his", "except perhaps",
                               "him through", "including two", "one said", "ago last", "up behind", "her but",
                               "few things", "out if", "for things", "see all", "however will", "second at", "may you",
                               "already know", "saw and", "their three", "many an", "about where", "gone up",
                               "that anything", "go from", "all there", "to how", "had once", "yet as", "just past",
                               "with man", "much on", "through four", "of too", "how could", "when is", "just had",
                               "which already", "we come", "are old", "under and", "all too", "most the", "our way",
                               "can happen", "than can", "over an", "he often", "even as", "don be", "more it",
                               "those and", "us always", "her will", "you we", "can no", "do have", "soon have",
                               "only once", "at up", "here because", "its many", "are within", "this th", "thing it",
                               "can he", "use an", "could the", "quickly to", "away he", "what seemed", "the can",
                               "what that", "we re", "re all", "its four", "her third", "until when", "you re",
                               "one should", "and toward", "you what", "over from", "never will", "there some",
                               "and neither", "even some", "again after", "you got", "here after", "going in",
                               "or where", "say so", "nearly six", "through one", "that let", "way when", "at was",
                               "was was", "she were", "but why", "who never", "probably would", "also his", "over he",
                               "how we", "at but", "from doing", "to herself", "but through", "man she", "when your",
                               "because his", "them about", "when my", "have four", "to even", "left us", "her is",
                               "even by", "but probably", "who of", "of same", "during mr", "so will", "which just",
                               "up so", "gone in", "will most", "be using", "using their", "at down", "including some",
                               "made us", "none has", "second to", "on here", "its day", "beside him", "having to",
                               "you had", "time again", "said after", "from few", "four more", "were mrs", "before one",
                               "who don", "into third", "way this", "from until", "all out", "often are", "was down",
                               "had anything", "below in", "ago is", "only with", "did last", "make use",
                               "over million", "is how", "of after", "what am", "and below", "through what", "few and",
                               "came for", "just say", "am very", "at near", "up little", "from under", "this at",
                               "nine to", "that second", "can in", "on how", "now she", "him again", "until their",
                               "where this", "back out", "for out", "in near", "once every", "one about", "were even",
                               "don have", "something is", "went with", "over more", "who often", "did but", "me what",
                               "think so", "which used", "at only", "way was", "not up", "still an", "for she",
                               "on about", "or do", "one you", "also make", "her five", "went back", "for re",
                               "have and", "and off", "not this", "between first", "here his", "in if", "at were",
                               "its one", "going back", "are out", "by using", "something out", "now say", "many had",
                               "we ve", "now had", "else was", "ago said", "and lot", "it our", "by with", "million is",
                               "inside and", "the do", "was second", "come upon", "come across", "so has",
                               "including her", "came as", "when most", "has really", "two little", "were with",
                               "her when", "the have", "as against", "even on", "or her", "one over", "in where",
                               "were little", "had five", "in had", "but much", "their long", "often they", "at them",
                               "those are", "who as", "fifth of", "eight men", "anything from", "may all", "herself to",
                               "through her", "all she", "not they", "here just", "here so", "never know", "on around",
                               "because mr", "time not", "may make", "but be", "each by", "off after", "million on",
                               "would the", "it too", "said all", "as each", "over what", "did their", "then but",
                               "up four", "for will", "be off", "yet on", "why in", "may never", "said now", "must see",
                               "said last", "here if", "old is", "see your", "saw an", "sixth of", "there ever",
                               "here may", "so there", "this had", "from fifth", "more as", "you how", "why do",
                               "at both", "because one", "began by", "but during", "it take", "own as", "seems an",
                               "were off", "say no", "old with", "now only", "make that", "day until", "no no",
                               "who became", "your way", "him because", "his next", "many the", "them before",
                               "while one", "in next", "having said", "see any", "may this", "how are",
                               "that sometimes", "or why", "above his", "them his", "but let", "doing what", "her only",
                               "nor will", "that through", "to after", "was both", "there more", "day here", "had as",
                               "was even", "not really", "about nine", "here mr", "used it", "goes back", "that next",
                               "also has", "million this", "go around", "with of", "nothing if", "said some",
                               "itself from", "see to", "is five", "have either", "yet his", "doing their",
                               "doing just", "but certain", "are perhaps", "again they", "it how", "get all",
                               "you probably", "there might", "no this", "see why", "what did", "what your",
                               "through on", "him away", "too have", "seven other", "time all", "their next",
                               "but since", "and past", "all five", "once there", "getting it", "going away", "be they",
                               "way mr", "his st", "their only", "here over", "they always", "always will", "old dr",
                               "his is", "never get", "six more", "not when", "who ever", "his six", "or against",
                               "goes by", "said just", "where and", "who once", "let his", "after nearly", "both an",
                               "by he", "when to", "all your", "get its", "next ten", "when no", "himself into",
                               "who seem", "by getting", "the near", "look more", "with too", "day old", "an out",
                               "would know", "for up", "by first", "others including", "was gone", "may his", "back as",
                               "after what", "it three", "to only", "must go", "once before", "did was", "out was",
                               "an to", "around with", "or use", "than million", "but each", "where did", "again but",
                               "has five", "but first", "came with", "for th", "often at", "never even", "be another",
                               "over much", "old or", "yet this", "first on", "is using", "that goes", "time ever",
                               "they re", "else but", "did all", "anything can", "we at", "were any", "who then",
                               "ago she", "each is", "without him", "why would", "five more", "only will", "him will",
                               "so few", "up they", "another was", "along on", "on four", "men here", "them can",
                               "make more", "that already", "their day", "down last", "on dr", "saying he", "for way",
                               "since will", "man whom", "may mr", "in between", "should use", "by don", "who used",
                               "went before", "did some", "here had", "when mrs", "she became", "next few",
                               "it against", "up against", "that between", "them has", "ll do", "once said", "now know",
                               "while those", "way toward", "of used", "only his", "was she", "things but", "but here",
                               "from he", "on himself", "because so", "them away", "get some", "get any", "what really",
                               "something very", "so you", "that got", "until all", "him very", "even so", "say or",
                               "on he", "up two", "his eighth", "about me", "whether she", "not getting", "are his",
                               "had even", "are either", "over my", "old she", "said no", "did he", "you look",
                               "may while", "nor his", "quickly and", "who only", "while no", "ago they", "and us",
                               "said were", "back into", "them how", "all goes", "with second", "you ve",
                               "about having", "now will", "what used", "how can", "second only", "still others",
                               "eight under", "for after", "we really", "around in", "around his", "go along",
                               "been lot", "soon it", "said such", "do an", "and next", "as dr", "back after",
                               "just off", "perhaps this", "just six", "three day", "see her", "should you", "too old",
                               "old for", "almost no", "how an", "did something", "will say", "no but", "why are",
                               "how she", "how mr", "has way", "of herself", "above in", "the but", "she never",
                               "old has", "been its", "them now", "around this", "now because", "until last",
                               "that eight", "at fourth", "into more", "when and", "are our", "him what", "that lot",
                               "an from", "not last", "one does", "about anything", "especially among", "how his",
                               "as three", "may no", "said both", "his seven", "doing things", "their and", "how some",
                               "are other", "could to", "see their", "were now", "when those", "re not", "in who",
                               "must do", "you use", "long way", "by or", "who the", "how one", "as always",
                               "with third", "or your", "time so", "never did", "may an", "there something", "at under",
                               "on just", "may even", "even have", "it isn", "behind its", "of up", "for herself",
                               "later when", "have her", "perhaps even", "near an", "upon time", "her six", "out how",
                               "that seven", "in back", "must make", "next time", "herself with", "getting there",
                               "near their", "back was", "about these", "came of", "into what", "another but",
                               "here between", "its fourth", "if for", "do when", "not among", "here would",
                               "make another", "doing this", "while being", "will happen", "nd at", "so mr",
                               "about you", "all except", "especially with", "do about", "said mrs", "after only",
                               "on six", "off three", "no he", "be back", "up most", "which became", "an especially",
                               "don do", "soon for", "itself at", "since most", "around an", "whether an", "doing and",
                               "itself out", "though that", "doing more", "across his", "to were", "of through",
                               "four million", "here when", "all from", "down here", "they think", "him are",
                               "behind his", "what if", "there only", "him more", "did at", "you said", "been around",
                               "around on", "much they", "doing that", "then at", "can go", "seems certain", "below it",
                               "not mr", "there always", "to up", "on first", "ever so", "through at", "say mr",
                               "around to", "on getting", "perhaps because", "know he", "that really", "really have",
                               "can of", "in way", "say their", "another it", "including four", "across this",
                               "might take", "probably more", "ve just", "isn it", "got its", "once made", "away but",
                               "her it", "often to", "on until", "than most", "then had", "eight day", "where many",
                               "here where", "take one", "he no", "for fourth", "was third", "last long",
                               "although many", "more on", "down two", "even their", "don think", "for when", "dr and",
                               "yes but", "will use", "saw no", "can almost", "back who", "now come", "still one",
                               "his or", "here two", "not something", "her little", "before to", "in anything",
                               "be few", "still not", "first there", "after going", "just this", "our long",
                               "another with", "sometimes he", "at fifth", "about your", "three time", "is above",
                               "one this", "then mr", "said more", "came about", "with back", "later became",
                               "how will", "first as", "the even", "so why", "behind her", "second or", "for even",
                               "off when", "did little", "think and", "may but", "that because", "time said",
                               "been something", "its million", "day without", "both had", "else he", "there really",
                               "by when", "around that", "more quickly", "you couldn", "by nine", "for how",
                               "from through", "seem an", "about those", "said however", "said only", "by next",
                               "why mr", "just not", "at much", "its back", "about but", "did she", "others say",
                               "was whether", "on others", "much but", "of where", "who own", "were long", "he going",
                               "her seven", "out because", "another time", "back is", "they already", "next five",
                               "did his", "up around", "take me", "did for", "was getting", "here how", "am and",
                               "after you", "how does", "though mr", "just beyond", "were doing", "its men",
                               "either way", "things happen", "is back", "then an", "be even", "is old", "how their",
                               "old at", "their fourth", "only if", "there last", "ago three", "something we",
                               "not happen", "but something", "that still", "just too", "eight other", "say if",
                               "came after", "but others", "you left", "they often", "up being", "its eighth",
                               "something you", "without her", "must still", "million with", "up where", "its five",
                               "do things", "and inside", "that doesn", "until there", "for using", "yes it", "up into",
                               "except on", "second with", "just around", "where was", "will let", "can come",
                               "time out", "now however", "the don", "always on", "what our", "an off", "has four",
                               "know which", "gone but", "so are", "who didn", "where at", "getting under",
                               "things about", "later he", "although their", "one seems", "up few", "what next",
                               "then became", "since may", "this might", "but should", "do just", "things it",
                               "few hundred", "had since", "two day", "they once", "is third", "no with", "its ninth",
                               "may very", "say are", "he wasn", "below are", "not used", "next one", "it probably",
                               "don you", "six million", "wouldn be", "once they", "then after", "because this",
                               "tell their", "it even", "off off", "have my", "am for", "those under", "do is",
                               "out four", "out just", "whom to", "pm in", "into other", "often do", "as perhaps",
                               "still no", "much it", "at those", "got back", "out where", "them down", "about not",
                               "in only", "take at", "behind by", "again when", "just for", "left as", "than her",
                               "across an", "almost two", "down because", "having one", "am from", "so let", "did this",
                               "an on", "off or", "before more", "down some", "now just", "was or", "into each",
                               "from inside", "also about", "he doesn", "am on", "just getting", "at ninth", "the this",
                               "both her", "from million", "they probably", "than just", "in men", "time here",
                               "all else", "there when", "yet mr", "away after", "why did", "are using", "but almost",
                               "million the", "until mr", "know at", "her old", "two out", "it soon", "didn know",
                               "the they", "as five", "things go", "about another", "as or", "which began", "not day",
                               "men including", "all said", "this second", "got there", "with lot", "old left",
                               "second on", "the nearly", "made many", "above its", "who began", "and yes",
                               "before long", "every five", "have lot", "made after", "be what", "also used",
                               "behind their", "after nine", "could almost", "look the", "eight million", "is way",
                               "of off", "might never", "made through", "her fifth", "at six", "them too",
                               "there seemed", "were her", "he an", "was below", "whether their", "either on",
                               "until an", "itself was", "or would", "few if", "against on", "for nine", "re on",
                               "not just", "so last", "since being", "gone back", "especially since", "saw his",
                               "after seven", "around here", "by old", "old but", "even his", "would almost",
                               "later as", "for almost", "go beyond", "say she", "not nearly", "only through", "so too",
                               "make certain", "him our", "getting an", "doing to", "been up", "few thousand",
                               "through last", "do its", "long he", "come by", "because their", "too is", "there after",
                               "just three", "both mr", "however this", "then she", "than day", "may just", "just four",
                               "men they", "might even", "toward that", "made only", "even be", "and ll", "on through",
                               "still do", "ago because", "five were", "make much", "her day", "been having",
                               "on eight", "when not", "own for", "at third", "ll go", "see as", "may still",
                               "saying she", "who who", "it your", "from for", "thing or", "was using", "use on",
                               "because as", "may through", "its tenth", "really be", "made off", "without saying",
                               "has her", "by doing", "at eighth", "did when", "or can", "before two", "it getting",
                               "me said", "should look", "while two", "over time", "off its", "that perhaps",
                               "as almost", "began and", "him how", "there she", "it either", "began its", "in she",
                               "don seem", "they couldn", "her long", "how about", "as something", "isn the",
                               "four day", "when saw", "first ten", "she used", "said dr", "was how", "last thing",
                               "down under", "would tell", "into mr", "is itself", "why does", "into how", "said an",
                               "out is", "for just", "at million", "on non", "let alone", "we didn", "make your",
                               "don see", "anything he", "down after", "is dr", "many he", "only now", "they didn",
                               "one had", "with perhaps", "than third", "would most", "already being", "in until",
                               "as both", "even been", "is lot", "on seventh", "then you", "you ll", "since before",
                               "again until", "with first", "inside out", "something he", "do without", "even one",
                               "not about", "came away", "it look", "with left", "often is", "really don",
                               "couldn have", "did more", "us will", "day because", "nd st", "why you", "time you",
                               "only does", "once was", "below those", "who just", "way you", "very very", "to fifth",
                               "an after", "were using", "first became", "but any", "as way", "over most", "come long",
                               "only too", "some would", "is re", "are back", "now until", "yet even", "not gone",
                               "still are", "against four", "when things", "things were", "use that", "about getting",
                               "by without", "his sixth", "then his", "still too", "doesn seem", "what my", "let their",
                               "up along", "ten day", "my two", "but although", "else that", "much else", "an ever",
                               "may if", "that look", "say will", "each will", "to before", "about each", "about third",
                               "can still", "not including", "through may", "to seem", "his nine", "she once",
                               "that began", "quickly the", "alone at", "get one", "used against", "as six",
                               "were saying", "don get", "third to", "though she", "almost anything", "under to",
                               "but left", "have until", "more but", "know there", "make for", "once he",
                               "toward their", "to old", "or st", "between its", "over who", "oh my", "was million",
                               "after each", "how would", "often used", "left me", "that take", "long gone", "did her",
                               "her many", "herself as", "are what", "getting back", "them again", "her fourth",
                               "don take", "almost one", "would happen", "only man", "let down", "from next", "you our",
                               "so do", "really are", "from nine", "later with", "make and", "lot by", "was later",
                               "however they", "million to", "down that", "they no", "at seventh", "soon by",
                               "in became", "became one", "through more", "if things", "to using", "him since",
                               "on seven", "doing its", "third man", "are six", "about every", "it around", "saw as",
                               "seemed the", "may more", "make you", "were here", "she first", "or through",
                               "on whether", "this an", "things will", "ve got", "against what", "we already",
                               "would they", "she saw", "up next", "million but", "is why", "they seemed", "this all",
                               "about he", "back when", "was until", "up almost", "over when", "was back",
                               "even during", "now was", "she in", "those around", "to also", "those things", "make or",
                               "seemed in", "just look", "what most", "gone with", "back an", "when both", "just don",
                               "his no", "time over", "don even", "some had", "other time", "into first", "didn take",
                               "about who", "would last", "too quickly", "left after", "she might", "never got",
                               "why there", "during may", "by million", "out whether", "said can", "its other",
                               "that say", "about million", "though most", "was saying", "are my", "than men", "now if",
                               "until then", "don go", "get that", "it time", "go after", "she been", "what could",
                               "one second", "these same", "said during", "each has", "did with", "on nd", "once an",
                               "on even", "never really", "were each", "just back", "its seven", "from when",
                               "while not", "through another", "those he", "really do", "she doesn", "that also",
                               "during these", "does an", "seemed that", "each had", "alone with", "this past",
                               "can just", "also being", "said here", "seemed almost", "just few", "has lot", "me they",
                               "ll tell", "in left", "use her", "up because", "his seventh", "including his",
                               "once were", "later for", "later they", "it happen", "have what", "its nine", "out why",
                               "why his", "after more", "own with", "else can", "billion and", "eight more", "it both",
                               "made little", "three man", "into something", "said could", "how did", "first nine",
                               "get there", "could go", "me about", "that saw", "million from", "them she", "made when",
                               "there anything", "it going", "or does", "saying we", "behind in", "an even",
                               "began their", "been saying", "they use", "all seven", "might still", "once one",
                               "where most", "million has", "ll see", "really know", "by non", "during and",
                               "getting more", "get much", "be million", "time because", "because all", "from more",
                               "men said", "until may", "saying there", "without getting", "in than", "may her",
                               "is you", "its all", "many such", "while still", "back this", "to million",
                               "million for", "he wouldn", "into last", "as what", "again were", "long long", "only do",
                               "left is", "still he", "there too", "through most", "on where", "for too", "an inside",
                               "never quite", "seem so", "who already", "she seems", "when many", "could just",
                               "around but", "th am", "down when", "million as", "or almost", "may up", "was certain",
                               "say could", "may will", "later was", "always seemed", "about man", "every two",
                               "they too", "back over", "look is", "or take", "be both", "still had", "way his",
                               "seven day", "just an", "is happening", "had seemed", "it her", "the what", "to why",
                               "at you", "sometimes they", "especially after", "would use", "came last", "to left",
                               "even know", "back toward", "said two", "often said", "more often", "than not",
                               "do next", "but often", "also because", "them you", "what all", "but later",
                               "something they", "if more", "old will", "sixth in", "behind to", "happen if", "let up",
                               "but ve", "already is", "just have", "four man", "which often", "often seems",
                               "in would", "said these", "from just", "on nine", "got an", "than do", "came just",
                               "this thing", "but sometimes", "those made", "toward an", "or because", "you going",
                               "without you", "at how", "day off", "off against", "happening in", "that later",
                               "because if", "that million", "in since", "million he", "can really", "because was",
                               "many many", "could also", "don look", "also are", "behind an", "down fifth", "by may",
                               "go long", "up just", "at has", "all across", "you always", "left who", "she ll",
                               "ll never", "every so", "would let", "just little", "get by", "them said", "don tell",
                               "were having", "could use", "way since", "used only", "when four", "million by",
                               "to getting", "in don", "perhaps most", "could you", "others through", "after last",
                               "there isn", "there said", "he already", "against six", "began an", "also will",
                               "first all", "she didn", "as next", "on only", "one long", "so how", "another two",
                               "she always", "may two", "because most", "on into", "these past", "billion the",
                               "two five", "who doesn", "behind us", "there just", "five under", "above those",
                               "about himself", "at next", "some million", "ve had", "of why", "its seventh",
                               "whose last", "which saw", "over st", "he almost", "too few", "on down", "in yet",
                               "why she", "almost three", "from around", "it alone", "over whether", "first since",
                               "sometimes even", "often than", "on something", "that third", "its sixth",
                               "especially his", "for later", "first seven", "by for", "again will", "doesn get",
                               "almost six", "near here", "now can", "had million", "six day", "about something",
                               "might also", "in non", "couldn get", "he just", "billion is", "is million",
                               "and million", "yet again", "about how", "at sixth", "million at", "began after",
                               "after almost", "what about", "might get", "said those", "than little", "still can",
                               "began her", "their no", "among three", "their six", "th time", "how quickly",
                               "can think", "its st", "do lot", "nearly third", "through much", "get you", "said three",
                               "began as", "five day", "may some", "seven under", "why can", "began here", "she not",
                               "was lot", "later this", "million that", "get past", "that didn", "into second",
                               "from left", "for million", "two time", "million into", "million which", "including its",
                               "that why", "including five", "it got", "go all", "never let", "way around",
                               "through next", "gone are", "yourself in", "from am", "over how", "could soon",
                               "saying his", "little things", "and doesn", "she just", "those same", "get what",
                               "in because", "are saying", "were million", "almost four", "out across", "doesn know",
                               "over first", "were later", "might soon", "inside his", "behind this", "at through",
                               "might just", "billion of", "long last", "things you", "always seems", "or million",
                               "his ninth", "is yes", "but didn", "see above", "us said", "then one", "what became",
                               "time around", "get me", "he isn", "she began", "just across", "just five",
                               "could still", "most were", "isn just", "old an", "said because", "by how",
                               "million more", "its six", "old mrs", "saying they", "up fifth", "came when", "later mr",
                               "as million", "million after", "man behind", "only million", "had lot", "here what",
                               "did have", "began two", "didn seem", "look that", "get used", "every once", "five man",
                               "but inside", "here said", "time soon", "said while", "that use", "what goes",
                               "of around", "began when", "that wasn", "me she", "can also", "may although", "just by",
                               "shouldn be", "way too", "because many", "by then", "this two", "can seem", "in million",
                               "can one", "get my", "almost never", "it wasn", "can often", "said yes", "and didn",
                               "two way", "that became", "go go", "ve come", "on why", "billion to", "seemed an",
                               "that how", "by th", "gone too", "there wasn", "don always", "back against", "don let",
                               "an already", "still was", "didn think", "happen again", "though is", "it couldn",
                               "others said", "said its", "didn even", "using its", "third with", "this isn", "is look",
                               "they just", "later after", "goes beyond", "about whether", "thing you", "by now",
                               "get around", "for fifth", "lets you", "sometimes seems", "were back", "began three",
                               "old said", "later said", "what going", "re going", "toward more", "down more",
                               "wasn the", "ve never", "are lot", "against against", "things up", "that isn", "oh and",
                               "in off", "ago ago", "got around", "ve made", "going after", "who later", "didn have",
                               "about why", "we couldn", "re just", "you wouldn", "did just", "be lot", "could happen",
                               "anything goes", "they ve", "and ve", "isn that", "wouldn have", "with million",
                               "there ll", "time off", "already own", "three under", "what doing", "you didn",
                               "your day", "made million", "million million", "his million", "ve ever", "ll get",
                               "doesn even", "he quickly", "billion by", "doesn make", "two under", "quickly became",
                               "most are", "said later", "last second", "all eight", "it yourself", "that been",
                               "re getting", "four time", "does have", "the sometimes", "at around", "doesn have",
                               "four under", "the billion", "didn make", "almost million", "he later", "the take",
                               "its billion", "at am", "lot about", "than billion", "may am", "that ve", "not million",
                               "above left", "almost five", "came day", "million it", "was happening", "nearly billion",
                               "didn really", "million was", "she later", "pm the", "doesn look", "million each",
                               "doesn take", "there lot", "what began", "quite few", "has million", "aren the",
                               "can sometimes", "sometimes you", "all began", "million will", "between million",
                               "an th", "can quickly", "don make", "second most", "that lets", "of billion", "who you",
                               "on million", "billion or", "re your", "ve always", "back then", "re an", "just can",
                               "just another", "what went", "about billion", "into whether", "billion more",
                               "at billion", "let get", "over billion", "three way", "billion in", "including million",
                               "with billion", "first such", "five time", "six under", "back nine", "almost billion",
                               "re still", "by billion", "billion for", "they aren", "is billion", "just didn",
                               "just last", "million would", "while also", "at nd", "ll always", "and billion", "at pm",
                               "there aren", "you every", "as billion", "to billion", "what happening",
                               "billion billion", "billion as", "in billion", "up million", "or billion", "don really",
                               "re doing", "for billion", "pm and", "billion over", "pm at", "billion at", "on billion",
                               "your may", "million mr", "billion but", "the us", "some billion", "pm on",
                               "billion last", "to pm", "was billion", "million during", "from billion", "billion it",
                               "billion that", "billion on", "an billion", "an million", "just might", "million last",
                               "billion this", "billion up", "billion from", "around million", "million over",
                               "million through", "from pm", "million up", "million not", "and pm", "across as",
                               "pm to", "am st", "pm pm", "th pm", "pm with", "may pm", ]
        self.positive_words = ["a+", "abound", "abounds", "abundance", "abundant", "accessable", "accessible",
                               "acclaim", "acclaimed", "acclamation", "accolade", "accolades", "accommodative",
                               "accomodative", "accomplish", "accomplished", "accomplishment", "accomplishments",
                               "accurate", "accurately", "achievable", "achievement", "achievements", "achievible",
                               "acumen", "adaptable", "adaptive", "adequate", "adjustable", "admirable", "admirably",
                               "admiration", "admire", "admirer", "admiring", "admiringly", "adorable", "adore",
                               "adored", "adorer", "adoring", "adoringly", "adroit", "adroitly", "adulate", "adulation",
                               "adulatory", "advanced", "advantage", "advantageous", "advantageously", "advantages",
                               "adventuresome", "adventurous", "advocate", "advocated", "advocates", "affability",
                               "affable", "affably", "affectation", "affection", "affectionate", "affinity", "affirm",
                               "affirmation", "affirmative", "affluence", "affluent", "afford", "affordable",
                               "affordably", "afordable", "agile", "agilely", "agility", "agreeable", "agreeableness",
                               "agreeably", "allaround", "alluring", "alluringly", "altruistic", "altruistically",
                               "amaze", "amazed", "amazement", "amazes", "amazing", "amazingly", "ambitious",
                               "ambitiously", "ameliorate", "amenable", "amenity", "amiability", "amiabily", "amiable",
                               "amicability", "amicable", "amicably", "amity", "ample", "amply", "amuse", "amusing",
                               "amusingly", "angel", "angelic", "apotheosis", "appeal", "appealing", "applaud",
                               "appreciable", "appreciate", "appreciated", "appreciates", "appreciative",
                               "appreciatively", "appropriate", "approval", "approve", "ardent", "ardently", "ardor",
                               "articulate", "aspiration", "aspirations", "aspire", "assurance", "assurances", "assure",
                               "assuredly", "assuring", "astonish", "astonished", "astonishing", "astonishingly",
                               "astonishment", "astound", "astounded", "astounding", "astoundingly", "astutely",
                               "attentive", "attraction", "attractive", "attractively", "attune", "audible", "audibly",
                               "auspicious", "authentic", "authoritative", "autonomous", "available", "aver", "avid",
                               "avidly", "award", "awarded", "awards", "awe", "awed", "awesome", "awesomely",
                               "awesomeness", "awestruck", "awsome", "backbone", "balanced", "bargain", "beauteous",
                               "beautiful", "beautifullly", "beautifully", "beautify", "beauty", "beckon", "beckoned",
                               "beckoning", "beckons", "believable", "believeable", "beloved", "benefactor",
                               "beneficent", "beneficial", "beneficially", "beneficiary", "benefit", "benefits",
                               "benevolence", "benevolent", "benifits", "best", "bestknown", "bestperforming",
                               "bestselling", "better", "betterknown", "betterthanexpected", "beutifully", "blameless",
                               "bless", "blessing", "bliss", "blissful", "blissfully", "blithe", "blockbuster", "bloom",
                               "blossom", "bolster", "bonny", "bonus", "bonuses", "boom", "booming", "boost",
                               "boundless", "bountiful", "brainiest", "brainy", "brandnew", "brave", "bravery", "bravo",
                               "breakthrough", "breakthroughs", "breathlessness", "breathtaking", "breathtakingly",
                               "breeze", "bright", "brighten", "brighter", "brightest", "brilliance", "brilliances",
                               "brilliant", "brilliantly", "brisk", "brotherly", "bullish", "buoyant", "cajole", "calm",
                               "calming", "calmness", "capability", "capable", "capably", "captivate", "captivating",
                               "carefree", "cashback", "cashbacks", "catchy", "celebrate", "celebrated", "celebration",
                               "celebratory", "champ", "champion", "charisma", "charismatic", "charitable", "charm",
                               "charming", "charmingly", "chaste", "cheaper", "cheapest", "cheer", "cheerful", "cheery",
                               "cherish", "cherished", "cherub", "chic", "chivalrous", "chivalry", "civility",
                               "civilize", "clarity", "classic", "classy", "clean", "cleaner", "cleanest",
                               "cleanliness", "cleanly", "clear", "clearcut", "cleared", "clearer", "clearly", "clears",
                               "clever", "cleverly", "cohere", "coherence", "coherent", "cohesive", "colorful",
                               "comely", "comfort", "comfortable", "comfortably", "comforting", "comfy", "commend",
                               "commendable", "commendably", "commitment", "commodious", "compact", "compactly",
                               "compassion", "compassionate", "compatible", "competitive", "complement",
                               "complementary", "complemented", "complements", "compliant", "compliment",
                               "complimentary", "comprehensive", "conciliate", "conciliatory", "concise", "confidence",
                               "confident", "congenial", "congratulate", "congratulation", "congratulations",
                               "congratulatory", "conscientious", "considerate", "consistent", "consistently",
                               "constructive", "consummate", "contentment", "continuity", "contrasty", "contribution",
                               "convenience", "convenient", "conveniently", "convience", "convienient", "convient",
                               "convincing", "convincingly", "cool", "coolest", "cooperative", "cooperatively",
                               "cornerstone", "correct", "correctly", "costeffective", "costsaving", "counterattack",
                               "counterattacks", "courage", "courageous", "courageously", "courageousness", "courteous",
                               "courtly", "covenant", "cozy", "creative", "credence", "credible", "crisp", "crisper",
                               "cure", "cureall", "cushy", "cute", "cuteness", "danke", "danken", "daring", "daringly",
                               "darling", "dashing", "dauntless", "dawn", "dazzle", "dazzled", "dazzling", "deadcheap",
                               "deadon", "decency", "decent", "decisive", "decisiveness", "dedicated", "defeat",
                               "defeated", "defeating", "defeats", "defender", "deference", "deft", "deginified",
                               "delectable", "delicacy", "delicate", "delicious", "delight", "delighted", "delightful",
                               "delightfully", "delightfulness", "dependable", "dependably", "deservedly", "deserving",
                               "desirable", "desiring", "desirous", "destiny", "detachable", "devout", "dexterous",
                               "dexterously", "dextrous", "dignified", "dignify", "dignity", "diligence", "diligent",
                               "diligently", "diplomatic", "dirtcheap", "distinction", "distinctive", "distinguished",
                               "diversified", "divine", "divinely", "dominate", "dominated", "dominates", "dote",
                               "dotingly", "doubtless", "dreamland", "dumbfounded", "dumbfounding", "dummyproof",
                               "durable", "dynamic", "eager", "eagerly", "eagerness", "earnest", "earnestly",
                               "earnestness", "ease", "eased", "eases", "easier", "easiest", "easiness", "easing",
                               "easy", "easytouse", "easygoing", "ebullience", "ebullient", "ebulliently", "ecenomical",
                               "economical", "ecstasies", "ecstasy", "ecstatic", "ecstatically", "edify", "educated",
                               "effective", "effectively", "effectiveness", "effectual", "efficacious", "efficient",
                               "efficiently", "effortless", "effortlessly", "effusion", "effusive", "effusively",
                               "effusiveness", "elan", "elate", "elated", "elatedly", "elation", "electrify",
                               "elegance", "elegant", "elegantly", "elevate", "elite", "eloquence", "eloquent",
                               "eloquently", "embolden", "eminence", "eminent", "empathize", "empathy", "empower",
                               "empowerment", "enchant", "enchanted", "enchanting", "enchantingly", "encourage",
                               "encouragement", "encouraging", "encouragingly", "endear", "endearing", "endorse",
                               "endorsed", "endorsement", "endorses", "endorsing", "energetic", "energize",
                               "energyefficient", "energysaving", "engaging", "engrossing", "enhance", "enhanced",
                               "enhancement", "enhances", "enjoy", "enjoyable", "enjoyably", "enjoyed", "enjoying",
                               "enjoyment", "enjoys", "enlighten", "enlightenment", "enliven", "ennoble", "enough",
                               "enrapt", "enrapture", "enraptured", "enrich", "enrichment", "enterprising", "entertain",
                               "entertaining", "entertains", "enthral", "enthrall", "enthralled", "enthuse",
                               "enthusiasm", "enthusiast", "enthusiastic", "enthusiastically", "entice", "enticed",
                               "enticing", "enticingly", "entranced", "entrancing", "entrust", "enviable", "enviably",
                               "envy", "equitable", "ergonomical", "errfree", "erudite", "ethical", "eulogize",
                               "euphoria", "euphoric", "euphorically", "evaluative", "evenly", "eventful",
                               "everlasting", "evocative", "exalt", "exaltation", "exalted", "exaltedly", "exalting",
                               "exaltingly", "examplar", "examplary", "excallent", "exceed", "exceeded", "exceeding",
                               "exceedingly", "exceeds", "excel", "exceled", "excelent", "excellant", "excelled",
                               "excellence", "excellency", "excellent", "excellently", "excels", "exceptional",
                               "exceptionally", "excite", "excited", "excitedly", "excitedness", "excitement",
                               "excites", "exciting", "excitingly", "exellent", "exemplar", "exemplary", "exhilarate",
                               "exhilarating", "exhilaratingly", "exhilaration", "exonerate", "expansive",
                               "expeditiously", "expertly", "exquisite", "exquisitely", "extol", "extoll",
                               "extraordinarily", "extraordinary", "exuberance", "exuberant", "exuberantly", "exult",
                               "exultant", "exultation", "exultingly", "eyecatch", "eyecatching", "fabulous",
                               "fabulously", "facilitate", "fair", "fairly", "fairness", "faith", "faithful",
                               "faithfully", "faithfulness", "fame", "famed", "famous", "famously", "fancier",
                               "fancinating", "fancy", "fanfare", "fans", "fantastic", "fantastically", "fascinate",
                               "fascinating", "fascinatingly", "fascination", "fashionable", "fashionably", "fast",
                               "fastgrowing", "fastpaced", "faster", "fastest", "fastestgrowing", "faultless", "fav",
                               "fave", "favor", "favorable", "favored", "favorite", "favorited", "favour", "fearless",
                               "fearlessly", "feasible", "feasibly", "feat", "featurerich", "fecilitous", "feisty",
                               "felicitate", "felicitous", "felicity", "fertile", "fervent", "fervently", "fervid",
                               "fervidly", "fervor", "festive", "fidelity", "fiery", "fine", "finelooking", "finely",
                               "finer", "finest", "firmer", "firstclass", "firstinclass", "firstrate", "flashy",
                               "flatter", "flattering", "flatteringly", "flawless", "flawlessly", "flexibility",
                               "flexible", "flourish", "flourishing", "fluent", "flutter", "fond", "fondly", "fondness",
                               "foolproof", "foremost", "foresight", "formidable", "fortitude", "fortuitous",
                               "fortuitously", "fortunate", "fortunately", "fortune", "fragrant", "free", "freed",
                               "freedom", "freedoms", "fresh", "fresher", "freshest", "friendliness", "friendly",
                               "frolic", "frugal", "fruitful", "ftw", "fulfillment", "fun", "futurestic", "futuristic",
                               "gaiety", "gaily", "gain", "gained", "gainful", "gainfully", "gaining", "gains",
                               "gallant", "gallantly", "galore", "geekier", "geeky", "gem", "gems", "generosity",
                               "generous", "generously", "genial", "genius", "gentle", "gentlest", "genuine", "gifted",
                               "glad", "gladden", "gladly", "gladness", "glamorous", "glee", "gleeful", "gleefully",
                               "glimmer", "glimmering", "glisten", "glistening", "glitter", "glitz", "glorify",
                               "glorious", "gloriously", "glory", "glow", "glowing", "glowingly", "godgiven", "godlike",
                               "godsend", "gold", "golden", "good", "goodly", "goodness", "goodwill", "goood", "gooood",
                               "gorgeous", "gorgeously", "grace", "graceful", "gracefully", "gracious", "graciously",
                               "graciousness", "grand", "grandeur", "grateful", "gratefully", "gratification",
                               "gratified", "gratifies", "gratify", "gratifying", "gratifyingly", "gratitude", "great",
                               "greatest", "greatness", "grin", "groundbreaking", "guarantee", "guidance", "guiltless",
                               "gumption", "gush", "gusto", "gutsy", "hail", "halcyon", "hale", "hallmark", "hallmarks",
                               "hallowed", "handier", "handily", "handsdown", "handsome", "handsomely", "handy",
                               "happier", "happily", "happiness", "happy", "hardworking", "hardier", "hardy",
                               "harmless", "harmonious", "harmoniously", "harmonize", "harmony", "headway", "heal",
                               "healthful", "healthy", "hearten", "heartening", "heartfelt", "heartily", "heartwarming",
                               "heaven", "heavenly", "helped", "helpful", "helping", "hero", "heroic", "heroically",
                               "heroine", "heroize", "heros", "highquality", "highspirited", "hilarious", "holy",
                               "homage", "honest", "honesty", "honor", "honorable", "honored", "honoring", "hooray",
                               "hopeful", "hospitable", "hot", "hotcake", "hotcakes", "hottest", "hug", "humane",
                               "humble", "humility", "humor", "humorous", "humorously", "humour", "humourous", "ideal",
                               "idealize", "ideally", "idol", "idolize", "idolized", "idyllic", "illuminate",
                               "illuminati", "illuminating", "illumine", "illustrious", "ilu", "imaculate",
                               "imaginative", "immaculate", "immaculately", "immense", "impartial", "impartiality",
                               "impartially", "impassioned", "impeccable", "impeccably", "important", "impress",
                               "impressed", "impresses", "impressive", "impressively", "impressiveness", "improve",
                               "improved", "improvement", "improvements", "improves", "improving", "incredible",
                               "incredibly", "indebted", "individualized", "indulgence", "indulgent", "industrious",
                               "inestimable", "inestimably", "inexpensive", "infallibility", "infallible", "infallibly",
                               "influential", "ingenious", "ingeniously", "ingenuity", "ingenuous", "ingenuously",
                               "innocuous", "innovation", "innovative", "inpressed", "insightful", "insightfully",
                               "inspiration", "inspirational", "inspire", "inspiring", "instantly", "instructive",
                               "instrumental", "integral", "integrated", "intelligence", "intelligent", "intelligible",
                               "interesting", "interests", "intimacy", "intimate", "intricate", "intrigue",
                               "intriguing", "intriguingly", "intuitive", "invaluable", "invaluablely", "inventive",
                               "invigorate", "invigorating", "invincibility", "invincible", "inviolable", "inviolate",
                               "invulnerable", "irreplaceable", "irreproachable", "irresistible", "irresistibly",
                               "issuefree", "jawdroping", "jawdropping", "jollify", "jolly", "jovial", "joy", "joyful",
                               "joyfully", "joyous", "joyously", "jubilant", "jubilantly", "jubilate", "jubilation",
                               "jubiliant", "judicious", "justly", "keen", "keenly", "keenness", "kidfriendly",
                               "kindliness", "kindly", "kindness", "knowledgeable", "kudos", "largecapacity", "laud",
                               "laudable", "laudably", "lavish", "lavishly", "lawabiding", "lawful", "lawfully", "lead",
                               "leading", "leads", "lean", "led", "legendary", "leverage", "levity", "liberate",
                               "liberation", "liberty", "lifesaver", "lighthearted", "lighter", "likable", "like",
                               "liked", "likes", "liking", "lionhearted", "lively", "logical", "longlasting", "lovable",
                               "lovably", "love", "loved", "loveliness", "lovely", "lover", "loves", "loving",
                               "lowcost", "lowprice", "lowpriced", "lowrisk", "lowerpriced", "loyal", "loyalty",
                               "lucid", "lucidly", "luck", "luckier", "luckiest", "luckiness", "lucky", "lucrative",
                               "luminous", "lush", "luster", "lustrous", "luxuriant", "luxuriate", "luxurious",
                               "luxuriously", "luxury", "lyrical", "magic", "magical", "magnanimous", "magnanimously",
                               "magnificence", "magnificent", "magnificently", "majestic", "majesty", "manageable",
                               "maneuverable", "marvel", "marveled", "marvelled", "marvellous", "marvelous",
                               "marvelously", "marvelousness", "marvels", "master", "masterful", "masterfully",
                               "masterpiece", "masterpieces", "masters", "mastery", "matchless", "mature", "maturely",
                               "maturity", "meaningful", "memorable", "merciful", "mercifully", "mercy", "merit",
                               "meritorious", "merrily", "merriment", "merriness", "merry", "mesmerize", "mesmerized",
                               "mesmerizes", "mesmerizing", "mesmerizingly", "meticulous", "meticulously", "mightily",
                               "mighty", "mindblowing", "miracle", "miracles", "miraculous", "miraculously",
                               "miraculousness", "modern", "modest", "modesty", "momentous", "monumental",
                               "monumentally", "morality", "motivated", "multipurpose", "navigable", "neat", "neatest",
                               "neatly", "nice", "nicely", "nicer", "nicest", "nifty", "nimble", "noble", "nobly",
                               "noiseless", "nonviolence", "nonviolent", "notably", "noteworthy", "nourish",
                               "nourishing", "nourishment", "novelty", "nurturing", "oasis", "obsession", "obsessions",
                               "obtainable", "openly", "openness", "optimal", "optimism", "optimistic", "opulent",
                               "orderly", "originality", "outdo", "outdone", "outperform", "outperformed",
                               "outperforming", "outperforms", "outshine", "outshone", "outsmart", "outstanding",
                               "outstandingly", "outstrip", "outwit", "ovation", "overjoyed", "overtake", "overtaken",
                               "overtakes", "overtaking", "overtook", "overture", "painfree", "painless", "painlessly",
                               "palatial", "pamper", "pampered", "pamperedly", "pamperedness", "pampers", "panoramic",
                               "paradise", "paramount", "pardon", "passion", "passionate", "passionately", "patience",
                               "patient", "patiently", "patriot", "patriotic", "peace", "peaceable", "peaceful",
                               "peacefully", "peacekeepers", "peach", "peerless", "pep", "pepped", "pepping", "peppy",
                               "peps", "perfect", "perfection", "perfectly", "permissible", "perseverance", "persevere",
                               "personages", "personalized", "phenomenal", "phenomenally", "picturesque", "piety",
                               "pinnacle", "playful", "playfully", "pleasant", "pleasantly", "pleased", "pleases",
                               "pleasing", "pleasingly", "pleasurable", "pleasurably", "pleasure", "plentiful",
                               "pluses", "plush", "plusses", "poetic", "poeticize", "poignant", "poise", "poised",
                               "polished", "polite", "politeness", "popular", "portable", "posh", "positive",
                               "positively", "positives", "powerful", "powerfully", "praise", "praiseworthy",
                               "praising", "precious", "precise", "precisely", "preeminent", "prefer", "preferable",
                               "preferably", "prefered", "preferes", "preferring", "prefers", "premier", "prestige",
                               "prestigious", "prettily", "pretty", "priceless", "pride", "principled", "privilege",
                               "privileged", "prize", "proactive", "problemfree", "problemsolver", "prodigious",
                               "prodigiously", "prodigy", "productive", "productively", "proficient", "proficiently",
                               "profound", "profoundly", "profuse", "profusion", "progress", "progressive", "prolific",
                               "prominence", "prominent", "promise", "promised", "promises", "promising", "promoter",
                               "prompt", "promptly", "proper", "properly", "propitious", "propitiously", "pros",
                               "prosper", "prosperity", "prosperous", "prospros", "protect", "protection", "protective",
                               "proud", "proven", "proves", "providence", "proving", "prowess", "prudence", "prudent",
                               "prudently", "punctual", "pure", "purify", "purposeful", "quaint", "qualified",
                               "qualify", "quicker", "quiet", "quieter", "radiance", "radiant", "rapid", "rapport",
                               "rapt", "rapture", "raptureous", "raptureously", "rapturous", "rapturously", "rational",
                               "razorsharp", "reachable", "readable", "readily", "ready", "reaffirm", "reaffirmation",
                               "realistic", "realizable", "reasonable", "reasonably", "reasoned", "reassurance",
                               "reassure", "receptive", "reclaim", "recomend", "recommend", "recommendation",
                               "recommendations", "recommended", "reconcile", "reconciliation", "recordsetting",
                               "recover", "recovery", "rectification", "rectify", "rectifying", "redeem", "redeeming",
                               "redemption", "refine", "refined", "refinement", "reform", "reformed", "reforming",
                               "reforms", "refresh", "refreshed", "refreshing", "refund", "refunded", "regal",
                               "regally", "regard", "rejoice", "rejoicing", "rejoicingly", "rejuvenate", "rejuvenated",
                               "rejuvenating", "relaxed", "relent", "reliable", "reliably", "relief", "relish",
                               "remarkable", "remarkably", "remedy", "remission", "remunerate", "renaissance",
                               "renewed", "renown", "renowned", "replaceable", "reputable", "reputation", "resilient",
                               "resolute", "resound", "resounding", "resourceful", "resourcefulness", "respect",
                               "respectable", "respectful", "respectfully", "respite", "resplendent", "responsibly",
                               "responsive", "restful", "restored", "restructure", "restructured", "restructuring",
                               "retractable", "revel", "revelation", "revere", "reverence", "reverent", "reverently",
                               "revitalize", "revival", "revive", "revives", "revolutionary", "revolutionize",
                               "revolutionized", "revolutionizes", "reward", "rewarding", "rewardingly", "rich",
                               "richer", "richly", "richness", "right", "righten", "righteous", "righteously",
                               "righteousness", "rightful", "rightfully", "rightly", "rightness", "riskfree", "robust",
                               "rockstar", "rockstars", "romantic", "romantically", "romanticize", "roomier", "roomy",
                               "rosy", "safe", "safely", "sagacity", "sagely", "saint", "saintliness", "saintly",
                               "salutary", "salute", "sane", "satisfactorily", "satisfactory", "satisfied", "satisfies",
                               "satisfy", "satisfying", "satisified", "saver", "savings", "savior", "savvy", "scenic",
                               "seamless", "seasoned", "secure", "securely", "selective", "selfdetermination",
                               "selfrespect", "selfsatisfaction", "selfsufficiency", "selfsufficient", "sensation",
                               "sensational", "sensationally", "sensations", "sensible", "sensibly", "sensitive",
                               "serene", "serenity", "sexy", "sharp", "sharper", "sharpest", "shimmering",
                               "shimmeringly", "shine", "shiny", "significant", "silent", "simpler", "simplest",
                               "simplified", "simplifies", "simplify", "simplifying", "sincere", "sincerely",
                               "sincerity", "skill", "skilled", "skillful", "skillfully", "slammin", "sleek", "slick",
                               "smart", "smarter", "smartest", "smartly", "smile", "smiles", "smiling", "smilingly",
                               "smitten", "smooth", "smoother", "smoothes", "smoothest", "smoothly", "snappy", "snazzy",
                               "sociable", "soft", "softer", "solace", "solicitous", "solicitously", "solid",
                               "solidarity", "soothe", "soothingly", "sophisticated", "soulful", "soundly", "soundness",
                               "spacious", "sparkle", "sparkling", "spectacular", "spectacularly", "speedily", "speedy",
                               "spellbind", "spellbinding", "spellbindingly", "spellbound", "spirited", "spiritual",
                               "splendid", "splendidly", "splendor", "spontaneous", "sporty", "spotless", "sprightly",
                               "stability", "stabilize", "stable", "stainless", "standout", "stateoftheart", "stately",
                               "statuesque", "staunch", "staunchly", "staunchness", "steadfast", "steadfastly",
                               "steadfastness", "steadiest", "steadiness", "steady", "stellar", "stellarly",
                               "stimulate", "stimulates", "stimulating", "stimulative", "stirringly", "straighten",
                               "straightforward", "streamlined", "striking", "strikingly", "striving", "strong",
                               "stronger", "strongest", "stunned", "stunning", "stunningly", "stupendous",
                               "stupendously", "sturdier", "sturdy", "stylish", "stylishly", "stylized", "suave",
                               "suavely", "sublime", "subsidize", "subsidized", "subsidizes", "subsidizing",
                               "substantive", "succeed", "succeeded", "succeeding", "succeeds", "succes", "success",
                               "successes", "successful", "successfully", "suffice", "sufficed", "suffices",
                               "sufficient", "sufficiently", "suitable", "sumptuous", "sumptuously", "sumptuousness",
                               "super", "superb", "superbly", "superior", "superiority", "supple", "support",
                               "supported", "supporter", "supporting", "supportive", "supports", "supremacy", "supreme",
                               "supremely", "supurb", "supurbly", "surmount", "surpass", "surreal", "survival",
                               "survivor", "sustainability", "sustainable", "swank", "swankier", "swankiest", "swanky",
                               "sweeping", "sweet", "sweeten", "sweetheart", "sweetly", "sweetness", "swift",
                               "swiftness", "talent", "talented", "talents", "tantalize", "tantalizing",
                               "tantalizingly", "tempt", "tempting", "temptingly", "tenacious", "tenaciously",
                               "tenacity", "tender", "tenderly", "terrific", "terrifically", "thank", "thankful",
                               "thinner", "thoughtful", "thoughtfully", "thoughtfulness", "thrift", "thrifty", "thrill",
                               "thrilled", "thrilling", "thrillingly", "thrills", "thrive", "thriving", "thumbup",
                               "thumbsup", "tickle", "tidy", "timehonored", "timely", "tingle", "titillate",
                               "titillating", "titillatingly", "togetherness", "tolerable", "tollfree", "top",
                               "topquality", "topnotch", "tops", "tough", "tougher", "toughest", "traction", "tranquil",
                               "tranquility", "transparent", "treasure", "tremendously", "trendy", "triumph",
                               "triumphal", "triumphant", "triumphantly", "trivially", "trophy", "troublefree", "trump",
                               "trumpet", "trust", "trusted", "trusting", "trustingly", "trustworthiness",
                               "trustworthy", "trusty", "truthful", "truthfully", "truthfulness", "twinkly",
                               "ultracrisp", "unabashed", "unabashedly", "unaffected", "unassailable", "unbeatable",
                               "unbiased", "unbound", "uncomplicated", "unconditional", "undamaged", "undaunted",
                               "understandable", "undisputable", "undisputably", "undisputed", "unencumbered",
                               "unequivocal", "unequivocally", "unfazed", "unfettered", "unforgettable", "unity",
                               "unlimited", "unmatched", "unparalleled", "unquestionable", "unquestionably", "unreal",
                               "unrestricted", "unrivaled", "unselfish", "unwavering", "upbeat", "upgradable",
                               "upgradeable", "upgraded", "upheld", "uphold", "uplift", "uplifting", "upliftingly",
                               "upliftment", "upscale", "usable", "useable", "useful", "userfriendly",
                               "userreplaceable", "valiant", "valiantly", "valor", "valuable", "variety", "venerate",
                               "verifiable", "veritable", "versatile", "versatility", "vibrant", "vibrantly",
                               "victorious", "victory", "viewable", "vigilance", "vigilant", "virtue", "virtuous",
                               "virtuously", "visionary", "vivacious", "vivid", "vouch", "vouchsafe", "warm", "warmer",
                               "warmhearted", "warmly", "warmth", "wealthy", "welcome", "well", "wellbacklit",
                               "wellbalanced", "wellbehaved", "wellbred", "wellconnected", "welleducated",
                               "wellestablished", "wellinformed", "wellintentioned", "wellknown", "wellmade",
                               "wellmanaged", "wellmannered", "wellpositioned", "wellreceived", "wellregarded",
                               "wellrounded", "wellrun", "wellwishers", "wellbeing", "whoa", "wholeheartedly",
                               "wholesome", "whooa", "whoooa", "wieldy", "willing", "willingly", "willingness", "win",
                               "windfall", "winnable", "winner", "winners", "winning", "wins", "wisdom", "wise",
                               "wisely", "witty", "won", "wonder", "wonderful", "wonderfully", "wonderous",
                               "wonderously", "wonders", "wondrous", "woo", "work", "workable", "worked", "works",
                               "worldfamous", "worth", "worthiness", "worthwhile", "worthy", "wow", "wowed", "wowing",
                               "wows", "yay", "youthful", "zeal", "zenith", "zest", "zippy", ]
        self.negative_words = ["2faced", "2faces", "abnormal", "abolish", "abominable", "abominably", "abominate",
                               "abomination", "abort", "aborted", "aborts", "abrade", "abrasive", "abrupt", "abruptly",
                               "abscond", "absence", "absentminded", "absentee", "absurd", "absurdity", "absurdly",
                               "absurdness", "abuse", "abused", "abuses", "abusive", "abysmal", "abysmally", "abyss",
                               "accidental", "accost", "accursed", "accusation", "accusations", "accuse", "accuses",
                               "accusing", "accusingly", "acerbate", "acerbic", "acerbically", "ache", "ached", "aches",
                               "achey", "aching", "acrid", "acridly", "acridness", "acrimonious", "acrimoniously",
                               "acrimony", "adamant", "adamantly", "addict", "addicted", "addicting", "addicts",
                               "admonish", "admonisher", "admonishingly", "admonishment", "admonition", "adulterate",
                               "adulterated", "adulteration", "adulterier", "adversarial", "adversary", "adverse",
                               "adversity", "afflict", "affliction", "afflictive", "affront", "afraid", "aggravate",
                               "aggravating", "aggravation", "aggression", "aggressive", "aggressiveness", "aggressor",
                               "aggrieve", "aggrieved", "aggrivation", "aghast", "agonies", "agonize", "agonizing",
                               "agonizingly", "agony", "aground", "ail", "ailing", "ailment", "aimless", "alarm",
                               "alarmed", "alarming", "alarmingly", "alienate", "alienated", "alienation", "allegation",
                               "allegations", "allege", "allergic", "allergies", "allergy", "aloof", "altercation",
                               "ambiguity", "ambiguous", "ambivalence", "ambivalent", "ambush", "amiss", "amputate",
                               "anarchism", "anarchist", "anarchistic", "anarchy", "anemic", "anger", "angrily",
                               "angriness", "angry", "anguish", "animosity", "annihilate", "annihilation", "annoy",
                               "annoyance", "annoyances", "annoyed", "annoying", "annoyingly", "annoys", "anomalous",
                               "anomaly", "antagonism", "antagonist", "antagonistic", "antagonize", "anti",
                               "antiamerican", "antiisraeli", "antioccupation", "antiproliferation", "antisemites",
                               "antisocial", "antius", "antiwhite", "antipathy", "antiquated", "antithetical",
                               "anxieties", "anxiety", "anxious", "anxiously", "anxiousness", "apathetic",
                               "apathetically", "apathy", "apocalypse", "apocalyptic", "apologist", "apologists",
                               "appal", "appall", "appalled", "appalling", "appallingly", "apprehension",
                               "apprehensions", "apprehensive", "apprehensively", "arbitrary", "arcane", "archaic",
                               "arduous", "arduously", "argumentative", "arrogance", "arrogant", "arrogantly",
                               "ashamed", "asinine", "asininely", "asinininity", "askance", "asperse", "aspersion",
                               "aspersions", "assail", "assassin", "assassinate", "assault", "assult", "astray",
                               "asunder", "atrocious", "atrocities", "atrocity", "atrophy", "attack", "attacks",
                               "audacious", "audaciously", "audaciousness", "audacity", "audiciously", "austere",
                               "authoritarian", "autocrat", "autocratic", "avalanche", "avarice", "avaricious",
                               "avariciously", "avenge", "averse", "aversion", "aweful", "awful", "awfully",
                               "awfulness", "awkward", "awkwardness", "ax", "babble", "backlogged", "backache",
                               "backaches", "backaching", "backbite", "backbiting", "backward", "backwardness",
                               "backwood", "backwoods", "bad", "badly", "baffle", "baffled", "bafflement", "baffling",
                               "bait", "balk", "banal", "banalize", "bane", "banish", "banishment", "bankrupt",
                               "barbarian", "barbaric", "barbarically", "barbarity", "barbarous", "barbarously",
                               "barren", "baseless", "bash", "bashed", "bashful", "bashing", "bastard", "bastards",
                               "battered", "battering", "batty", "bearish", "beastly", "bedlam", "bedlamite", "befoul",
                               "beg", "beggar", "beggarly", "begging", "beguile", "belabor", "belated", "beleaguer",
                               "belie", "belittle", "belittled", "belittling", "bellicose", "belligerence",
                               "belligerent", "belligerently", "bemoan", "bemoaning", "bemused", "bent", "berate",
                               "bereave", "bereavement", "bereft", "berserk", "beseech", "beset", "besiege", "besmirch",
                               "bestial", "betray", "betrayal", "betrayals", "betrayer", "betraying", "betrays",
                               "bewail", "beware", "bewilder", "bewildered", "bewildering", "bewilderingly",
                               "bewilderment", "bewitch", "bias", "biased", "biases", "bicker", "bickering",
                               "bidrigging", "bigotries", "bigotry", "bitch", "bitchy", "biting", "bitingly", "bitter",
                               "bitterly", "bitterness", "bizarre", "blab", "blabber", "blackmail", "blah", "blame",
                               "blameworthy", "bland", "blandish", "blaspheme", "blasphemous", "blasphemy", "blasted",
                               "blatant", "blatantly", "blather", "bleak", "bleakly", "bleakness", "bleed", "bleeding",
                               "bleeds", "blemish", "blind", "blinding", "blindingly", "blindside", "blister",
                               "blistering", "bloated", "blockage", "blockhead", "bloodshed", "bloodthirsty", "bloody",
                               "blotchy", "blow", "blunder", "blundering", "blunders", "blunt", "blur", "bluring",
                               "blurred", "blurring", "blurry", "blurs", "blurt", "boastful", "boggle", "bogus", "boil",
                               "boiling", "boisterous", "bomb", "bombard", "bombardment", "bombastic", "bondage",
                               "bonkers", "bore", "bored", "boredom", "bores", "boring", "botch", "bother", "bothered",
                               "bothering", "bothers", "bothersome", "bowdlerize", "boycott", "braggart", "bragger",
                               "brainless", "brainwash", "brash", "brashly", "brashness", "brat", "bravado", "brazen",
                               "brazenly", "brazenness", "breach", "break", "breakdown", "breaking", "breaks",
                               "breakup", "breakups", "bribery", "brimstone", "bristle", "brittle", "broke", "broken",
                               "brokenhearted", "brood", "browbeat", "bruise", "bruised", "bruises", "bruising",
                               "brusque", "brutal", "brutalising", "brutalities", "brutality", "brutalize",
                               "brutalizing", "brutally", "brute", "brutish", "bs", "buckle", "bug", "bugging", "buggy",
                               "bugs", "bulkier", "bulkiness", "bulky", "bulkyness", "bull", "bullies", "bullshit",
                               "bullshyt", "bully", "bullying", "bullyingly", "bum", "bump", "bumped", "bumping",
                               "bumpping", "bumps", "bumpy", "bungle", "bungler", "bungling", "bunk", "burden",
                               "burdensome", "burdensomely", "burn", "burned", "burning", "burns", "bust", "busts",
                               "busybody", "butcher", "butchery", "buzzing", "byzantine", "cackle", "calamities",
                               "calamitous", "calamitously", "calamity", "callous", "calumniate", "calumniation",
                               "calumnies", "calumnious", "calumniously", "calumny", "cancer", "cancerous", "cannibal",
                               "cannibalize", "capitulate", "capricious", "capriciously", "capriciousness", "capsize",
                               "careless", "carelessness", "caricature", "carnage", "carp", "cartoonish",
                               "cashstrapped", "castigate", "castrated", "casualty", "cataclysm", "cataclysmal",
                               "cataclysmic", "cataclysmically", "catastrophe", "catastrophes", "catastrophic",
                               "catastrophically", "catastrophies", "caustic", "caustically", "cautionary", "cave",
                               "censure", "chafe", "chaff", "chagrin", "challenging", "chaos", "chaotic", "chasten",
                               "chastise", "chastisement", "chatter", "chatterbox", "cheap", "cheapen", "cheaply",
                               "cheat", "cheated", "cheater", "cheating", "cheats", "checkered", "cheerless", "cheesy",
                               "chide", "childish", "chill", "chilly", "chintzy", "choke", "choleric", "choppy",
                               "chore", "chronic", "chunky", "clamor", "clamorous", "clash", "cliche", "cliched",
                               "clique", "clog", "clogged", "clogs", "cloud", "clouding", "cloudy", "clueless",
                               "clumsy", "clunky", "coarse", "cocky", "coerce", "coercion", "coercive", "cold",
                               "coldly", "collapse", "collude", "collusion", "combative", "combust", "comical",
                               "commiserate", "commonplace", "commotion", "commotions", "complacent", "complain",
                               "complained", "complaining", "complains", "complaint", "complaints", "complex",
                               "complicated", "complication", "complicit", "compulsion", "compulsive", "concede",
                               "conceded", "conceit", "conceited", "concen", "concens", "concern", "concerned",
                               "concerns", "concession", "concessions", "condemn", "condemnable", "condemnation",
                               "condemned", "condemns", "condescend", "condescending", "condescendingly",
                               "condescension", "confess", "confession", "confessions", "confined", "conflict",
                               "conflicted", "conflicting", "conflicts", "confound", "confounded", "confounding",
                               "confront", "confrontation", "confrontational", "confuse", "confused", "confuses",
                               "confusing", "confusion", "confusions", "congested", "congestion", "cons", "conscons",
                               "conservative", "conspicuous", "conspicuously", "conspiracies", "conspiracy",
                               "conspirator", "conspiratorial", "conspire", "consternation", "contagious",
                               "contaminate", "contaminated", "contaminates", "contaminating", "contamination",
                               "contempt", "contemptible", "contemptuous", "contemptuously", "contend", "contention",
                               "contentious", "contort", "contortions", "contradict", "contradiction", "contradictory",
                               "contrariness", "contravene", "contrive", "contrived", "controversial", "controversy",
                               "convoluted", "corrode", "corrosion", "corrosions", "corrosive", "corrupt", "corrupted",
                               "corrupting", "corruption", "corrupts", "corruptted", "costlier", "costly",
                               "counterproductive", "coupists", "covetous", "coward", "cowardly", "crabby", "crack",
                               "cracked", "cracks", "craftily", "craftly", "crafty", "cramp", "cramped", "cramping",
                               "cranky", "crap", "crappy", "craps", "crash", "crashed", "crashes", "crashing", "crass",
                               "craven", "cravenly", "craze", "crazily", "craziness", "crazy", "creak", "creaking",
                               "creaks", "credulous", "creep", "creeping", "creeps", "creepy", "crept", "crime",
                               "criminal", "cringe", "cringed", "cringes", "cripple", "crippled", "cripples",
                               "crippling", "crisis", "critic", "critical", "criticism", "criticisms", "criticize",
                               "criticized", "criticizing", "critics", "cronyism", "crook", "crooked", "crooks",
                               "crowded", "crowdedness", "crude", "cruel", "crueler", "cruelest", "cruelly",
                               "cruelness", "cruelties", "cruelty", "crumble", "crumbling", "crummy", "crumple",
                               "crumpled", "crumples", "crush", "crushed", "crushing", "cry", "culpable", "culprit",
                               "cumbersome", "cunt", "cunts", "cuplrit", "curse", "cursed", "curses", "curt", "cuss",
                               "cussed", "cutthroat", "cynical", "cynicism", "dmn", "damage", "damaged", "damages",
                               "damaging", "damn", "damnable", "damnably", "damnation", "damned", "damning", "damper",
                               "danger", "dangerous", "dangerousness", "dark", "darken", "darkened", "darker",
                               "darkness", "dastard", "dastardly", "daunt", "daunting", "dauntingly", "dawdle", "daze",
                               "dazed", "dead", "deadbeat", "deadlock", "deadly", "deadweight", "deaf", "dearth",
                               "death", "debacle", "debase", "debasement", "debaser", "debatable", "debauch",
                               "debaucher", "debauchery", "debilitate", "debilitating", "debility", "debt", "debts",
                               "decadence", "decadent", "decay", "decayed", "deceit", "deceitful", "deceitfully",
                               "deceitfulness", "deceive", "deceiver", "deceivers", "deceiving", "deception",
                               "deceptive", "deceptively", "declaim", "decline", "declines", "declining", "decrement",
                               "decrepit", "decrepitude", "decry", "defamation", "defamations", "defamatory", "defame",
                               "defect", "defective", "defects", "defensive", "defiance", "defiant", "defiantly",
                               "deficiencies", "deficiency", "deficient", "defile", "defiler", "deform", "deformed",
                               "defrauding", "defunct", "defy", "degenerate", "degenerately", "degeneration",
                               "degradation", "degrade", "degrading", "degradingly", "dehumanization", "dehumanize",
                               "deign", "deject", "dejected", "dejectedly", "dejection", "delay", "delayed", "delaying",
                               "delays", "delinquency", "delinquent", "delirious", "delirium", "delude", "deluded",
                               "deluge", "delusion", "delusional", "delusions", "demean", "demeaning", "demise",
                               "demolish", "demolisher", "demon", "demonic", "demonize", "demonized", "demonizes",
                               "demonizing", "demoralize", "demoralizing", "demoralizingly", "denial", "denied",
                               "denies", "denigrate", "denounce", "dense", "dent", "dented", "dents", "denunciate",
                               "denunciation", "denunciations", "deny", "denying", "deplete", "deplorable",
                               "deplorably", "deplore", "deploring", "deploringly", "deprave", "depraved", "depravedly",
                               "deprecate", "depress", "depressed", "depressing", "depressingly", "depression",
                               "depressions", "deprive", "deprived", "deride", "derision", "derisive", "derisively",
                               "derisiveness", "derogatory", "desecrate", "desert", "desertion", "desiccate",
                               "desiccated", "desititute", "desolate", "desolately", "desolation", "despair",
                               "despairing", "despairingly", "desperate", "desperately", "desperation", "despicable",
                               "despicably", "despise", "despised", "despoil", "despoiler", "despondence",
                               "despondency", "despondent", "despondently", "despot", "despotic", "despotism",
                               "destabilisation", "destains", "destitute", "destitution", "destroy", "destroyer",
                               "destruction", "destructive", "desultory", "deter", "deteriorate", "deteriorating",
                               "deterioration", "deterrent", "detest", "detestable", "detestably", "detested",
                               "detesting", "detests", "detract", "detracted", "detracting", "detraction", "detracts",
                               "detriment", "detrimental", "devastate", "devastated", "devastates", "devastating",
                               "devastatingly", "devastation", "deviate", "deviation", "devil", "devilish",
                               "devilishly", "devilment", "devilry", "devious", "deviously", "deviousness", "devoid",
                               "diabolic", "diabolical", "diabolically", "diametrically", "diappointed", "diatribe",
                               "diatribes", "dick", "dictator", "dictatorial", "die", "diehard", "died", "dies",
                               "difficult", "difficulties", "difficulty", "diffidence", "dilapidated", "dilemma",
                               "dillydally", "dim", "dimmer", "din", "ding", "dings", "dinky", "dire", "direly",
                               "direness", "dirt", "dirtbag", "dirtbags", "dirts", "dirty", "disable", "disabled",
                               "disaccord", "disadvantage", "disadvantaged", "disadvantageous", "disadvantages",
                               "disaffect", "disaffected", "disaffirm", "disagree", "disagreeable", "disagreeably",
                               "disagreed", "disagreeing", "disagreement", "disagrees", "disallow", "disapointed",
                               "disapointing", "disapointment", "disappoint", "disappointed", "disappointing",
                               "disappointingly", "disappointment", "disappointments", "disappoints", "disapprobation",
                               "disapproval", "disapprove", "disapproving", "disarm", "disarray", "disaster",
                               "disasterous", "disastrous", "disastrously", "disavow", "disavowal", "disbelief",
                               "disbelieve", "disbeliever", "disclaim", "discombobulate", "discomfit", "discomfititure",
                               "discomfort", "discompose", "disconcert", "disconcerted", "disconcerting",
                               "disconcertingly", "disconsolate", "disconsolately", "disconsolation", "discontent",
                               "discontented", "discontentedly", "discontinued", "discontinuity", "discontinuous",
                               "discord", "discordance", "discordant", "discountenance", "discourage", "discouragement",
                               "discouraging", "discouragingly", "discourteous", "discourteously", "discoutinous",
                               "discredit", "discrepant", "discriminate", "discrimination", "discriminatory", "disdain",
                               "disdained", "disdainful", "disdainfully", "disfavor", "disgrace", "disgraced",
                               "disgraceful", "disgracefully", "disgruntle", "disgruntled", "disgust", "disgusted",
                               "disgustedly", "disgustful", "disgustfully", "disgusting", "disgustingly", "dishearten",
                               "disheartening", "dishearteningly", "dishonest", "dishonestly", "dishonesty", "dishonor",
                               "dishonorable", "dishonorablely", "disillusion", "disillusioned", "disillusionment",
                               "disillusions", "disinclination", "disinclined", "disingenuous", "disingenuously",
                               "disintegrate", "disintegrated", "disintegrates", "disintegration", "disinterest",
                               "disinterested", "dislike", "disliked", "dislikes", "disliking", "dislocated",
                               "disloyal", "disloyalty", "dismal", "dismally", "dismalness", "dismay", "dismayed",
                               "dismaying", "dismayingly", "dismissive", "dismissively", "disobedience", "disobedient",
                               "disobey", "disoobedient", "disorder", "disordered", "disorderly", "disorganized",
                               "disorient", "disoriented", "disown", "disparage", "disparaging", "disparagingly",
                               "dispensable", "dispirit", "dispirited", "dispiritedly", "dispiriting", "displace",
                               "displaced", "displease", "displeased", "displeasing", "displeasure", "disproportionate",
                               "disprove", "disputable", "dispute", "disputed", "disquiet", "disquieting",
                               "disquietingly", "disquietude", "disregard", "disregardful", "disreputable", "disrepute",
                               "disrespect", "disrespectable", "disrespectablity", "disrespectful", "disrespectfully",
                               "disrespectfulness", "disrespecting", "disrupt", "disruption", "disruptive", "diss",
                               "dissapointed", "dissappointed", "dissappointing", "dissatisfaction", "dissatisfactory",
                               "dissatisfied", "dissatisfies", "dissatisfy", "dissatisfying", "dissed", "dissemble",
                               "dissembler", "dissension", "dissent", "dissenter", "dissention", "disservice", "disses",
                               "dissidence", "dissident", "dissidents", "dissing", "dissocial", "dissolute",
                               "dissolution", "dissonance", "dissonant", "dissonantly", "dissuade", "dissuasive",
                               "distains", "distaste", "distasteful", "distastefully", "distort", "distorted",
                               "distortion", "distorts", "distract", "distracting", "distraction", "distraught",
                               "distraughtly", "distraughtness", "distress", "distressed", "distressing",
                               "distressingly", "distrust", "distrustful", "distrusting", "disturb", "disturbance",
                               "disturbed", "disturbing", "disturbingly", "disunity", "disvalue", "divergent",
                               "divisive", "divisively", "divisiveness", "dizzing", "dizzingly", "dizzy", "doddering",
                               "dodgey", "dogged", "doggedly", "dogmatic", "doldrums", "domineer", "domineering",
                               "donside", "doom", "doomed", "doomsday", "dope", "doubt", "doubtful", "doubtfully",
                               "doubts", "douchbag", "douchebag", "douchebags", "downbeat", "downcast", "downer",
                               "downfall", "downfallen", "downgrade", "downhearted", "downheartedly", "downhill",
                               "downside", "downsides", "downturn", "downturns", "drab", "draconian", "draconic",
                               "drag", "dragged", "dragging", "dragoon", "drags", "drain", "drained", "draining",
                               "drains", "drastic", "drastically", "drawback", "drawbacks", "dread", "dreadful",
                               "dreadfully", "dreadfulness", "dreary", "dripped", "dripping", "drippy", "drips",
                               "drones", "droop", "droops", "dropout", "dropouts", "drought", "drowning", "drunk",
                               "drunkard", "drunken", "dubious", "dubiously", "dubitable", "dud", "dull", "dullard",
                               "dumb", "dumbfound", "dump", "dumped", "dumping", "dumps", "dunce", "dungeon",
                               "dungeons", "dupe", "dust", "dusty", "dwindling", "dying", "earsplitting", "eccentric",
                               "eccentricity", "effigy", "effrontery", "egocentric", "egomania", "egotism",
                               "egotistical", "egotistically", "egregious", "egregiously", "electionrigger",
                               "elimination", "emaciated", "emasculate", "embarrass", "embarrassing", "embarrassingly",
                               "embarrassment", "embattled", "embroil", "embroiled", "embroilment", "emergency",
                               "emphatic", "emphatically", "emptiness", "encroach", "encroachment", "endanger",
                               "enemies", "enemy", "enervate", "enfeeble", "enflame", "engulf", "enjoin", "enmity",
                               "enrage", "enraged", "enraging", "enslave", "entangle", "entanglement", "entrap",
                               "entrapment", "envious", "enviously", "enviousness", "epidemic", "equivocal", "erase",
                               "erode", "erodes", "erosion", "err", "errant", "erratic", "erratically", "erroneous",
                               "erroneously", "error", "errors", "eruptions", "escapade", "eschew", "estranged",
                               "evade", "evasion", "evasive", "evil", "evildoer", "evils", "eviscerate", "exacerbate",
                               "exagerate", "exagerated", "exagerates", "exaggerate", "exaggeration", "exasperate",
                               "exasperated", "exasperating", "exasperatingly", "exasperation", "excessive",
                               "excessively", "exclusion", "excoriate", "excruciating", "excruciatingly", "excuse",
                               "excuses", "execrate", "exhaust", "exhausted", "exhaustion", "exhausts", "exhorbitant",
                               "exhort", "exile", "exorbitant", "exorbitantance", "exorbitantly", "expel", "expensive",
                               "expire", "expired", "explode", "exploit", "exploitation", "explosive", "expropriate",
                               "expropriation", "expulse", "expunge", "exterminate", "extermination", "extinguish",
                               "extort", "extortion", "extraneous", "extravagance", "extravagant", "extravagantly",
                               "extremism", "extremist", "extremists", "eyesore", "fk", "fabricate", "fabrication",
                               "facetious", "facetiously", "fail", "failed", "failing", "fails", "failure", "failures",
                               "faint", "fainthearted", "faithless", "fake", "fall", "fallacies", "fallacious",
                               "fallaciously", "fallaciousness", "fallacy", "fallen", "falling", "fallout", "falls",
                               "false", "falsehood", "falsely", "falsify", "falter", "faltered", "famine", "famished",
                               "fanatic", "fanatical", "fanatically", "fanaticism", "fanatics", "fanciful", "farce",
                               "farcical", "farcicalyetprovocative", "farcically", "farfetched", "fascism", "fascist",
                               "fastidious", "fastidiously", "fastuous", "fat", "fatal", "fatalistic", "fatalistically",
                               "fatally", "fatcat", "fatcats", "fateful", "fatefully", "fathomless", "fatigue",
                               "fatigued", "fatique", "fatty", "fatuity", "fatuous", "fatuously", "fault", "faults",
                               "faulty", "fawningly", "faze", "fear", "fearful", "fearfully", "fears", "fearsome",
                               "feckless", "feeble", "feeblely", "feebleminded", "feign", "feint", "fell", "felon",
                               "felonious", "ferociously", "ferocity", "fetid", "fever", "feverish", "fevers", "fiasco",
                               "fib", "fibber", "fickle", "fiction", "fictional", "fictitious", "fidget", "fidgety",
                               "fiend", "fiendish", "fierce", "figurehead", "filth", "filthy", "finagle", "finicky",
                               "fissures", "fist", "flabbergast", "flabbergasted", "flagging", "flagrant", "flagrantly",
                               "flair", "flairs", "flak", "flake", "flakey", "flakieness", "flaking", "flaky", "flare",
                               "flares", "flareup", "flareups", "flatout", "flaunt", "flaw", "flawed", "flaws", "flee",
                               "fleed", "fleeing", "fleer", "flees", "fleeting", "flicering", "flicker", "flickering",
                               "flickers", "flighty", "flimflam", "flimsy", "flirt", "flirty", "floored", "flounder",
                               "floundering", "flout", "fluster", "foe", "fool", "fooled", "foolhardy", "foolish",
                               "foolishly", "foolishness", "forbid", "forbidden", "forbidding", "forceful",
                               "foreboding", "forebodingly", "forfeit", "forged", "forgetful", "forgetfully",
                               "forgetfulness", "forlorn", "forlornly", "forsake", "forsaken", "forswear", "foul",
                               "foully", "foulness", "fractious", "fractiously", "fracture", "fragile", "fragmented",
                               "frail", "frantic", "frantically", "franticly", "fraud", "fraudulent", "fraught",
                               "frazzle", "frazzled", "freak", "freaking", "freakish", "freakishly", "freaks", "freeze",
                               "freezes", "freezing", "frenetic", "frenetically", "frenzied", "frenzy", "fret",
                               "fretful", "frets", "friction", "frictions", "fried", "friggin", "frigging", "fright",
                               "frighten", "frightening", "frighteningly", "frightful", "frightfully", "frigid",
                               "frost", "frown", "froze", "frozen", "fruitless", "fruitlessly", "frustrate",
                               "frustrated", "frustrates", "frustrating", "frustratingly", "frustration",
                               "frustrations", "fuck", "fucking", "fudge", "fugitive", "fullblown", "fulminate",
                               "fumble", "fume", "fumes", "fundamentalism", "funky", "funnily", "funny", "furious",
                               "furiously", "furor", "fury", "fuss", "fussy", "fustigate", "fusty", "futile",
                               "futilely", "futility", "fuzzy", "gabble", "gaff", "gaffe", "gainsay", "gainsayer",
                               "gall", "galling", "gallingly", "galls", "gangster", "gape", "garbage", "garish", "gasp",
                               "gauche", "gaudy", "gawk", "gawky", "geezer", "genocide", "getrich", "ghastly", "ghetto",
                               "ghosting", "gibber", "gibberish", "gibe", "giddy", "gimmick", "gimmicked", "gimmicking",
                               "gimmicks", "gimmicky", "glare", "glaringly", "glib", "glibly", "glitch", "glitches",
                               "gloatingly", "gloom", "gloomy", "glower", "glum", "glut", "gnawing", "goad", "goading",
                               "godawful", "goof", "goofy", "goon", "gossip", "graceless", "gracelessly", "graft",
                               "grainy", "grapple", "grate", "grating", "gravely", "greasy", "greed", "greedy", "grief",
                               "grievance", "grievances", "grieve", "grieving", "grievous", "grievously", "grim",
                               "grimace", "grind", "gripe", "gripes", "grisly", "gritty", "gross", "grossly",
                               "grotesque", "grouch", "grouchy", "groundless", "grouse", "growl", "grudge", "grudges",
                               "grudging", "grudgingly", "gruesome", "gruesomely", "gruff", "grumble", "grumpier",
                               "grumpiest", "grumpily", "grumpish", "grumpy", "guile", "guilt", "guiltily", "guilty",
                               "gullible", "gutless", "gutter", "hack", "hacks", "haggard", "haggle", "hairloss",
                               "halfhearted", "halfheartedly", "hallucinate", "hallucination", "hamper", "hampered",
                               "handicapped", "hang", "hangs", "haphazard", "hapless", "harangue", "harass", "harassed",
                               "harasses", "harassment", "harboring", "harbors", "hard", "hardhit", "hardline",
                               "hardball", "harden", "hardened", "hardheaded", "hardhearted", "hardliner", "hardliners",
                               "hardship", "hardships", "harm", "harmed", "harmful", "harms", "harpy", "harridan",
                               "harried", "harrow", "harsh", "harshly", "hasseling", "hassle", "hassled", "hassles",
                               "haste", "hastily", "hasty", "hate", "hated", "hateful", "hatefully", "hatefulness",
                               "hater", "haters", "hates", "hating", "hatred", "haughtily", "haughty", "haunt",
                               "haunting", "havoc", "hawkish", "haywire", "hazard", "hazardous", "haze", "hazy",
                               "headache", "headaches", "heartbreaker", "heartbreaking", "heartbreakingly", "heartless",
                               "heathen", "heavyhanded", "heavyhearted", "heck", "heckle", "heckled", "heckles",
                               "hectic", "hedge", "hedonistic", "heedless", "hefty", "hegemonism", "hegemonistic",
                               "hegemony", "heinous", "hell", "hellbent", "hellion", "hells", "helpless", "helplessly",
                               "helplessness", "heresy", "heretic", "heretical", "hesitant", "hestitant", "hideous",
                               "hideously", "hideousness", "highpriced", "hiliarious", "hinder", "hindrance", "hiss",
                               "hissed", "hissing", "hohum", "hoard", "hoax", "hobble", "hogs", "hollow", "hoodium",
                               "hoodwink", "hooligan", "hopeless", "hopelessly", "hopelessness", "horde", "horrendous",
                               "horrendously", "horrible", "horrid", "horrific", "horrified", "horrifies", "horrify",
                               "horrifying", "horrifys", "hostage", "hostile", "hostilities", "hostility", "hotbeds",
                               "hothead", "hotheaded", "hothouse", "hubris", "huckster", "hum", "humid", "humiliate",
                               "humiliating", "humiliation", "humming", "hung", "hurt", "hurted", "hurtful", "hurting",
                               "hurts", "hustler", "hype", "hypocricy", "hypocrisy", "hypocrite", "hypocrites",
                               "hypocritical", "hypocritically", "hysteria", "hysteric", "hysterical", "hysterically",
                               "hysterics", "idiocies", "idiocy", "idiot", "idiotic", "idiotically", "idiots", "idle",
                               "ignoble", "ignominious", "ignominiously", "ignominy", "ignorance", "ignorant", "ignore",
                               "illadvised", "illconceived", "illdefined", "illdesigned", "illfated", "illfavored",
                               "illformed", "illmannered", "illnatured", "illsorted", "illtempered", "illtreated",
                               "illtreatment", "illusage", "illused", "illegal", "illegally", "illegitimate", "illicit",
                               "illiterate", "illness", "illogic", "illogical", "illogically", "illusion", "illusions",
                               "illusory", "imaginary", "imbalance", "imbecile", "imbroglio", "immaterial", "immature",
                               "imminence", "imminently", "immobilized", "immoderate", "immoderately", "immodest",
                               "immoral", "immorality", "immorally", "immovable", "impair", "impaired", "impasse",
                               "impatience", "impatient", "impatiently", "impeach", "impedance", "impede", "impediment",
                               "impending", "impenitent", "imperfect", "imperfection", "imperfections", "imperfectly",
                               "imperialist", "imperil", "imperious", "imperiously", "impermissible", "impersonal",
                               "impertinent", "impetuous", "impetuously", "impiety", "impinge", "impious", "implacable",
                               "implausible", "implausibly", "implicate", "implication", "implode", "impolite",
                               "impolitely", "impolitic", "importunate", "importune", "impose", "imposers", "imposing",
                               "imposition", "impossible", "impossiblity", "impossibly", "impotent", "impoverish",
                               "impoverished", "impractical", "imprecate", "imprecise", "imprecisely", "imprecision",
                               "imprison", "imprisonment", "improbability", "improbable", "improbably", "improper",
                               "improperly", "impropriety", "imprudence", "imprudent", "impudence", "impudent",
                               "impudently", "impugn", "impulsive", "impulsively", "impunity", "impure", "impurity",
                               "inability", "inaccuracies", "inaccuracy", "inaccurate", "inaccurately", "inaction",
                               "inactive", "inadequacy", "inadequate", "inadequately", "inadverent", "inadverently",
                               "inadvisable", "inadvisably", "inane", "inanely", "inappropriate", "inappropriately",
                               "inapt", "inaptitude", "inarticulate", "inattentive", "inaudible", "incapable",
                               "incapably", "incautious", "incendiary", "incense", "incessant", "incessantly", "incite",
                               "incitement", "incivility", "inclement", "incognizant", "incoherence", "incoherent",
                               "incoherently", "incommensurate", "incomparable", "incomparably", "incompatability",
                               "incompatibility", "incompatible", "incompetence", "incompetent", "incompetently",
                               "incomplete", "incompliant", "incomprehensible", "incomprehension", "inconceivable",
                               "inconceivably", "incongruous", "incongruously", "inconsequent", "inconsequential",
                               "inconsequentially", "inconsequently", "inconsiderate", "inconsiderately",
                               "inconsistence", "inconsistencies", "inconsistency", "inconsistent", "inconsolable",
                               "inconsolably", "inconstant", "inconvenience", "inconveniently", "incorrect",
                               "incorrectly", "incorrigible", "incorrigibly", "incredulous", "incredulously",
                               "inculcate", "indecency", "indecent", "indecently", "indecision", "indecisive",
                               "indecisively", "indecorum", "indefensible", "indelicate", "indeterminable",
                               "indeterminably", "indeterminate", "indifference", "indifferent", "indigent",
                               "indignant", "indignantly", "indignation", "indignity", "indiscernible", "indiscreet",
                               "indiscreetly", "indiscretion", "indiscriminate", "indiscriminately", "indiscriminating",
                               "indistinguishable", "indoctrinate", "indoctrination", "indolent", "indulge",
                               "ineffective", "ineffectively", "ineffectiveness", "ineffectual", "ineffectually",
                               "ineffectualness", "inefficacious", "inefficacy", "inefficiency", "inefficient",
                               "inefficiently", "inelegance", "inelegant", "ineligible", "ineloquent", "ineloquently",
                               "inept", "ineptitude", "ineptly", "inequalities", "inequality", "inequitable",
                               "inequitably", "inequities", "inescapable", "inescapably", "inessential", "inevitable",
                               "inevitably", "inexcusable", "inexcusably", "inexorable", "inexorably", "inexperience",
                               "inexperienced", "inexpert", "inexpertly", "inexpiable", "inexplainable", "inextricable",
                               "inextricably", "infamous", "infamously", "infamy", "infected", "infection",
                               "infections", "inferior", "inferiority", "infernal", "infest", "infested", "infidel",
                               "infidels", "infiltrator", "infiltrators", "infirm", "inflame", "inflammation",
                               "inflammatory", "inflammed", "inflated", "inflationary", "inflexible", "inflict",
                               "infraction", "infringe", "infringement", "infringements", "infuriate", "infuriated",
                               "infuriating", "infuriatingly", "inglorious", "ingrate", "ingratitude", "inhibit",
                               "inhibition", "inhospitable", "inhospitality", "inhuman", "inhumane", "inhumanity",
                               "inimical", "inimically", "iniquitous", "iniquity", "injudicious", "injure", "injurious",
                               "injury", "injustice", "injustices", "innuendo", "inoperable", "inopportune",
                               "inordinate", "inordinately", "insane", "insanely", "insanity", "insatiable", "insecure",
                               "insecurity", "insensible", "insensitive", "insensitively", "insensitivity", "insidious",
                               "insidiously", "insignificance", "insignificant", "insignificantly", "insincere",
                               "insincerely", "insincerity", "insinuate", "insinuating", "insinuation", "insociable",
                               "insolence", "insolent", "insolently", "insolvent", "insouciance", "instability",
                               "instable", "instigate", "instigator", "instigators", "insubordinate", "insubstantial",
                               "insubstantially", "insufferable", "insufferably", "insufficiency", "insufficient",
                               "insufficiently", "insular", "insult", "insulted", "insulting", "insultingly", "insults",
                               "insupportable", "insupportably", "insurmountable", "insurmountably", "insurrection",
                               "intefere", "inteferes", "intense", "interfere", "interference", "interferes",
                               "intermittent", "interrupt", "interruption", "interruptions", "intimidate",
                               "intimidating", "intimidatingly", "intimidation", "intolerable", "intolerablely",
                               "intolerance", "intoxicate", "intractable", "intransigence", "intransigent", "intrude",
                               "intrusion", "intrusive", "inundate", "inundated", "invader", "invalid", "invalidate",
                               "invalidity", "invasive", "invective", "inveigle", "invidious", "invidiously",
                               "invidiousness", "invisible", "involuntarily", "involuntary", "irascible", "irate",
                               "irately", "ire", "irk", "irked", "irking", "irks", "irksome", "irksomely",
                               "irksomeness", "irksomenesses", "ironic", "ironical", "ironically", "ironies", "irony",
                               "irragularity", "irrational", "irrationalities", "irrationality", "irrationally",
                               "irrationals", "irreconcilable", "irrecoverable", "irrecoverableness",
                               "irrecoverablenesses", "irrecoverably", "irredeemable", "irredeemably", "irreformable",
                               "irregular", "irregularity", "irrelevance", "irrelevant", "irreparable", "irreplacible",
                               "irrepressible", "irresolute", "irresolvable", "irresponsible", "irresponsibly",
                               "irretating", "irretrievable", "irreversible", "irritable", "irritably", "irritant",
                               "irritate", "irritated", "irritating", "irritation", "irritations", "isolate",
                               "isolated", "isolation", "issue", "issues", "itch", "itching", "itchy", "jabber",
                               "jaded", "jagged", "jam", "jarring", "jaundiced", "jealous", "jealously", "jealousness",
                               "jealousy", "jeer", "jeering", "jeeringly", "jeers", "jeopardize", "jeopardy", "jerk",
                               "jerky", "jitter", "jitters", "jittery", "jobkilling", "jobless", "joke", "joker",
                               "jolt", "judder", "juddering", "judders", "jumpy", "junk", "junky", "junkyard", "jutter",
                               "jutters", "kaput", "kill", "killed", "killer", "killing", "killjoy", "kills", "knave",
                               "knife", "knock", "knotted", "kook", "kooky", "lack", "lackadaisical", "lacked",
                               "lackey", "lackeys", "lacking", "lackluster", "lacks", "laconic", "lag", "lagged",
                               "lagging", "laggy", "lags", "laidoff", "lambast", "lambaste", "lame", "lameduck",
                               "lament", "lamentable", "lamentably", "languid", "languish", "languor", "languorous",
                               "languorously", "lanky", "lapse", "lapsed", "lapses", "lascivious", "lastditch",
                               "latency", "laughable", "laughably", "laughingstock", "lawbreaker", "lawbreaking",
                               "lawless", "lawlessness", "layoff", "layoffhappy", "lazy", "leak", "leakage", "leakages",
                               "leaking", "leaks", "leaky", "lech", "lecher", "lecherous", "lechery", "leech", "leer",
                               "leery", "leftleaning", "lemon", "lengthy", "lessdeveloped", "lesserknown", "letch",
                               "lethal", "lethargic", "lethargy", "lewd", "lewdly", "lewdness", "liability", "liable",
                               "liar", "liars", "licentious", "licentiously", "licentiousness", "lie", "lied", "lier",
                               "lies", "lifethreatening", "lifeless", "limit", "limitation", "limitations", "limited",
                               "limits", "limp", "listless", "litigious", "littleknown", "livid", "lividly", "loath",
                               "loathe", "loathing", "loathly", "loathsome", "loathsomely", "lone", "loneliness",
                               "lonely", "loner", "lonesome", "longtime", "longwinded", "longing", "longingly",
                               "loophole", "loopholes", "loose", "loot", "lorn", "lose", "loser", "losers", "loses",
                               "losing", "loss", "losses", "lost", "loud", "louder", "lousy", "loveless", "lovelorn",
                               "lowrated", "lowly", "ludicrous", "ludicrously", "lugubrious", "lukewarm", "lull",
                               "lumpy", "lunatic", "lunaticism", "lurch", "lure", "lurid", "lurk", "lurking", "lying",
                               "macabre", "mad", "madden", "maddening", "maddeningly", "madder", "madly", "madman",
                               "madness", "maladjusted", "maladjustment", "malady", "malaise", "malcontent",
                               "malcontented", "maledict", "malevolence", "malevolent", "malevolently", "malice",
                               "malicious", "maliciously", "maliciousness", "malign", "malignant", "malodorous",
                               "maltreatment", "mangle", "mangled", "mangles", "mangling", "mania", "maniac",
                               "maniacal", "manic", "manipulate", "manipulation", "manipulative", "manipulators", "mar",
                               "marginal", "marginally", "martyrdom", "martyrdomseeking", "mashed", "massacre",
                               "massacres", "matte", "mawkish", "mawkishly", "mawkishness", "meager", "meaningless",
                               "meanness", "measly", "meddle", "meddlesome", "mediocre", "mediocrity", "melancholy",
                               "melodramatic", "melodramatically", "meltdown", "menace", "menacing", "menacingly",
                               "mendacious", "mendacity", "menial", "merciless", "mercilessly", "mess", "messed",
                               "messes", "messing", "messy", "midget", "miff", "militancy", "mindless", "mindlessly",
                               "mirage", "mire", "misalign", "misaligned", "misaligns", "misapprehend", "misbecome",
                               "misbecoming", "misbegotten", "misbehave", "misbehavior", "miscalculate",
                               "miscalculation", "miscellaneous", "mischief", "mischievous", "mischievously",
                               "misconception", "misconceptions", "miscreant", "miscreants", "misdirection", "miser",
                               "miserable", "miserableness", "miserably", "miseries", "miserly", "misery", "misfit",
                               "misfortune", "misgiving", "misgivings", "misguidance", "misguide", "misguided",
                               "mishandle", "mishap", "misinform", "misinformed", "misinterpret", "misjudge",
                               "misjudgment", "mislead", "misleading", "misleadingly", "mislike", "mismanage",
                               "mispronounce", "mispronounced", "mispronounces", "misread", "misreading",
                               "misrepresent", "misrepresentation", "miss", "missed", "misses", "misstatement", "mist",
                               "mistake", "mistaken", "mistakenly", "mistakes", "mistified", "mistress", "mistrust",
                               "mistrustful", "mistrustfully", "mists", "misunderstand", "misunderstanding",
                               "misunderstandings", "misunderstood", "misuse", "moan", "mobster", "mock", "mocked",
                               "mockeries", "mockery", "mocking", "mockingly", "mocks", "molest", "molestation",
                               "monotonous", "monotony", "monster", "monstrosities", "monstrosity", "monstrous",
                               "monstrously", "moody", "moot", "mope", "morbid", "morbidly", "mordant", "mordantly",
                               "moribund", "moron", "moronic", "morons", "mortification", "mortified", "mortify",
                               "mortifying", "motionless", "motley", "mourn", "mourner", "mournful", "mournfully",
                               "muddle", "muddy", "mudslinger", "mudslinging", "mulish", "multipolarization", "mundane",
                               "murder", "murderer", "murderous", "murderously", "murky", "muscleflexing", "mushy",
                               "musty", "mysterious", "mysteriously", "mystery", "mystify", "myth", "nag", "nagging",
                               "naive", "naively", "narrower", "nastily", "nastiness", "nasty", "naughty", "nauseate",
                               "nauseates", "nauseating", "nauseatingly", "naïve", "nebulous", "nebulously", "needless",
                               "needlessly", "needy", "nefarious", "nefariously", "negate", "negation", "negative",
                               "negatives", "negativity", "neglect", "neglected", "negligence", "negligent", "nemesis",
                               "nepotism", "nervous", "nervously", "nervousness", "nettle", "nettlesome", "neurotic",
                               "neurotically", "niggle", "niggles", "nightmare", "nightmarish", "nightmarishly",
                               "nitpick", "nitpicking", "noise", "noises", "noisier", "noisy", "nonconfidence",
                               "nonexistent", "nonresponsive", "nonsense", "nosey", "notoriety", "notorious",
                               "notoriously", "noxious", "nuisance", "numb", "obese", "object", "objection",
                               "objectionable", "objections", "oblique", "obliterate", "obliterated", "oblivious",
                               "obnoxious", "obnoxiously", "obscene", "obscenely", "obscenity", "obscure", "obscured",
                               "obscures", "obscurity", "obsess", "obsessive", "obsessively", "obsessiveness",
                               "obsolete", "obstacle", "obstinate", "obstinately", "obstruct", "obstructed",
                               "obstructing", "obstruction", "obstructs", "obtrusive", "obtuse", "occlude", "occluded",
                               "occludes", "occluding", "odd", "odder", "oddest", "oddities", "oddity", "oddly", "odor",
                               "offence", "offend", "offender", "offending", "offenses", "offensive", "offensively",
                               "offensiveness", "officious", "ominous", "ominously", "omission", "omit", "onesided",
                               "onerous", "onerously", "onslaught", "opinionated", "opponent", "opportunistic",
                               "oppose", "opposition", "oppositions", "oppress", "oppression", "oppressive",
                               "oppressively", "oppressiveness", "oppressors", "ordeal", "orphan", "ostracize",
                               "outbreak", "outburst", "outbursts", "outcast", "outcry", "outlaw", "outmoded",
                               "outrage", "outraged", "outrageous", "outrageously", "outrageousness", "outrages",
                               "outsider", "overhyped", "overvaluation", "overact", "overacted", "overawe",
                               "overbalance", "overbalanced", "overbearing", "overbearingly", "overblown", "overdo",
                               "overdone", "overdue", "overemphasize", "overheat", "overkill", "overloaded", "overlook",
                               "overpaid", "overpayed", "overplay", "overpower", "overpriced", "overrated", "overreach",
                               "overrun", "overshadow", "oversight", "oversights", "oversimplification",
                               "oversimplified", "oversimplify", "oversize", "overstate", "overstated", "overstatement",
                               "overstatements", "overstates", "overtaxed", "overthrow", "overthrows", "overturn",
                               "overweight", "overwhelm", "overwhelmed", "overwhelming", "overwhelmingly", "overwhelms",
                               "overzealous", "overzealously", "overzelous", "pain", "painful", "painfull", "painfully",
                               "pains", "pale", "pales", "paltry", "pan", "pandemonium", "pander", "pandering",
                               "panders", "panic", "panick", "panicked", "panicking", "panicky", "paradoxical",
                               "paradoxically", "paralize", "paralyzed", "paranoia", "paranoid", "parasite", "pariah",
                               "parody", "partiality", "partisan", "partisans", "passe", "passive", "passiveness",
                               "pathetic", "pathetically", "patronize", "paucity", "pauper", "paupers", "payback",
                               "peculiar", "peculiarly", "pedantic", "peeled", "peeve", "peeved", "peevish",
                               "peevishly", "penalize", "penalty", "perfidious", "perfidity", "perfunctory", "peril",
                               "perilous", "perilously", "perish", "pernicious", "perplex", "perplexed", "perplexing",
                               "perplexity", "persecute", "persecution", "pertinacious", "pertinaciously",
                               "pertinacity", "perturb", "perturbed", "pervasive", "perverse", "perversely",
                               "perversion", "perversity", "pervert", "perverted", "perverts", "pessimism",
                               "pessimistic", "pessimistically", "pest", "pestilent", "petrified", "petrify",
                               "pettifog", "petty", "phobia", "phobic", "phony", "picket", "picketed", "picketing",
                               "pickets", "picky", "pig", "pigs", "pillage", "pillory", "pimple", "pinch", "pique",
                               "pitiable", "pitiful", "pitifully", "pitiless", "pitilessly", "pittance", "pity",
                               "plagiarize", "plague", "plasticky", "plaything", "plea", "pleas", "plebeian", "plight",
                               "plot", "plotters", "ploy", "plunder", "plunderer", "pointless", "pointlessly", "poison",
                               "poisonous", "poisonously", "pokey", "poky", "polarisation", "polemize", "pollute",
                               "polluter", "polluters", "polution", "pompous", "poor", "poorer", "poorest", "poorly",
                               "posturing", "pout", "poverty", "powerless", "prate", "pratfall", "prattle",
                               "precarious", "precariously", "precipitate", "precipitous", "predatory", "predicament",
                               "prejudge", "prejudice", "prejudices", "prejudicial", "premeditated", "preoccupy",
                               "preposterous", "preposterously", "presumptuous", "presumptuously", "pretence",
                               "pretend", "pretense", "pretentious", "pretentiously", "prevaricate", "pricey",
                               "pricier", "prick", "prickle", "prickles", "prideful", "prik", "primitive", "prison",
                               "prisoner", "problem", "problematic", "problems", "procrastinate", "procrastinates",
                               "procrastination", "profane", "profanity", "prohibit", "prohibitive", "prohibitively",
                               "propaganda", "propagandize", "proprietary", "prosecute", "protest", "protested",
                               "protesting", "protests", "protracted", "provocation", "provocative", "provoke", "pry",
                               "pugnacious", "pugnaciously", "pugnacity", "punch", "punish", "punishable", "punitive",
                               "punk", "puny", "puppet", "puppets", "puzzled", "puzzlement", "puzzling", "quack",
                               "qualm", "qualms", "quandary", "quarrel", "quarrellous", "quarrellously", "quarrels",
                               "quarrelsome", "quash", "queer", "questionable", "quibble", "quibbles", "quitter",
                               "rabid", "racism", "racist", "racists", "racy", "radical", "radicalization", "radically",
                               "radicals", "rage", "ragged", "raging", "rail", "raked", "rampage", "rampant",
                               "ramshackle", "rancor", "randomly", "rankle", "rant", "ranted", "ranting", "rantingly",
                               "rants", "rape", "raped", "raping", "rascal", "rascals", "rash", "rattle", "rattled",
                               "rattles", "ravage", "raving", "reactionary", "rebellious", "rebuff", "rebuke",
                               "recalcitrant", "recant", "recession", "recessionary", "reckless", "recklessly",
                               "recklessness", "recoil", "recourses", "redundancy", "redundant", "refusal", "refuse",
                               "refused", "refuses", "refusing", "refutation", "refute", "refuted", "refutes",
                               "refuting", "regress", "regression", "regressive", "regret", "regreted", "regretful",
                               "regretfully", "regrets", "regrettable", "regrettably", "regretted", "reject",
                               "rejected", "rejecting", "rejection", "rejects", "relapse", "relentless", "relentlessly",
                               "relentlessness", "reluctance", "reluctant", "reluctantly", "remorse", "remorseful",
                               "remorsefully", "remorseless", "remorselessly", "remorselessness", "renounce",
                               "renunciation", "repel", "repetitive", "reprehensible", "reprehensibly", "reprehension",
                               "reprehensive", "repress", "repression", "repressive", "reprimand", "reproach",
                               "reproachful", "reprove", "reprovingly", "repudiate", "repudiation", "repugn",
                               "repugnance", "repugnant", "repugnantly", "repulse", "repulsed", "repulsing",
                               "repulsive", "repulsively", "repulsiveness", "resent", "resentful", "resentment",
                               "resignation", "resigned", "resistance", "restless", "restlessness", "restrict",
                               "restricted", "restriction", "restrictive", "resurgent", "retaliate", "retaliatory",
                               "retard", "retarded", "retardedness", "retards", "reticent", "retract", "retreat",
                               "retreated", "revenge", "revengeful", "revengefully", "revert", "revile", "reviled",
                               "revoke", "revolt", "revolting", "revoltingly", "revulsion", "revulsive", "rhapsodize",
                               "rhetoric", "rhetorical", "ricer", "ridicule", "ridicules", "ridiculous", "ridiculously",
                               "rife", "rift", "rifts", "rigid", "rigidity", "rigidness", "rile", "riled", "rip",
                               "ripoff", "ripped", "risk", "risks", "risky", "rival", "rivalry", "roadblocks", "rocky",
                               "rogue", "rollercoaster", "rot", "rotten", "rough", "rremediable", "rubbish", "rude",
                               "rue", "ruffian", "ruffle", "ruin", "ruined", "ruining", "ruinous", "ruins", "rumbling",
                               "rumor", "rumors", "rumours", "rumple", "rundown", "runaway", "rupture", "rust", "rusts",
                               "rusty", "rut", "ruthless", "ruthlessly", "ruthlessness", "ruts", "sabotage", "sack",
                               "sacrificed", "sad", "sadden", "sadly", "sadness", "sag", "sagged", "sagging", "saggy",
                               "sags", "salacious", "sanctimonious", "sap", "sarcasm", "sarcastic", "sarcastically",
                               "sardonic", "sardonically", "sass", "satirical", "satirize", "savage", "savaged",
                               "savagery", "savages", "scaly", "scam", "scams", "scandal", "scandalize", "scandalized",
                               "scandalous", "scandalously", "scandals", "scandel", "scandels", "scant", "scapegoat",
                               "scar", "scarce", "scarcely", "scarcity", "scare", "scared", "scarier", "scariest",
                               "scarily", "scarred", "scars", "scary", "scathing", "scathingly", "sceptical", "scoff",
                               "scoffingly", "scold", "scolded", "scolding", "scoldingly", "scorching", "scorchingly",
                               "scorn", "scornful", "scornfully", "scoundrel", "scourge", "scowl", "scramble",
                               "scrambled", "scrambles", "scrambling", "scrap", "scratch", "scratched", "scratches",
                               "scratchy", "scream", "screech", "screwup", "screwed", "screwedup", "screwy", "scuff",
                               "scuffs", "scum", "scummy", "secondclass", "secondtier", "secretive", "sedentary",
                               "seedy", "seethe", "seething", "selfcoup", "selfcriticism", "selfdefeating",
                               "selfdestructive", "selfhumiliation", "selfinterest", "selfserving", "selfinterested",
                               "selfish", "selfishly", "selfishness", "semiretarded", "senile", "sensationalize",
                               "senseless", "senselessly", "seriousness", "sermonize", "servitude", "setup", "setback",
                               "setbacks", "sever", "severe", "severity", "sht", "shabby", "shadowy", "shady", "shake",
                               "shaky", "shallow", "sham", "shambles", "shame", "shameful", "shamefully",
                               "shamefulness", "shameless", "shamelessly", "shamelessness", "shark", "sharply",
                               "shatter", "shemale", "shimmer", "shimmy", "shipwreck", "shirk", "shirker", "shit",
                               "shiver", "shock", "shocked", "shocking", "shockingly", "shoddy", "shortlived",
                               "shortage", "shortchange", "shortcoming", "shortcomings", "shortness", "shortsighted",
                               "shortsightedness", "showdown", "shrew", "shriek", "shrill", "shrilly", "shrivel",
                               "shroud", "shrouded", "shrug", "shun", "shunned", "sick", "sicken", "sickening",
                               "sickeningly", "sickly", "sickness", "sidetrack", "sidetracked", "siege", "sillily",
                               "silly", "simplistic", "simplistically", "sin", "sinful", "sinfully", "sinister",
                               "sinisterly", "sink", "sinking", "skeletons", "skeptic", "skeptical", "skeptically",
                               "skepticism", "sketchy", "skimpy", "skinny", "skittish", "skittishly", "skulk", "slack",
                               "slander", "slanderer", "slanderous", "slanderously", "slanders", "slap", "slashing",
                               "slaughter", "slaughtered", "slave", "slaves", "sleazy", "slime", "slog", "slogged",
                               "slogging", "slogs", "sloooooooooooooow", "sloooow", "slooow", "sloow", "sloppily",
                               "sloppy", "sloth", "slothful", "slow", "slowmoving", "slowed", "slower", "slowest",
                               "slowly", "sloww", "slowww", "slowwww", "slug", "sluggish", "slump", "slumping",
                               "slumpping", "slur", "slut", "sluts", "sly", "smack", "smallish", "smash", "smear",
                               "smell", "smelled", "smelling", "smells", "smelly", "smelt", "smoke", "smokescreen",
                               "smolder", "smoldering", "smother", "smoulder", "smouldering", "smudge", "smudged",
                               "smudges", "smudging", "smug", "smugly", "smut", "smuttier", "smuttiest", "smutty",
                               "snag", "snagged", "snagging", "snags", "snappish", "snappishly", "snare", "snarky",
                               "snarl", "sneak", "sneakily", "sneaky", "sneer", "sneering", "sneeringly", "snob",
                               "snobbish", "snobby", "snobish", "snobs", "snub", "socal", "soapy", "sob", "sober",
                               "sobering", "solemn", "solicitude", "somber", "sore", "sorely", "soreness", "sorrow",
                               "sorrowful", "sorrowfully", "sorry", "sour", "sourly", "spade", "spank", "spendy",
                               "spew", "spewed", "spewing", "spews", "spilling", "spinster", "spiritless", "spite",
                               "spiteful", "spitefully", "spitefulness", "splatter", "split", "splitting", "spoil",
                               "spoilage", "spoilages", "spoiled", "spoilled", "spoils", "spook", "spookier",
                               "spookiest", "spookily", "spooky", "spoonfeed", "spoonfed", "sporadic", "spotty",
                               "spurious", "spurn", "sputter", "squabble", "squabbling", "squander", "squash", "squeak",
                               "squeaks", "squeaky", "squeal", "squealing", "squeals", "squirm", "stab", "stagnant",
                               "stagnate", "stagnation", "staid", "stain", "stains", "stale", "stalemate", "stall",
                               "stalls", "stammer", "stampede", "standstill", "stark", "starkly", "startle",
                               "startling", "startlingly", "starvation", "starve", "static", "steal", "stealing",
                               "steals", "steep", "steeply", "stench", "stereotype", "stereotypical", "stereotypically",
                               "stern", "stew", "sticky", "stiff", "stiffness", "stifle", "stifling", "stiflingly",
                               "stigma", "stigmatize", "sting", "stinging", "stingingly", "stingy", "stink", "stinks",
                               "stodgy", "stole", "stolen", "stooge", "stooges", "stormy", "straggle", "straggler",
                               "strain", "strained", "straining", "strange", "strangely", "stranger", "strangest",
                               "strangle", "streaky", "strenuous", "stress", "stresses", "stressful", "stressfully",
                               "stricken", "strict", "strictly", "strident", "stridently", "strife", "strike",
                               "stringent", "stringently", "struck", "struggle", "struggled", "struggles", "struggling",
                               "strut", "stubborn", "stubbornly", "stubbornness", "stuck", "stuffy", "stumble",
                               "stumbled", "stumbles", "stump", "stumped", "stumps", "stun", "stunt", "stunted",
                               "stupid", "stupidest", "stupidity", "stupidly", "stupified", "stupify", "stupor",
                               "stutter", "stuttered", "stuttering", "stutters", "sty", "stymied", "subpar", "subdued",
                               "subjected", "subjection", "subjugate", "subjugation", "submissive", "subordinate",
                               "subpoena", "subpoenas", "subservience", "subservient", "substandard", "subtract",
                               "subversion", "subversive", "subversively", "subvert", "succumb", "suck", "sucked",
                               "sucker", "sucks", "sucky", "sue", "sued", "sueing", "sues", "suffer", "suffered",
                               "sufferer", "sufferers", "suffering", "suffers", "suffocate", "sugarcoat", "sugarcoated",
                               "suicidal", "suicide", "sulk", "sullen", "sully", "sunder", "sunk", "sunken",
                               "superficial", "superficiality", "superficially", "superfluous", "superstition",
                               "superstitious", "suppress", "suppression", "surrender", "susceptible", "suspect",
                               "suspicion", "suspicions", "suspicious", "suspiciously", "swagger", "swamped", "sweaty",
                               "swelled", "swelling", "swindle", "swipe", "swollen", "symptom", "symptoms", "syndrome",
                               "taboo", "tacky", "taint", "tainted", "tamper", "tangle", "tangled", "tangles", "tank",
                               "tanked", "tanks", "tantrum", "tardy", "tarnish", "tarnished", "tarnishes", "tarnishing",
                               "tattered", "taunt", "taunting", "tauntingly", "taunts", "taut", "tawdry", "taxing",
                               "tease", "teasingly", "tedious", "tediously", "temerity", "temper", "tempest",
                               "temptation", "tenderness", "tense", "tension", "tentative", "tentatively", "tenuous",
                               "tenuously", "tepid", "terrible", "terribleness", "terribly", "terror", "terrorgenic",
                               "terrorism", "terrorize", "testily", "testy", "tetchily", "tetchy", "thankless",
                               "thicker", "thirst", "thorny", "thoughtless", "thoughtlessly", "thoughtlessness",
                               "thrash", "threat", "threaten", "threatening", "threats", "threesome", "throb",
                               "throbbed", "throbbing", "throbs", "throttle", "thug", "thumbdown", "thumbsdown",
                               "thwart", "timeconsuming", "timid", "timidity", "timidly", "timidness", "tiny",
                               "tingled", "tingling", "tired", "tiresome", "tiring", "tiringly", "toil", "toll",
                               "topheavy", "topple", "torment", "tormented", "torrent", "tortuous", "torture",
                               "tortured", "tortures", "torturing", "torturous", "torturously", "totalitarian",
                               "touchy", "toughness", "tout", "touted", "touts", "toxic", "traduce", "tragedy",
                               "tragic", "tragically", "traitor", "traitorous", "traitorously", "tramp", "trample",
                               "transgress", "transgression", "trap", "traped", "trapped", "trash", "trashed", "trashy",
                               "trauma", "traumatic", "traumatically", "traumatize", "traumatized", "travesties",
                               "travesty", "treacherous", "treacherously", "treachery", "treason", "treasonous",
                               "trick", "tricked", "trickery", "tricky", "trivial", "trivialize", "trouble", "troubled",
                               "troublemaker", "troubles", "troublesome", "troublesomely", "troubling", "troublingly",
                               "truant", "tumble", "tumbled", "tumbles", "tumultuous", "turbulent", "turmoil", "twist",
                               "twisted", "twists", "twofaced", "twofaces", "tyrannical", "tyrannically", "tyranny",
                               "tyrant", "ugh", "uglier", "ugliest", "ugliness", "ugly", "ulterior", "ultimatum",
                               "ultimatums", "ultrahardline", "unable", "unacceptable", "unacceptablely",
                               "unacceptably", "unaccessible", "unaccustomed", "unachievable", "unaffordable",
                               "unappealing", "unattractive", "unauthentic", "unavailable", "unavoidably", "unbearable",
                               "unbearablely", "unbelievable", "unbelievably", "uncaring", "uncertain", "uncivil",
                               "uncivilized", "unclean", "unclear", "uncollectible", "uncomfortable", "uncomfortably",
                               "uncomfy", "uncompetitive", "uncompromising", "uncompromisingly", "unconfirmed",
                               "unconstitutional", "uncontrolled", "unconvincing", "unconvincingly", "uncooperative",
                               "uncouth", "uncreative", "undecided", "undefined", "undependability", "undependable",
                               "undercut", "undercuts", "undercutting", "underdog", "underestimate", "underlings",
                               "undermine", "undermined", "undermines", "undermining", "underpaid", "underpowered",
                               "undersized", "undesirable", "undetermined", "undid", "undignified", "undissolved",
                               "undocumented", "undone", "undue", "unease", "uneasily", "uneasiness", "uneasy",
                               "uneconomical", "unemployed", "unequal", "unethical", "uneven", "uneventful",
                               "unexpected", "unexpectedly", "unexplained", "unfairly", "unfaithful", "unfaithfully",
                               "unfamiliar", "unfavorable", "unfeeling", "unfinished", "unfit", "unforeseen",
                               "unforgiving", "unfortunate", "unfortunately", "unfounded", "unfriendly", "unfulfilled",
                               "unfunded", "ungovernable", "ungrateful", "unhappily", "unhappiness", "unhappy",
                               "unhealthy", "unhelpful", "unilateralism", "unimaginable", "unimaginably", "unimportant",
                               "uninformed", "uninsured", "unintelligible", "unintelligile", "unipolar", "unjust",
                               "unjustifiable", "unjustifiably", "unjustified", "unjustly", "unkind", "unkindly",
                               "unknown", "unlamentable", "unlamentably", "unlawful", "unlawfully", "unlawfulness",
                               "unleash", "unlicensed", "unlikely", "unlucky", "unmoved", "unnatural", "unnaturally",
                               "unnecessary", "unneeded", "unnerve", "unnerved", "unnerving", "unnervingly",
                               "unnoticed", "unobserved", "unorthodox", "unorthodoxy", "unpleasant", "unpleasantries",
                               "unpopular", "unpredictable", "unprepared", "unproductive", "unprofitable", "unprove",
                               "unproved", "unproven", "unproves", "unproving", "unqualified", "unravel", "unraveled",
                               "unreachable", "unreadable", "unrealistic", "unreasonable", "unreasonably",
                               "unrelenting", "unrelentingly", "unreliability", "unreliable", "unresolved",
                               "unresponsive", "unrest", "unruly", "unsafe", "unsatisfactory", "unsavory",
                               "unscrupulous", "unscrupulously", "unsecure", "unseemly", "unsettle", "unsettled",
                               "unsettling", "unsettlingly", "unskilled", "unsophisticated", "unsound", "unspeakable",
                               "unspeakablely", "unspecified", "unstable", "unsteadily", "unsteadiness", "unsteady",
                               "unsuccessful", "unsuccessfully", "unsupported", "unsupportive", "unsure",
                               "unsuspecting", "unsustainable", "untenable", "untested", "unthinkable", "unthinkably",
                               "untimely", "untouched", "untrue", "untrustworthy", "untruthful", "unusable", "unusably",
                               "unuseable", "unuseably", "unusual", "unusually", "unviewable", "unwanted",
                               "unwarranted", "unwatchable", "unwelcome", "unwell", "unwieldy", "unwilling",
                               "unwillingly", "unwillingness", "unwise", "unwisely", "unworkable", "unworthy",
                               "unyielding", "upbraid", "upheaval", "uprising", "uproar", "uproarious", "uproariously",
                               "uproarous", "uproarously", "uproot", "upset", "upseting", "upsets", "upsetting",
                               "upsettingly", "urgent", "useless", "usurp", "usurper", "utterly", "vagrant", "vague",
                               "vagueness", "vain", "vainly", "vanity", "vehement", "vehemently", "vengeance",
                               "vengeful", "vengefully", "vengefulness", "venom", "venomous", "venomously", "vent",
                               "vestiges", "vex", "vexation", "vexing", "vexingly", "vibrate", "vibrated", "vibrates",
                               "vibrating", "vibration", "vice", "vicious", "viciously", "viciousness", "victimize",
                               "vile", "vileness", "vilify", "villainous", "villainously", "villains", "villian",
                               "villianous", "villianously", "villify", "vindictive", "vindictively", "vindictiveness",
                               "violate", "violation", "violator", "violators", "violent", "violently", "viper",
                               "virulence", "virulent", "virulently", "virus", "vociferous", "vociferously", "volatile",
                               "volatility", "vomit", "vomited", "vomiting", "vomits", "vulgar", "vulnerable", "wack",
                               "wail", "wallow", "wane", "waning", "wanton", "warily", "wariness", "warlike", "warned",
                               "warning", "warp", "warped", "wary", "washedout", "waste", "wasted", "wasteful",
                               "wastefulness", "wasting", "waterdown", "watereddown", "wayward", "weak", "weaken",
                               "weakening", "weaker", "weakness", "weaknesses", "weariness", "wearisome", "weary",
                               "wedge", "weed", "weep", "weird", "weirdly", "wheedle", "whimper", "whine", "whining",
                               "whiny", "whips", "whore", "whores", "wicked", "wickedly", "wickedness", "wild",
                               "wildly", "wiles", "wilt", "wily", "wimpy", "wince", "wobble", "wobbled", "wobbles",
                               "woe", "woebegone", "woeful", "woefully", "womanizer", "womanizing", "worn", "worried",
                               "worriedly", "worrier", "worries", "worrisome", "worry", "worrying", "worryingly",
                               "worse", "worsen", "worsening", "worst", "worthless", "worthlessly", "worthlessness",
                               "wound", "wounds", "wrangle", "wrath", "wreak", "wreaked", "wreaks", "wreck", "wrest",
                               "wrestle", "wretch", "wretched", "wretchedly", "wretchedness", "wrinkle", "wrinkled",
                               "wrinkles", "wrip", "wripped", "wripping", "writhe", "wrong", "wrongful", "wrongly",
                               "wrought", "yawn", "zap", "zapped", "zaps", "zealot", "zealous", "zealously", "zombie", ]
        self.stop_words = self.function_words + self.positive_words + self.negative_words
        self.sentiment_words = self.positive_words + self.negative_words

        # This is a placeholder for a gensim collocation model
        self.phrases = None

        # This is a placeholder for spacy's tagger
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.max_length = 9999999999999

        # Specific paths for the course labs
        self.data_dir = os.path.join("///", "srv", "data", "shared_data_folder", "data")
        self.states_dir = os.path.join("///", "srv", "data", "shared_data_folder", "states")

        # Initialize Style Vectorizer
        self.style_vectorizer = CountVectorizer(
            input="content",
            encoding="utf-8",
            decode_error="replace",
            ngram_range=(1, 2),
            preprocessor=self.clean_pre,
            analyzer="word",
            vocabulary=self.function_words,
            tokenizer=None,
        )

        # Initialize Sentiment Vectorizer
        self.sentiment_vectorizer = CountVectorizer(
            input="content",
            encoding="utf-8",
            decode_error="replace",
            ngram_range=(1, 1),
            preprocessor=self.clean_pre,
            analyzer="word",
            vocabulary=self.sentiment_words,
            tokenizer=None,
        )

    # ---------------------------------------------------------------------
    # Go through a dataset to build a content word vocabulary, with TF-IDF weighting
    # ---------------------------------------------------------------------
    def fit_tfidf(self, df, min_count=None, non_eng=False):

        # If no min_count, find one
        if min_count == None:
            min_count = self.get_min_count(df)

        # Get multi-word expressions using PMI with gensim
        self.fit_phrases(df, min_count=min_count, non_eng=non_eng)
        print("Finished finding phrases.")

        # Get vocabulary
        vocab = defaultdict(int)
        for line in self.read_clean(df):
            for word in line:
                vocab[word] += 1

        # Remove infrequent words and stopwords
        vocab_list = []

        # English-only version
        if non_eng == False:
            for word in vocab:
                if vocab[word] > min_count:
                    if word not in self.function_words:
                        if word not in self.sentiment_words:
                            vocab_list.append(word)

        # Multi-lingual version, doesn't have stopwords
        if non_eng == True:
            for word in vocab:
                if vocab[word] > min_count:
                    vocab_list.append(word)

        # Initialize TF-IDF Vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            input="content",
            encoding="utf-8",
            decode_error="replace",
            ngram_range=(1, 1),
            analyzer=self.clean,
            vocabulary=vocab_list,
            norm="l2",
            use_idf=True,
            smooth_idf=True,
            tokenizer=None,
        )

        # Fit on the dataset
        print("Fitting TF-IDF")
        self.tfidf_vectorizer.fit(raw_documents=self.read(df))

    # ---------------------------------------------------------------------
    # Use PMI to learn what phrases and collocations should be treated as one word
    # ---------------------------------------------------------------------
    def fit_phrases(self, df, min_count=100, non_eng=False):

        if non_eng == False:
            common_terms = self.function_words_single
        else:
            common_terms = []

        phrases = Phrases(
            sentences=self.read_clean(df),
            min_count=min_count,
            threshold=0.70,
            scoring="npmi",
            max_vocab_size=100000000,
            delimiter=b"_",
            common_terms=common_terms
        )

        # Save the lite version from gensim
        phrases = Phraser(phrases)
        self.phrases = phrases

    # print(self.phrases.phrasegrams)

    # ---------------------------------------------------------------------
    # Pre-processing function that doesn't strip words (for style and sentiment)
    # ---------------------------------------------------------------------
    def clean_pre(self, line):

        # Remove links, hashtags, at-mentions, mark-up, and "RT"
        line = re.sub(r"http\S+", "", line)
        line = re.sub(r"@\S+", "", line)
        line = re.sub(r"#\S+", "", line)
        line = re.sub("<[^>]*>", "", line)
        line = line.replace(" RT", "").replace("RT ", "")

        # Remove punctuation and extra spaces
        line = ct.pipe(line,
                       preprocessing.strip_tags,
                       preprocessing.strip_punctuation,
                       preprocessing.strip_numeric,
                       preprocessing.strip_non_alphanum,
                       preprocessing.strip_multiple_whitespaces
                       )

        # Strip and lowercase
        line = line.lower().strip().lstrip()

        return line

    # ---------------------------------------------------------------------
    # Pre-processing function that splits words, gets phrases, removes stopwords
    # ---------------------------------------------------------------------
    def clean(self, line, tag=False):

        # Remove links, hashtags, at-mentions, mark-up, and "RT"
        line = re.sub(r"http\S+", "", line)
        line = re.sub(r"@\S+", "", line)
        line = re.sub(r"#\S+", "", line)
        line = re.sub("<[^>]*>", "", line)
        line = line.replace(" RT", "").replace("RT ", "")

        # Remove punctuation and extra spaces
        line = ct.pipe(line,
                       preprocessing.strip_tags,
                       preprocessing.strip_punctuation,
                       preprocessing.strip_numeric,
                       preprocessing.strip_non_alphanum,
                       preprocessing.strip_multiple_whitespaces
                       )

        # Strip and lowercase
        line = line.lower().strip().lstrip().split()

        # If we've used PMI to find phrases, get those phrases now
        if self.phrases != None:
            line = list(self.phrases[line])

        # If we want Part-of-Speech tagging, do that now
        if tag == True:
            line = self.nlp(" ".join(line))
            line = [w.text + "_" + w.pos_ for w in line]

        return line

    # ---------------------------------------------------------------------
    # Pre-processing function that splits words, gets phrases, removes stopwords
    ## 0 = just split into words
    ## 1 = remove stop words
    ## 2 = lowercase
    ## 3 = remove punctuation
    ## 4 = remove non-linguistic material
    ## 5 = join phrases
    # ---------------------------------------------------------------------
    def clean_wordclouds(self, line, stage=1):

        if stage > 3:
            # Remove links, hashtags, at-mentions, mark-up, and "RT"
            line = re.sub(r"http\S+", "", line)
            line = re.sub(r"@\S+", "", line)
            line = re.sub(r"#\S+", "", line)
            line = re.sub("<[^>]*>", "", line)
            line = line.replace(" RT", "").replace("RT ", "")

        if stage > 2:
            # Remove punctuation and extra spaces
            line = ct.pipe(line,
                           preprocessing.strip_tags,
                           preprocessing.strip_punctuation,
                           preprocessing.strip_numeric,
                           preprocessing.strip_non_alphanum,
                           preprocessing.strip_multiple_whitespaces
                           )

        if stage > 1:
            # Strip and lowercase
            line = line.lower().strip().lstrip().split()
        else:
            line = line.split()

        if stage > 4:
            if self.phrases != None:
                line = list(self.phrases[line])

        if stage > 0:
            line = [x for x in line if x not in self.function_words_single]

        return line

    # ---------------------------------------------------------------------
    # Returns a list of raw strings from the dataframe
    # ---------------------------------------------------------------------
    def read(self, df, column="Text"):
        return [str(x) for x in df.loc[:, column].values]

    # ---------------------------------------------------------------------
    # Returns a list of cleaned strings from the dataframe
    # ---------------------------------------------------------------------
    def read_clean(self, df, tag=False, column="Text"):
        return [self.clean(str(x), tag=tag) for x in df.loc[:, column].values]

    # ---------------------------------------------------------------------
    # Save current state: includes all features and classifiers
    # ---------------------------------------------------------------------
    def save(self, name, thing):
        with open("AI.State." + name + ".pickle", "wb") as f:
            pickle.dump(thing, f)

    # ---------------------------------------------------------------------
    # Extract feature vectors (x)
    # ---------------------------------------------------------------------
    def get_features(self, df, features="style"):

        # Function word ngrams
        if features == "style":
            x = self.style_vectorizer.transform(self.read(df))
            vocab_size = len(self.style_vectorizer.vocabulary_.keys())

        # Positive and negative words
        elif features == "sentiment":
            x = self.sentiment_vectorizer.transform(self.read(df))
            vocab_size = len(self.sentiment_vectorizer.vocabulary_.keys())

        # TF-IDF weighted content words, with PMI for phrases
        elif features == "content":
            x = self.tfidf_vectorizer.transform(self.read(df))
            vocab_size = len(self.tfidf_vectorizer.vocabulary_.keys())

        return x, vocab_size

    # ---------------------------------------------------------------------
    # Train and test a Linear SVM classifier
    # ---------------------------------------------------------------------
    def split_data(self, df, test_size=0.10, n=2):

        # In most cases, we just want training/testing data
        if n == 2:
            train_df, test_df = train_test_split(df, test_size=test_size)
            return train_df, test_df

        # If we're using an MLP, we might want training/testing/validation data
        elif n == 3:
            train_df, test_df = train_test_split(df, test_size=test_size + test_size)
            test_df, val_df = train_test_split(test_df, test_size=0.50)
            return train_df, test_df, val_df

    # ---------------------------------------------------------------------
    # Train and test a Linear SVM classifier
    # ---------------------------------------------------------------------
    def svm(self, df, labels, features="style", cv=False):

        report = None
        scores = None

        # Initialize the classifier
        cls = LinearSVC(
            penalty="l2",
            loss="squared_hinge",
            dual=True,
            tol=0.0001,
            C=1.0,
            multi_class="ovr",
            fit_intercept=True,
            intercept_scaling=1,
            max_iter=200000
        )

        # Use training/testing evaluation method
        if cv == False:

            # Split into train/test
            train_df, test_df = self.split_data(df, test_size=0.10)

            # Get features
            train_x, vocab_size = self.get_features(train_df, features)
            test_x, vocab_size = self.get_features(test_df, features)

            # Train and save classifier
            cls.fit(X=train_x, y=train_df.loc[:, labels].values)
            self.cls = cls

            # Evaluate on test data
            predictions = cls.predict(test_x)
            report = classification_report(y_true=test_df.loc[:, labels].values, y_pred=predictions)
            print(report)
            return report

        # Use 10-fold cross-validation for evaluation method
        elif cv == True:

            # Get features
            x, vocab_size = self.get_features(df, features)

            # Run cross-validator
            scores = cross_validate(
                estimator=cls,
                X=x,
                y=df.loc[:, labels].values,
                scoring=["precision_weighted", "recall_weighted", "f1_weighted"],
                cv=10,
                return_estimator=False,
            )

            # Show results; we can't save the classifier because we trained 10 different times
            print(scores)
            return scores

        return scores, report

    # ---------------------------------------------------------------------
    # Train and test a Multi-Layer Perceptron classifier (only works for non-binary classes)
    # ---------------------------------------------------------------------
    def mlp(self, df, labels, features="style", x=None, validation_set=False):

        # Make train/test split
        if validation_set == False:
            train_df, test_df = self.split_data(df, test_size=0.10)

        # Make train / test / validation split
        elif validation_set == True:
            train_df, test_df, val_df = self.split_data(df, test_size=0.10, n=3)

        # Find the number of classes
        n_labels = len(list(set(train_df.loc[:, labels].values)))

        # TensorFlow requires one-hot encoded labels (not strings)
        labeler = LabelEncoder()
        y_train = labeler.fit_transform(train_df.loc[:, labels].values)
        y_test = labeler.transform(test_df.loc[:, labels].values)
        y_val = labeler.transform(val_df.loc[:, labels].values)

        # Get y_val if necessary
        if validation_set == False:
            y_val = y_test

        # Feature extraction
        train_x, vocab_size = self.get_features(train_df, features)
        test_x, vocab_size = self.get_features(test_df, features)

        if validation_set == True:
            val_x, vocab_size = self.get_features(val_df, features)

        # Initializing the model
        model = tf.keras.Sequential()
        model.add(tf.keras.Input(shape=(vocab_size,)))

        # One or more dense layers.
        for units in [50, 50, 50]:
            model.add(tf.keras.layers.Dense(units, activation="relu"))

        # Output layer. The first argument is the number of labels.
        model.add(tf.keras.layers.Dense(n_labels))

        # Compile model
        model.compile(optimizer="adam",
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=["accuracy"]
                      )

        # Now, begin or resume training
        model.fit(x=train_x.todense(),
                  y=y_train,
                  validation_data=(test_x.todense(), y_test),
                  epochs=25,
                  use_multiprocessing=True,
                  workers=5,
                  )

        # Reuse testing data if no validation set
        if validation_set == False:
            val_x = test_x
            val_y = y_test
            val_y = labeler.inverse_transform(val_y)
        else:
            val_y = labeler.inverse_transform(y_val)

        # Evaluate on held-out data; TensorFlow returns probabilities, not classes
        y_predict = np.argmax(model.predict(val_x.todense()), axis=-1)

        # Turn classes into string labels
        y_predict = labeler.inverse_transform(y_predict)

        # Get evaluation report
        report = classification_report(y_true=val_y, y_pred=y_predict)
        print(report)

        # Save to class object
        self.model = model

    # ---------------------------------------------------------------------
    # - Get embedding indexes for whole dataframe
    # ---------------------------------------------------------------------
    def df_to_index(self, df):

        x = np.array([self.line_to_index(line) for line in df.loc[:, "Text"].values])

        return x

    # ---------------------------------------------------------------------
    # - Go from the input line to a list of word2vec indexes
    # ---------------------------------------------------------------------
    def line_to_index(self, line):

        # Get an empty list for indexes, clean the line, and prune to max size
        line_index = []
        line = self.clean(line, tag=True)
        line = line[:self.max_size]

        # Get the embedding index for each word
        for word in line:

            try:
                line_index.append(self.word_vectors_vocab[word].index)

            except:
                pass

        # We need each speech to have the same dimensions, so we might need to add padding
        while len(line_index) < self.max_size:
            line_index.append(0)

        line_index = np.array(line_index)

        return line_index

    # ---------------------------------------------------------------------
    # - A Multi-layer perceptron with embeddings as input (only works for binary classes)
    # ---------------------------------------------------------------------
    def mlp_embeddings(self, df, labels, x, model=None):

        # TensorFlow requires encoded labels (not strings)
        labeler = LabelEncoder()
        y = df.loc[:, labels].values.reshape(-1, 1)
        y = labeler.fit_transform(y)

        # Get train/test split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)

        # Find the number of classes
        n_labels = len(list(set(df.loc[:, labels].values)))

        # If there's no model already, make one
        if model == None:

            # Initializing the model
            model = tf.keras.Sequential()

            # Create a tensorflow layer from our word2vec embeddings
            embedding_layer = tf.keras.layers.Embedding(input_dim=self.word_vectors.shape[0],
                                                        output_dim=self.word_vectors.shape[1],
                                                        weights=[self.word_vectors],
                                                        input_length=self.max_size,
                                                        )

            # Add embedding layer as first layer in model
            model.add(embedding_layer)

            # The embedding layer needs to be flattened to fit into an MLP
            model.add(tf.keras.layers.Flatten())

            # One or more dense layers
            for units in [500, 500, 500]:
                add_layer = tf.keras.layers.Dense(units, activation="relu")
                model.add(add_layer)

            # Drop out layer, avoid over-fitting
            dropout_layer = tf.keras.layers.Dropout(0.2)
            model.add(dropout_layer)

            # Output layer. The first argument is the number of labels
            output_layer = tf.keras.layers.Dense(1, activation="sigmoid")
            model.add(output_layer)

            # Compile model
            model.compile(optimizer="adam",
                          loss=tf.keras.losses.BinaryCrossentropy(),
                          metrics=["accuracy"]
                          )

        # Now, begin or resume training
        model.fit(x=x_train,
                  y=y_train,
                  validation_data=(x_test, y_test),
                  epochs=25,
                  use_multiprocessing=True,
                  )

        # Evaluate on held-out data; TensorFlow returns a sigmoid function, not classes
        y_predict = model.predict(x_test)
        y_predict = (y_predict[:, 0] > 0.5).astype(np.int32)

        # Turn classes into string labels
        y_predict = labeler.inverse_transform(y_predict)
        y_test = labeler.inverse_transform(y_test)

        # Get evaluation report
        report = classification_report(y_true=y_test, y_pred=y_predict)
        print(report)

        return model

    # ---------------------------------------------------------------------
    # Build wordclouds and choose what features to use
    # ---------------------------------------------------------------------
    def wordclouds(self, df, stage=0, features="frequency", name=None, stopwords=None):

        # If only using frequency, use a pure Python method
        if features == "frequency":
            vocab = defaultdict(int)

            for line in self.read(df):
                line = self.clean_wordclouds(line, stage=stage)
                for word in line:
                    vocab[word] += 1

        # If using TF-IDF, use pre-fit vectorizer
        elif features == "tfidf":
            x = self.tfidf_vectorizer.transform((" ".join(df.loc[:, "Text"].values),))

            # Make usable for the wordcloud package
            vocab = x.todense()
            columns = [k for k, v in sorted(self.tfidf_vectorizer.vocabulary_.items(), key=lambda item: item[1])]
            vocab = pd.DataFrame(vocab, columns=columns).T
            vocab = vocab.to_dict()
            vocab = vocab[0]

        # Remove defined stopwords
        if stopwords != None:
            is_stop = lambda x: x not in stopwords
            vocab = ct.keyfilter(is_stop, vocab)

        # Initialize wordcloud package
        wordcloud = WordCloud(width=1200,
                              height=1200,
                              max_font_size=75,
                              min_font_size=10,
                              max_words=200,
                              background_color="white",
                              relative_scaling=0.65,
                              normalize_plurals=False,
                              include_numbers=True,
                              )

        # Pass pre-made frequencies to wordcloud, allowing for TF-IDF
        wordcloud.generate_from_frequencies(frequencies=vocab)

        # Prepare plot with title, etc
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=0.95, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.title(label="Cleaning: " + str(stage), fontdict=None, loc="center", pad=None)

        # Save to disk if a filename is given, otherwise just display it
        if name != None:
            plt.savefig(name, format="tif", dpi=300, pad_inches=0)
            plt.close("all")
        else:
            plt.show()

    # ---------------------------------------------------------------------
    # Use K-Means clustering
    # ---------------------------------------------------------------------
    def cluster(self, x, y="Missing", k=None, ari=True):

        # If necessary, set k to the number of unique labels
        if k == None:
            try:
                k = len(list(set(y)))
            except:
                k = 10
            print("Using k = " + str(k))

        # Initiate KMeans clustering
        cluster = KMeans(
            n_clusters=k,
            init="k-means++",
            n_init=10,
            max_iter=1000,
            tol=0.0001,
            copy_x=False,
            algorithm="full"
        )

        # Get cluster assignments
        clustering = cluster.fit_predict(X=x)

        # Set a null y if necessary
        try:
            print(y.shape)
        except:
            if y == "Missing":
                y = [0 for x in range(len(x))]

        # Make a DataFrame showing the label and the cluster assignment
        cluster_df = pd.DataFrame([y, clustering]).T
        cluster_df.columns = ["Label", "Cluster"]

        if ari == True:
            ari = adjusted_rand_score(cluster_df.loc[:, "Label"].values, cluster_df.loc[:, "Cluster"].values)
            return ari, cluster_df

        else:
            return cluster_df

    # ---------------------------------------------------------------------
    # Manipulate linguistic distance using a KDTree
    # ---------------------------------------------------------------------
    def linguistic_distance(self, x, y, sample=1, n=1):

        # Get the vector that represents our sample
        x_sample = x[sample]

        # Make sure we're using a dense matrix
        if isspmatrix(x_sample):
            x_sample = x_sample.todense()

        # We get each distance as we go
        holder = []

        # Compare each vector with the sample
        for i in range(x.shape[0]):
            if i != sample:
                x_test = x[i]

                # Make sure we're using a dense matrix
                if isspmatrix(x_test):
                    x_test = x_test.todense()

                # Calculate distance
                distance = euclidean(x_sample, x_test)

                # Add index and distance
                holder.append([i, distance])

        # Make a dataframe with all distances and sort, smallest to largest
        distance_df = pd.DataFrame(holder, columns=["Index", "Distance"])
        distance_df.sort_values(by="Distance", axis=0, ascending=True, inplace=True)

        # Reduce to desired number of comparisons
        distance_df = distance_df.head(n)

        # Get the labels for the sample and the closest document
        y_sample = y[sample]
        y_closest = [y[x] for x in distance_df.loc[:, "Index"].values]

        return y_sample, y_closest

    # ---------------------------------------------------------------------
    # Learn a word2vec embeddings from input data using gensim
    # ---------------------------------------------------------------------
    def train_word2vec(self, df, min_count=None):

        # If no min_count, find one
        if min_count == None:
            min_count = self.get_min_count(df)

        # If we haven't learned phrases yet, do that now
        # fit_phrases(self, df, min_count, non_eng = False

        # Learn the word embeddings
        embeddings = Word2Vec(
            sentences=self.read_clean(df, tag=True),
            size=100,
            sg=0,
            window=5,
            min_count=min_count,
            workers=10
        )

        # Keep just the keyed vectors
        print("Finished training")
        word_vectors = embeddings.wv
        word_vectors = word_vectors.syn0
        vocab = embeddings.wv.vocab
        print(word_vectors.shape)

        # Save to class
        self.word_vectors = word_vectors
        self.word_vectors_vocab = vocab

    # ---------------------------------------------------------------------
    # Learn an LDA topic model from input data using gensim
    # ---------------------------------------------------------------------
    def train_lda(self, df, n_topics, min_count=None):

        # If no min_count, find one
        if min_count == None:
            min_count = self.get_min_count(df)

        # Get gensim dictionary, remove function words and infrequent words
        common_dictionary = Dictionary(self.read_clean(df))
        common_dictionary.filter_extremes(no_below=min_count)
        remove_ids = [common_dictionary.token2id[x] for x in self.function_words_single if
                      x in common_dictionary.token2id]

        # Filter out words we don't want
        common_dictionary.filter_tokens(bad_ids=remove_ids)
        common_corpus = [common_dictionary.doc2bow(text) for text in self.read_clean(df)]

        # Train LDA
        lda = LdaModel(common_corpus, num_topics=n_topics)

        # Save to class
        self.lda = lda
        self.lda_dictionary = common_dictionary
        print("Done learning LDA model")

    # ---------------------------------------------------------------------
    # Get a fixed minimum frequency threshold based on the size of the current data set
    # ---------------------------------------------------------------------
    def use_lda(self, df, labels):

        # Get the gensim representation
        corpus = [self.lda_dictionary.doc2bow(text) for text in self.read_clean(df)]

        # Get labels
        y = df.loc[:, labels].values

        # For storing topic results
        holder = []

        # Process each sample
        for i in range(len(corpus)):
            vector = self.lda[corpus[i]]
            label = y[i]
            main = 0.0
            main_index = 0

            # Find most relevant topic
            for cluster, val in vector:
                if val > main:
                    main_index = cluster
                    main = val

            holder.append([i, label, main_index])

        topic_df = pd.DataFrame(holder, columns=["Index", "Class", "Topic"])
        return topic_df

    # ---------------------------------------------------------------------
    # Get a fixed minimum frequency threshold based on the size of the current data set
    # ---------------------------------------------------------------------
    def get_min_count(self, df):

        if len(df) < 10000:
            min = 5
        else:
            min = int(len(df) / 10000)
        return max(min, 5)

    # ---------------------------------------------------------------------
    # Print just one text from a data set
    # ---------------------------------------------------------------------
    def print_sample(self, df):
        line = df.sample().loc[:, "Text"].values
        print(line)
        return line[0]

    # ---------------------------------------------------------------------
    # Print an inventory of labels counts, and return it as a dictionary
    # ---------------------------------------------------------------------
    def print_labels(self, df, labels):
        freqs = ct.frequencies(df.loc[:, labels])
        for label in freqs:
            print(label, freqs[label])
        return freqs

    # ---------------------------------------------------------------------
    # Transform a sparse vector into a series with word labels
    # ---------------------------------------------------------------------
    def print_vector(self, vector, vectorizer):
        columns = [k for k, v in sorted(vectorizer.vocabulary_.items(), key=lambda item: item[1])]
        vector = pd.DataFrame(vector.todense()[0], columns=columns).T
        return vector

    # ---------------------------------------------------------------------
    # Transform a sparse vector into a series with word labels
    # ---------------------------------------------------------------------
    def unmasking(self, df, labels, features):

        # Split into train/test
        train_df, test_df = train_test_split(df, test_size=0.10)

        # Get features
        train_x, vocab_size = self.get_features(train_df, features=features)
        test_x, vocab_size = self.get_features(test_df, features=features)

        # Make dense feature vectors
        train_x = pd.DataFrame(train_x.todense())
        test_x = pd.DataFrame(test_x.todense())
        print(len(train_x.columns))

        # Iterate over 100 rounds of feature pruning
        for i in range(0, 100):

            # Initialize the classifier
            cls = LinearSVC(
                penalty="l2",
                loss="squared_hinge",
                dual=True,
                tol=0.0001,
                C=1.0,
                multi_class="ovr",
                fit_intercept=True,
                intercept_scaling=1,
                max_iter=200000
            )

            # Train and save classifier
            cls.fit(X=train_x, y=train_df.loc[:, labels].values)

            # Evaluate on test data
            predictions = cls.predict(test_x)
            report = classification_report(y_true=test_df.loc[:, labels].values, y_pred=predictions)
            print(report)

            # The features to drop
            to_drop = []

            # Get most predictive features
            weights = pd.DataFrame(cls.coef_)

            # Look for highest feature for each class
            for index, row in weights.iterrows():
                max_index = row.idxmax()
                max_index = train_x.columns[max_index]
                to_drop.append(max_index)

            # Now remove features and start again
            train_x.drop(columns=to_drop, inplace=True)
            test_x.drop(columns=to_drop, inplace=True)
            print(len(train_x.columns))