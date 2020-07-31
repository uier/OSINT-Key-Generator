from pathlib import Path
pwd = Path(__file__).parent.absolute()

CH2CNS={}
with open(f'{pwd}/CNS2CH.txt') as file:
    for line in file.readlines():
        first,last = line.split('\t')
        CH2CNS[last.strip()]=first

CNS2phonetic={}
with open(f'{pwd}/CNS_phonetic.txt') as file:
    for line in file.readlines():
        first,last = line.split('\t')
        CNS2phonetic[first]=last.strip()

CNS2cangjie={}
with open(f'{pwd}/CNS_cangjie.txt') as file:
    for line in file.readlines():
        first,last = line.split('\t')
        CNS2cangjie[first]=last.strip()

phonetic2pinyin={}
with open(f'{pwd}/CNS_pinyin.txt') as file:
    for line in file.readlines():
        first,last = line.split('\t')
        phonetic2pinyin[first]=last.strip()

phonetic2en={}
zhu='ㄅㄆㄇㄈㄉㄊㄋㄌˇㄍㄎㄏˋㄐㄑㄒㄓㄔㄕㄖˊㄗㄘㄙ˙ㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦ'
en='1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,9ol.0p;/-'
for i in range(len(zhu)):
    phonetic2en[zhu[i]]=en[i]


def zhuyin(ch:str)->str:
    return ''.join(map(lambda c: CNS2phonetic[CH2CNS[c]],[c for c in ch]))

def zhuen(ch:str)->str:
    return ''.join(map(lambda c: phonetic2en[c],[c for c in zhuyin(ch)]))
    
def cangjie(ch:str)->str:
    return ''.join(map(lambda c: CNS2cangjie[CH2CNS[c]],[c for c in ch]))

def pinyin(ch:str)->str:
    return ''.join(map(lambda c: phonetic2pinyin[CNS2phonetic[CH2CNS[c]]],[c for c in ch]))
