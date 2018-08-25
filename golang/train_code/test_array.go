package main

import "fmt"

/**
learning array
author:tianjiqx
time:2018/08/25
*/

//tips: not modify origin array
func modifyArray(num [3]int) { // value copy !

	if len(num) > 0 {
		num[0] = num[0] * 2

	}
	fmt.Println("modidfy : ", num)

}

func main() {

	//arrary statement
	//[n]T

	var a [3]int // inited zero value
	fmt.Println(a)
	//output: [0 0 0]

	//update
	a[1] = 2
	fmt.Println(a)
	//statement and create an array
	b := [3]int{12, 22, 44} //can not use a := due to variable 'a' exist
	fmt.Println(b)

	c := [3]int{23} // ok
	fmt.Println(c)  // [23 0 0]

	d := [...]int{12, 3, 4, 5, 66, 5}
	fmt.Println(d)

	//copy
	c1 := [...]string{"abc", "def"}
	c2 := c1
	c2[0] = "ggg"
	fmt.Println("c1 is :", c1)
	fmt.Println("c2 is :", c2)

	nums := [...]int{12, 44, 56}

	modifyArray(nums)
	fmt.Println("origin array: ", nums)

	//for rang

	sum := 0
	for i, v := range nums {
		sum += v
		fmt.Printf("%d the element of nums is %d\n", i, v)
	}
	fmt.Println("nums sum is :", sum)

	str1 := [3][2]string{
		{"aaa", "bbb"},
		{"ccc", "ddd"},
		{"eee", "fff"}, // ',' is necessary
	}

	fmt.Print("str1:", str1)

	var str2 [2][1]string

	str2[0][0] = "22"
	fmt.Println("str2:", str2)

}
