#!/usr/bin/python
#-*- encoding: UTF-8 -*-

from collections import OrderedDict
from multiprocessing import Pool
import sys
import socket
import time

target_host = "140.116.245.151"
target_port = 2001

def seg(sentence):
    # create socket
    # AF_INET 代表使用標準 IPv4 位址或主機名稱
    # SOCK_STREAM 代表這會是一個 TCP client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client 建立連線
    client.connect((target_host, target_port))
    # 傳送資料給 target
    data = "seg@@" + sentence
    client.send(data.encode("utf-8"))
    
    # 回收結果信息
    data = bytes()
    while True:
        request = client.recv(8)
        if request:
            data += request
            begin = time.time()
        else:
            break

    WSResult = []
    response = data

    v = "null"
    n = "null"
    Ne = "null"

    if(response is not None or response != ''):
        response = response.decode('utf-8').split()
        for resp in response:
            resp = resp.strip()
            resp = resp[0:len(resp)-1]
            temp = resp.split('(')
            word = temp[0]
            pos = temp[1]
            if v != "null" and Ne != "null" and pos == 'Nf':
                n = Ne+word
                Ne = "null"
            if pos == 'COMMACATEGORY' or pos == 'EXCLAMATIONCATEGORY' or pos == 'PERIODCATEGORY' or pos == 'QUESTIONCATEGORY' or pos == 'SEMICOLONCATEGORY' or pos == 'PARENTHESISCATEGORY':
                if n != "null":
                    event = v+n
                    v_type.append(event)
                v = "null"
                n = "null"

            if pos == 'Nb':
                n_type.append(word)
            if pos == 'Nd':
                t_type.append(word)
            if pos == 'Nc':
                l_type.append(word)
            if pos == 'Na':
                o_type.append(word)
            
            if pos[0] == 'V':
                if pos == 'VA':
                    v_type.append(word)
                elif pos == 'VC' or pos == 'VJ':
                    v = word

            if pos[0] == 'N' and pos != 'Nf' and pos != 'Ng' and pos != 'Nh':
                if v != "null":
                    n = word
                if pos[1] == 'e':
                    Ne = word

            tmp = word
            file = open('positive.txt',encoding = 'utf-8')
            dic = file.read()
            dic_list = dic.split()
            if tmp in dic_list:
                pos = 'positive'
                pos_type.append(word)
            file = open('negative.txt',encoding = 'utf-8')
            dic = file.read()
            dic_list = dic.split()
            if tmp in dic_list:
                pos = 'negative'
                neg_type.append(word)

            WSResult.append((word,pos))

    return WSResult

n_type = []
v_type = []
t_type = []
l_type = []
o_type = []
pos_type = []
neg_type = []

try:
    f = open('test.txt','r')
    print("目標檔案(text.txt)的斷詞與詞性標記結果：\n")
    sentence = f.read()
    print(seg(sentence))
    f.close()

except IOError:
    sentence = input("請輸入一個中文句子/文章：")
    print("斷詞與詞性標記結果：",seg(sentence),"\n")

print("<人名>\n")
for n_type in n_type:
    print(n_type,end=' ')
print("\n")

print("<時間>\n")
for t_type in t_type:
    print(t_type,end=' ')
print("\n")

print("<地點>\n")
for l_type in l_type:
    print(l_type,end=' ')
print("\n")

print("<物件>\n")
for o_type in o_type:
    print(o_type,end=' ')
print("\n")

print("<事件>\n")
n = 1
for v_type in v_type:
    print(n,v_type,sep='. ')
    n += 1

print("\n<正面>\n")
for pos_type in pos_type:
    print(pos_type,end=' ')
print("\n")

print("<負面>\n")
for neg_type in neg_type:
    print(neg_type,end=' ')
print("\n")
