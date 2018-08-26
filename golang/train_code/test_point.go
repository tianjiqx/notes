package main

/*
test point
author:tianjiqx
time: 2018/08/26

*/

import "fmt"

func change(val *int) {

	*val *= 2
}

func modify(sls []int) {

	for i := 0; i < len(sls); i++ {

		sls[i] *= 2
	}
}

type Person struct {
	Name string
	Age  int
}

func main() {

	b := 24
	var a *int = &b
	fmt.Println("a=", *a)
	fmt.Println("a address is ", a)

	*a = 44
	//a++ is illegal
	fmt.Println("b =", b) // b is 44 !!
	fmt.Println("*a=", *a)
	var c *string // default zero value is nil

	if c == nil {

		fmt.Println("c is nil")
	}

	d := 4

	fmt.Println("before d=", d)
	change(&d)
	fmt.Println("after d=", d)

	e := [4]int{23, 44, 56, 8}
	//not use *[4]int ,replaced by slice
	modify(e[:]) //get an slice from e
	fmt.Println(e)

	p := &Person{Name: "A", Age: 34} //point a struct

	fmt.Println("name:", p.Name, "age:", p.Age)

}
