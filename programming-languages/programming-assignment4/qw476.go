package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"
	"time"
)

const (
	ILLEGAL = 1

	TYPE           = 2
	PRIMITIVE_TYPE = 3
	TYPEVAR        = 4
	VARNAME        = 5
	FUNCTYPE       = 6
	ARGLIST        = 7
	LISTTYPE       = 8
)

func is_primitive_type(token string) bool {
	if token == "int" || token == "float" || token == "long" || token == "string" {
		return true
	}
	return false
}

func parse_oneline(ch chan string, chn_tx chan string) bool {

	ret, _ := parse_type(ch, chn_tx)
	if ret == false {
		return false
	}

	chn_tx <- "END_OF_TYPE"
	return parse_lineend(ch, chn_tx)
}

func parse_type(ch chan string, chn_tx chan string) (bool, string) {

	token := <-ch

	if is_primitive_type(token) == true {
		chn_tx <- token
		return true, token
	}

	if strings.HasPrefix(token, "`") == true {
		chn_tx <- token
		return true, token
	}

	if token == "(" {
		chn_tx <- token
		return parse_function(ch, chn_tx), token
	}

	if token == "[" {
		chn_tx <- token
		return parse_list(ch, chn_tx), token
	}

	return false, token
}

func parse_lineend(ch chan string, chn_tx chan string) bool {
	token := <-ch
	if token == "\n" {
		return true
	}
	return false
}

func parse_function(ch chan string, chn_tx chan string) bool {

	ret := parse_arg_list(ch, chn_tx)
	if ret == false {
		return false
	}

	token := <-ch
	if token != "->" {
		return false
	}
	chn_tx <- token

	ret, _ = parse_type(ch, chn_tx)
	return ret
}

func parse_list(ch chan string, chn_tx chan string) bool {

	ret, _ := parse_type(ch, chn_tx)
	if ret == false {
		return false
	}

	token := <-ch
	if token != "]" {
		return false
	}

	chn_tx <- token
	return true
}

func parse_arg_list(ch chan string, chn_tx chan string) bool {
	ret, token := parse_type(ch, chn_tx)
	if ret == false {
		if token == ")" {
			chn_tx <- token
			return true
		} else {
			return false
		}
	}

	token = <-ch
	if token == ")" {
		chn_tx <- token
		return true
	}
	if token != "," {
		return false
	}

	chn_tx <- token
	return parse_arg_list(ch, chn_tx)
}

func what_type(token string) int {

	if token == "int" || token == "float" || token == "long" || token == "string" {
		return PRIMITIVE_TYPE
	}

	if strings.HasPrefix(token, "`") == true {
		return TYPEVAR
	}

	if token == "[" {
		return LISTTYPE
	}

	if token == "(" {
		return FUNCTYPE
	}

	return ILLEGAL
}

