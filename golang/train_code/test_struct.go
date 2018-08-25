package main

/*
Test  struct useage

*/

import "fmt"

type A struct {
	X int
}

type B struct {
	Y int
	A
}

type C struct {
	Z int
	A
}

type D struct {
	B
	C
	W int
}

func main() {

	fmt.Println("test 2: go  struct useage :")

	var a A
	a.X = 2
	fmt.Println("a.X= ", a.X)
	var b B
	b.X = 3
	b.Y = 3
	fmt.Printf("b.X=%d B.Y=%d\n", b.X, b.Y)

	c := &C{A: A{X: 4}, Z: 4}

	fmt.Printf("c.X=%d C.Z=%d\n", c.X, c.Z)

	var d D
	//	d.X = 2
	d.Y = 3
	d.Z = 4
	d.W = 5
	// unknow X from B or C
	//fmt.Printf("d.X=%d d.Y=%d d.Z=%d d.W=%d\n", d.X, d.Y, d.Z, d.W)

	fmt.Printf("d.X=%d d.Y=%d d.Z=%d d.W=%d\n", d.B.X, d.Y, d.Z, d.W)
	d.B.X = 2
	d.C.X = 3
	// B and C own independ X
	fmt.Printf("d.X=%d d.Y=%d d.Z=%d d.W=%d\n", d.B.X, d.Y, d.Z, d.W)
	fmt.Printf("d.X=%d d.Y=%d d.Z=%d d.W=%d\n", d.C.X, d.Y, d.Z, d.W)

}
