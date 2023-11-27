/**
 * This class provides a Pancake Sorting algorithm to sort an array of pancakes.
 */
public class PancakeSort {

    // Maximum number of pancakes allowed
    private static final int MAX_PANCAKES = 25;

    /**
     * Sorts an array of pancakes using the Pancake Sorting algorithm.
     *
     * @param pancakes The array of pancakes to be sorted.
     * @throws IllegalArgumentException if the array exceeds the maximum allowed pancakes,
     *         if it contains negative values, or if it contains non-numeric values.
     */
    public static void sort(double[] pancakes) {
        // Check if the number of pancakes exceeds the maximum limit
        if (pancakes.length > MAX_PANCAKES) {
            throw new IllegalArgumentException("Number of pancakes cannot exceed 25.");
        }

        // Validate each pancake
        for (double pancake : pancakes) {
            // Check for negative pancake values
            if (pancake < 0) {
                throw new IllegalArgumentException("Negative pancake values are invalid.");
            }

            // Check for non-numeric values
            if (Double.isNaN(pancake) || Double.isInfinite(pancake)) {
                throw new IllegalArgumentException("Invalid data type. Only numeric values are allowed.");
            }
        }

        // Pancake sorting algorithm
        for (int i = pancakes.length; i > 1; i--) {
            int maxIndex = findMaxIndex(pancakes, i);
            if (maxIndex != i - 1) {
                flip(pancakes, maxIndex);
                flip(pancakes, i - 1);
            }
        }
    }

    /**
     * Finds the index of the maximum element in a sub-array.
     *
     * @param arr The array of pancakes.
     * @param n   The size of the sub-array.
     * @return The index of the maximum element.
     */
    private static int findMaxIndex(double[] arr, int n) {
        // Initialize the index of the maximum element to the first element
        int maxIndex = 0;

        // Iterate through the sub-array to find the maximum element
        for (int i = 0; i < n; i++) {
            // Update maxIndex if a greater element is found
            if (arr[i] > arr[maxIndex]) {
                maxIndex = i;
            }
        }

        // Return the index of the maximum element
        return maxIndex;
    }

    /**
     * Flips the order of elements in the array up to the specified index.
     *
     * @param arr The array of pancakes.
     * @param idx The index to flip until.
     */
    private static void flip(double[] arr, int idx) {
        // Initialize start and end pointers for flipping
        int start = 0;

        // Continue flipping until start pointer reaches the end pointer
        while (start < idx) {
            // Swap elements at start and end positions
            double temp = arr[start];
            arr[start] = arr[idx];
            arr[idx] = temp;

            // Move start pointer forward and end pointer backward
            start++;
            idx--;
        }
    }
}