func is_unifiable(token_l string, token_r string) bool {

	if token_l == token_r {
		return true
	}

	type_l := what_type(token_l)
	type_r := what_type(token_r)

	/* type variable could be unifiable with any type */
	if type_l == TYPEVAR {
		return true
	}
	/* primitive type could only be unifiable with the same primitive type */
	/* such as int with int, not int with float */
	if type_l == PRIMITIVE_TYPE {
		if type_r == TYPEVAR {
			return true
		}
		return false
	}
	/* func type could only be unifiable with func type and type variable */
	if type_l == FUNCTYPE {
		if type_r == TYPEVAR || type_r == FUNCTYPE {
			return true
		}
		return false
	}
	/* list type could only be unifiable with list type and type variable */
	if type_l == LISTTYPE {
		if type_r == TYPEVAR || type_r == LISTTYPE {
			return true
		}
		return false
	}

	return false
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

		// split the line buffer into left and right part with "&"
		line_buf_l := type_list[0]
		line_buf_r := type_list[1]

		// customized splitter for our unification rules
		my_split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
			advance_byte, token_byte, err := bufio.ScanBytes(data, atEOF)

			token_str := string(token_byte)
			if token_str == "[" || token_str == "]" || token_str == "{" || token_str == "}" || token_str == "," || token_str == "(" || token_str == ")" || token_str == "&" {
				return advance_byte, token_byte, err
			}

			// int
			if token_str == "i" {
				primitive_type := "int"
				if strings.HasPrefix(string(data), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return advance_byte, token_byte, io.EOF
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// float
			if token_str == "f" {
				primitive_type := "float"
				if strings.HasPrefix(string(data), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.ErrNoProgress
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// long
			if token_str == "l" {
				primitive_type := "long"
				if strings.HasPrefix(string(data), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.ErrNoProgress
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// string
			if token_str == "s" {
				primitive_type := "string"
				if strings.HasPrefix(string(data), primitive_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.EOF
				}
				return advance_byte + len(primitive_type) - 1, []byte(primitive_type), err
			}

			// ->
			if token_str == "-" {
				function_ret_type := "->"
				if strings.HasPrefix(string(data), function_ret_type) == false {
					fmt.Printf("ERR\n")
					os.Exit(3)
					return 0, nil, io.ErrNoProgress
				}
				return advance_byte + len(function_ret_type) - 1, []byte(function_ret_type), err
			}

			// `<TYPE>
			if token_str == "`" {
				re := regexp.MustCompile("^`[a-zA-Z][a-zA-Z0-9]*")
				type_str := re.FindString(string(data))
				return advance_byte + len(type_str) - 1, []byte(type_str), err
			}

			// If the character doesn't fall into any defined category, it's an error
			fmt.Printf("ERR\n")
			os.Exit(3)
			return advance_byte, token_byte, err
		}

		scanner_l := bufio.NewScanner(strings.NewReader(line_buf_l))
		scanner_l.Split(my_split)

		scanner_r := bufio.NewScanner(strings.NewReader(line_buf_r))
		scanner_r.Split(my_split)

		channel_l := make(chan string)
		channel_r := make(chan string)

		/*
		 * One go routine for generating left type tokens
		 */
		generate_token_l := func() {
			for scanner_l.Scan() {
				if err := scanner_l.Err(); err != nil {
					fmt.Println("ERR")
					os.Exit(3)
				}

				buf_str := scanner_l.Text()
				channel_l <- buf_str
			}
		}

		/*
		 * One go routine for generating right type tokens
		 */
		generate_token_r := func() {
			for scanner_r.Scan() {
				if err := scanner_r.Err(); err != nil {
					fmt.Println("ERR")
					os.Exit(3)
				}

				buf_str := scanner_r.Text()
				channel_r <- buf_str
			}
		}

		channel_tx_left := make(chan string)
		channel_tx_right := make(chan string)

		/*
		 * Another go routine for parsing the tokens and generate the parse tree
		 */
		parse_type_left := func() {
			for true {
				ret := parse_oneline(channel_l, channel_tx_left)
				if ret != true {
					fmt.Println("ERR")
					os.Exit(4)
				}
			}
		}

		/*
		 * Another go routine for parsing the tokens and generate the parse tree
		 */
		parse_type_right := func() {
			for true {
				ret := parse_oneline(channel_r, channel_tx_right)
				if ret != true {
					fmt.Println("ERR")
					os.Exit(4)
				}
			}
		}

		/*
		 * Another go routine for type unification
		 */
		run_unification := func() {

			token_l := ""
			token_r := ""

			var newList []string

			for true {
				token_l = <-channel_tx_left
				token_r = <-channel_tx_right

				if token_l == "END_OF_TYPE" || token_r == "END_OF_TYPE" {
					break
				}

				if is_unifiable(token_l, token_r) == false {
					fmt.Println("BOTTOM")
					os.Exit(5)
				}

				if what_type(token_l) == TYPEVAR {
					if what_type(token_r) == PRIMITIVE_TYPE {
						token_l = token_r
					}
					if what_type(token_r) == FUNCTYPE {
					}
					if what_type(token_r) == LISTTYPE {
					}
				}

				if what_type(token_r) == TYPEVAR {
					if what_type(token_l) == FUNCTYPE {
					}
					if what_type(token_l) == LISTTYPE {
					}
				}

				newList = append(newList, token_l)
			}

			/* print the unified result */
			for i := 0; i < len(newList); i++ {
				fmt.Printf("%s", newList[i])
			}
			fmt.Printf("\n")
		}

		/*
		 * Launch all go routines
		 */
		go generate_token_l()
		go generate_token_r()
		go parse_type_left()
		go parse_type_right()
		go run_unification()

		// FIXME: sync up the threads before going to next loop
		time.Sleep(10000000)

	}
}
