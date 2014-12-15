package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"
	"sync"
)

const (
	ILLEGAL = 1

	PRIMITIVE_TYPE = 3
	TYPEVAR        = 4
	FUNCTYPE       = 6
	LISTTYPE       = 8

	FUNCTYPE_END = 16
	LISTTYPE_END = 18
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

	if token == "]" {
		return LISTTYPE_END
	}

	if token == "}" {
		return FUNCTYPE_END
	}

	return ILLEGAL
}

func is_initial_unifiable(token_l string, token_r string) bool {

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

func is_further_unifiable(list_left []string, list_right []string) bool {

	index_l := 0
	index_r := 0
	len_l := len(list_left)
	len_r := len(list_right)

	for {
		if index_l == len_l && index_r == len_r {
			break
		}

		if index_l == len_l || index_r == len_r {
			return false
		}

		single_token_status := is_initial_unifiable(list_left[index_l], list_right[index_r])
		if single_token_status == false {
			return false
		}

		index_l++
		index_r++
	}

	return true
}

func get_list_token_offline(type_list []string) []string {
	return type_list
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
		query_dict, is_cached := query_unification_dict(unification_dict, key)
		if is_cached == false {
			fmt.Printf("%s", strlist[i])
			continue
		}

		print_unified_result(query_dict, 0, unification_dict)

	}

	if newline == 1 {
		fmt.Printf("\n")
	}
}

func check_recursive_type_list(strlist []string, unification_dict map[string][]string) bool {

	for i := 0; i < len(strlist); i++ {

		if what_type(strlist[i]) != TYPEVAR {
			continue
		}

		ret := check_recursive_type(strlist[i], strlist[i], unification_dict)
		if ret == true {
			return true
		}
	}

	return false
}

func check_recursive_type(origin string, token string, unification_dict map[string][]string) bool {

	query_dict, is_cached := query_unification_dict(unification_dict, token)
	if is_cached == false {
		return false
	}

	for i := 0; i < len(query_dict); i++ {
		if origin == query_dict[i] {
			return true
		}

		if what_type(query_dict[i]) == TYPEVAR {
			ret := check_recursive_type(origin, query_dict[i], unification_dict)
			if ret == true {
				return true
			}
		}
	}

	return false
}

func query_unification_dict(unification_dict map[string][]string, token string) ([]string, bool) {

	token_query_dict, ok := unification_dict[token]
	status := true

	if ok == false {
		token_query_dict = append(token_query_dict, token)
		status = false
	} else {
		for {
			val := string_list_to_string(token_query_dict)
			if what_type(val) != TYPEVAR {
				break
			}

			/* exit at loop */
			if val == token {
				break
			}

			token_query_dict, ok = unification_dict[val]
			if ok == false {
				token_query_dict = append(token_query_dict, val)
				break
			}
		}
	}

	return token_query_dict, status
}

func print_unified_dict(unification_dict map[string][]string) {
	fmt.Println("-------unification dictionary-------")
	for key := range unification_dict {
		str := string_list_to_string(unification_dict[key])
		fmt.Printf("%s -> %s\n", key, str)
	}
	fmt.Println("------------------------------------")
}

