import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Hyphenator {
    private final List<String> patterns = new ArrayList<>();

    public Hyphenator(String dicPath) throws IOException {
        InputStream is = getClass().getClassLoader().getResourceAsStream(dicPath);
        if (is == null) throw new FileNotFoundException(dicPath);

        BufferedReader br = new BufferedReader(new InputStreamReader(is));
        String line;

        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (!line.isEmpty() && !line.startsWith("%")) {
                patterns.add(line);
            }
        }
    }

    public List<Integer> hyphenate(String word) {
        String lower = word.toLowerCase();
        int[] scores = new int[lower.length() + 1];

        for (String p : patterns) {
            String letters = p.replaceAll("[0-9]", "");
            int idx = lower.indexOf(letters);
            if (idx == -1) continue;

            int pos = 0;
            for (char c : p.toCharArray()) {
                if (Character.isDigit(c)) {
                    scores[idx + pos] = Math.max(scores[idx + pos], c - '0');
                } else {
                    pos++;
                }
            }
        }

        List<Integer> result = new ArrayList<>();
        for (int i = 1; i < scores.length - 1; i++) {
            if (scores[i] % 2 == 1) result.add(i);
        }
        return result;
    }
}
