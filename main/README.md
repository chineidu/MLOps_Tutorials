# GoLang Tutorial

## Table of Content

- [GoLang Tutorial](#golang-tutorial)
  - [Table of Content](#table-of-content)
  - [Initialize Package](#initialize-package)
  - [Create A Simple Program](#create-a-simple-program)
  - [Basics](#basics)
    - [Create Variables](#create-variables)
    - [Run A Go Script](#run-a-go-script)
    - [Ask For User Input](#ask-for-user-input)
  - [Data Types](#data-types)
    - [Arrays](#arrays)
    - [Slices](#slices)
    - [Maps](#maps)
    - [Structs](#structs)
      - [Modelling Data With Structs](#modelling-data-with-structs)
  - [Control Flow](#control-flow)
    - [`If` Statement](#if-statement)
    - [`If - else` Statement](#if---else-statement)
    - [`If - else if - else` Statement](#if---else-if---else-statement)
    - [`Switch` Statement](#switch-statement)
  - [Working With JSON Data](#working-with-json-data)
    - [Convert A Nested Data (JSON) To Struct](#convert-a-nested-data-json-to-struct)

## Initialize Package

```sh
go mod init your_directory_name

# e.g.
go mod init src
```

## Create A Simple Program

```go
package main

import "fmt"

func main(){
    fmt.Print("This prints the sentence WITHOUT a new line.")
    fmt.Println("")
    fmt.Println("This prints the sentence with a new line")
}
```

## Basics

### Create Variables

```go
package main

import "fmt"

func main() {
    // This is a comment

    // Create variables
    // Method 1
    var name string = "Mike"
    // Constant variables can NOT be modified
    const totalTickets uint = 50

    // Create a variable w/o assigning a value to it
    var numTickets uint

    // Method 2
    // Go can infer the data type if you create a variable using this approach.
    firstName := "Michael" // string data type

    // Printf is used to format a string
    fmt.Printf("Your name is %v.\n", name)
    fmt.Printf("Your name is %v.\n", firstName)
    fmt.Printf("The total number of available tickets are: %v tickets. \n", totalTickets)
    fmt.Printf("The total number of purchased tickets are: %v tickets. \n", numTickets)
    // Check the type of the variable/data
    fmt.Printf("Type of the variable `name`: %T\n", name)
}
```

### Run A Go Script

```bash
go run file_name.go

# Run the script with all the dependencies: file1 to fileN
go run file_name1.go file_name2.go [...] file_nameN.go

# Run the script with all the dependencies. [Better approach]
go run .
```

### Ask For User Input

```go
package main

import "fmt"

func main() {
    // This is a comment

    // Create variables
    firstName := ""
    var lastName string
    var email string
    const totalTickets uint = 100
    var numTickets uint
    var remainingTickets uint

    // Ask the user for input
    fmt.Println("Please enter your firstname: ")
    fmt.Scan(&firstName)

    fmt.Println("Please enter your lastName: ")
    fmt.Scan(&lastName)

    fmt.Println("Please enter your email address: ")
    fmt.Scan(&email)

    fmt.Println("Please enter the number of tickets to purchase: ")
    fmt.Scan(&numTickets)

    remainingTickets = totalTickets - numTickets

    fmt.Println("==================================================================================")
    fmt.Printf("Thank you %v %v for purchasing %v tickets.\n", firstName, lastName, numTickets)
    fmt.Printf("You will receive a confirmation mail at %v.\n\n", email)
    fmt.Printf("The number of remaining tickets is %v\n", remainingTickets)
```

## Data Types

### Arrays

```text
- Arrays are fixed-size data structures.
```

```go
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
```

### Slices

```text
- Slices are dynamic-size data structures.
```

```go
func slices() {
    fmt.Println("\n==== Running examples on `slice` datatype")
    // Slice (dynamic size)
    // Slice syntax:
    // var varName []dataType
    var clubs []string
    // Create a slice with a dtype of uint containing only the element 87
    ages := []uint{87}
    anotherSlice := make([]string, 0)
    // Add elements to the slice
    clubs = append(clubs, "Chelsea")
    clubs.append[1] = "Brighton"
    ages = append(ages, 123)
    fmt.Printf("Clubs: %v\n", clubs)
    fmt.Printf("Ages: %v\n", ages)
}
```

### Maps

```go
func maps() {
    fmt.Println("==== Running examples on `map` datatype")
    // Maps: Similar to dict in Python but with uniform datatypes
    // Syntax: make(map[key_dtype]value_dtype, size)
    var myMap = make(map[string]string, 5)

    // Add key-value pairs
    myMap["firstname"] = "Neidu"
    myMap["lastname"] = "Angelo"

    // Access the values
    firstName := myMap["firstname"]

    fmt.Printf("This is the content of the map: %v\n", myMap)
    fmt.Printf("This is the firstName in the map: %v\n", firstName)

    // Slice of maps
    players := make([]map[string]string, 2)

    // Syntax 1
    firstPlayer := make(map[string]string)
    firstPlayer["firstname"] = "Nico"
    firstPlayer["lastname"] = "Jackson"

    // Syntax 2
    secondPlayer := map[string]string{
        "firstname": "Cole",
        "lastname":  "Palmer",
    }

    players = append(players, firstPlayer, secondPlayer)

    fmt.Printf("This is another map [players]: %v\n", players)

}
```

### Structs

```text
The struct data type is a composite data type that allows you to define your own custom data structures. It is similar to a class in other programming languages and provides a way to group related data fields together.

A struct is defined using the `type` keyword followed by the struct name and a list of fields enclosed in curly braces. Each field has a name and a type. Here's an example of a struct definition:
```

```go
type Person struct {
    Name  string
    Age   int
    Email string
}
```

In this example, the `Person` struct has three fields: `Name` of type `string`, `Age` of type `int`, and `Email` of type `string`.

You can create instances of the struct by declaring variables of the struct type and initializing the field values. Here's an example:

```go
person := Person{
    Name:  "John Doe",
    Age:   25,
    Email: "john@example.com",
}
```


You can access the field values using the dot notation. For example, `person.Name` would give you the name "John Doe".

#### Modelling Data With Structs

```python
class Dog:
  def __init__(self, name, breed):
    self.name = name
    self.breed = breed

  def bark(self):
    print(f"{self.name} barks!")

  def run(self):
    print(f"{self.name} runs!")

  def sit(self):
    print(f"{self.name} sits!")


if __name__ == "__main__":
  my_dog = Dog("Lassie", "Border Collie")
  my_dog.bark()
  my_dog.run()
  my_dog.sit()

```

```text
Golang equivalent
-----------------
```

```go
package main

import "fmt"

type Dog struct {
  name string
  breed string
}

func (d *Dog) Bark() {
  fmt.Println(d.name, "barks!")
}

func (d *Dog) Run() {
  fmt.Println(d.name, "runs!")
}

func (d *Dog) Sit() {
  fmt.Println(d.name, "sits!")
}

func main() {
  myDog := Dog{
    name: "Lassie",
    breed: "Border Collie",
  }

  myDog.Bark()
  myDog.Run()
  myDog.Sit()
}

```

```text
Explanation

This code is similar to the Python code, but there are some differences. In Go, the struct keyword is used to define a data structure. The Dog struct has two fields: name and breed. The *Dog pointer type is used to refer to an instance of the Dog struct. i.e. similar to `self` in Python.

The Bark(), Run(), and Sit() methods are defined as methods on the Dog struct. Methods are functions that are associated with a particular type. In this case, the Bark(), Run(), and Sit() methods are associated with the Dog struct.

The main() function is used to run the code when the file is executed as a script. In this case, we create a new instance of the Dog struct called myDog and then call the Bark(), Run(), and Sit() methods on it.
```

## Control Flow

### `If` Statement

```go
gender := "boy"

if gender == "boy" {
    fmt.Println("You're a boy!")
}
```

### `If - else` Statement

```go
gender := "boy"

if gender == "boy" {
    fmt.Println("You're a boy!")
} else{
    fmt.Println("You're NOT a boy!")
}
```

### `If - else if - else` Statement

```go
gender := "boy"

if gender == "boy" {
    fmt.Println("You're a boy!")
} else if gender == "girl" {
    fmt.Println("You're a girl")
} else{
    fmt.Println("You're NOT a boy or a girl!")
```

### `Switch` Statement

```go
day := "Monday"

switch day {
case "Monday":
    fmt.Println("Today is Monday")
case "Tuesday":
  fmt.Println("Today is Tuesday")
case "Wednesday":
  fmt.Println("Today is Wednesday")
case "Thursday":
  fmt.Println("Today is Thursday")
case "Friday":
  fmt.Println("Today is Friday")
case "Saturday":
  fmt.Println("Today is Saturday")
case "Sunday":
  fmt.Println("Today is Sunday")
default: // else
  fmt.Println("Invalid day!")
}

```

## Working With JSON Data

### Convert A Nested Data (JSON) To Struct

```go
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
  // Create a person object
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

  // Return the JSON encoding of person1
  jsonData, err := json.Marshal(person1)

  // Print the data in a formatted way
  fmt.Printf("Person: %v\n\n", string(jsonData))

  // Format the output nicely!
  jsonPeople, _ := json.MarshalIndent(jsonData, "", " ")
  fmt.Printf("Person: %v\n\n", string(jsonPeople))
}
```
