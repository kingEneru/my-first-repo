package main

import (
	"fmt"
	"sync"
	"time"
)

func worker(wg *sync.WaitGroup, number int, results chan<- int) {
	defer wg.Done()
	fmt.Printf("%d * %d = %d\n", number, number, number*number)
	results <- number * number
	time.Sleep(2 * time.Second)
}

func main() {
	var wg sync.WaitGroup
	var results = make(chan int)
	num_list := []int{1, 2, 3}

	for index := range len(num_list) {
		wg.Add(1)
		go worker(&wg, num_list[index], results)
	}
	go func() {
		wg.Wait()
		close(results)
	}()
	for result := range results {
		fmt.Println(result)
	}
}
