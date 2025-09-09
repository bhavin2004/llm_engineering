
import java.util.Locale;

public class Main {

    public static double calculate(int iterations, int param1Int, int param2Int) {
        double result = 1.0;
        double param1 = param1Int;
        double param2 = param2Int;

        for (int i = 1; i <= iterations; i++) {
            double i_double = (double) i;

            double j_minus = i_double * param1 - param2;
            result -= (1.0 / j_minus);

            double j_plus = i_double * param1 + param2;
            result += (1.0 / j_plus);
        }
        return result;
    }

    public static void main(String[] args) {
        long startTime = System.nanoTime();

        double result = calculate(100_000_000, 4, 1) * 4;

        long endTime = System.nanoTime();

        double executionTimeSeconds = (endTime - startTime) / 1_000_000_000.0;

        System.out.printf(Locale.US, "Result: %.12f%n", result);
        System.out.printf(Locale.US, "Execution Time: %.6f seconds%n", executionTimeSeconds);
    }
}
