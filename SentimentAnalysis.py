#coding=utf-8
import jieba
import collections as coll
import json

def classifyWords(wordDict):
    # (1) 情感词
    fbos = open('source/BosonNLP_sentiment_score.txt', 'r')
    senList = fbos.readlines()
    senDict = coll.defaultdict()
    for s in senList:
        slen = len(s.split(' '))
        if slen > 1:
            senDict[s.split(' ')[0]] = s.split(' ')[1]
        else:
            print s
    # (2) 否定词
    fno = open('source/notDict', 'r')
    notList = fno.readlines()
    # (3) 程度副词
    fdd = open('source/degreeDict', 'r')
    degreeList = fdd.readlines()
    degreeDict = coll.defaultdict()
    for d in degreeList:
        slen = len(d.split(','))
        if slen > 1:
            degreeDict[d.split(',')[0]] = d.split(',')[1]
        else:
            print d

    senWord = coll.defaultdict()
    notWord = coll.defaultdict()
    degreeWord = coll.defaultdict()

    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord

def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    # notloc = -1
    # degreeloc = -1

    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            # print "score = %f" % score
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(senLoc[senloc], senLoc[senloc + 1]):
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
        # i定位至下一个情感词
        if senloc < len(senLoc) - 1:
            i = senLoc[senloc + 1]
    return score

def VPrint(content):
    print json.dumps(content, encoding='utf-8', ensure_ascii=False, indent=1)

#分词
seg_list = jieba.cut("XXX是骗人的，我明明抽中了儿童滑板车，没过几分钟又说很遗憾我没有中奖，太可恶了", cut_all=False)
#print "Default Mode:", "/ ".join(seg_list) # 精确模式

#过滤停用词
stopwords = {}.fromkeys([line.rstrip() for line in open('source/stopwords')])
final = coll.defaultdict()
i = 0
for seg in seg_list:
    seg = seg.encode('utf-8')
    if seg not in stopwords:
            final[seg] = i
            i += 1
print '句子'
VPrint(final)
[a, b, c] = classifyWords(final)

print '情感词'
VPrint(a)
print '否定词'
VPrint(b)
print '程度词'
VPrint(c)

score = scoreSent(a,b,c,final)
print score



