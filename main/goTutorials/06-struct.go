package goTutorials

import (
	"encoding/json"
	"fmt"
	"os"
)

/* Convert this to a struct object
[
  {
    "name": "John Doe",
    "age": 30,
    "occupation": "Software Engineer",
    "hobbies": ["Coding", "Reading", "Gaming"],
    "address": {
      "street": "123 Main Street",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105"
    },
    "phoneNumber": "+15555555555",
    "email": "john.doe@example.com",
    "createdAt": "2023-09-18T10:59:11.000Z"
  },
]
*/

func RunExampleThree() {
	jsonExample()
	loadJSONExample1()
	loadJSONExample2()
}

// "json:"tag" customizes struct-to-JSON mapping."
type Address struct {
	Street  string `json:"street"`
	City    string `json:"city"`
	State   string `json:"state"`
	Zipcode string `json:"zipcode"`
}

type Person struct {
	Name        string   `json:"name"`
	Age         uint     `json:"age"`
	Occupation  string   `json:"occupation"`
	Hobbies     []string `json:"hobbies"`
	Address     Address  `json:"address"`
	PhoneNumber string   `json:"phoneNumber"`
	Email       string   `json:"email"`
	CreatedAt   string   `json:"createdAt"`
}

func jsonExample() {
	person1 := Person{
		Name:       "John Doe",
		Age:        30,
		Occupation: "Software Engineer",
		Hobbies:    []string{"Coding", "Reading", "Gaming"},
		Address: Address{
			Street:  "123 Main Street",
			City:    "San Francisco",
			State:   "CA",
			Zipcode: "94105",
		},
		PhoneNumber: "+15555555555",
		Email:       "john.doe@example.com",
		CreatedAt:   "2023-09-18T10:59:11.000Z",
	}

	person2 := Person{
		Name:       "Jane Doe",
		Age:        25,
		Occupation: "Web Developer",
		Hobbies:    []string{"Traveling", "Hiking", "Cooking"},
		Address: Address{
			Street:  "456 Elm Street",
			City:    "New York",
			State:   "NY",
			Zipcode: "10001",
		},
		PhoneNumber: "+15555555556",
		Email:       "jane.doe@example.com",
		CreatedAt:   "2023-09-18T11:04:11.000Z",
	}

	var people []Person
	people = append(people, person1, person2)
	jsonData, err := json.Marshal(person2)

	// Format the output nicely!
	jsonPeople, _ := json.MarshalIndent(people, "", " ")

	fmt.Printf("Person: %v\n\n", person1)
	fmt.Printf("Person: %v\n\n", person2)
	fmt.Printf("People: %v\n\n", people)
	if err == nil {
		fmt.Printf("ERROR: %v\n\n", err)
	}
	fmt.Printf("Person: %v\n\n", string(jsonData))
	fmt.Printf("Person: %v\n\n", string(jsonPeople))
}

func readJSONFile(filePath string) ([]byte, error) {
	// Read the JSON file
	data, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}
	return data, nil
}

type _Employee struct {
	Name       string  `json:"name"`
	Role       string  `json:"role"`
	Experience float32 `json:"experience"`
	Salary     float32 `json:"salary"`
	Department string  `json:"department"`
}
type Employee struct {
	Data []_Employee `json:"data"`
}

func loadJSONExample1() {
	/* This is used to load a JSON file as a dict.*/

	// This is assumed to be the loaded JSON data
	sampleData := []byte(`{
		"name": "Frank Zayn",
		"role": "MLOps Engineer",
		"experience": 3.0,
		"predicted_salary": 535415.34,
		"department": "Swaks"
	}`)

	// Empty object
	var pData _Employee
	// Parse the JSON
	err := json.Unmarshal(sampleData, &pData)
	if err != nil {
		fmt.Printf("ERROR: %v\n\n", err)
	}
	// It prints out the pData struct
	fmt.Printf("loaded JSON file: %v\n\n", pData)

}

func loadJSONExample2() {
	/* This is used to load a JSON file as a dict.*/
	jsonData, err := readJSONFile("./data/DB.json")
	if err != nil {
		fmt.Printf("ERROR: %v\n\n", err)
	}

	var myData Employee
	err = json.Unmarshal(jsonData, &myData)
	if err != nil {
		fmt.Printf("ERROR: %v\n\n", err)
	}

	//  Access the data
	for _, value := range myData.Data {
		fmt.Printf("Name: %v\n", value.Name)
		fmt.Printf("Role: %v\n", value.Role)
	}

}
