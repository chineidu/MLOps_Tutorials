package main

import "fmt"

func main() {
	// This is a comment
	// This prints the sentence WITHOUT a new line.
	fmt.Print("Hello World")
	fmt.Println("")
	fmt.Println("This prints the sentence with a new line")

	// Create variables
	// Method 1
	var name string = "Mike"
	// Constant variables can NOT be modified
	const totalTickets uint = 50

	// Create a variable w/o assigning a value to it
	var numTickets uint
	var remainingTickets uint
	var email string

	// Method 2
	firstName := ""
	lastName := ""

	// Printf is used to format a string
	fmt.Printf("Your name is %v.\n", name)
	fmt.Printf("The total number of available tickets are: %v tickets. \n", totalTickets)
	fmt.Printf("The total number of purchased tickets are: %v tickets. \n", numTickets)
	// Check the type of the variable/data
	fmt.Printf("Type of the variable `name`: %T\n", name)

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
	fmt.Printf("Thank you %v %v for purchasing %v tickets. \nYou will receive a confirmation mail at %v.\n\n", firstName, lastName, numTickets, email)
	fmt.Printf("The number of remaining tickets is %v\n", remainingTickets)

}
