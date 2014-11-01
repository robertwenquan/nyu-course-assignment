      program gototest

      integer idx11
      write (*,*) "Input (1,2,3):"
      read (*,*) idx11

      GO TO (100, 200, 300, 555), idx11

c     integer NN=200

100   write (*,*) "Come to label 100"
      GO TO 555

200   write (*,*) "Come to label 200"
      GO TO 555

300   write (*,*) "Come to label 300"
      GO TO 555

555   write (*,*) "Come to label 555"
      write (*,*) "Exit"

      end
