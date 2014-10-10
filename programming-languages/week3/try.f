      program inpdat
c
c  This program reads n points from a data file and stores them in 
c  3 arrays x, y, z.
c
      integer nmax, u
      parameter (nmax=1000, u=20)
      real x(nmax), y(nmax), z(nmax)
      character aa*(100)
      integer lenxx

      do i = 1,100
          aa(i:i) = char(0)
      end do

      CALL SYSTEM ("date")

      CALL SYSTEM ("stty -echo -icanon")

      lenxx = 0
      write(*,*) lenxx

      open(11,file='/proc/self/fd/0', access='stream', action='read')

      do i = 1,100

          read(11) aa(i:i)
          lenxx = lenxx + 1

          if (ichar(aa(i:i)) .eq. 10) then
              aa(i:i) = char(0)
              lenxx = lenxx - 1
              go to 1123
          endif

      end do


1123  CALL SYSTEM ("stty echo icanon")
      CALL SYSTEM ("date")

      write(*,*) aa, "ZZZZ"
      write(*,*) lenxx

      go to 9999

c  Open the data file
      open (u, FILE='points.dat', STATUS='OLD')

c  Read the number of points
      read(u,*) n
      if (n.GT.nmax) then
         write(*,*) 'Error: n = ', n, 'is larger than nmax =', nmax
         goto 9999
      endif

      read(u,'(A)', err=9999, end=9999) aa
      write(*,*) aa
      read(u,'(A)', err=9999, end=9999) aa
      write(*,*) aa

c  Close the file
      close (u)

c  Now we should process the data somehow...
c  (missing part)

 9999 stop
      end
