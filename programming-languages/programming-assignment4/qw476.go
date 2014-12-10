package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"
)

const (
	ILLEGAL = 1

	TYPE
	PRIMITIVE_TYPE
	TYPEVAR
	VARNAME
	FUNCTYPE
	ARGLIST
	LISTTYPE
)

func is_primitive_type(token string) bool {
	if token == "int" || token == "float" || token == "long" || token == "string" {
		return true
	}

	return false
}

func parse_oneline(ch chan string) bool {

	ret, _ := parse_type(ch)
	if ret != true {
		fmt.Println("1111")
		return false
	}

	ret = parse_ampersand(ch)
	if ret != true {
		fmt.Println("2222")
		return false
	}

	ret, _ = parse_type(ch)
	if ret != true {
		fmt.Println("3333")
		return false
	}

	return true
}

func parse_type(ch chan string) (bool, string) {

	token := <-ch

	if is_primitive_type(token) == true {
		fmt.Println("parse primitive")
		return true, token
	}

	if strings.HasPrefix(token, "`") == true {
		fmt.Println("parse type")
		return true, token
	}

	if token == "(" {
		fmt.Println("parse function")
		return parse_function(ch), token
	}

	if token == "[" {
		fmt.Println("parse list")
		return parse_list(ch), token
	}

	return false, token
}

func parse_ampersand(ch chan string) bool {
	token := <-ch
	if token == "&" {
		return true
	}
	return false
}

func parse_function(ch chan string) bool {

	ret := parse_arg_list(ch)
	if ret == false {
		return false
	}

	token := <-ch
	if token != "->" {
		return false
	}

	ret, _ = parse_type(ch)
	return ret
}

func parse_list(ch chan string) bool {

	ret, _ := parse_type(ch)
	if ret == false {
		return false
	}

	token := <-ch
	if token != "]" {
		return false
	}

	return true
}

func parse_arg_list(ch chan string) bool {
	ret, token := parse_type(ch)
	if ret == false {
		if token == ")" {
			return true
		} else {
			return false
		}
	}

	token = <-ch
	if token == ")" {
		return true
	}
	if token != "," {
		return false
	}

	return parse_arg_list(ch)
}

func main() {

	reader := bufio.NewReader(os.Stdin)

	for {
		line_buf, err := reader.ReadString('\n')
		if err == io.EOF {
			fmt.Println("ERR")
			os.Exit(0)
		}

		line_buf = strings.TrimRight(line_buf, "\n")
		line_buf = strings.Trim(line_buf, " ")
		line_buf = strings.Replace(line_buf, " ", "", -1)

		// Handle QUIT
		if line_buf == "QUIT" {
			os.Exit(0)
		}

		type_list := strings.Split(line_buf, "&")
		if len(type_list) != 2 {
			fmt.Println("ERR")
			os.Exit(1)
		}

		scanner := bufio.NewScanner(strings.NewReader(line_buf))

		// customized splitter for our unification rules
		my_split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
			advance_byte, token_byte, err := bufio.ScanBytes(data, atEOF)

			offset := 0

			token_str := string(token_byte)
			if token_str == "[" || token_str == "]" || token_str == "{" || token_str == "}" || token_str == "," || token_str == "(" || token_str == ")" || token_str == "&" {
				return advance_byte, token_byte, err
			}

			// int
			if token_str == "i" {
				primitive_type := "int"
				if strings.HasPrefix(string(data[offset:]), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return advance_byte, token_byte, io.EOF
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// float
			if token_str == "f" {
				primitive_type := "float"
				if strings.HasPrefix(string(data[offset:]), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.ErrNoProgress
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// long
			if token_str == "l" {
				primitive_type := "long"
				if strings.HasPrefix(string(data[offset:]), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.ErrNoProgress
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// string
			if token_str == "s" {
				primitive_type := "string"
				if strings.HasPrefix(string(data[offset:]), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.EOF
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// ->
			if token_str == "-" {
				function_ret_type := "->"
				if strings.HasPrefix(string(data[offset:]), function_ret_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.ErrNoProgress
				}
				return advance_byte + len(function_ret_type) - 1, []byte(function_ret_type), err
			}

			// `<TYPE>
			if token_str == "`" {
				re := regexp.MustCompile("^`[a-zA-Z][a-zA-Z0-9]*")
				type_str := re.FindString(string(data[offset:]))
				return advance_byte + len(type_str) - 1, []byte(type_str), err
			}

			// If the character doesn't fall into any defined category, it's an error
			fmt.Printf("ERR\n")
			os.Exit(3)
			return advance_byte, token_byte, err
		}

		scanner.Split(my_split)

		channel := make(chan string)

		/*
		 * One go routine for accepting STDIN and generate tokens
		 */
		generate_token := func() {
			for scanner.Scan() {
				if err := scanner.Err(); err != nil {
					fmt.Println("ERR")
					os.Exit(3)
				}

				buf_str := scanner.Text()
				channel <- buf_str
			}
		}

		/*
		 * Another go routine for parsing the tokens and generate the parse tree
		 */
		generate_parse_tree := func() {

			for true {
				ret := parse_oneline(channel)
				if ret != true {
					fmt.Println("ERR")
					os.Exit(4)
				}
			}
		}

		go generate_token()
		go generate_parse_tree()

	}
}
