import re
import sys

if __name__ == "__main__":
    total = 0
    corr = 0
    unreg_total = 0
    unreg_corr = 0

    with open("./output/result.txt", 'r')as r, open("./data/for_eval_199806#part.txt")as e, open("./output/score.txt", 'w')as s:
        for line in e:
            linee = line.strip()
            if not linee: continue

            while True:
                liner = r.readline().strip()
                if liner: break

            linee = linee.split()
            liner = liner.split()

            err = False

            if len(linee) != len(liner):
                print('err!')
                continue
            else:
                total += len(linee)
                for i in range(len(linee)):
                    is_unreg = False
                    if liner[i][-1] == '?':
                        is_unreg = True
                        unreg_total += 1
                        liner[i] = liner[i][:-1]
                    if linee[i] == liner[i]:
                        corr += 1
                        if is_unreg: unreg_corr += 1
                    else:
                        err = True
                        s.write("not your result: %s ,but: %s \n" % (liner[i], linee[i]))
                if err:
                    s.write(line + '-----------------------\n\n')

        s.write("\n\n[最终结果]\n\n给%s个词做词性标注，对了%s个。\n标注正确率：%s" % (total, corr, corr * 1.0 / total))

        if unreg_total:
            s.write("\n\n%s个词中，未登录词有%s个，对了%s个。\n未登录词出现率：%s\n未登录词标注正确率：%s\n\n" % (
                total, unreg_total, unreg_corr, unreg_total * 1.0 / total, unreg_corr * 1.0 / unreg_total))
