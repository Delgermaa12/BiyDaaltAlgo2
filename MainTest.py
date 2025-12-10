import unittest
from Main import greedy, dp, BilingualHyphenator

class TestTextJustifyAlgorithms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hyph = BilingualHyphenator()
        cls.width = 20

    def test_basic_output_type_mn(self):
        text = "Монгол хэлний үгийг зөв таслана"
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        self.assertIsInstance(greedy_result, list)
        self.assertIsInstance(dp_result, list)

    def test_line_length_not_exceed_width_mn(self):
        text = "Монгол хэл дээр мөрийг зөв таслах ёстой текст"
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        for line in greedy_result:
            self.assertLessEqual(len(line), self.width)

        for line in dp_result:
            self.assertLessEqual(len(line), self.width)

    def test_dp_better_or_equal_mn(self):
        text = "Энэ бол текстийг зөв мөр таслах хоёр өөр алгоритмын харьцуулалт юм."
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        def badness(lines):
            b = 0
            for ln in lines[:-1]:
                b += (self.width - len(ln)) ** 2
            return b

        greedy_score = badness(greedy_result)
        dp_score = badness(dp_result)

        self.assertLessEqual(dp_score, greedy_score)

    def test_hyphenation_cut_mn(self):
        word = "хөгжүүлэх"
        cuts = self.hyph.hyphenate(word)

        self.assertGreater(len(cuts), 0)
        for pos in cuts:
            self.assertTrue(0 < pos < len(word))

    def test_basic_output_type_en(self):
        text = "This is a simple English sentence for testing."
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        self.assertIsInstance(greedy_result, list)
        self.assertIsInstance(dp_result, list)

    def test_line_length_not_exceed_width_en(self):
        text = "Justifying English text should not exceed the given width."
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        for line in greedy_result:
            self.assertLessEqual(len(line), self.width)
        for line in dp_result:
            self.assertLessEqual(len(line), self.width)

    def test_hyphenation_cut_en(self):
        word = "information"
        cuts = self.hyph.hyphenate(word)

        self.assertGreater(len(cuts), 0)
        for pos in cuts:
            self.assertTrue(0 < pos < len(word))

    def test_mn_en_combined(self):
        text = "Монгол үг болон English words энд байна."
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        for line in greedy_result:
            self.assertLessEqual(len(line), self.width)
        for line in dp_result:
            self.assertLessEqual(len(line), self.width)

if __name__ == "__main__":
    unittest.main()
