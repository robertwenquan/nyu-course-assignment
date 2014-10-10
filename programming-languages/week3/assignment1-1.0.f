c     ==================================================================
c       Programming Language Class Fall 2014 Semester
c         Programming Assignment 1
c
c         Quan Wen (robert.wen@nyu.edu) | netid: qw476
c
c         Last modified on 9/30/2014
c     ==================================================================

      program assignment1


c     ==== constants declaration
      parameter (MAX_STR_BUF=255)


c     ==== NITEM - The first input as number of subsequent numbers
c     ==== NUM - The decimal number
c      character(len=100) NITEM_STR
c      character(len=100) INPUT_NUM_STR
      character NITEM_STR*(MAX_STR_BUF)
      character INPUT_NUM_STR*(MAX_STR_BUF)
      integer NITEM
      double precision NUM
      double precision sum, avg, min, max

c     ==== Read NITEM from console, on non-digit or EOF print ERR and exit
      read (*,'(A255)',err=555,end=555) NITEM_STR

c     ==== Validate integer numbers
c      1. characters, scientific notation, etc. eliminated
c         decimals are eliminated
c         comma, space divided numbers are also eliminated
      lens = my_trim_length(NITEM_STR)
      if (is_integer(NITEM_STR, lens) .EQ. 0) then
          go to 555
      endif

c      2. all numbers will come here
      read (NITEM_STR, *,err=555,end=555) NITEM

c      3. negative numbers eliminated
      if (NITEM .LT. 0) then
          go to 555
      endif

c     ==== Handle special case ZERO
      if (NITEM .EQ. 0) then
          NUM = 0
          sum = NUM
          avg = NUM
          min = NUM
          max = NUM

          call print_stats(NITEM, sum, avg, min, max)
          go to 999
      endif

c     ==== Handle normal case
      do 101 i = 1, NITEM

          read (*,'(A255)',err=555,end=555) INPUT_NUM_STR

c     ==== Validate decimal numbers
c      1. eliminate scientific notations
c         eliminate letters
c         eliminate space or comma divided numbers
          lens = my_trim_length(INPUT_NUM_STR)
          if (is_decimal(INPUT_NUM_STR, lens) .EQ. 0) then
              go to 555
          endif

          read (INPUT_NUM_STR, *,err=555,end=555) NUM

          if (i .EQ. 1) then
              sum = NUM
              avg = NUM
              min = NUM
              max = NUM
          else
              sum = sum + NUM
              avg = sum/i
              if (NUM .LT. min) then
                  min = NUM
              endif
              if (NUM .GT. max) then
                  max = NUM
              endif
          endif

101   continue

      call print_stats(NITEM, sum, avg, min, max)

999   stop

555   call print_error()
      go to 999

      end

c     ============ end of the program ===============




c     ======================
c      my_trim_length
c       return trimed length rather than full length
c
c      This function is written only because len_trim is not supported
c      in f77 but in f95
c     ======================
      function my_trim_length(str)
        implicit none
        integer my_trim_length, i
        character*(*) str

        do 15, i = len(str), 1, -1
          if (str(i:i) .ne. ' ') then
            go to 20
          end if
15      continue

20      my_trim_length = i
        return
      end function


c     ============ function declaration =============

c     ======================
c      print_error
c     ======================

c     ASCII TABLE (man(7) ascii)
c       DEC   ASC
c        43     +
c        45     -    (- is only for -0)
c     48-57   0-9

      function is_integer(s, n)
         implicit none
         integer is_integer
         character*(*) s
         integer i, k, n

c        n = len_trim(s)

         do i = 1, n
            k = ichar(s(i:i))
            if (k < 48 .or. k > 57) then
               if (k .ne. 43 .and. k .ne. 45) then
                   is_integer = 0
                   return
               end if
            end if
         end do

         is_integer = 1
         return
      end function


c     ======================
c      print_error
c     ======================

c     ASCII TABLE (man(7) ascii)
c       DEC   ASC
c        43     +
c        45     -
c        46     .
c     48-57   0-9

      function is_decimal(s, n)
         implicit none
         integer is_decimal
         character*(*) s
         integer i, k, n

c        n = len_trim(s)

         do i = 1, n
            k = ichar(s(i:i))
            if (k .LT. 48 .or. k .GT. 57) then
               if (k .ne. 43 .and. k .ne. 45 .and. k .ne. 46) then
                  is_decimal = 0
                  return
               end if
            end if
         end do

         is_decimal = 1
         return
      end function


c     ======================
c      print_error
c     ======================
      subroutine print_error()
        write (*,'(A)') 'ERR'
        return
      end subroutine


c     ======================
c      print_stats
c       Print all statistics numbers
c        Num in integer format
c        Subsequent numbers in standard decimal notation
c     ======================
      subroutine print_stats(num, sum, avg, min, max)
        integer num
        double precision sum, avg, min, max
        write (*,'(A,I32)')   'Num: ', num
        write (*,'(A,F35.2)') 'Sum: ', sum
        write (*,'(A,F35.2)') 'Avg: ', avg
        write (*,'(A,F35.2)') 'Min: ', min
        write (*,'(A,F35.2)') 'Max: ', max
        return
      end subroutine

