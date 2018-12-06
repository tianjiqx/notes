package main

import (
	"fmt"
)

/*
test channel
author: tianjiqx
time: 2018/08/29

*/

//one way channel
func sendData(sendch chan<- int, val int) {

	sendch <- val

}

func digits(number int, ch chan int) {

	for number != 0 {
		digit := number % 10
		ch <- digit
		number = number / 10
	}
	close(ch)
}

func calcS(number int, ch chan int) {

	sum := 0
	ch1 := make(chan int)
	go digits(number, ch1)
	for v := range ch1 {
		sum += v * v
	}
	ch <- sum
}
func calcC(number int, ch chan int) {

	sum := 0
	ch1 := make(chan int)
	go digits(number, ch1)
	for v := range ch1 {

		sum += v * v * v
	}
	ch <- sum

}

func main() {

	fmt.Println("test channel")
	// deadlock  ???
	//ch := make(chan int)
	//ch <- 5
	//due to goroutine not execution, main gorouine already exit
	/*
		go func() {

			i := <-ch
			fmt.Println("from ch get", i)
		}()
	*/
	//cause wait then main function goroutine is wait,can't exection next code !!!
	//i := <-ch
	//fmt.Println("from ch get", i)
	//<-ch
	/*
		//not work
		var wg sync.WaitGroup
		wg.Add(1)
		go func() {

			i := <-ch
			fmt.Println("from ch get", i)

			defer wg.Done()
		}()

		wg.Wait()

	*/

	//first write then read
	done := make(chan bool)
	go func() {
		fmt.Println("hello")
		done <- true
	}()

	<-done
	fmt.Println("main end")

	sendch := make(chan int)

	go sendData(sendch, 34) // swtch one way channel
	fmt.Println("get value from sendch", <-sendch)

	ch2 := make(chan int)
	go func(ch chan int) {

		for i := 0; i < 10; i++ {
			ch2 <- i
		}
		close(ch2)

	}(ch2)

	for {

		v, ok := <-ch2
		if ok {
			fmt.Println("received value ", v)
		} else {
			fmt.Println("channel is closed")
			break
		}

	}
	num := 589
	sch := make(chan int)
	cch := make(chan int)
	go calcS(num, sch)
	go calcC(num, cch)

	s, c := <-sch, <-cch

	fmt.Println("output:", s, c)

}
