import java.util.*;

public class BilingualHyphenator {
    private Hyphenator mn;
    private Hyphenator en;

    public BilingualHyphenator() throws Exception {
        mn = new Hyphenator("hyph_mn_MN.dic");
        en = new Hyphenator("hyph_en_US.dic");
    }

    public List<Integer> hyphenate(String word) {
        if (word.matches("^[a-zA-Z-]+$"))
            return en.hyphenate(word);
        return mn.hyphenate(word);
    }
}
