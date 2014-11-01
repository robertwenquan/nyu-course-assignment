c    This is a Fortran program
      program test

c     parameter (pi = 3.1415926)
      pi = 3.1415926

      write (*,*) "Hello World!"
      r = 12.0
      x = areaf(pi, r)
      write (*,*) pi

      integer xx = 1
      integer yy = 2
      integer zz = 1

      integer s = 1

      DO n = 1, 2, 1
        s = s * n
        write (*,*) s
      END DO

      end

      function areaf(p, r)
        p = 13
        areaf = p * r ** 2
      end function
