with Ada.Text_IO;   -- Tell compiler to use i/o library
use  Ada.Text_IO;   -- Use library routines w/o fully qualified names

procedure hello is
begin
  put("Hello World!\n");
  Ada.Text_IO.Put_Line ("Hello world in Ada!");
end hello;

procedure A_Test (A, B: in Integer; C: out Integer) is
begin
   C := A + B;
end A_Test;
