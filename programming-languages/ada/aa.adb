with Ada.Numerics.Elementary_Functions;
use  Ada.Numerics.Elementary_Functions;

procedure Quadratic_Equation
   (A, B, C :     Float;   -- By default it is "in".
    R1, R2  : out Float;
    Valid   : out Boolean)
is
   Z : Float;
begin
   Z := B**2 - 4.0 * A * C;
   if Z < 0.0 or A = 0.0 then
      Valid := False;  -- Being out parameter, it should be modified at least once.
      R1    := 0.0;
      R2    := 0.0;
   else
      Valid := True;
      R1    := (-B + Sqrt (Z)) / (2.0 * A);
      R2    := (-B - Sqrt (Z)) / (2.0 * A);
   end if;
end Quadratic_Equation;
