package main

import "fmt"

/*
learning slice
author: tianjiqx
time: 20180825

*/

func find(num int, nums ...int) {

	fmt.Printf("type of nums is %T\n", nums)
	found := false
	for i, v := range nums {

		if v == num {

			fmt.Println(num, "found at index", i, "in", nums)
			found = true
			break
		}

	}
	if !found {
		fmt.Println(num, "not found in", nums)

	}

}

func change(s ...string) {

	s[0] = "GO"
	s = append(s, "playgroud")
	fmt.Println(s)

}

func main() {

	//create statement []T

	a := [5]int{3, 4, 5, 6, 7}
	//way 1:
	var b []int = a[1:4] // slice fomm a[1] ... a[3]
	//4-1=3 elements in slice b

	fmt.Println("slice b :", b)
	//way 2:
	c := []int{2, 3, 4, 5} // create an arrary and return a slice

	fmt.Println("slice c:", c)

	for i := range b {
		//i is index ,value is discard
		b[i] *= 2 // in fact,it modiy array

	}

	fmt.Println("silce b:", b)
	fmt.Println("arrary a:", a)

	// length and capacity
	//length= end-start
	//capacity=end'-start
	fmt.Printf("slice b length %d capacity %d\n", len(b), cap(b))

	//make create an arrary and return a slice
	m1 := make([]int, 5, 10)
	fmt.Printf("silice m1 length=%d capacity =%d\n", len(m1), cap(m1))

	pls := [][]string{
		{"c", "c++"},
		{"java"},
		{"Go", "Rust"},
	}
	for _, v1 := range pls {
		// _ discard index of pls
		for i, v2 := range v1 {
			fmt.Printf(" %d:%s", i, v2)

		}
		fmt.Println()
	}

	find(2, 1, 2, 3, 4)
	find(33, 2, 3, 4, 5)
	find(78, 33)
	find(3)

	slice1 := []int{3, 5, 6, 7, 8, 9, 33, 55}
	find(33, slice1...)

	wel := []string{"hello", "world"}
	//pass slice argument, it's ref copy
	change(wel...)
	fmt.Println(wel) //output: Go world
	// due to append()  create a new arrary  and update ref

}
