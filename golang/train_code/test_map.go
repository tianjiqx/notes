package main

import "fmt"

/*
learnning map
author: tianjiqx
time2018/08/25

*/

func main() {

	//create
	m1 := make(map[string]int)

	m1["abc"] = 1
	m1["def"] = 2

	fmt.Println("map m1:", m1)

	m2 := map[string]int{

		"abc": 2,
		"def": 4,
	}

	m2["xyz"] = 6
	fmt.Println("map m2:", m2)

	//find
	value, ok := m2["abc"]

	if ok == true {
		fmt.Println("abc is exsits!", value)
	} else {
		fmt.Println("abc is not exists!")
	}

	//delete
	delete(m2, "abc")
	fmt.Println("deleted abc map m2:", m2)
}
