#!/usr/bin/python
# -*-coding:utf-8
import sys
import math
import pdb
import json
import codecs
import re
import os

trans_dic = {}
emit_dic = {}
num_of_tag = {}
start_dic = {}

word_set = set()
tag_set = set()

line_num = 0

PROB_START = "./model/prob_start.json"
PROB_EMIT = "./model/prob_emit.json"
PROB_TRANS = "./model/prob_trans.json"

WORD_SET = "./model/word_set.txt"
TAG_SET = "./model/tag_set.txt"


# 将参数输出到模型
def output():
    with open(TAG_SET, 'w') as f:
        f.write("\n".join(tag_set))

    with open(WORD_SET, 'w') as f:
        f.write("\n".join(word_set))

    with open(PROB_START, 'w') as start_f, open(PROB_EMIT, 'w')as emit_f, open(PROB_TRANS, 'w')as trans_f:
        for key in start_dic:
            p = start_dic[key] * 1.0 / line_num
            start_dic[key] = math.log(p) if p > 0 else -1000

        start_f.write(json.dumps(start_dic))

        for key in trans_dic:
            for key1 in trans_dic[key]:
                p = trans_dic[key][key1] / num_of_tag[key]
                trans_dic[key][key1] = math.log(p) if p > 0 else -1000

        trans_f.write(json.dumps(trans_dic))

        for key in emit_dic:
            for word in emit_dic[key]:
                p = emit_dic[key][word] / num_of_tag[key]
                emit_dic[key][word] = math.log(p) if p > 0 else -1000

        emit_f.write(json.dumps(emit_dic))


# 直接统计发射概率，初始状态，转移概率
def train(file):
    global line_num

    global word_set
    global tag_set
    global trans_dic
    global emit_dic
    global num_of_tag
    global start_dic

    with open(file) as f:
        for line in f.readlines():

            line = re.sub(r'\[|\][a-z]+', '', line).strip()
            if not line: continue

            line_num += 1

            if line_num % 1000 == 0:
                print(line_num)

            word_tag_list = line.split()

            word_list = []
            tag_list = []




            for i in range(1, len(word_tag_list)):
                arr = word_tag_list[i].split('/')
                if len(arr) >= 2:
                    word_list.append(arr[0])
                    tag_list.append(arr[1])

            for tag in tag_list:
                if tag not in tag_set:
                    tag_set.add(tag)
                    num_of_tag[tag] = 0
                    emit_dic[tag] = {}
                    trans_dic[tag] = {}

            word_set = word_set | set(word_list)

            for i in range(len(tag_list)):
                num_of_tag[tag_list[i]] += 1

                if i == 0:

                    if tag_list[0] in start_dic:
                        start_dic[tag_list[0]] += 1
                    else:
                        start_dic[tag_list[0]] = 1.0
                else:

                    if tag_list[i] in trans_dic[tag_list[i - 1]]:
                        trans_dic[tag_list[i - 1]][tag_list[i]] += 1
                    else:
                        trans_dic[tag_list[i - 1]][tag_list[i]] = 1.0

                    if word_list[i] in emit_dic[tag_list[i]]:
                        emit_dic[tag_list[i]][word_list[i]] += 1
                    else:
                        emit_dic[tag_list[i]][word_list[i]] = 1.0


if __name__ == "__main__":
    path = "./data/1998"

    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isfile(file) and os.path.splitext(file)[1] == '.txt':
            train(file)

    output()
