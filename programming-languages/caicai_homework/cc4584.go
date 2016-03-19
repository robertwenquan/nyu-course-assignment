package main

import (
  "bufio"
  "os"
  "fmt"
  "strings"
)

var (
  inputReader *bufio.Reader
  input string
  err error 
  strList []string
  left []string
  right []string
  LHS string
  RHS string
  m map[string]string = make(map[string]string)
)

func main(){
  inputReader = bufio.NewReader(os.Stdin)

  for {
    /* Get input from Screen */
    input, err = inputReader.ReadString('\n')

    /* Strip last "\n" */
    input = strings.TrimSpace(input)

    /* Split at "&" */
    strList = strings.Split(input, "&")

    /* Deal with "QUIT" */
    if len(strList) == 1 {
      if strings.TrimSpace(strList[0]) == "QUIT" {
        os.Exit(1)
      } else {
        fmt.Printf("%s\n", "ERR")
        os.Exit(1)
      }
    } else if len(strList) != 2 {
      fmt.Printf("%s\n", "ERR")
      os.Exit(1)
    }

    LHS = strings.TrimSpace(strList[0])
    RHS = strings.TrimSpace(strList[1])

    if isValidType(LHS) != true || isValidType(RHS) != true{
      fmt.Printf("%s\n", "ERR")
      os.Exit(1)
    }

    typeTokenizer(LHS, RHS)

    typeUnify()

    ret := outputFormating(LHS)
    for k := 0; k < len(ret);k++ {
      fmt.Printf("%s", ret[k])
    }
    fmt.Printf("\n")
  }
}

func lengthOfTypeVar(s string) int {
  var j int = 1
  for ;j < len(s) ; j++ {
    if !isLetter(s[j]) && !isDigit(s[j]) {
      break
    }
  } 
  return j    
}

func outputFormating(LHS string) []string{
  var elem string
  var ok bool
  var ret []string
  var start int = 0

  for i := 0; i < len(LHS); i++ {
    if LHS[i] == '`' {
      ret = append(ret, LHS[start:i])

      j := i + lengthOfTypeVar(LHS[i:len(LHS)])
      elem, ok = m[LHS[i:j]]

      /* No constrain about this variable type */
      if !ok {
        ret = append(ret, LHS[i:j])
      } else {
        /* This type unify with a Primitive Type */
        if isValidPrimitive(elem){
          ret = append(ret, elem)
        } else {
        /* Chainning Replace */
          var seen map[string]string = make(map[string]string)
          rep := typeRelacing(seen, LHS[i:j])
          for k := 0; k < len(rep); k++ {
            ret = append(ret, rep[k])
          }
        }
      }
      start = j
      i = j
    }
  }

  ret = append(ret, LHS[start:len(LHS)])
  return ret
}

func typeRelacing(seen map[string]string, s string) []string{
  seen[s] = ""
  rep := m[s]
  var ret []string
  var start int = 0
  var j int
  var ok bool

  for i := 0 ; i < len(rep); i++ {
    if rep[i] == '`' {
      ret = append(ret, rep[start:i])
      j = i + lengthOfTypeVar(rep[i: len(rep)])
      _, ok = seen[rep[i:j]]
      if ok {
        fmt.Printf("%s\n", "BOTTOM")
        os.Exit(1)
      } else {
        _, ok = m[rep[i:j]]
        if !ok {
          ret = append(ret, rep[i:j])
        } else {
          getBack := typeRelacing(seen, rep[i:j])
          for k := 0; k < len(getBack); k++ {
            ret = append(ret, getBack[k])
          }
        }
      }
      start = j
      i = j
    }
  }

  ret = append(ret, rep[start:len(rep)])

  return ret
}

func typeUnify(){
  var elem string
  var ok bool

  for i:= 0; i < len(left) ; i++ {
    /* BOTH TYPEVAR */
    if isValidTypeVar(right[i]) {
      /* If they are the same, delete from environment */
      if strings.Compare(left[i], right[i]) == 0 {
        continue
      }

      /* Change it into decending order */
      if strings.Compare(left[i], right[i]) > 0 {
        typeTokenizer(right[i],left[i])
        continue
      }
    }
    /* Check Whether have self cycle */
    if containType(left[i], right[i]) {
      fmt.Printf("%s\n", "BOTTOM")
      os.Exit(1)
    }
    /* Check if it exists */
    elem, ok = m[left[i]]
    if ok == true {
      /* Unify right part */
      typeTokenizer(elem, right[i])
    } else {
    /* Add to MAP */
      m[left[i]] = right[i]
    }
  }
}

func containType(left string, right string) bool{
  for i:= 0; i < len(right);i++ {
    if right[i] == '`' {
      j := i+1
      for ;j < len(right); j++ {
        if isLetter(right[j]) || isDigit(right[j]) {
          continue
        }
        break
      }
      if right[i:j] == left {
        return true
      }
      i = j-1
    }
  }
  return false
}

