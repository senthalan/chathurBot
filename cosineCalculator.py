import re, math
from collections import Counter
from difflib import SequenceMatcher

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x ] **2 for x in vec1.keys()])
    sum2 = sum([vec2[x ] **2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

if __name__ == "__main__":
    v1=text_to_vector("http://aaa.lk")
    v2=text_to_vector("http://aab.lk")
    print SequenceMatcher(None,'HTC Desire 326G Dual','HTC Desire 326G').ratio()