import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HyphenatorTest {

    @Test
    void testEnglishHyphenation() throws Exception {
        Hyphenator hy = new Hyphenator("hyph_en_US.dic");
        var cuts = hy.hyphenate("dictionary");

        assertTrue(cuts.size() > 0);
        assertTrue(cuts.contains(4));  // dict-ion-ary гэх мэт
    }

    @Test
    void testMongolianHyphenation() throws Exception {
        Hyphenator hy = new Hyphenator("hyph_mn_MN.dic");
        var cuts = hy.hyphenate("компьютер");

        assertTrue(cuts.size() > 0);
    }
}
