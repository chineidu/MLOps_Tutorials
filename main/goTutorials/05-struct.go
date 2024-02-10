package goTutorials

import (
	"fmt"
)

// Public function
func StructExamples() {
	structExample1()
}

type PersonDetails struct {
	firstname  string
	lastname   string
	department string
	role       string
	salary     float32
}

func (p *PersonDetails) overallCompensation() float32{
	var rate float32 = 1.21

	return (p.salary) * rate
}

// Private functions
func structExample1() {

	// Create objects
	employee1 := PersonDetails{
		firstname:  "John",
		lastname:   "Doe",
		department: "Data",
		role:       "Data Engineer",
		salary:     550_000.0,
	}

	// Print results
	fmt.Printf("Employee 1: %v\n", employee1)
	fmt.Printf("firstname: %v, lastname: %v, role: %v\n", employee1.firstname, employee1.lastname, employee1.role)
	fmt.Printf("Overall compensation: %v\n", employee1.overallCompensation())
}