func main() {

	reader := bufio.NewReader(os.Stdin)

	var wg sync.WaitGroup

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
		line_buf_l := strings.Trim(type_list[0], " ")
		line_buf_r := strings.Trim(type_list[1], " ")

		// customized splitter for our unification rules
		my_split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
			advance_byte, token_byte, err := bufio.ScanBytes(data, atEOF)

			offset := 0
			for string(token_byte) == " " {
				offset += 1
				_, token_byte, err = bufio.ScanBytes(data[offset:], atEOF)
				advance_byte += 1
			}

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

		scanner_l := bufio.NewScanner(strings.NewReader(line_buf_l))
		scanner_l.Split(my_split)

		scanner_r := bufio.NewScanner(strings.NewReader(line_buf_r))
		scanner_r.Split(my_split)

		channel_l := make(chan string)
		channel_r := make(chan string)

		/*
		 * One go routine for generating left type tokens
		 */
		read_left_tokens := func() {
			defer wg.Done()
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
		read_right_tokens := func() {
			defer wg.Done()
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
		parse_left_type := func() {
			defer wg.Done()
			ret, list := parse_oneline(channel_l, channel_tx_left)
			if ret != true {
				fmt.Println("ERR")
				os.Exit(4)
			}

			spit_token_to_channel(channel_tx_left, list)
		}

		/*
		 * Another go routine for parsing the tokens and generate the parse tree
		 */
		parse_right_type := func() {
			defer wg.Done()
			ret, list := parse_oneline(channel_r, channel_tx_right)
			if ret != true {
				fmt.Println("ERR")
				os.Exit(4)
			}

			spit_token_to_channel(channel_tx_right, list)
		}

		/*
		 * Another go routine for type unification
		 */
		start_unification := func() {
			defer wg.Done()

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
				token_l_query_dict, is_cached_l := query_unification_dict(unification_dict, token_l)
				token_r_query_dict, is_cached_r := query_unification_dict(unification_dict, token_r)

				if is_initial_unifiable(token_l_query_dict[0], token_r_query_dict[0]) == false {
					fmt.Println("BOTTOM")
					os.Exit(5)
				}

				if what_type(token_l_query_dict[0]) == TYPEVAR {

					// `abc & int
					if what_type(token_r_query_dict[0]) == PRIMITIVE_TYPE {
						val, is_cached := query_unification_dict(unification_dict, token_l)
						if is_cached == false {
							unification_dict[token_l] = token_r_query_dict
							newList = append(newList, token_r_query_dict[0])
						} else {
							unification_dict[token_l] = token_r_query_dict
							unification_dict[val[0]] = token_r_query_dict
							newList = append(newList, token_r_query_dict[0])
						}
						continue
					}

					// `abc & []
					if what_type(token_r_query_dict[0]) == LISTTYPE {
						if is_cached_r == false {
							token_list_r := get_list_token(channel_tx_right)
							unification_dict[token_l] = token_list_r
							newList = append(newList, token_list_r...)
						} else {
							token_list_r := get_list_token_offline(token_r_query_dict)
							unification_dict[token_l] = token_list_r
							newList = append(newList, token_list_r...)
						}
						continue
					}

					// `abc & ()
					if what_type(token_r_query_dict[0]) == FUNCTYPE {
						if is_cached_r == false {
							token_func_r := get_func_token(channel_tx_right)
							unification_dict[token_l] = token_func_r
							newList = append(newList, token_func_r...)
						} else {
							unification_dict[token_l] = token_r_query_dict
							newList = append(newList, token_r_query_dict...)
						}
						continue
					}

					// `abc & `bbc
					if what_type(token_r_query_dict[0]) == TYPEVAR {
						if string_list_to_string(token_l_query_dict) != string_list_to_string(token_r_query_dict) {
							unification_dict[token_l_query_dict[0]] = token_r_query_dict
						}
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
						if is_cached_l == false {
							token_list_l := get_list_token(channel_tx_left)
							unification_dict[token_r] = token_list_l
							newList = append(newList, token_list_l...)
						} else {
							token_list_l := get_list_token_offline(token_l_query_dict)
							unification_dict[token_r] = token_list_l
							newList = append(newList, token_list_l...)
						}
						continue
					}

					// () & `abc
					if what_type(token_l_query_dict[0]) == FUNCTYPE {
						if is_cached_l == false {
							token_func_l := get_func_token(channel_tx_left)
							unification_dict[token_r] = token_func_l
							newList = append(newList, token_func_l...)
						} else {
							unification_dict[token_r] = token_l_query_dict
							newList = append(newList, token_l_query_dict...)
						}
						continue
					}

				}

				/* list with list */
				if is_cached_l == true && what_type(token_r_query_dict[0]) == LISTTYPE {
					if is_cached_r == false {
						token_r_query_dict = get_list_token(channel_tx_right)
					}
					if is_further_unifiable(token_l_query_dict, token_r_query_dict) == false {
						fmt.Println("BOTTOM")
						os.Exit(5)
					}
					newList = append(newList, token_l_query_dict...)
					continue
				}

				if is_cached_r == true && what_type(token_l_query_dict[0]) == LISTTYPE {
					if is_cached_l == false {
						token_l_query_dict = get_list_token(channel_tx_left)
					}
					if is_further_unifiable(token_l_query_dict, token_r_query_dict) == false {
						fmt.Println("BOTTOM")
						os.Exit(5)
					}
					newList = append(newList, token_r_query_dict...)
					continue
				}

				/* func with func */
				if is_cached_l == true && what_type(token_r_query_dict[0]) == FUNCTYPE {
					if is_cached_r == false {
						token_r_query_dict = get_func_token(channel_tx_right)
					}
					if is_further_unifiable(token_l_query_dict, token_r_query_dict) == false {
						fmt.Println("BOTTOM")
						os.Exit(5)
					}
					newList = append(newList, token_l_query_dict...)
					continue
				}

				if is_cached_r == true && what_type(token_l_query_dict[0]) == FUNCTYPE {
					if is_cached_l == false {
						token_l_query_dict = get_func_token(channel_tx_left)
					}
					if is_further_unifiable(token_l_query_dict, token_r_query_dict) == false {
						fmt.Println("BOTTOM")
						os.Exit(5)
					}
					newList = append(newList, token_r_query_dict...)
					continue
				}

				newList = append(newList, token_r_query_dict[0])
			}

			ret := check_recursive_type_list(newList, unification_dict)
			if ret == true {
				fmt.Println("BOTTOM")
				os.Exit(5)
			}

			/* print the unified result */
			print_unified_result(newList, 1, unification_dict)

		}

		/*
		 * Launch a few go routines to work out the type unification
		 */

		wg.Add(5)

		go read_left_tokens()
		go read_right_tokens()
		go parse_left_type()
		go parse_right_type()
		go start_unification()

		wg.Wait()
	}
}
