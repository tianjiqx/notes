package main

import "fmt"

/*
test interface useage
author: tianjiqx
time:2018/08/25

*/

//interface definition

type Counter interface {
	StatCount() []rune // rune is int32 alias

}

type MyString string
type MyString2 string

// MyString implements Counter
func (ms MyString) StatCount() []rune {

	var vowels []rune
	for _, rune := range ms {

		if rune == 'a' || rune == 'e' || rune == 'i' ||
			rune == 'o' || rune == 'u' {

			vowels = append(vowels, rune)
		}
	}
	return vowels

}

// MyString implements Counter
func (ms MyString2) StatCount() []rune {

	var vowels []rune
	for _, rune := range ms {

		if rune == 'A' || rune == 'E' || rune == 'I' ||
			rune == 'O' || rune == 'U' {

			vowels = append(vowels, rune)
		}
	}
	return vowels

}

//type assert
func assert(i interface{}) {

	v, ok := i.(int)
	if ok {
		fmt.Println("i is int type, value=", v)
	} else {
		//ok is false
		//v is nil
		fmt.Println("i is not int type")
	}

}

//type switch
func CommonPrinter(i interface{}) {
	switch i.(type) {

	case string:
		fmt.Printf("string value:%s\n", i.(string))
	case int:
		fmt.Printf("int value:%d\n", i.(int))
	default:
		fmt.Println("Unknown type")
	}

}

type Describer interface {
	Describe()
}

type Shower interface {
	Show()
}

type Person struct {
	name string
	age  int
}

// point implements recivier
func (p *Person) Describe() {
	fmt.Printf("name:%s age:%d\n", p.name, p.age)
}

// point implements recivier
func (p *Person) Show() {
	fmt.Printf("show info name:%s age:%d\n", p.name, p.age)
}

func main() {

	name := MyString("Sam Anderson")
	var s Counter
	s = name // MySting implements Counter
	fmt.Printf("name:%s inlcude vowels %c\n", name, s.StatCount())

	name2 := MyString2("Sam Anderson")
	s = name2
	fmt.Printf("name:%s inlcude vowels %c\n", name2, s.StatCount())
	/*
		//illegal due to not define point reciver StatCount()
		var ps *Counter
		ps = &name
		ps.StatCount()
	*/
	assert(23)
	assert("sdds")
	CommonPrinter("abcfff")
	CommonPrinter(345)
	CommonPrinter(34.5)

	var d Describer

	person := Person{"Tom", 23}

	// d= a // illegal not define value reciver implements Describe
	d = &person // due to Person implements Describe use point recivier

	d.Describe()
	var shower Shower

	shower = &person
	shower.Show()

	/*
					//illeagl
		      // not use * interface = &implement
					var shower *Shower
					shower=&person
					shower.Show()
	*/

	var sh *Shower = &shower
	// use interface point need more careful
	// var p * Shower
	//due to interface point type is not nil value is nil
	// just is say p != nil is ture !!!
	// however, var p Shower
	// p == nil is ture ,it's more safely
	// p type and value all is nil
	(*sh).Show()
	// illegal  sh is point not is interface can't call Show()
	// Show
	//sh.Show()
	// however, pp is not interface
	var pp *Person = &person
	pp.Show()

}
