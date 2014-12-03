package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)


func main() {

  reader := bufio.NewReader(os.Stdin)

  for {
    line_buf,_ := reader.ReadString('\n')
    line_buf = strings.TrimRight(line_buf, "\n")

    // QUIT
    if line_buf == "QUIT" {
      os.Exit(0)
    }

    fmt.Println(line_buf)

  }

}
