package main

/*
test method
authon tianjiqx
time 2018/0826

func (t Type) methodName(parameter list){


}

*/
import "fmt"

type Employee struct {
	Name        string
	Age, Salary float32
}

//method displaySalary() Employee as recivier
//value recivier
func (e Employee) displaySalary() {

	fmt.Printf("%s 's salary is %.2f\n", e.Name, e.Salary)
}

//point recivier
func (e *Employee) displayAge() {

	fmt.Printf("%s 's age is %d\n", e.Name, int(e.Age))
}

//value recivier , not modify outer object
func (e Employee) setName(newName string) {
	e.Name = newName
}

// point recivier effect outer object
func (e *Employee) setAge(newAge int) {
	e.Age = float32(newAge)
}

func main() {

	e1 := Employee{
		Name:   "Tom",
		Salary: 23.445,
		Age:    34.3,
	}
	e1.displaySalary()

	p1 := &e1
	p1.displayAge()
	e1.displayAge()

	p1.displaySalary()

	fmt.Println("name:", e1.Name) // Tom
	e1.setName("Andy")
	fmt.Println("name:", e1.Name) // Tom

	fmt.Println("age:", e1.Age) // 34.3
	p1.setAge(55)
	fmt.Println("age:", e1.Age) // 55

}
