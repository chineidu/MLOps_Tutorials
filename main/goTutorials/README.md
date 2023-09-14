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
  - [Control Flow](#control-flow)
    - [`If` Statement](#if-statement)
    - [`If - else` Statement](#if---else-statement)
    - [`If - else if - else` Statement](#if---else-if---else-statement)

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
    firstName := "Michael"

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

# Run the script with all the dependencies
go run file_name1.go file_name2.go

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

    fmt.Println("=====================================================================================")
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
    // Add elements to the slice
    clubs = append(clubs, "Chelsea")
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

## Control Flow

### `If` Statement

```go

```

### `If - else` Statement

```go

```

### `If - else if - else` Statement

```go

```
