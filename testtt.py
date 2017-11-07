from entityEvaluator import get_cosine
from entityEvaluator import text_to_vector

# actualList={}
# estimatedList={}

entitylist=['model','brand','onlinestore','number','amount_of_money']



# actualList['person']=['Victor Charles Goldbloom','Alton Goldbloom','Goldbloom','Annie Ballon']
# actualList['Location']=['Montreal','New York']
# actualList['Organization']=['Selwyn House','Lower Canada College','McGill University','Columbia Presbyterian Medical Center']
#
# estimatedList['Location']=['Montreal','New York','Canada']
# estimatedList['Organization']=['Selwyn House','McGill University','Medical Center']
# estimatedList['person']=['Victor Charles Goldbloom','MD','Dr.Goldbloom']

# Actual Entities : price , HTC Desire 326G Dual , http://www.ideabeam.com , http://telescience.lk
#
# Output Entities from NLP Tool : price , HTC Desire 326G , http://telescience.lk , phone , at

# actualList['model']=['HTC Desire 326G Dual']
# actualList['onlineStore']=['http://www.ideabeam.com' , 'http://telescience.lk']
#
#
# estimatedList['model']=['HTC Desire 326G']
# estimatedList['brand']=['price','phone','at']
# estimatedList['onlineStore']=['http://telescience.lk']

# if __name__ == "__main__":
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
        print entity
        matchEntity=set(actualList[entity]).intersection(estimatedList[entity])
        # print matchEntity
        print 'match' ,matchEntity
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
    return
