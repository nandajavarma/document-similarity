from create_vector import vectorize
from lsh import LSH
from parse_document import extract_from_pdf
import sys
import pandas as pd

if __name__ == "__main__":
    csv = sys.argv[1:]
    if csv:
        questions = pd.read_csv(csv)
        question1 = questions(2)
        question2 = questions(3)
        vector_list = [vectorize(question1), vectorize(question2)]
    else:
        print "Usage: python create_vector.py pdf1 [pdf2] [pdf3] .."
        sys.exit()
    print vector_list
    # lsh = LSH(300)
    # [lsh.insert_document(title, vector) for (title, vector) in vector_list]
    # # print lsh.get_similarities()
    # print lsh.closest_match(vector_list[0][0])
    # return vector_list
