package goTutorials

import "fmt"

// Public function that can be called from outside the package
// Public functions must start with capital letters
func RunDTypesExample() {
	arrays()
	slices()
	maps()
}

// Internal function for your data types example
func arrays() {
	fmt.Println("\n==== Running examples on `array` datatype")
	// Arrays
	// An empty array that can take a max of [20] string elements
	// Array syntax:
	// var varName [size]dataType
	var studentsArray [20]string // Added string type
	// Add elements to the array
	studentsArray[0] = "Dave"
	studentsArray[1] = "Ben"

	fmt.Printf("StudentArray: %v\n\n", studentsArray)
	fmt.Printf("The total number of students is: %v.\n", len(studentsArray))
	fmt.Printf("The name of the first student is %v.\n", studentsArray[0])
}

func slices() {
	fmt.Println("\n==== Running examples on `slice` datatype")
	// Slice (dynamic size)
	// Slice syntax:
	// var varName []dataType
	var clubs []string
	// Create a slice with a dtype of uint containing only the element 87
	ages := []uint{87}
	// Add elements to the slice
	clubs = append(clubs, "Chelsea")
	ages = append(ages, 123)
	fmt.Printf("Clubs: %v\n", clubs)
	fmt.Printf("Ages: %v\n", ages)
}

func maps() {
	fmt.Println("==== Running examples on `map` datatype")
	// Maps: Similar to dict in Python but with uniform datatypes
	// Syntax: make(map[key_dtype]value_dtype)
	var myMap = make(map[string]string)

	// Add key-value pairs
	myMap["firstname"] = "Neidu"
	myMap["lastname"] = "Angelo"

	// Access the values
	firstName := myMap["firstname"]

	fmt.Printf("This is the content of the map: %v\n", myMap)
	fmt.Printf("This is the firstName in the map: %v\n", firstName)
}
