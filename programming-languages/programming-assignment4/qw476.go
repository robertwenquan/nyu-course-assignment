package main

import (
    "bufio"
    "fmt"
    "os"
    "io"
    "strings"
)


func main() {

  reader := bufio.NewReader(os.Stdin)

  for {
    line_buf,err := reader.ReadString('\n')
    if err == io.EOF {
      fmt.Println("ERR")
      os.Exit(0)
    }

    line_buf = strings.TrimRight(line_buf, "\n")
    line_buf = strings.Trim(line_buf, " ")

    if strings.Contains(line_buf, "&") {
      fmt.Println(line_buf)
    } else if line_buf == "QUIT" {
      // QUIT
      os.Exit(0)
    } else {
      fmt.Println("ERR")
      os.Exit(1)
    }

  }

}
