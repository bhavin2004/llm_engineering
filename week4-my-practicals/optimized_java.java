
import java.text.DecimalFormat;

public class Main {
    public static void main(String[] args) {
        long start_time = System.nanoTime();
        double result = calculate(100_000_000, 4, 1) * 4;
        long end_time = System.nanoTime();

        DecimalFormat df = new DecimalFormat("#.############");
        System.out.println("Result: " + df.format(result));
        System.out.printf("Execution Time: %.6f seconds%n", (end_time - start_time) / 1_000_000_000.0);
    }

    public static double calculate(long iterations, double param1, double param2) {
        double result = 1.0;
        for (long i = 1; i <= iterations; i++) {
            double j = i * param1 - param2;
            result -= (1 / j);
            j = i * param1 + param2;
            result += (1 / j);
        }
        return result;
    }
}
