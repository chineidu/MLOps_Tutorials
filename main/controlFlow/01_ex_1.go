package controlFlow

import (
	"fmt"
	"strings"
)

func ControlFlowLogic() {
	whileLoop()
	forEach()
	// ifExample()
	ifElseExample()
}

type Player struct {
	firstName   string
	lastName    string
	nationality string
	age         uint
}

func whileLoop() {
	fmt.Println("\n==== Running examples on `while loop` example ====")
	// This is the equivalent of a while loop.
	idx := 0
	for idx < 10 {
		// Do something
		fmt.Printf("idx: %v\n", idx)
		// idx++
		idx += 1

	}
	fmt.Println("Done!!!")
}

func forEach() {
	fmt.Println("\n==== Running examples on for each loop` example ====")
	// This is the equivalent of a `for` loop in Python.
	player1 := Player{"Nico", "Jackson", "Senegal", 23}
	player2 := Player{"Reheem", "Sterling", "England", 28}
	player3 := Player{"Enzo", "Fernandez", "Argentina", 22}
	player4 := Player{"Moises", "Caicedo", "Ecuador", 22}
	player5 := Player{"Mykhailo", "Murdryk", "Seneegal", 22}

	playerSlice := []Player{player1, player2, player3, player4, player5}

	for _, _player := range playerSlice {
		fmt.Printf("Firstname: %v\n", _player.firstName)
		fmt.Printf("Nationality: %v\n", _player.nationality)
		fmt.Println()
	}
}

func ifExample() {
	fmt.Println("\n==== Running examples on `if` example ====")
	clubNames := []string{"Chelsea", "Brighton", "Man City", "Liverpool"}
	var clubName string
	fmt.Printf("Enter clubName of football club:\n")
	fmt.Scan(&clubName)

	isValid := false
	for _, n := range clubNames {
		if strings.ToLower(clubName) == strings.ToLower(n) {
			isValid = true
			break
		}
	}

	if isValid {
		fmt.Printf("Your football club `%v` has won the UCL before:\n", clubName)
	}

}
func ifElseExample() {
	fmt.Println("\n==== Running examples on `if-Else` example ====")
	clubNames := []string{"Chelsea", "Brighton", "Man City", "Liverpool"}
	var clubName string
	fmt.Printf("Enter clubName of football club:\n")
	fmt.Scan(&clubName)

	isValid := false
	for _, n := range clubNames {
		// if strings.ToLower(clubName) == strings.ToLower(n)
		result := strings.EqualFold(clubName, n)
		if result {
			break
		}
	}

	if isValid {
		fmt.Printf("Your football club `%v` has won the UCL before:\n", clubName)
	} else{
		fmt.Printf("Your football club `%v` has NOT won the UCL before:\n", clubName)
	}

}
