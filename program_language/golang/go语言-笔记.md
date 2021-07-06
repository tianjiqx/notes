# go语言-笔记

## 结构体

结构体是一种聚合的数据类型，是由零个或多个任意类型的值聚合成的实体  。

```go
type Employee struct {
ID int
Name string
Address string
DoB time.Time
Position string
Salary int
ManagerID int
}
// 访问
// 1. 直接点访问成员
dilbert.Salary -= 5000
// 2. 指针访问
position := &dilbert.Position
*position = "Senior " + *position

// 指针访问结构体
var employeeOfTheMonth *Employee = &dilbert
employeeOfTheMonth.Position += " (proactive team player)"

// 字面值
type Point struct{ X, Y int }
p := Point{1, 2}

```



## 函数

```go
// 函数声明包括函数名、形式参数列表、返回值列表（可省略） 以及函数体
func name(parameter-list) (result-list) {
body
}

func hypot(x, y float64) float64 {
return math.Sqrt(x*x + y*y)
} f
mt.Println(hypot(3,4)) // "5"


// 形参类型简写
func f(i, j, k int, s, t string) { /* ... */ }
// <=> 等价
func f(i int, j int, k int, s string, t string) { /* ... */ }

```

defer函数：defer语句中的函数会在return语句更新返回值变量后再执行。



## 方法

在函数声明时，在其名字之前放上一个变量，即是一个方法 。

这个附加的参数会将该函数附加到这种类型上，即相当于为这种类型定义了一个独占的方法。  

```go
type Point struct{ X, Y float64 }
// traditional function
func Distance(p, q Point) float64 {
return math.Hypot(q.X-p.X, q.Y-p.Y)
} /
/ same thing, but as a method of the Point type
func (p Point) Distance(q Point) float64 {
return math.Hypot(q.X-p.X, q.Y-p.Y)
}

//调用
p := Point{1, 2}
q := Point{4, 6}
fmt.Println(Distance(p, q)) // "5", function call
fmt.Println(p.Distance(q)) // "5", method call

```

参数p，方法的接收器(receiver)  。

接收器使用指针，避免大对象值拷贝。

```go
func (p *Point) ScaleBy(factor float64) {
p.X *= factor
p.Y *= factor
}
```

并且，接收器只有这两种：类型(Point)和指向他们的指针(*Point)  

方法的调用：

```go
r := &Point{1, 2}
r.ScaleBy(2)

p := Point{1, 2}
pptr := &p
pptr.ScaleBy(2)

p := Point{1, 2}
(&p).ScaleBy(2)
```





## 接口

对其他类型行为的抽象和概括。接口类型不会和特定的实现细节绑定。

隐式实现——不用想java类，对给定具体的类型时定义，定义需要实现的接口。

```go
// Writer is the interface that wraps the basic Write method.
type Writer interface {
// Write writes len(p) bytes from p to the underlying data stream.
// It returns the number of bytes written from p (0 <= n <= len(p))
// and any error encountered that caused the write to stop early.
// Write must return a non-nil error if it returns n < len(p).
// Write must not modify the slice data, even temporarily.
//
// Implementations must not retain p.
Write(p []byte) (n int, err error)
}

// ByteCounter实现 writer接口
func (c *ByteCounter) Write(p []byte) (int, error) {
*c += ByteCounter(len(p)) // convert int to ByteCounter
return len(p), nil
}
```

接口类型，描述了一系列方法的集合，一个实现了这些方法的具体类型是这个接口类型的
实例。  

```go
type Reader interface {
Read(p []byte) (n int, err error)
} t
ype Closer interface {
Close() error
}

// 接口内嵌
type ReadWriter interface {
Reader
Writer
}
```



## REF

- Go语言圣经The Go Programming Language (Alan A.A. Donovan)

