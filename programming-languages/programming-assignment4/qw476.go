package main

import (
    "bufio"
    "fmt"
    "os"
)


func main() {

  reader := bufio.NewReader(os.Stdin)

  for {
    line_buf,_ := reader.ReadString('\n')
    fmt.Print(line_buf)
  }

}
