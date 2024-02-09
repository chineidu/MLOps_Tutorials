package goTutorials

import "fmt"

func Example() {
	example1()
}

type Statement struct {
	Id        string  `json:"id"`
	Type      string  `json:"type"`
	Amount    float64 `json:"amount"`
	Narration string  `json:"narration"`
	Date      string  `json:"date"`
	Balance   float64 `json:"balance"`
}

func example1() {
	ex1 := Statement{
		Id:        "1",
		Type:      "Credit",
		Amount:    0,
		Narration: "Opening Balance",
		Date:      "2020-08-10",
		Balance:   0,
	}

	ex2 := Statement{
		Id:        "1",
		Type:      "Credit",
		Amount:    60000,
		Narration: "Payment for abc",
		Date:      "2020-09-05",
		Balance:   60000,
	}
	ex3 := Statement{
		Id:        "1",
		Type:      "Debit",
		Amount:    5000,
		Narration: "Purchase of internet bundle",
		Date:      "2020-09-05",
		Balance:   55000,
	}
	ex4 := Statement{
		Id:        "1",
		Type:      "Debit",
		Amount:    2000,
		Narration: "Purchase of airtime",
		Date:      "2020-08-06",
		Balance:   53000,
	}
	var data = []Statement{}
	data = append(data, ex1, ex2, ex3, ex4)

	var cleanedData = []Statement{}

	for _, _d := range data {
		if _d.Amount != 0 && _d.Balance != 0 {
			cleanedData = append(cleanedData, _d)
		}
	}
	fmt.Printf("data: %v", cleanedData)
}

// Remove Opening balance. i.e. where amount=0 and balance=0
func RemoveOpeningBalance(data []Statement) ([]Statement){
	var cleanedData = []Statement{}

	for _, _d := range data {
		if _d.Amount != 0 && _d.Balance != 0 {
			cleanedData = append(cleanedData, _d)
		}
	}
	return cleanedData
}
