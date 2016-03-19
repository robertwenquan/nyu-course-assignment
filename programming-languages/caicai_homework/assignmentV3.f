c       ********************************************************
c       * Programming Language Fall 2015                       *
c       *   Programming Assignment 1                           *
c       *                                                      *
c       *   Caicai CHEN                                        *
c       *     caicai.chen@nyu.edu                              *
c       *     NetId: cc4584                                    *
c       ********************************************************

        program  assignmentV3

        parameter (INT_MAX = 2147483647)
        parameter (MAX_STR_LEN = 255)

        character num_str*(MAX_STR_LEN) 
        integer num, stt, fin, length
        double precision D_ZERO

        D_ZERO = 0.00

        read(UNIT=*, FMT='(A)', IOSTAT=KODE, ERR=88) num_str
        if (KODE .NE. 0) stop

c       -------------------------------------------------------
c         CHECK WHETHER THE FIRST INTEGER IS VALID INPUT
c         Valid input:    WS INTEGER WS
c           1. Strip head WS
c           2. Strip tail WS 
c           3. Check is_negative
c           4. Check is_invalid_int
c           5. Check is_zero
c           6. Check is_overflow
c           7. Convert into integer
c       -------------------------------------------------------

c       STRIP HEAD WS

        stt = strip_head_ws(num_str, len(num_str))

c       STRIP TAIL WS

        fin = strip_tail_ws(num_str, stt, len(num_str))

        length = fin - stt + 1

        if ( length .le. 0 ) then
          goto 88
        endif

c       CHECK IS_NEGATIVE  

        if (is_negative(num_str(stt:fin)) .eq. 1) then
          goto 88
        endif

c       CHECK IS_INVALID_INT

        if (is_invalid_int(num_str(stt:fin), length) .eq. 1) then
          goto 88
        endif

c       CHECK IS_ZERO
        if (is_zero(num_str(stt:fin), length) .eq. 1) then
c          call print_result(0.00,0.00,0.00,0.00)
          call print_result(D_ZERO, D_ZERO, D_ZERO, D_ZERO)
          goto 100
        endif

c       CHECK OVERFLOW
        if (is_overflow(num_str(stt:fin), length). eq. 1) then
          goto 88
        endif

        read(num_str(stt:fin), '(I10)',ERR=88) num

        call Calculation(num)

        goto 100  
  88    call print_error()
  100   stop
        end

c       ********************************************************
c       * Strip head and tail WS                               *
c       ********************************************************

        function strip_head_ws(s, length)
          character *(*) s
          integer length
          do 10 i = 1, length 
            if ((s(i:i) .ne. ' ') .and. (ichar(s(i:i)) .ne. 9) ) then
              goto 40
            endif
  10      continue

  40      strip_head_ws = i
          return
        end function

        function strip_tail_ws(s, stt, length)
          character *(*) s
          integer stt, length
          do 20 i = length, stt, -1
            if ((s(i:i) .ne. ' ') .and. (ichar(s(i:i)) .ne. 9)) then
              goto 80
            endif
  20      continue

  80      strip_tail_ws = i
          return

          end function
        
c       ********************************************************
c       * Check whether the integer is negative                *
c       ********************************************************

        function is_negative(s)
          character*(*) s

          if (s(1:1) .eq. '-') then
            is_negative = 1
          else
            is_negative = 0
          endif

          return
        end function

c       ********************************************************
c       * Check whether the integer invalid                    *
c       ********************************************************

        function is_invalid_int(s, len)
          character*(*) s
          integer len, num

          do 33 i = 1, len
            num = ichar(s(i:i))
            if ((num .lt. 48) .or. (num .gt. 57)) then
              goto 34
            endif
  33      continue

          is_invalid_int = 0
          return

  34      is_invalid_int = 1
          return
        end function

c       ********************************************************
c       * Check whether the integer is 0                       *
c       ********************************************************

        function is_zero(s,len)
          character*(*) s
          integer len, num

          do 44 i = 1, len
            num = ichar(s(i:i))
            if ( num .ne. 48 ) then
              goto 43
            endif
  44      continue

          is_zero = 1
          return

  43      is_zero = 0
          return
          end function
            
c       ********************************************************
c       * Check whether the integer is 0                       *
c       ********************************************************

        function is_overflow(s,len)
          character*(*) s
          integer len, num, cur_num, n_max
          integer INT_MAX
          INT_MAX = 2147483647

          num = 0
          if (len .lt. 10) then
            goto 45
          else if (len .gt. 10) then
            goto 46
          else
            do 440 i = 1, (len - 1)
              cur_num = ichar(s(i:i)) - 48
              num = num * 10 + cur_num
              n_max = INT_MAX / (10**(10-i))
              if (num .gt. n_max) then
                goto 46
              endif
  440       continue
            if (ichar(s(10:10))-48 .gt. 7) then
              goto 46
            endif
          endif

  45      is_overflow = 0
          return

  46      is_overflow = 1
          return
          end function

