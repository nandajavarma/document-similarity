from parse_document import extract_from_pdf
import os, sys
import numpy as np

dm_dict = {}
num_dimensions = 300
stopwords = ["", "(", ")", "a", "about", "an", "and", "are", "around", "as", "at", "away", "be", "become", "became",
             "been", "being", "by", "did", "do", "does", "during", "each", "for", "from", "get", "have", "has", "had",
             "he", "her", "his", "how", "i", "if", "in", "is", "it", "its", "made", "make", "many", "most", "not", "of",
             "on", "or", "s", "she", "some", "that", "the", "their", "there", "this", "these", "those", "to", "under",
             "was", "were", "what", "when", "where", "which", "who", "will", "with", "you", "your"]


def load_entropies(entropies_file='utils/ukwac.entropy.txt'):
    entropies_dict = {}
    with open(entropies_file, "r") as entropies:
        for line in entropies:
            word, score = line.split('\t')
            word = word.lower()
            # Must have this cos lower() can match two instances of the same word in the list
            if word.isalpha() and word not in entropies_dict:
                entropies_dict[word] = float(score)
    return entropies_dict


def weight_file(buff):
    entropies_dict = load_entropies()
    word_dict = {}
    words = buff.split()
    for w in words:
        w = w.lower()
        if w in entropies_dict and w not in stopwords:
            if w in word_dict:
                word_dict[w] += 1
            else:
                word_dict[w] = 1
    for k, v in word_dict.items():
        if np.math.log(entropies_dict[k] + 1) > 0:
            word_dict[k] = float(v) / float(np.math.log(entropies_dict[k] + 1))
    return word_dict


def read_dm():
    global dm_dict
    with open("utils/wikiwoods.dm") as f:
        dmlines = f.readlines()

    # Make dictionary with key=row, value=vector
    for l in dmlines:
        items = l.rstrip('\n').split('\t')
        word = items[0]
        vec = np.array([float(i) for i in items[1:]])
        dm_dict[word.split('_')[0]] = vec


def normalise(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def mk_vector(word_dict):
    """ Make vectors from weights """
    vbase = np.zeros(num_dimensions)
    empty_array = vbase
    # Add vectors together
    if len(word_dict) > 0:
        c = 0
        for w in sorted(word_dict, key=word_dict.get, reverse=True):
            if c < 10:
                w_vector = dm_dict.get(w, empty_array)
                if w_vector.any():
                    vbase = vbase + float(word_dict[w]) * w_vector
                    c += 1

        vbase = normalise(vbase)

    # Make string version of document distribution
    doc_dist_str = ""
    for n in vbase:
        doc_dist_str = doc_dist_str + "%.6f" % n + " "

    return doc_dist_str


def vectorize(pdf_list, pdf_name):
    read_dm()
    buff = ""
    line_counter = 0
    print pdf_name
    title = pdf_name.encode('utf-8').lower()
    title = title.split('/')[-1]


    buff = pdf_list[1].decode('utf-8')

    v = weight_file(buff)
    s = mk_vector(v)

    return (title, s)


if __name__ == "__main__":
    pdfs = sys.argv[1:]
    if pdfs:
        vector_list = [vectorize(pdf_list=extract_from_pdf(pdf), pdf_name=pdf) for pdf in pdfs]
        print vector_list
    else:
        print "Usage: python create_vector.py pdf1 [pdf2] [pdf3] .."
        sys.exit()
    # return vector_list
