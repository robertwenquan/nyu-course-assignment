c     ==================================================================
c       Programming Language Class Fall 2014 Semester
c         Programming Assignment 1
c
c         Quan Wen (robert.wen@nyu.edu) | netid: qw476
c
c         Last modified on 10/1/2014
c     ==================================================================

      program assignment1


c     ==== constants declaration
      parameter (MAX_STR_BUF=255)


c     ==== NITEM_STR - String buffer to hold the initial number
c     ==== NITEM - The first input as number of subsequent numbers
      character NITEM_STR*(MAX_STR_BUF)
      integer NITEM

c     ==== INPUT_NUM_STR - String buffer to hold the subsequent numbers
c     ==== NUM - The decimal number as subsequent numbers
      character INPUT_NUM_STR*(MAX_STR_BUF)
      double precision NUM

c     ==== The statistics numbers
      double precision sum, avg, min, max

      integer lens
      integer padding
      integer fd

      padding = 32
      fd = 22

c     ==== Initialize string NITEM_STR with '\0'
c     ==== padding is a "WHILE SPACE", ASCII CODE 32 in decimal
      do i = 1,MAX_STR_BUF
          NITEM_STR(i:i) = char(padding)
      end do

c     ==== I am not sure if this is the best solution but it just works
c     ==== Probably need further learning for this
      open(fd, file='/proc/self/fd/0', access='stream', action='read')

      lens = 0

      do i = 1,MAX_STR_BUF
          read(fd, err=555, end=555) NITEM_STR(i:i)
          lens = lens + 1

          if (ichar(NITEM_STR(i:i)) .eq. 10) then
              NITEM_STR(i:i) = char(padding)
              lens = lens - 1
              go to 1123
          endif
      end do

c     ==== Read NITEM from console, on non-digit or EOF print ERR and exit
c      read (*,'(A255)',err=555,end=555) NITEM_STR

c     ==== Validate integer numbers
c      1. characters, scientific notation, etc. eliminated
c         decimals are eliminated
c         comma, space divided numbers are also eliminated
1123  if (is_integer(NITEM_STR, lens) .eq. 0) then
          go to 555
      endif

c      2. all numbers will come here
      read (NITEM_STR, * , err=555, end=555) NITEM

c      3. negative numbers eliminated
      if (NITEM .LT. 0) then
          go to 555
      endif

c     ==== Handle special case ZERO
      if (NITEM .eq. 0) then
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

          lens = 0

          do j = 1,MAX_STR_BUF
              INPUT_NUM_STR(j:j) = char(padding)
          end do

          do j = 1,MAX_STR_BUF
              read(fd, err=555, end=555) INPUT_NUM_STR(j:j)
              lens = lens + 1

              if (ichar(INPUT_NUM_STR(j:j)) .eq. 10) then
                  INPUT_NUM_STR(j:j) = char(padding)
                  lens = lens - 1
                  go to 1153
              endif
          end do

c     ==== Validate decimal numbers
c      1. eliminate scientific notations
c         eliminate letters
c         eliminate space or comma divided numbers
1153      if (is_decimal(INPUT_NUM_STR, lens) .eq. 0) then
              go to 555
          endif

          read (INPUT_NUM_STR, *,err=555,end=555) NUM

          if (i .eq. 1) then
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

c     #### close opened standard input
999   close(fd)
      stop

c     #### print "ERR" and jump to exit code
555   call print_error()
      go to 999

      end

c     ============ end of the program ===============




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

c        Only accept characters [0-9], +, - and . for standard decimal notation
         do i = 1, n
            k = ichar(s(i:i))
            if (k .LT. 48 .or. k .GT. 57) then
               if (k .ne. 43 .and. k .ne. 45 .and. k .ne. 46) then
                  is_decimal = 0
                  return
               end if
            end if
         end do

c        Hendle the other format of the scientific notation
c         3+3 as 3 * 10^3
c         3-3 as 3 * 10^-3
         if (index(s, "+") .gt. 1 .or. index(s, "-") .gt. 1) then
           is_decimal = 0
           return
         end if

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

c     =====================================
c      END OF THE PROGRAM
c     =====================================
