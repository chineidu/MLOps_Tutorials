// Maps: Similar to dicts in Python but with must have uniform datatypes.
// Syntax: make(map[key_dtype]value_dtype, size) `size` is optional.

package goTutorials

import "fmt"

// Public function
func MapExamples() {
	mapExample1()
	mapExample2()
	mapExample3()
}

// Private functions
func mapExample1() {
	// Method 1
	var phone = make(map[string]string, 2)
	phone["operating_system"] = "Android"
	phone["name"] = "Xiaomi"

	fmt.Printf("Map `[phone]`: %v\n", phone)

}

func mapExample2() {
	// Method 2
	var student = map[string]string{
		"name":   "John Doe",
		"gender": "male",
		"age":    "25",
	}

	fmt.Printf("Name: %v\n", student["name"])

}

func mapExample3() {
	// Method 3
	student := map[string]float32{
		"age":   24.,
		"height": 1.92,
		"weight": 88,
	}

	fmt.Printf("[Student]: %v\n", student)

}
