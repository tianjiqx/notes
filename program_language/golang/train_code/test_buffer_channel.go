package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

/*
test buffer channel
author:tianjiqx
time:2018/08/28

*/

func test_waitgroup() {

	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {

		wg.Add(1)
		go func(i int, wg *sync.WaitGroup) {

			fmt.Println("start groutine", i)
			time.Sleep(1 * time.Second)
			fmt.Println("end groutine", i)
			wg.Done()
		}(i, &wg) // use pointer

	}
	wg.Wait()
	fmt.Println("all go routine finished")

}

type Job struct {
	id       int
	randomNo int
}
type Result struct {
	job Job
	sum int
}

var (
	jobs    = make(chan Job, 10)
	results = make(chan Result, 10)
)

func dsum(number int) int {
	sum := 0
	no := number
	for no != 0 {
		sum += no % 10
		no /= 10
	}
	time.Sleep(1 * time.Second)
	return sum
}
func worker(wg *sync.WaitGroup) {

	for job := range jobs {
		output := Result{job, dsum(job.randomNo)}
		results <- output

	}
	wg.Done()

}

func createWorkPool(numOfWorkers int) {

	var wg sync.WaitGroup

	for i := 0; i < numOfWorkers; i++ {

		wg.Add(1)
		go worker(&wg)
	}
	wg.Wait()
	close(results)
}

func allocate(jobsNum int) {

	for i := 0; i < jobsNum; i++ {

		randomNo := rand.Intn(999)
		job := Job{i, randomNo}
		jobs <- job
	}
	close(jobs)

}
func reslut(done chan bool) {
	for result := range results {

		fmt.Printf("job id=%d,random no=%d ,sum=%d\n", result.job.id, result.job.randomNo, result.sum)

	}
	done <- true

}

func test_work_pool() {

	startTime := time.Now()
	jobNum := 100
	go allocate(jobNum)
	done := make(chan bool)
	//get result from results(100), wait in goroutine
	go reslut(done)
	//create 10 worker get job from jobs(100)
	workerNum := 10
	createWorkPool(workerNum)
	//wait all result calculation finished
	<-done
	endTime := time.Now()
	spendTime := endTime.Sub(startTime)

	fmt.Println("total spend time", spendTime.Seconds(), "seconds")

}

func main() {

	//ch :=make(chan int,capacity)

	ch := make(chan string, 2)
	//not block,due to buffer space is 2
	ch <- "amy"
	ch <- "bob"
	fmt.Println(<-ch)
	fmt.Println(<-ch)

	test_waitgroup()

	test_work_pool()

}
