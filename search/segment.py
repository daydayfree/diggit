# -*- coding: utf-8 -*-

from collections import defaultdict
from mmseg.search import seg_txt
from mmseg.word2 import WORD2

SMALLCHAR = set(
(u'很', u'则', u'该', u'次', u'给', u'又', u'里', u'号', u'着', u'名', u'可', u'更', u'由', u'下', u'至', u'或', u'多', u'大', u'新', u'并', u'让', u'她', u'已', u'向', u'其', u'股', u'点', u'们', u'所', u'会', u'要', u'于', u'前', u'来', u'万', u'比', u'只', u'及', u'地', u'队', u'个', u'不', u'说', u'第', u'元', u'人', u'一', u'分', u'被', u'我', u'这', u'到', u'都', u'从', u'等', u'时', u'以', u'上', u'后', u'就', u'将', u'而', u'还', u'他', u'但', u'对', u'也', u'与', u'为', u'中', u'年', u'月', u'日', u'有', u'和', u'是', u'在', u'了', u'的', )
)


def word_len2(s):
    tmp = [u""]
    for char in s:
        if u"一" <= char <= u"龥": tmp[-1] += char
    result = []
    for word in [word for word in tmp if word]:
        if len(word) <= 2: 
            result.append(word)
        else:
            for i in xrange(len(word) - 1):
                w = word[i : i+2]
                if w in WORD2: result.append(w)
        if 2 < len(word) <= 5:
            result.append(word)
    return result


def seg_title_search(txt):
    result = []
    for word in seg_txt(txt):
        if word.isalnum(): 
            result.append(word.lower())
            continue
        word = word.decode("utf-8", "ignore")
        if len(word) == 1:
            if u"一" <= word <= u"龥": 
                result.append(word)
        else:
            if len(word) <= 2: result.append(word)
            else:
                result.extend(word_len2(word))
            if not word.encode("utf-8").isalnum():
                for char in word: 
                    if char not in result: result.append(char)
    result = [i.encode("utf-8", "ignore") if type(i) is unicode 
              else i for i in result]
    return result


def seg_title_2_dict(txt):
    result = defaultdict(int)
    for word in seg_title_search(txt):
        result[word] += 1
    return result


def seg_keyword_search(txt):
    return  sorted(seg_title_search(txt), key=lambda x:-len(x))


def seg_txt_search(txt):
    result = []
    for word in seg_txt(txt):
        if word.isalnum(): 
            result.append(word.lower())
            continue
        word = word.decode("utf-8", "ignore")
        if len(word) == 1:
            if u"一" <= word <= u"龥" and word not in SMALLCHAR: 
                result.append(word)
        else:
            result.append(word)
    result = [i.encode("utf-8", "ignore") if type(i) is unicode 
              else i for i in result]
    return result
    

def seg_txt_2_dict(txt):
    result = defaultdict(int)
    for word in seg_txt_search(txt):
        result[word] += 1
    return result


if __name__ == "__main__":
    pass