func typeTokenizer(LHS string, RHS string){
  var (
    i int
    tmp_left string
    tmp_right string
  )

  LHS = strings.TrimSpace(LHS)
  RHS = strings.TrimSpace(RHS) 

  /* Primitive always at the right side
     VarType always at the left side
     FuncType couldn't match ListTyp */

  /* TypeVar can Unify with every Type */
  /* TypeVar always exist on the left side */
  if isValidTypeVar(LHS) {
    left = append(left, LHS)
    right = append(right, RHS)
  } else if isValidTypeVar(RHS) {
    left = append(left, RHS)
    right = append(right, LHS)
  } else if isValidPrimitive(LHS) {

  /* Primitive can only Unify with itself */
    if LHS != RHS {
      fmt.Printf("%s\n", "BOTTOM")
      os.Exit(1)
    }
  } else if isValidFuncType(LHS) {

  /* FuncType can only Unify with FuncType */
    if !isValidFuncType(RHS) {
      fmt.Printf("%s\n", "BOTTOM")
      os.Exit(1)
    }

    /* Split it to Input Part and Output Part */
    i = bracketEnd(LHS)

    tmp_left = strings.TrimSpace(LHS[0 : i+1])
    LHS = strings.TrimSpace(LHS[i+1 : len(LHS)])
    LHS = LHS[2: len(LHS)]

    i = bracketEnd(RHS)

    tmp_right = strings.TrimSpace(RHS[0 : i+1])
    RHS = strings.TrimSpace(RHS[i+1 : len(RHS)])
    RHS = RHS[2:len(RHS)]

    /* Unify output type */
    typeTokenizer(LHS, RHS)

    /* Remove "(" and ")" */
    tmp_left = strings.TrimSpace(tmp_left[1: len(tmp_left)-1])
    tmp_right = strings.TrimSpace(tmp_right[1:len(tmp_right)-1])

    /* ARGLIST is Empty */
    if len(tmp_left) == 0 && len(tmp_right) == 0 {
      return
    }

    /* ARGLIST should not empty */
    if len(tmp_left) == 0 || len(tmp_right) == 0 {
      fmt.Printf("%s\n", "BOTTOM")
      os.Exit(1)
    }

    /* Split ARGLIST Part */
    content_left := argListContent(tmp_left)
    content_right := argListContent(tmp_right)

    /* ARGLIST Should have same number of Type */
    if len(content_left) != len(content_right) {
      fmt.Printf("%s\n", "BOTTOM")
      os.Exit(1)
    }

    /* Each part of ARGLIST should be Unified */
    for j := 0; j < len(content_left) ; j++ {
      typeTokenizer(content_left[j], content_right[j])
    }
  } else if !isValidList(RHS) {
  /* List can be only unified with List */

    fmt.Printf("%s\n", "BOTTOM")
    os.Exit(1)
  } else {
  /* Remove "[" and "]", rest should be Unified */
    LHS = LHS[1: len(LHS)-1]
    RHS = RHS[1: len(RHS)-1]
    typeTokenizer(LHS, RHS)
  }
}

/* Four kinds of Types */
func isValidType(s string) bool {
  s = strings.TrimSpace(s)
  if len(s) == 0 {
    return false 
  }

  switch s[0:1] {
    case "`" : return isValidTypeVar(s)
    case "(" : return isValidFuncType(s)
    case "[" : return isValidList(s)
    default : return isValidPrimitive(s)
  }
}

func isValidTypeVar(s string) bool{
  /* begin with "`" */
  if !strings.HasPrefix(s, "`") {
    return false
  }

  /* At least one letter */
  if len(s) < 2 {
    return false
  }

  /* First character should be letter */
  if !isLetter(s[1]) {
    return false
  }

  /* Rest Character should be letter or digit */
  for i := 2; i < len(s); i++ {
    if !isLetter(s[i]) && !isDigit(s[i]) {
      return false
    }
  }

  return true
}

func isLetter(ch byte) bool{
  if (ch >= 'A') && (ch <= 'Z') {
    return true
  }

  if (ch >= 'a') && (ch <= 'z') {
    return true
  }

  return false
}

func isDigit(ch byte) bool{
  if (ch >= '0') && (ch <= '9') {
    return true
  }

  return false
}

func bracketEnd(s string) int{
  var stack int = 0
  var i int = 0 

  for ; i < len(s); i++ {
    if s[i] == '(' {
      stack++
    }
    if s[i] == ')' {
      stack--
    }
    if stack < 0 {
      return -1
    }
    if stack == 0 {
      break
    }
  }
  return i
}

func isValidFuncType(s string) bool{
  if !strings.HasPrefix(s, "(") {
    return false
  }

  i := bracketEnd(s)
  if i == len(s) || i == -1{
    return false
  }

  /* Character after complete "()" should be "->" */
  right_part := strings.TrimSpace(s[i+1: len(s)])

  if len(right_part) < 2 || right_part[0:2] != "->" {
    return false
  }

  /* String after "->" should be valid TYPE */
  if ! isValidType(right_part[2: len(right_part)]) {
    return false
  }

  s = strings.TrimSpace(s[0:i+1])

  return isValidArgList(s[1:len(s)-1])
}

func isValidList(s string) bool{
  if !strings.HasPrefix(s, "[") {
    return false
  }
  if !strings.HasSuffix(s, "]") {
    return false
  }
  return isValidType(s[1:len(s)-1])
}

func isValidPrimitive(s string) bool{
  if s == "int" || s == "real" || s == "str"{
    return true
  }

  return false
}

/* Split by outside bracket "," */
func argListContent(s string) []string{
  var bracket int = 0
  var start int = 0
  var ret []string
  for i:=0 ; i < len(s); i++ {
    if s[i] == '(' {
      bracket ++
    }
    if s[i] == ')' {
      bracket--
    }
    if s[i] == ',' && bracket == 0 {
      tmp := strings.TrimSpace(s[start:i])
      start = i+1
      ret = append(ret, tmp)
    }
  }
  ret = append(ret, s[start: len(s)])
  return ret
}

func isValidArgList(s string) bool{
  s = strings.TrimSpace(s)
  if len(s) == 0 {
    return true
  }

  /* Get content of ArgList */
  content := argListContent(s)

  /* Every Part of ArgList should be Valid TYPE */
  for i:= 0; i < len(content);i++ {
    if !isValidType(content[i]) {
      return false
    }
  }

  return true
}
