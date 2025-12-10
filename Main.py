import pathlib
import pyphen
import math
import time
import re

class BilingualHyphenator:
    def __init__(self):
        current_dir = pathlib.Path(__file__).parent
        mn_dic_path = current_dir / "hyph_mn_MN.dic"
        self.mn_dic = pyphen.Pyphen(filename=str(mn_dic_path))
        self.en_dic = pyphen.Pyphen(lang='en_US')

    def hyphenate(self, word):
        if re.match(r'^[a-zA-Z-]+$', word):
            dic = self.en_dic
        else:
            dic = self.mn_dic

        inserted = dic.inserted(word)
        cuts = [i for i, c in enumerate(inserted) if c == "-"]
        return cuts

def justify_line(words, width):
    if len(words) == 1:
        return words[0]

    total_chars = sum(len(w) for w in words)
    spaces_needed = width - total_chars
    gaps = len(words) - 1

    base = spaces_needed // gaps
    extra = spaces_needed % gaps

    line = ""
    for i, w in enumerate(words):
        line += w
        if i < gaps:
            line += " " * (base + (1 if i < extra else 0))

    return line

def greedy(text, width, hyph):
    words = text.split()
    result = []
    line_words = []
    current_len = 0

    for w in words:
        if current_len + len(w) + len(line_words) <= width:
            line_words.append(w)
            current_len += len(w)
        else:
            cuts = hyph.hyphenate(w)
            placed = False

            for c in reversed(cuts):
                left = w[:c] + "-"
                right = w[c:]
                if current_len + len(left) + len(line_words) <= width:
                    line_words.append(left)
                    result.append(justify_line(line_words, width))
                    line_words = [right]
                    current_len = len(right)
                    placed = True
                    break

            if not placed:
                result.append(justify_line(line_words, width))
                line_words = [w]
                current_len = len(w)

    if line_words:
        result.append(justify_line(line_words, width))

    return result

def dp(text, width):
    words = text.split()
    n = len(words)

    def badness(i, j):
        line_words = words[i:j]
        total_chars = sum(len(w) for w in line_words)
        spaces = j - i - 1
        length = total_chars + spaces
        if length > width:
            return math.inf
        return (width - length) ** 2

    dp_arr = [math.inf] * (n + 1)
    nxt = [0] * (n + 1)
    dp_arr[n] = 0

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            cost = badness(i, j)
            if cost == math.inf:
                break
            if dp_arr[j] + cost < dp_arr[i]:
                dp_arr[i] = dp_arr[j] + cost
                nxt[i] = j

    lines = []
    i = 0
    while i < n:
        j = nxt[i]
        lines.append(justify_line(words[i:j], width))
        i = j

    return lines

def compare_and_print_paragraphs(text, width, hy):
    paragraphs = text.split("\n\n")

    all_greedy = []
    all_dp = []

    t1 = time.perf_counter()
    for p in paragraphs:
        if p.strip() == "":
            all_greedy.append("")
            continue
        all_greedy.extend(greedy(p, width, hy))
        all_greedy.append("")
    t2 = time.perf_counter()

    t3 = time.perf_counter()
    for p in paragraphs:
        if p.strip() == "":
            all_dp.append("")
            continue
        all_dp.extend(dp(p, width))
        all_dp.append("")
    t4 = time.perf_counter()

    print(f"\nGreedy: {(t2 - t1) * 1000:.4f} ms")
    print(f"DP: {(t4 - t3) * 1000:.4f} ms")

    print("\n=== GREEDY ===")
    for line in all_greedy:
        print(line)

    print("\n=== DP ===")
    for line in all_dp:
        print(line)

if __name__ == "__main__":
    hy = BilingualHyphenator()

    print("Enter text:")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    text = "\n".join(lines)
    width = int(input("Line width: "))
    compare_and_print_paragraphs(text, width, hy)
