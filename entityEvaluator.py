import re, math
from collections import Counter
from calculation import calculateFullPrecision

WORD = re.compile(r'\w+')

entitylist=['model','brand','onlinestore','number','amount_of_money']
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

text1 = 'Apple iPhone 6s 16GB'
text2 = '6s'

vector1 = text_to_vector(text1.lower())
vector2 = text_to_vector(text2.lower())
if __name__ == "__main__":
    cosine = get_cosine(vector1, vector2)
    print 'Cosine:', cosine

def eveluateEntity(actualList,estimatedList):
    fullMatch = 0
    partialMatch = 0
    WHFlag = 0
    CMFlag = 0

    partialFlag = 0
    misssmatch = 0
    whmatch = 0
    print 'actual entity list :', actualList
    print 'estimated entity list: ' , estimatedList
    # global fullMatch,partialFlag,partialMatch,WHFlag,CMFlag,misssmatch,whmatch
    for entity in entitylist:

        if entity not in actualList:
            actualList[entity]=[]
        if entity  not in estimatedList:
            estimatedList[entity]=[]

    for entity in entitylist:

        matchEntity=set(actualList[entity]).intersection(estimatedList[entity])
        # print matchEntity

        fullMatch+=len(matchEntity)

        for value in actualList[entity]:

            CMFlag = 0
            for key in entitylist:
                if ((value not in set(estimatedList[key]))):
                    CMFlag+=1
                    # print value,CMFlag

                temp=estimatedList[key]
                for str in temp:

                    if str not in matchEntity:
                        vector1 = text_to_vector(value)
                        vector2 = text_to_vector(str)
                        if get_cosine(vector1,vector2)>0.5:
                            # print value,str
                            partialFlag=1
                            partialMatch+=1
            if CMFlag==len(entitylist):
                misssmatch+=1
        for value in estimatedList[entity]:
            WHFlag = 0

            for key in entitylist:

                if value not in set(actualList[key]):
                    WHFlag+=1
                    # print value, WHFlag
            if WHFlag==len(entitylist):
                whmatch+=1



    print 'fullMatch : ',fullMatch
    print 'partialMatch : ',partialMatch
    print 'complete miss: ', misssmatch-partialMatch
    print 'wrong hit: ', whmatch-partialMatch
    print 'full presicion :' , calculateFullPrecision(fullMatch,partialMatch,whmatch-partialMatch)
    return

