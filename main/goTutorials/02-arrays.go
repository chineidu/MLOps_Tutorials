package goTutorials

import "fmt"

// Public function
func ArrayExamples() {
	arrayExample1()
	arrayExample2()
}

// Private functions
func arrayExample1() {
	// For arrays, the size must be stated during init.
	// Method 1
	var fruits [3]string

	// Add values to the slice
	fruits[0] = "orange"
	fruits[1] = "mango"
	fruits[2] = "apple"

	// Print result
	fmt.Printf("Available fruits: %v\n", fruits)
}

func arrayExample2() {
	// For arrays, the size must be stated during init.
	// Method 2
	roles := [5]string{"ML-Engineer"}

	// Add values to the slice
	roles[1] = "Data-Scientist"
	roles[2] = "DevOps-Engineer"
	roles[3] = "HR-Manager"
	roles[4] = "Research-Scientist"

	// Print result
	fmt.Printf("Available roles: %v\n", roles)
}

// You cannot create arrays using `make`