c       ********************************************************
c       * Convert String to Integer                            *
c       ********************************************************

        function convert_integer(s,len)
          character*(*) s
          integer len, num, cur_num

          num = 0
          do 58 i = 1, len
            cur_num = ichar(s(i:i)) - 48
            num = num*10 + cur_num
  58      continue

          convert_integer = num

          return
        end function

c       ********************************************************
c       * Begin Calculation                                    *
c       ********************************************************

        subroutine Calculation(num)

c       READ IN ALL ELEMENTS
          parameter (INT_MAX = 2147483647)
          integer num, k
          integer stt, fin, length
          integer sign, pnt

          character kbd_in*255
          character cur_num_buf*255
          double precision cur_num, sum, tmp
          double precision cur_max, cur_min
          double precision pos(num), neg(num)
          integer n_pos, n_neg

          n_pos = 0
          n_neg = 0

c       -------------------------------------------------------
c         VALIDATION CHECK OF INPUT
c         1. Read input as character*(*)
c         2. Stip head and tail WS
c         3. Get sign of number
c         4. Get rid of WS between sign and number
c         5. Check validation of integer part and fraction part
c         6. Check whether the number would be change after convert
c         7. Store according to sign
c       -------------------------------------------------------

          do 10 k = 1, num 
            read(UNIT=*, FMT='(A)', IOSTAT=KODE, ERR=888) kbd_in

c           Stip head and tail WS
            stt = strip_head_ws(kbd_in, len(kbd_in))
            fin = strip_tail_ws(kbd_in, stt, len(kbd_in))
            length = fin - stt + 1
            if (length .le. 0) then
              goto 888
            endif

c           Check Input is positive or negative
            if(kbd_in(stt:stt) .eq. '+') then
              sign = 1
              stt = stt+strip_head_ws(kbd_in(stt+1:fin),fin-stt)
            else if(kbd_in(stt:stt) .eq. '-') then
              sign = -1
              stt = stt+strip_head_ws(kbd_in(stt+1:fin),fin-stt)
            else
              sign = 1
            endif

c           Find position of "."
c           Check integer part and fraction part separately
            if(INDEX(kbd_in(stt:fin), '.') .ne. 0) then
              pnt = stt + INDEX(kbd_in(stt:fin), '.') - 1

              if(is_invalid_int(kbd_in(stt:pnt-1),pnt-stt).eq.1)then
                goto 888
              endif

              if(is_invalid_int(kbd_in(pnt+1:fin),fin-pnt).eq.1)then
                goto 888
              endif

            else

              if(is_invalid_int(kbd_in(stt:fin),fin-stt+1).eq.1)then
                goto 888
              endif

            endif

c           Compose "-" and "." to check precision lose
            if (sign .eq. -1) then
              cur_num_buf(1:1) = '-'
              if(is_zero(kbd_in(stt:pnt-1), pnt-stt).eq.1)then
                cur_num_buf(2:2) = '0'
                cur_num_buf(3:) = kbd_in(pnt:fin)
              else
                cur_num_buf(2:) = kbd_in(stt:fin)
              endif
            else
              if(is_zero(kbd_in(stt:pnt-1),pnt-stt).eq.1) then
                cur_num_buf(1:1) = '0'
                cur_num_buf(2:) = kbd_in(pnt:fin)
              else
                cur_num_buf = kbd_in(stt:fin)
              endif
            endif

            if(INDEX(kbd_in(stt:fin), '.') .eq. 0) then
              cur_num_buf((fin+1):(fin+1)) = '.'
            endif
            read(cur_num_buf, '(F60.4)',ERR=888) cur_num
            if ( flt_overflow(cur_num_buf, cur_num) .eq. 1 ) then
              goto 888
            endif

c           Get Max and Min
            if ( k .eq. 1 ) then
              cur_min = cur_num
              cur_max = cur_num
            else
              cur_max = max(cur_max, cur_num)
              cur_min = min(cur_min, cur_num)
            endif

c           Store according to sign
            if (sign .eq. 1) then
              n_pos = n_pos + 1
              pos(n_pos) = cur_num
            else
              cur_num_buf = kbd_in(stt:fin)
              if(INDEX(kbd_in(stt:fin), '.') .eq. 0) then
                cur_num_buf((fin+1):(fin+1)) = '.'
              endif
              read(cur_num_buf, '(F60.4)',ERR=888) cur_num
              n_neg = n_neg + 1
              neg(n_neg) = cur_num
            endif

  10      continue

