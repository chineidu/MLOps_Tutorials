# GoLang Tutorial

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
