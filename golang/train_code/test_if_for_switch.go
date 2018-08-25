package main

/*

test if/for switch statement

*/

import (
	"fmt"
)

func main() {

	fmt.Println("test 3 golang if/for/switch statement:")
	//for statement
	for i := 1; i <= 10; i++ {

		fmt.Printf(" %d", i)

	}
	//break
	fmt.Println()
	for i := 1; i <= 10; i++ {

		if i > 5 {

			break // leave loop
		} else {

			fmt.Printf(" %d", i)
		}

	}
	//continue
	fmt.Println()
	for i := 1; i <= 10; i++ {

		if i%2 == 0 {

			continue // leave loop
		}
		fmt.Printf(" %d", i)

	}
	// no one expr in for clause
	fmt.Println()
	i := 0
	for i <= 10 {

		fmt.Printf(" %d", i)
		i += 2
	}

	// no expr in for equal while statement
	fmt.Println()
	for {

		if i > 20 {

			break
		}
		fmt.Printf(" %d", i)

		i += 2

	}

	//switch
	fmt.Println("\nswitch stmt")
	key := 5
	switch key {
	case 1:
		fmt.Println("one")
		//then will break !!! not going
	case 2: //Notice!!! here nothing to do
	case 3:
		fmt.Println("three")
	case 4, 5, 6:
		fmt.Println("4.5.6")
	default:
		fmt.Println("default handle")

	}

}