c       -------------------------------------------------------
c         SUM EVERYTHING UP
c           To avoid overflow, use following order of add
c           1. If the current sum is positive
c              goto find a negative number
c           2. If the current sum is negative
c              goto find a positive number
c           3. Only when "+" + "+" and "-" - "-"
c              Check overflow  
c       -------------------------------------------------------

          sum = 0 
          do 72 i = 1, num
            if (sum .gt. 0) then
              if (n_neg .ne. 0) then
                sum = sum - neg(n_neg)
                n_neg = n_neg - 1
              else
                tmp = sum + pos(n_pos)
                if ( ((tmp-sum) - pos(n_pos)) .gt. 1) goto 888
                if ( ((tmp-sum) - pos(n_pos)) .lt. -1) goto 888
                sum = tmp
                n_pos = n_pos - 1
              endif
            else
              if (n_pos .ne. 0) then
                sum = sum + pos(n_pos)
                n_pos = n_pos - 1
              else
                tmp = sum - neg(n_neg)
                if ( ((sum-tmp) - neg(n_neg)) .gt. 1) goto 888
                if ( ((sum-tmp) - neg(n_neg)) .lt. -1) goto 888
                sum = tmp
                n_neg = n_neg - 1
              endif
            endif
  72      continue

          call print_result(sum, sum/num, cur_min, cur_max)
          return

  888     call print_error
          return

        end subroutine

c       ********************************************************
c       * Convert a string to float number first               * 
c       * Then convert back to string                          *
c       * If they are not same, it means number changed        *
c       ********************************************************

        function flt_overflow(buf_in, cur_num)
          character*(*) buf_in
          character buf*255
          double precision cur_num, tmp_num, tmp
          integer i, stt_in, fin_in, stt_b, fin_b, p_in, p_b

          write(buf , '(F60.4)') cur_num

c         GET ACTUAL LENGTH OF STRING
          stt_in = strip_head_ws(buf_in, 255)
          fin_in = strip_tail_ws(buf_in, stt_in, 255)

          stt_b = strip_head_ws(buf, 255)
          fin_b = strip_tail_ws(buf, stt_b, 255)

c         GET LOCATION OF POINT "."
          p_in = INDEX(buf_in(stt_in:fin_in),'.')
          p_b = INDEX(buf(stt_b:fin_b),'.')

          if (p_in .ne. p_b) goto 777

c         DEAL WITH INTEGER PART
          if(buf_in(stt_in:stt_in+p_in-1).ne.buf(stt_b:stt_b+p_b-1))then

c         DEAL WITH ROUNDING OFF
            read(buf(stt_b:stt_b+p_b-1),'(F60.4)',ERR=777) tmp_num
            read(buf_in(stt_in:stt_in+p_in-1),'(F60.4)',ERR=777) tmp
            if ((tmp_num-tmp).le.1.and.(tmp_num-tmp).ge.-1)then
              goto 444
            endif
            goto 777
          endif

c         DEAL WITH FRACTION PART
          p_in = stt_in + p_in - 1
          p_b = stt_b + p_b - 1
          if ( (fin_in - p_in) .lt. (fin_b - p_b) ) then
            i = (fin_b - p_b) - (fin_in - p_in)
            do 111 j = 1, i
              buf_in(fin_in+j:fin_in+j) = '0'
  111       continue
            fin_in = fin_in + i
          else
            fin_in = p_in + (fin_b - p_b)
          endif

          if (buf_in(p_in:fin_in-1) .ne. buf(p_b:fin_b-1)) then
c         DEAL WITH ROUNDING OFF
            read(buf(p_b+1:fin_in),'(F60.4)',ERR=777) tmp_num
            read(buf_in(p_in+1:fin_b),'(F60.4)',ERR=777) tmp
            if((tmp_num-tmp).le.0.01.and.(tmp_num-tmp).ge.-0.01)then
              goto 444
            endif
            goto 777
          endif

  444     flt_overflow = 0
          return

  777     flt_overflow = 1
          return
        end function

c       ********************************************************
c       *  If program ends normally                            *
c       *  Print out final result                              *
c       ********************************************************
        subroutine print_result(sum, avg, cur_min, cur_max)
          double precision sum, cur_max, cur_min, avg

          write(*,'(A,F25.2)') 'Sum: ', sum 
          write(*,'(A,F25.2)') 'Average: ', avg
          write(*,'(A,F25.2)') 'Minimum: ', cur_min 
          write(*,'(A,F25.2)') 'Maximum: ', cur_max

          return
        end subroutine

c       ********************************************************
c       *  If program has invalid input                        *
c       *  Print out ERR and return                            *
c       ********************************************************

        subroutine print_error
          write(*,'(A)') 'ERR'
          return
        end subroutine

