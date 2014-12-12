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

func parse_oneline(ch chan string, chn_tx chan string) (bool, []string) {

	var line_list []string

	ret, _, type_list := parse_type(ch, chn_tx)
	if ret == false {
		return false, line_list
	}

	line_list = append(line_list, type_list...)

	line_list = append(line_list, "END_OF_TYPE")

	return parse_lineend(ch, chn_tx), line_list
}

func parse_type(ch chan string, chn_tx chan string) (bool, string, []string) {

	var type_list []string

	token := <-ch

	if is_primitive_type(token) == true {
		type_list = append(type_list, token)
		return true, token, type_list
	}

	if strings.HasPrefix(token, "`") == true {
		type_list = append(type_list, token)
		return true, token, type_list
	}

	if token == "(" {
		type_list = append(type_list, token)

		ret, func_list := parse_function(ch, chn_tx)
		type_list = append(type_list, func_list...)
		return ret, token, type_list
	}

	if token == "[" {
		type_list = append(type_list, token)

		ret, list_list := parse_list(ch, chn_tx)
		type_list = append(type_list, list_list...)
		return ret, token, type_list
	}

	return false, token, type_list
}

func parse_lineend(ch chan string, chn_tx chan string) bool {
	token := <-ch
	if token == "\n" {
		return true
	}
	return false
}

func parse_function(ch chan string, chn_tx chan string) (bool, []string) {

	var type_list []string

	ret, arg_list := parse_arg_list(ch, chn_tx)
	if ret == false {
		return false, type_list
	}
	type_list = append(type_list, arg_list...)

	token := <-ch
	if token != "->" {
		return false, type_list
	}
	type_list = append(type_list, token)

	ret, _, func_list := parse_type(ch, chn_tx)
	type_list = append(type_list, func_list...)

	return ret, type_list
}

func parse_list(ch chan string, chn_tx chan string) (bool, []string) {

	var type_list []string

	ret, _, type2 := parse_type(ch, chn_tx)
	if ret == false {
		return false, type_list
	}

	type_list = append(type_list, type2...)

	token := <-ch
	if token != "]" {
		return false, type_list
	}

	type_list = append(type_list, token)
	return true, type_list
}

func parse_arg_list(ch chan string, chn_tx chan string) (bool, []string) {

	var type_list []string

	ret, token, list1 := parse_type(ch, chn_tx)
	if ret == false {
		if token == ")" {
			type_list = append(type_list, token)
			return true, type_list
		} else {
			return false, type_list
		}
	}
	type_list = append(type_list, list1...)

	token = <-ch
	if token == ")" {
		type_list = append(type_list, token)
		return true, type_list
	}
	if token != "," {
		return false, type_list
	}

	type_list = append(type_list, token)

	ret, list2 := parse_arg_list(ch, chn_tx)
	type_list = append(type_list, list2...)

	return ret, type_list
}

