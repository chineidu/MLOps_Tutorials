package goTutorials

import (
	"encoding/json"
	"fmt"
)

// Public function
func StructExamples() {
	structExample1()
	structExample2()
	structExample3()
}

type PersonDetails struct {
	firstname  string
	lastname   string
	department string
	role       string
	salary     float32
}

func (p *PersonDetails) overallCompensation() float32 {
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

// Create JSON data. structs with JSON tags
type AddressJSON struct {
	Street  string `json:"street"`
	City    string `json:"city"`
	State   string `json:"state"`
	Zipcode string `json:"zipcode"`
}

// Create JSON data. structs with JSON tags
type PersonJSON struct {
	Firstname  string  `json:"firstname"`
	Lastname   string  `json:"lasttname"`
	Department string  `json:"department"`
	Role       string  `json:"role"`
	Salary     float32 `json:"salary"`
	Address    AddressJSON
}

func structExample2() string {
	employee1 := PersonJSON{
		Firstname:  "David",
		Lastname:   "Stings",
		Department: "Engineering",
		Role:       "QA Engineer",
		Salary:     345_000.0,
		Address: AddressJSON{
			Street:  "abc boulevard",
			City:    "Fort Worth",
			State:   "Texas",
			Zipcode: "76177",
		},
	}
	jsonData, _ := json.MarshalIndent(employee1, "", "  ")

	fmt.Printf("[INFO]: Showing info of employee1: %v\n", string(jsonData))

	return string(jsonData)
}

func structExample3() {
	var employeesList []PersonJSON

	emp1 := PersonJSON{
		Firstname:  "Samuel",
		Lastname:   "Aderopo",
		Department: "Products",
		Role:       "Senior Products Manager",
		Address: AddressJSON{
			Street:  "12, Ozumba Mbadiwe",
			City:    "Lagos",
			State:   "Lagos",
			Zipcode: "101241",
		},
	}
	emp2 := PersonJSON{
		Firstname:  "Chioma",
		Lastname:   "Okafor",
		Department: "Sales",
		Role:       "Head of Sales",
		Address: AddressJSON{
			Street:  "5a Admiral way",
			City:    "Ikeja",
			State:   "Lagos",
			Zipcode: "100001",
		},
	}
	employeesList = append(employeesList, emp1, emp2)

	fmt.Println("\tEmployees")
	fmt.Println("\t=========")
	for _id, emp := range employeesList {
		fmt.Printf("Employee id: %v Fullname: %v %v\n", _id+1, emp.Firstname, emp.Lastname)
	}
}
