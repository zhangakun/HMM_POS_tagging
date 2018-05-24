import re

if __name__ == "__main__":
    count = 0

    with open("./data/199806.txt", 'r')as r, open("./data/for_test_199806#part.txt", 'w')as t, open(
            "./data/for_eval_199806#part.txt", 'w')as s:
        for line in r:
            line = re.sub(r'\[|\][a-z]+', '', line).strip()
            if not line: continue

            count += 1
            # 只取1000句，用作测试数据
            if count > 1000:
                break

            word_tag_list = line.split()[1:]
            s.write("  ".join(word_tag_list) + "\n")

            word_list = []
            for i in list(range(len(word_tag_list))):
                arr = word_tag_list[i].split('/')
                if len(arr) >= 2:
                    word_list.append(arr[0])

            t.write("  ".join(word_list) + "\n")
