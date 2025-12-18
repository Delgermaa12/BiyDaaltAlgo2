import pathlib
import pyphen
import math
import re

class BilingualHyphenator:
    def __init__(self):
        current_dir = pathlib.Path(__file__).parent
        mn_dic_path = current_dir / "hyph_mn_MN.dic"
        self.mn_dic = pyphen.Pyphen(filename=str(mn_dic_path))
        self.en_dic = pyphen.Pyphen(lang="en_US")

    def hyphenate(self, word):
        if re.match(r'^[a-zA-Z-]+$', word):
            dic = self.en_dic
        else:
            dic = self.mn_dic
        inserted = dic.inserted(word)
        return [i for i, c in enumerate(inserted) if c == "-"]


def justify_line(words, width, last_line=False):
    if last_line or len(words) == 1:
        return " ".join(words)

    total_chars = sum(len(w) for w in words)
    gaps = len(words) - 1
    spaces_needed = width - total_chars

    base = spaces_needed // gaps
    extra = spaces_needed % gaps

    line = ""
    for i, w in enumerate(words):
        line += w
        if i < gaps:
            line += " " * (base + (1 if i < extra else 0))
    return line

def dp(text, width, hy):
    words = text.split()
    n = len(words)

    def badness(ws):
        total = sum(len(w) for w in ws)
        spaces = len(ws) - 1
        length = total + spaces
        if length > width:
            return math.inf
        return (width - length) ** 2

    dp_arr = [math.inf] * (n + 1)
    next_idx = [-1] * (n + 1)
    next_words = [None] * (n + 1)

    dp_arr[n] = 0

    for i in range(n - 1, -1, -1):
        line_words = []
        curr_len = 0

        for j in range(i, n):
            w = words[j]
            add_len = len(w) if not line_words else len(w) + 1

            if curr_len + add_len <= width:
                line_words.append(w)
                curr_len += add_len
                cost = badness(line_words)

                if cost + dp_arr[j + 1] < dp_arr[i]:
                    dp_arr[i] = cost + dp_arr[j + 1]
                    next_idx[i] = j + 1
                    next_words[i] = line_words.copy()
            else:
                # Try hyphenation ONLY here
                for c in reversed(hy.hyphenate(w)):
                    left = w[:c] + "-"
                    right = w[c:]

                    add_len = len(left) if not line_words else len(left) + 1
                    if curr_len + add_len <= width:
                        temp = line_words + [left]
                        cost = badness(temp)

                        if cost + dp_arr[j + 1] < dp_arr[i]:
                            dp_arr[i] = cost + dp_arr[j + 1]
                            next_idx[i] = j + 1
                            next_words[i] = temp.copy()
                        break
                break

    lines = []
    i = 0
    while i < n:
        ws = next_words[i]
        j = next_idx[i]
        last = j == n
        lines.append(justify_line(ws, width, last_line=last))
        i = j

    return lines


def greedy(text, width, hy):
    words = text.split()
    result = []

    line_words = []
    curr_len = 0

    for w in words:
        add_len = len(w) if not line_words else len(w) + 1

        if curr_len + add_len <= width:
            line_words.append(w)
            curr_len += add_len
        else:
            placed = False
            for c in reversed(hy.hyphenate(w)):
                left = w[:c] + "-"
                right = w[c:]

                add_len = len(left) if not line_words else len(left) + 1
                if curr_len + add_len <= width:
                    line_words.append(left)
                    result.append(justify_line(line_words, width))
                    line_words = [right]
                    curr_len = len(right)
                    placed = True
                    break

            if not placed:
                result.append(justify_line(line_words, width))
                line_words = [w]
                curr_len = len(w)

    if line_words:
        result.append(justify_line(line_words, width, last_line=True))

    return result

if __name__ == "__main__":
    hy = BilingualHyphenator()

    while True:
        print("\n-----------------------------")
        print(" 1. GREEDY")
        print(" 2. DP")
        print(" 3. BOTH")
        print(" 4. EXIT")

        choice = input("Your choice: ").strip()

        if choice == "4":
            break

        print("\nEnter text (END to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        text = " ".join(lines)
        width = int(input("Line width: "))

        if choice in ("1", "3"):
            print("\n=== GREEDY ===")
            for l in greedy(text, width, hy):
                print(l)

        if choice in ("2", "3"):
            print("\n=== DP ===")
            for l in dp(text, width, hy):
                print(l)
