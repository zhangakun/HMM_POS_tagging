#!/usr/bin/python
# -*-coding:utf-8
import os
import sys
import pdb
import json


# 从文件中，加载模型
def load_model():
    global start_p, trans_p, emit_p, tag_set, word_set

    with open("./model/tag_set.txt")as tag_f:
        tag_set = set()
        for line in tag_f:
            tag_set.add(line.strip())

    print("标注集大小：%s" % len(tag_set))

    with open("./model/word_set.txt")as word_f:
        word_set = set()
        for line in word_f:
            word_set.add(line.strip())

    print("词集大小：%s" % len(word_set))

    with open("./model/prob_start.json") as start_f:
        start_p = json.loads(start_f.read())

    with open("./model/prob_trans.json") as trans_f:
        trans_p = json.loads(trans_f.read())

    with open("./model/prob_emit.json") as emit_f:
        emit_p = json.loads(emit_f.read())


unreg_out = []

unreg_line_num = 0

unreg_total=0


# 利用HMM模型，获得标注序列
def viterbi(obs):
    global unreg_out, tag_set, start_p, trans_p, emit_p, unreg_line_num,unreg_total

    V = [{}]
    path = {}

    unreg_ob = []

    unreg = obs[0] not in word_set

    if unreg:
        # print("未登录词！！")
        unreg_ob.append(0)


    for y in tag_set:
        if unreg:
            V[0][y] = start_p.get(y, -10000)
        else:
            V[0][y] = start_p.get(y, -10000) + emit_p[y].get(obs[0], -10000)
        path[y] = [y]

    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        unreg = obs[t] not in word_set

        if unreg:
            # print("未登录词！！")
            unreg_ob.append(t)

        for y in tag_set:
            if unreg:
                choice = [(V[t - 1][y0] + trans_p[y0].get(y, -10000), y0) for y0 in tag_set]
            else:
                choice = [(V[t - 1][y0] + trans_p[y0].get(y, -10000) + emit_p[y].get(obs[t], -10000), y0) for y0 in
                          tag_set]
            (prob, state) = max(choice)

            V[t][y] = prob
            newpath[y] = path[state] + [y]

        path = newpath

    (prob, state) = max([(V[len(obs) - 1][y], y) for y in tag_set])

    if unreg_ob:
        unreg_total+=len(unreg_ob)
        unreg_line_num += 1
        unreg_out.append("(%s)" % unreg_line_num)
        for index in unreg_ob:
            path[state][index] += '?'
            unreg_out.append(obs[index] + "/" + path[state][index])
        unreg_out.append("  ".join(obs))
        unreg_out.append("")

    return (prob, path[state])


# 将标注序列，转换为标注结果输出
def tag(sentence):
    sentence = sentence.split()

    prob, pos_list = viterbi(sentence)

    result = []
    for i in range(len(sentence)):
        result.append(sentence[i] + '/' + pos_list[i])

    return "  ".join(result) + '\n'


if __name__ == "__main__":
    load_model()

    line_num = 0
    with open("./data/for_test_199806#part.txt") as test_f, open("./output/result.txt", 'w') as result_f:
        for line in test_f:
            line = line.strip()
            if not line:
                continue
            line_num += 1
            if line_num % 10 == 0:
                print(line_num)
            result_f.write(tag(line))

    with open("./output/unregister.txt", 'w')as unreg_f:
        unreg_f.write("共找到%s个未登录词，分布于%s个句子中\n\n"%(unreg_total,unreg_line_num))
        unreg_f.write("\n".join(unreg_out))
