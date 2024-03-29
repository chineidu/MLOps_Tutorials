package goTutorials

import "fmt"

// Public function that can be called from outside the package
// Public functions must start with capital letters
func RunDTypesExample() {
	arrays()
	slices()
	maps()
	structExample()
	anotherStructExample()
}

// Internal function for your data types example
// It starts with lowercase.
func arrays() {
	fmt.Println("\n==== Running examples on `array` datatype ====")
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
	fmt.Println("\n==== Running examples on `slice` datatype ====")
	// Slice (dynamic size)
	// Slice syntax:
	// var varName []dataType
	var clubs []string
	// Create a slice with a dtype of uint containing only the element 87
	ages := []uint{87}
	anotherSlice := make([]string, 2)

	// Add elements to the slice
	clubs = append(clubs, "Chelsea")
	ages = append(ages, 123)

	anotherSlice[0] = "ChatGPT"
	anotherSlice[1] = "Google_Bard"


	fmt.Printf("Clubs: %v\n", clubs)
	fmt.Printf("Ages: %v\n", ages)
	fmt.Printf("anotherSlice: %v\n", anotherSlice)
}

func maps() {
	fmt.Println("\n==== Running examples on `map` datatype ====")
	// Maps: Similar to dicts in Python but with must have uniform datatypes.
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

	// Add all the players
	players = append(players, firstPlayer, secondPlayer)

	fmt.Printf("This is another map [players]: %v\n", players)
	fmt.Printf("Type: %T\n", players)
}

// Struct: Similar to classes in Python


func structExample() {
	fmt.Println("\n==== Running examples on `struct` datatype ====")

	// Create a new instance of the "Player" struct
	var player1 Player
	player1.firstname = "Neidu"
	player1.lastname = "Angelo"
	player1.age = 22

	// Create a new instance of the "Player" struct
	player2 := Player{
		firstname: "John",
		lastname:  "Doe",
		age:       30,
	}

	// Create a new instance of the "Player" struct
	player3 := Player{"Enzo", "Fernandez", 22}

	// Access the values
	namePlayer1 := player1.firstname

	// Print the struct
	fmt.Println(player1, player2, player3)
	fmt.Println((namePlayer1))
}

type Player struct {
	firstname string
	lastname  string
	age       uint
}

func (p *Player) shoot() {
	// This is a method in the Player struct.
	fmt.Printf("%v just took a shot.\n", p.firstname)
}

func (p *Player) dribble() {
	// This is a method in the Player struct.
	fmt.Printf("%v just dribbled past an opposition.\n", p.firstname)
}

func (p *Player) tackle() {
	// This is a method in the Player struct.
	fmt.Printf("%v just tackled an opposition.\n", p.firstname)
}

func anotherStructExample() {
	fmt.Println("\n==== Running examples on `anotherStruct` example ====")

	playerObj := Player{
		firstname: "Nico",
		lastname: "Jackson",
		age: 23,
	}
	playerObj.shoot()
	playerObj.dribble()
	playerObj.tackle()
}
