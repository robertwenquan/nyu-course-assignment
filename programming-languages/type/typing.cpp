#include <iostream>
#include <cstdio>

class Base {
    public:
        int publicMember;

        void setprotected(int n)
        {
          protectedMember = n;
        }

        int getprotected()
        {
          return protectedMember;
        }

        void setprivate(int n)
        {
          privateMember = n;
        }

        int getprivate()
        {
          return privateMember;
        }

    protected:
        int protectedMember;

    private:
        int privateMember;
};

class Sub: public Base {

  public:
    int getprotectedfromsubclass() {
      return protectedMember;
    }

    /*
     * this won't compile because private member is not accessile outside of the parent class 
    int getprivatefromsubclass() {
      return privateMember;
    }
    */

};

int main()
{
  Base aa;

  aa.publicMember = 100;
  printf("direct access to publicMember = %d\n", aa.publicMember);

  /*
  aa.protectedMember = 200;
  printf("direct access to protectedMember = %d\n", aa.protectedMember);
  */

  aa.setprotected(222);
  printf("access to protectedMember = %d\n", aa.getprotected());

  aa.setprivate(333);
  //printf("direct access to privateMember = %d\n", aa.privateMember);
  printf("access to privateMember = %d\n", aa.getprivate());

  Sub bb;
  bb.publicMember = 888;
  //bb.protectedMember = 344;
  bb.setprotected(433);
  printf("access to inherited protectedMember = %d\n", bb.getprotectedfromsubclass());

  bb.setprivate(455);
  printf("access to inherited privateMember = %d\n", bb.getprivate());
}