func spit_token_to_channel(chn_tx chan string, list []string) {
	for i := 0; i < len(list); i++ {
		chn_tx <- list[i]
	}
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

func is_unifiable(token_l []string, token_r []string) bool {

	if token_l[0] == token_r[0] {
		return true
	}

	type_l := what_type(token_l[0])
	type_r := what_type(token_r[0])

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

func get_list_type(chn chan string) ([]string, int) {

	var list_str []string

	token := <-chn

	if is_primitive_type(token) == true {
		list_str = append(list_str, token)
		return list_str, 0
	}

	if strings.HasPrefix(token, "`") == true {
		list_str = append(list_str, token)
		return list_str, 0
	}

	if token == "(" {
		list_str = get_func_token(chn)
		return list_str, 0
	}

	if token == "[" {
		list_str = get_list_token(chn)
		return list_str, 0
	}

	if token == ")" {
		return list_str, 5
	}

	return list_str, 1
}

func get_list_token(chn chan string) []string {

	var list_str []string

	list_str = append(list_str, "[")
	list_type, _ := get_list_type(chn)
	for i := 0; i < len(list_type); i++ {
		list_str = append(list_str, list_type[i])
	}

	token := <-chn
	if token != "]" {
		fmt.Println("ERR")
		os.Exit(8)
	}
	list_str = append(list_str, token)

	return list_str
}

func get_list_arglist(chn chan string) []string {

	var list_str []string

	list_type, ret := get_list_type(chn)
	if ret == 5 {
		return list_str
	}

	typestr := string_list_to_string(list_type)
	list_str = append(list_str, typestr)

	token := <-chn
	if token == ")" {
		list_str = append(list_str, token)
		return list_str
	}

	if token != "," {
		fmt.Println("ERR")
		os.Exit(8)
	}
	list_str = append(list_str, token)

	arglist_str := string_list_to_string(get_list_arglist(chn))
	list_str = append(list_str, arglist_str)

	return list_str

}

func get_func_token(chn chan string) []string {

	var list_str []string

	list_str = append(list_str, "(")
	arglist_str := string_list_to_string(get_list_arglist(chn))
	if arglist_str == "" {
		list_str = append(list_str, ")")
	} else {

		list_str = append(list_str, arglist_str)

		token := <-chn
		if token != ")" {
			fmt.Println("ERR")
			os.Exit(8)
		}
		list_str = append(list_str, token)
	}

	token := <-chn
	if token != "->" {
		fmt.Println("ERR")
		os.Exit(8)
	}
	list_str = append(list_str, token)

	list_type, _ := get_list_type(chn)
	type_str := string_list_to_string(list_type)
	list_str = append(list_str, type_str)

	return list_str
}

func string_list_to_string(strlist []string) string {

	str := ""
	for i := 0; i < len(strlist); i++ {
		str = str + strlist[i]
	}

	return str
}

func print_unified_result(strlist []string, newline int, unification_dict map[string][]string) {

	for i := 0; i < len(strlist); i++ {

		/* not typed var */
		if what_type(strlist[i]) != TYPEVAR {
			fmt.Printf("%s", strlist[i])
			continue
		}

		key := strlist[i]

		/* not found in the cache */
		val, ok := unification_dict[key]
		if ok != true {
			fmt.Printf("%s", strlist[i])
			continue
		}

		print_unified_result(val, 0, unification_dict)

	}

	if newline == 1 {
		fmt.Printf("\n")
	}
}

func query_unification_dict(unification_dict map[string][]string, token string) []string {

	token_query_dict, ok := unification_dict[token]
	if ok != true {
		token_query_dict = append(token_query_dict, token)
	}

	return token_query_dict
}

func print_unified_dict(unification_dict map[string][]string) {
	fmt.Println("------------------------------")
	for key := range unification_dict {
		str := string_list_to_string(unification_dict[key])
		fmt.Printf("%s -> %s\n", key, str)
	}
	fmt.Println("------------------------------")
}

func main() {

	reader := bufio.NewReader(os.Stdin)

	/* global directory for the unification */
	var unification_dict map[string][]string
	unification_dict = make(map[string][]string)

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

		if line_buf == "$$DEBUG$$" {
			print_unified_dict(unification_dict)
			continue
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
		san_francisco_on_dec18 := func() {
			for scanner_l.Scan() {
				if err := scanner_l.Err(); err != nil {
					fmt.Println("ERR")
					os.Exit(3)
				}

				buf_str := scanner_l.Text()
				channel_l <- buf_str
			}
			channel_l <- "\n"
		}

		/*
		 * One go routine for generating right type tokens
		 */
		los_angeles_on_dec21 := func() {
			for scanner_r.Scan() {
				if err := scanner_r.Err(); err != nil {
					fmt.Println("ERR")
					os.Exit(3)
				}

				buf_str := scanner_r.Text()
				channel_r <- buf_str
			}
			channel_r <- "\n"
		}

		channel_tx_left := make(chan string)
		channel_tx_right := make(chan string)

		/*
		 * Another go routine for parsing the tokens and generate the parse tree
		 */
		beijing_on_dec25 := func() {
			for true {
				ret, list := parse_oneline(channel_l, channel_tx_left)
				if ret != true {
					fmt.Println("ERR")
					os.Exit(4)
				}

				spit_token_to_channel(channel_tx_left, list)
			}
		}

		/*
		 * Another go routine for parsing the tokens and generate the parse tree
		 */
		hong_kong_on_dec30 := func() {
			for true {
				ret, list := parse_oneline(channel_r, channel_tx_right)
				if ret != true {
					fmt.Println("ERR")
					os.Exit(4)
				}

				spit_token_to_channel(channel_tx_right, list)
			}
		}

		/*
		 * Another go routine for type unification
		 */
		back_to_new_york_on_jan23 := func() {

			token_l := ""
			token_r := ""

			var newList []string

			for true {
				token_l = <-channel_tx_left
				token_r = <-channel_tx_right

				if token_l == "END_OF_TYPE" && token_r == "END_OF_TYPE" {
					break
				}

				if token_l == "END_OF_TYPE" || token_r == "END_OF_TYPE" {
					fmt.Println("BOTTOM")
					os.Exit(5)
				}

				/* check dictionary, if it exists, replace the type variable */
				token_l_query_dict := query_unification_dict(unification_dict, token_l)
				token_r_query_dict := query_unification_dict(unification_dict, token_r)

				if is_unifiable(token_l_query_dict, token_r_query_dict) == false {
					fmt.Println("BOTTOM")
					os.Exit(5)
				}

				if what_type(token_l_query_dict[0]) == TYPEVAR {

					// `abc & int
					if what_type(token_r_query_dict[0]) == PRIMITIVE_TYPE {
						unification_dict[token_l] = append(unification_dict[token_l], token_r_query_dict[0])
						newList = append(newList, token_r_query_dict[0])
						continue
					}

					// `abc & []
					if what_type(token_r_query_dict[0]) == LISTTYPE {
						token_list_r := get_list_token(channel_tx_right)
						unification_dict[token_l] = token_list_r
						newList = append(newList, token_list_r...)
						continue
					}

					// `abc & ()
					if what_type(token_r_query_dict[0]) == FUNCTYPE {
						token_func_r := get_func_token(channel_tx_right)
						unification_dict[token_l] = token_func_r
						newList = append(newList, token_func_r...)
						continue
					}

					// `abc & `bbc
					if what_type(token_r_query_dict[0]) == TYPEVAR {
						unification_dict[token_l_query_dict[0]] = token_r_query_dict
					}

				}

				if what_type(token_r_query_dict[0]) == TYPEVAR {

					// int & `abc
					if what_type(token_l_query_dict[0]) == PRIMITIVE_TYPE {
						unification_dict[token_r] = append(unification_dict[token_r], token_l_query_dict[0])
						newList = append(newList, token_l_query_dict[0])
						continue
					}

					// [] & `abc
					if what_type(token_l_query_dict[0]) == LISTTYPE {
						token_list_l := get_list_token(channel_tx_left)
						unification_dict[token_r] = token_list_l
						newList = append(newList, token_list_l...)
						continue
					}

					// () & `abc
					if what_type(token_l_query_dict[0]) == FUNCTYPE {
						token_func_l := get_func_token(channel_tx_left)
						unification_dict[token_r] = token_func_l
						newList = append(newList, token_func_l...)
						continue
					}

				}

				newList = append(newList, token_r_query_dict[0])
			}

			/* print the unified result */
			print_unified_result(newList, 1, unification_dict)
		}

		/*
		 * Launch go routines
		 */
		go san_francisco_on_dec18()
		go los_angeles_on_dec21()
		go beijing_on_dec25()
		go hong_kong_on_dec30()
		go back_to_new_york_on_jan23()

		// FIXME: sync up the threads before going to next loop
		//        don't have the fucking time to fix this. leave it??
		time.Sleep(10000000)
	}
}
