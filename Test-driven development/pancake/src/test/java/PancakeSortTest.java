import org.testng.annotations.Test;

import static org.testng.Assert.assertThrows;
import static org.testng.internal.junit.ArrayAsserts.assertArrayEquals;

public class PancakeSortTest {

    // Testing sorting an empty array
    @Test
    public void testSortEmptyArray() {
        double[] pancakes = {};
        double[] expected = {};

        // Sorting the pancakes
        PancakeSort.sort(pancakes);

        // Asserting that the sorted array matches the expected array
        assertArrayEquals(expected, pancakes, 0.0001);
    }

    // Testing sorting a single pancake
    @Test
    public void testSortSinglePancake() {
        double[] pancakes = {5.5};
        double[] expected = {5.5};

        // Sorting the pancakes
        PancakeSort.sort(pancakes);

        // Asserting that the sorted array matches the expected array
        assertArrayEquals(expected, pancakes, 0.0001);
    }

    // Testing sorting an already sorted array
    @Test
    public void testSortAlreadySorted() {
        double[] pancakes = {1.0, 2.5, 3.0, 4.2, 5.7};
        double[] expected = {1.0, 2.5, 3.0, 4.2, 5.7};

        // Sorting the pancakes
        PancakeSort.sort(pancakes);

        // Asserting that the sorted array matches the expected array
        assertArrayEquals(expected, pancakes, 0.0001);
    }

    // Testing sorting a reversed order array
    @Test
    public void testSortReverseOrder() {
        double[] pancakes = {5.7, 4.2, 3.0, 2.5, 1.0};
        double[] expected = {1.0, 2.5, 3.0, 4.2, 5.7};

        // Sorting the pancakes
        PancakeSort.sort(pancakes);

        // Asserting that the sorted array matches the expected array
        assertArrayEquals(expected, pancakes, 0.0001);
    }

    // Testing sorting an array with mixed order
    @Test
    public void testSortMixedOrder() {
        double[] pancakes = {3.2, 1.5, 4.0, 5.7, 2.3};
        double[] expected = {1.5, 2.3, 3.2, 4.0, 5.7};

        // Sorting the pancakes
        PancakeSort.sort(pancakes);

        // Asserting that the sorted array matches the expected array
        assertArrayEquals(expected, pancakes, 0.0001);
    }

    // Testing sorting an array with non-numeric values
    @Test
    public void testSortNonNumericValues() {
        double[] pancakes = {3.2, 1.5, 4.0, Double.NaN, 2.3}; // Contains a non-numeric value (NaN)
        assertThrows(IllegalArgumentException.class, () -> PancakeSort.sort(pancakes));
    }

    // Testing sorting an array with more than 25 pancakes
    @Test
    public void testSortMoreThanMaxPancakes() {
        double[] pancakes = new double[26]; // Creating an array with 26 pancakes
        assertThrows(IllegalArgumentException.class, () -> PancakeSort.sort(pancakes));
    }

    // Testing sorting an array with negative pancake values
    @Test
    public void testSortNegativePancakes() {
        double[] pancakes = {-3.0, -1.5, -4.0, -5.7, -2.3};
        assertThrows(IllegalArgumentException.class, () -> PancakeSort.sort(pancakes));
    }


}
