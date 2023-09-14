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
