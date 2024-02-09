package goTutorials

import "fmt"

// Public functions
func SlicesExamples() {
	createSimpleSlice1()
	createSimpleSlice2()
	createSimpleSlice3()
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
	// Method 2
	languages := []string{"Python", "SQL", "Go"}
	pythonPackages := []string{"NumPy", "Polars", "Sci-kit Learn", "FastAPI", "PyTorch"}

	// Add more values
	languages = append(languages, "Rust")

	// Add an unpacked slice to a slice
	languages = append(languages, pythonPackages...)

	// Print result
	fmt.Printf("Programming languages OR Python packages: %v\n", languages)
}
