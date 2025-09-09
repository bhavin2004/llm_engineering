
import java.text.DecimalFormat;

public class Main {

    public static double calculate(int iterations, int param1, int param2) {
        double result = 1.0;
        for (int i = 1; i <= iterations; i++) {
            // These intermediate calculations fit within int range
            // (100,000,000 * 4) is 400,000,000, well within Integer.MAX_VALUE (~2.1 billion)
            int jSub = i * param1 - param2;
            result -= (1.0 / jSub); // Use 1.0 for double division

            int jAdd = i * param1 + param2;
            result += (1.0 / jAdd); // Use 1.0 for double division
        }
        return result;
    }

    public static void main(String[] args) {
        long startTime = System.nanoTime();

        double calculationResult = calculate(100_000_000, 4, 1) * 4;

        long endTime = System.nanoTime();

        // Format the output to match Python's f-string precision (12 decimal places)
        DecimalFormat resultFormatter = new DecimalFormat("0.000000000000");
        // Format the execution time to match Python's f-string precision (6 decimal places)
        DecimalFormat timeFormatter = new DecimalFormat("0.000000");

        System.out.println("Result: " + resultFormatter.format(calculationResult));
        // Convert nanoseconds to seconds for execution time
        System.out.println("Execution Time: " + timeFormatter.format((endTime - startTime) / 1_000_000_000.0) + " seconds");
    }
}
