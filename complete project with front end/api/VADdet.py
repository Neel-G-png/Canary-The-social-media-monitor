import csv
import statistics

import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()
stops = set(stopwords.words("english"))
#anew = "../lib/vad-nrc.csv"
anew = "files/EnglishShortened.csv"
avg_V = 5.06    # average V from ANEW dict
avg_A = 4.21
avg_D = 5.18
emotion = arousal = dominance = 0
def analyze(input_str,mode):
    s = tokenize.word_tokenize(input_str.lower())
    all_words = []
    found_words = []
    v_list = []  # holds valence scores
    a_list = []  # holds arousal scores
    d_list = []  # holds dominance scores

    words = nltk.pos_tag(s)
    for index,p in enumerate(words):
        w = p[0]
        pos = p[1]
        if w in stops or not w.isalpha():
            continue

        # check for negation in 3 words before current word
        j = index-1
        neg = False
        while j >= 0 and j >= index-3:
            if words[j][0] == 'not' or words[j][0] == 'no' or words[j][0] == 'n\'t':
                neg = True
                break
            j -= 1

        # lemmatize word based on pos
        if pos[0] == 'N' or pos[0] == 'V':
            lemma = lmtzr.lemmatize(w, pos=pos[0].lower())
        else:
            lemma = w

        all_words.append(lemma)
        with open(anew) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Word'].casefold() == lemma.casefold():
                    if neg:
                        found_words.append("neg-"+lemma)
                    else:
                        found_words.append(lemma)
                    v = float(row['valence'])
                    a = float(row['arousal'])
                    d = float(row['dominance'])

                    if neg:
                        # reverse polarity for this word
                        v = 5 - (v - 5)
                        a = 5 - (a - 5)
                        d = 5 - (d - 5)

                    v_list.append(v)
                    a_list.append(a)
                    d_list.append(d)
    if len(found_words) != 0:
        if mode == 'median':
            emotion = statistics.median(v_list)
            arousal = statistics.median(a_list)
            dominance = statistics.median(d_list)
        elif mode == 'mean':
            emotion = statistics.mean(v_list)
            arousal = statistics.mean(a_list)
            dominance = statistics.mean(d_list)
        elif mode == 'mika':
            # calculate valence
            if statistics.mean(v_list) < avg_V:
                emotion = max(v_list) - avg_V
            elif max(v_list) < avg_V:
                emotion = avg_V - min(v_list)
            else:
                emotion = max(v_list) - min(v_list)
            # calculate arousal
            if statistics.mean(a_list) < avg_A:
                arousal = max(a_list) - avg_A
            elif max(a_list) < avg_A:
                arousal = avg_A - min(a_list)
            else:
                arousal = max(a_list) - min(a_list)
            # calculate dominance
            if statistics.mean(d_list) < avg_D:
                dominance = max(d_list) - avg_D
            elif max(d_list) < avg_D:
                dominance = avg_D - min(a_list)
            else:
                dominance = max(d_list) - min(d_list)
        else:
            raise Exception('Unknown mode')
    else:
        emotion = 5.06    # average V from ANEW dict
        arousal = 4.21
        dominance = 5.18
    return emotion,arousal,dominance

if __name__ == "__main__":
    sentence = "Has anyone else grown tired of the trend of self-help/motivational books with swear words in their titles?"
    mode = 'mean'
    v,a,d = analyze(sentence,mode)
    print(f"\nVAL = {v}\tARO = {a}\tDOM = {d}")