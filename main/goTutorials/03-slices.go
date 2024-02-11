package goTutorials

import "fmt"

// Maps: Similar to lists in Python but with must have uniform datatypes.
// Syntax: make([]dtype, size) `size` is optional.


// Public functions
func SlicesExamples() {
	createSimpleSlice1()
	createSimpleSlice2()
	createSimpleSlice3()
	createSimpleSlice4()
	createSimpleSlice5()
}

// Internal functions
func createSimpleSlice1() {
	// Method 1
	var fruits []string

	// Add values to the slice
	fruits = append(fruits, "orange", "mango", "apple")

	// Print result
	fmt.Printf("Available fruits: %v\n", fruits)
}

func createSimpleSlice2() {
	// Method 2
	languages := []string{"Python", "SQL", "Go"}
	pythonPackages := []string{"NumPy", "Polars", "Sci-kit Learn", "FastAPI"}

	// Add more values
	languages = append(languages, "Rust")

	// Replace values using a given index
	pythonPackages[3] = "PyTorch"

	// Print result
	fmt.Printf("Programming languages: %v\n", languages)
	fmt.Printf("Python packages: %v\n", pythonPackages)
}

func createSimpleSlice3() {
	// Method 3: Using make
	names := make([]string, 0) // make(type, size)

	// Add more values
	names = append(names, "Neidu", "Grace", "Michael", "Ayo")

	// Print result
	fmt.Printf("Names: %v\n", names)
}

func createSimpleSlice4() {
	packages := []string{"Flask", "Pandas", "LangChain"}
	pythonPackages := []string{"NumPy", "Polars", "Sci-kit Learn", "FastAPI", "PyTorch"}

	// Add more values
	packages = append(packages, "Rust")

	// Add an unpacked slice to a slice
	packages = append(packages, pythonPackages...)

	// Print result
	fmt.Printf("Python packages: %v\n", packages)
}

// Helper function for calculating the mean
func CalculateMean(inputArray []float32) float32 {
	var result float32
	var _sum float32

	for _, val := range inputArray {
		_sum += val
	}
	result = _sum / float32(len(inputArray))
	return result
}

func createSimpleSlice5() {
	salary := []float32{500_000, 550_000}

	// Add values
	salary = append(salary, 625_000.55)

	// Calculate mean
	averageSalary := CalculateMean(salary)

	// Print result
	fmt.Printf("Average salary: %v\n", averageSalary)
}
