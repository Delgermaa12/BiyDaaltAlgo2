package main.java;

import org.jetbrains.annotations.NotNull;
import java.util.*;
import java.io.*;


public class Main {

    public static String justify(@NotNull List<String> words, int width) {
        if (words.size() == 1) return words.get(0);

        int totalChars = words.stream().mapToInt(String::length).sum();
        int spacesNeeded = width - totalChars;
        if (spacesNeeded < 0) spacesNeeded = 0;  // prevent negative

        int gaps = words.size() - 1;
        int base = spacesNeeded / gaps;
        int extra = spacesNeeded % gaps;

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.size(); i++) {
            sb.append(words.get(i));
            if (i < gaps) sb.append(" ".repeat(base + (i < extra ? 1 : 0)));
        }
        return sb.toString();
    }

    public static List<String> greedy(String text, int width, BilingualHyphenator hy) {
        List<String> lines = new ArrayList<>();
        List<String> cur = new ArrayList<>();
        int curLen = 0;

        for (String w : text.split("\\s+")) {
            if (curLen + w.length() + cur.size() <= width) {
                cur.add(w);
                curLen += w.length();
            } else {
                List<Integer> cuts = hy.hyphenate(w);
                boolean placed = false;

                for (int i = cuts.size() - 1; i >= 0; i--) {
                    int c = cuts.get(i);
                    String left = w.substring(0, c) + "-";
                    String right = w.substring(c);

                    if (curLen + left.length() + cur.size() <= width) {
                        cur.add(left);
                        lines.add(justify(cur, width));
                        cur = new ArrayList<>();
                        cur.add(right);
                        curLen = right.length();
                        placed = true;
                        break;
                    }
                }

                if (!placed) {
                    lines.add(justify(cur, width));
                    cur = new ArrayList<>();
                    cur.add(w);
                    curLen = w.length();
                }
            }
        }

        if (!cur.isEmpty()) lines.add(justify(cur, width));
        return lines;
    }

    public static List<String> dp(String text, int width, BilingualHyphenator hy) {
        String[] words = text.split("\\s+");
        int n = words.length;
        int[] dp = new int[n + 1];
        int[] nextBreak = new int[n + 1];
        String[] nextLine = new String[n + 1];

        dp[n] = 0;

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = Integer.MAX_VALUE;

            List<String> curLine = new ArrayList<>();
            int curLen = 0;

            for (int j = i; j < n; j++) {
                String w = words[j];

                if (curLen + w.length() + curLine.size() <= width) {
                    curLine.add(w);
                    curLen += w.length();
                    int spaces = width - (curLen + curLine.size() - 1);
                    int cost = spaces * spaces + dp[j + 1];

                    if (cost < dp[i]) {
                        dp[i] = cost;
                        nextBreak[i] = j + 1;
                        nextLine[i] = justify(new ArrayList<>(curLine), width);
                    }
                } else {
                    List<Integer> cuts = hy.hyphenate(w);
                    boolean placed = false;
                    for (int k = cuts.size() - 1; k >= 0; k--) {
                        int c = cuts.get(k);
                        String left = w.substring(0, c) + "-";
                        String right = w.substring(c);
                        if (curLen + left.length() + curLine.size() <= width) {
                            curLine.add(left);
                            int spaces = width - (curLen + left.length() + curLine.size() - 1);
                            int cost = spaces * spaces + dp[j + 1];
                            if (cost < dp[i]) {
                                dp[i] = cost;
                                nextBreak[i] = j + 1;
                                nextLine[i] = justify(new ArrayList<>(curLine), width);
                            }
                            words[j] = right;
                            placed = true;
                            break;
                        }
                    }
                    if (!placed) break;
                    break;
                }
            }
        }

        List<String> lines = new ArrayList<>();
        int idx = 0;
        while (idx < n) {
            lines.add(nextLine[idx]);
            idx = nextBreak[idx];
        }

        return lines;
    }

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        BilingualHyphenator hy = new BilingualHyphenator();

        System.out.println("Enter text (END to stop):");
        StringBuilder sb = new StringBuilder();
        while (true) {
            String line = sc.nextLine();
            if (line.equals("END")) break;
            sb.append(line).append("\n");
        }

        System.out.print("Line width: ");
        int width = sc.nextInt();

        System.out.println("\n=== Greedy result ===");
        List<String> greedyResult = greedy(sb.toString(), width, hy);
        greedyResult.forEach(System.out::println);

        System.out.println("\n=== DP result ===");
        List<String> dpResult = dp(sb.toString(), width, hy);
        dpResult.forEach(System.out::println);
    }
}
