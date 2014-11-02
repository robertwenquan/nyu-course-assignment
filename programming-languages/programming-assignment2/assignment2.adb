------------------------------------------------------------------------
-- Programming Language Class Fall 2014 Semester
--   Programming Assignment 2
--
--   Quan Wen (robert.wen@nyu.edu) | netid: qw476
--
--   $Id$
------------------------------------------------------------------------

-- Resolved concerns from Professor Viega:
--
-- Oct 29
--
-- >>> Q: QUIT with argument
--   > A: No ERR, just quit
-- >>> Q: EOF on phase1
--   > A: Silently exit the program
-- >>> Q: Name conflict on phase 1
--   > A: Ignore and proceed to phase 2
--   > A: When any operation happens on the duplicated node, throw ERR
--   > A: Any syntax error should be thrown IMMEDIATELY at phase 1 with BAD
-- >>> Q: Could the list items be out of order?
--   > A: YES
-- >>> Q: Definition of inconsistent node
--   > A: If you would need to look at a node that doesn’t exist, then you should give a runtime error
-- >>> Q: Looped link?
--   > A: YES
-- >>> Q: Multiple nodes pointing to one?
--   > A: YES
-- >>> Q: Multiple lists allowed?
--   > A: YES
-- >>> Q: Mixed with loop, N-to-1, and multiple list?
--   > A: YES
-- >>> Q: LINKS for directly linking or indirectly linking?
--   > A: DIRECTLY linking
-- >>> Q: + and - sign allowed for the integers?
--   > A: YES
--   > A: Decimal notation, no scientific notation
--
-- Nov 1
--
-- >>> Q: command on looped list, throw err or detect loop and report correct answer?
--   > A: detect the loop
-- >>> Q: Only report ERR when we work on that item?
--   > A: YES
--   > A: Do not report ERR when that item is there but not worked
--
-- TODO: Unresolved concerns from Professor Viega:
--
-- Nov 2
--
-- >>> Q: Links with loop, 0 or 1?
--   > A:
-- >>> Q: Links with multiple lists, should we check dup for them?
--   > A:
-- >>> Q: typo on case2?
--   > A:
-- >>> Q: echo -n "" | ./assignment2
--   > A:
-- >>> Q: node with empty name
--   > A:
-- >>> Q: UNUSED, check dup for those unused or not?
--   > A:
-- >>> Q: C O U N T 1 works?
--   > A:
-- >>> Q: Integer range
--   > A:
-- >>> Q: Integer out-of-range handling
--   > A:
-- >>> Q: Integer overflow at sum: 2147483648
--   > A:
-- >>> Q: SUM with number and empty value mixture
--   > A:
-- >>> Q: empty value acceptance in phase 1? 2? or nothing?
--   > A:


with Ada.Text_IO;                         use Ada.Text_IO;
with Ada.Strings.Equal_Case_Insensitive;
with Ada.Strings.Unbounded;               use Ada.Strings.Unbounded;
with Ada.Strings.Unbounded.Text_IO;
with Ada.Characters.Handling;             use Ada.Characters.Handling;
with Ada.Strings;                         use Ada.Strings;
with Ada.Strings.Fixed;                   use Ada.Strings.Fixed;
with Ada.Integer_Text_IO;                 use Ada.Integer_Text_IO;
with Ada.Task_Identification;             use Ada.Task_Identification;


procedure assignment2 is

  package SU renames Ada.Strings.Unbounded;

  LineBuf   : SU.Unbounded_String;
  Str       : SU.Unbounded_String;
  Cmd       : SU.Unbounded_String;
  Arg       : SU.Unbounded_String;
  SPACE_LOC : Integer;
  DELIM_LOC : Integer;

  -- Function return value
  Ret : Integer := 0;

  NUM_OF_NODES : Integer := -1;

  type LinkNode is record
    Key     : SU.Unbounded_String;
    Value   : SU.Unbounded_String;
    Next    : SU.Unbounded_String;
  end record;

  --type LinkList is array (Integer range <>) of LinkNode;
  type LinkList is array (1..20000) of LinkNode;

  DataList : LinkList;

  use Ada.Text_IO;
  Function eq(Left, Right : String) return Boolean
    renames Ada.Strings.Equal_Case_Insensitive;


  Function Locate_Key(List : in LinkList; Key : in SU.Unbounded_String) return Integer is
    i : Integer := 1;
    n : Integer := 0;
  begin

    LOOP_FIND_START_NODE:
    while SU.To_String(List(i).Key) /= "" loop
      if (eq(SU.To_String(List(i).Key), SU.To_String(Key))) then
        return i;
      end if;
      i := i + 1;
    end loop LOOP_FIND_START_NODE;

    -- Not Found, return FALSE
    return -1;

  end Locate_Key;


  --
  -- Detect duplicate in the list
  --
  -- Assumption: The node exist at least once
  --
  Function Detect_Dup_With_First(List : in LinkList; Key : in SU.Unbounded_String; StartSearchIndex : Integer) return Boolean is
    i : Integer := 1;
    n : Integer := 0;
  begin

    i := StartSearchIndex + 1;

    LOOP_FIND_START_NODE:
    while SU.To_String(List(i).Key) /= "" loop
      if (eq(SU.To_String(List(i).Key), SU.To_String(Key))) then
        return True;
      end if;
      i := i + 1;
    end loop LOOP_FIND_START_NODE;

    -- Not Found, Good News, return False for not dup!
    return False;

  end Detect_Dup_With_First;


  Function Detect_Dup(List : in LinkList; Key : in SU.Unbounded_String) return Boolean is
    i : Integer := 1;
    n : Integer := 0;
    Found : Boolean := False;
    Dup   : Boolean := False;
  begin

    LOOP_FIND_START_NODE:
    while SU.To_String(List(i).Key) /= "" loop
      if (eq(SU.To_String(List(i).Key), SU.To_String(Key))) then
        Found := True;
        exit;
      end if;
      i := i + 1;
    end loop LOOP_FIND_START_NODE;

    if Found = True then
      return Detect_Dup_With_First(List, Key, i);
    else
      return False;
    end if;

  end Detect_Dup;


  Function Validate_Node(List : in LinkList; Key : in SU.Unbounded_String) return Boolean is
    i : Integer := 1;
    Dupli : Boolean;
  begin

    -- Check Availability of the start node
    -- If found, i will be the index of the start node to traverse
    i := Locate_Key(List, Key);
    if i = -1 then
      return False;
    end if;

    -- Check Duplicity of the start node
    Dupli := Detect_Dup_With_First(List, Key, i);
    if Dupli = True then
      return False;
    end if;

    return True;

  end Validate_Node;

  --
  -- COMMAND -- COUNT
  --
  Function CMD_COUNT(List : in LinkList; StartKey : in SU.Unbounded_String; PrintFlag : Boolean) return Integer is
    i : Integer := 1;
    n : Integer := 0;
    Valid : Boolean;
    Dupli : Boolean;
    next : SU.Unbounded_String;
  begin

    -- DONT replace with Validate_Node() because we need the index to proceed
    -- Check Availability of the start node
    -- If found, i will be the index of the start node to traverse
    i := Locate_Key(List, StartKey);
    if i = -1 then
      if PrintFlag = True then
        Put_Line("ERR");
      end if;
      return -1;
    end if;

    -- Check Duplicity of the start node
    Dupli := Detect_Dup_With_First(List, StartKey, i);
    if Dupli = True then
      if PrintFlag = True then
        Put_Line("ERR");
      end if;
      return -1;
    end if;

    -- Count the items
    n := 1;

    next := List(i).Next;

    -- If it's the end of the link, end the count procedure
    if SU.To_String(next) = "" then
      goto End_of_Count;
    end if;

    -- Detect Loop Here
    if SU.To_String(next) = SU.To_String(StartKey) then
      goto End_of_Count;
    end if;

    -- Validate next node when it exists
    Valid := Validate_Node(List, next);
    if Valid = False then
      if PrintFlag = True then
        Put_Line("ERR");
      end if;
      return -1;
    end if;

    i := 1;

    LOOP_COUNT_NODES:
    while SU.To_String(List(i).Key) /= "" loop
      if (eq(SU.To_String(List(i).Key), SU.To_String(next))) then
        n := n + 1;

        next := List(i).Next;

        -- If it's the end of the link, end the count procedure
        if SU.To_String(next) = "" then
          exit;
        end if;

        -- Detect Loop Here
        if SU.To_String(next) = SU.To_String(StartKey) then
          exit;
        end if;

        -- Validate next node when it exists
        Valid := Validate_Node(List, next);
        if Valid = False then
          if PrintFlag = True then
            Put_Line("ERR");
          end if;
          return -1;
        end if;

        i := 1;
      else
        i := i + 1;
      end if;
    end loop LOOP_COUNT_NODES;

    <<End_of_Count>>

    if PrintFlag = True then
      Put_Line(Trim(Source => Integer'Image(n), Side => Both));
    end if;

    return n;

  end CMD_COUNT;


  --
  -- COMMAND -- SUM
  --
  Procedure CMD_SUM(List : in LinkList; StartKey : in SU.Unbounded_String; IsString : Boolean) is
    i : Integer := 1;
    n : Integer := 0;
    sum : Integer := 0;
    sum_str : SU.Unbounded_String := SU.To_Unbounded_String("");
    next : SU.Unbounded_String;
    Dupli : Boolean;
    Valid : Boolean;
  begin

    -- DONT replace with Validate_Node() because we need the index to proceed
    -- Check Availability of the start node
    -- If found, i will be the index of the start node to traverse
    i := Locate_Key(List, StartKey);
    if i = -1 then
      Put_Line("ERR");
      return;
    end if;

    -- Check Duplicity of the start node
    Dupli := Detect_Dup_With_First(List, StartKey, i);
    if Dupli = True then
      Put_Line("ERR");
      return;
    end if;

    -- Count the items
    n := 1;

    --sum_str := "";

    if IsString = False then
      sum := sum + Integer'Value(SU.To_String(List(i).Value));
    else
      Append(sum_str, List(i).Value);
    end if;

    next := List(i).Next;

    -- If it's the end of the link, end the count procedure
    if SU.To_String(next) = "" then
      goto End_of_Sum;
    end if;

    -- Detect Loop Here
    if SU.To_String(next) = SU.To_String(StartKey) then
      goto End_of_Sum;
    end if;

    -- Validate next node when it exists
    Valid := Validate_Node(List, next);
    if Valid = False then
      Put_Line("ERR");
      return;
    end if;

    i := 1;

    LOOP_COUNT_NODES:
    while SU.To_String(List(i).Key) /= "" loop

      if SU.To_String(List(i).Key) = SU.To_String(next) then
        n := n + 1;

        if IsString = False then
          sum := sum + Integer'Value(SU.To_String(List(i).Value));
        else
          Append(sum_str, List(i).Value);
        end if;

        next := List(i).Next;

        -- If it's the end of the link, end the count procedure
        if SU.To_String(next) = "" then
          exit;
        end if;

        -- Detect Loop Here
        if SU.To_String(next) = SU.To_String(StartKey) then
          exit;
        end if;

        -- Validate next node when it exists
        Valid := Validate_Node(List, next);
        if Valid = False then
          Put_Line("ERR");
          return;
        end if;

        i := 1;
      else
        i := i + 1;
      end if;
    end loop LOOP_COUNT_NODES;

    <<End_of_Sum>>

    if IsString = False then
      Put_Line(Trim(Source => Integer'Image(sum), Side => Both));
    else
      Put_Line(SU.To_String(sum_str));
    end if;

  end CMD_SUM;


  --
  -- COMMAND -- UNUSED
  --
  Procedure CMD_UNUSED(List : in LinkList; StartKey : in SU.Unbounded_String) is
    n_unused : Integer;
    n_count  : Integer;
  begin

    n_count  := CMD_COUNT(DataList, StartKey, False);

    if n_count = -1 then
      Put_Line("ERR");
      return;
    end if;

    n_unused := NUM_OF_NODES - n_count;
    Put_Line(Trim(Source => Integer'Image(n_unused), Side => Both));

  end CMD_UNUSED;


  --
  -- COMMAND -- LINKS
  --
  Procedure CMD_LINKS(List : in LinkList; StartKey : in SU.Unbounded_String) is
    i : Integer := 1;
    n : Integer := 0;
    Valid : Boolean;
    next : SU.Unbounded_String;
  begin

    -- Check Availability of the start node
    Valid := Validate_Node(List, StartKey);
    if Valid = False then
      Put_Line("ERR");
      return;
    end if;

    -- Count the links
    i := 1;
    n := 0;

    LOOP_COUNT_LINKS:
    while SU.To_String(List(i).Key) /= "" loop
      Valid := Validate_Node(List, List(i).Key);
      if Valid = False then
        Put_Line("ERR");
        return;
      end if;

      if (eq(SU.To_String(List(i).Next), SU.To_String(StartKey))) then
        n := n + 1;
      end if;

      i := i + 1;
    end loop LOOP_COUNT_LINKS;
    
    Put_Line(Trim(Source => Integer'Image(n), Side => Both));

  end CMD_LINKS;


  Function Is_String(ValueStr : in SU.Unbounded_String) return Boolean is
    i : Integer := 1;
    n : Integer := 0;
  begin

    -- Empty String is String
    if (SU.To_String(ValueStr) = "") then
      return True;
    end if;

    -- First check the sign bit
    if (Is_Digit(Element(ValueStr, 1)) = False and Element(ValueStr, 1) /= '+' and Element(ValueStr, 1) /= '-') then
      return True;
    end if;

    -- Next check the other digit bit
    -- If there are numbers, should be all numbers
    n := Length(ValueStr);

    VALUE_CHECK_LOOP:
    for i in 2..n loop
      if (Is_Digit(Element(ValueStr, i)) = False) then
        return True;
      end if;
    end loop VALUE_CHECK_LOOP;

    return False;

  end Is_String;


  --
  -- Validate the key if it is alphanumeric
  --
  Function Validate_AlphaNumeric(KeyStr : in SU.Unbounded_String) return Boolean is
    i : Integer := 1;
    n : Integer := 0;
    next : SU.Unbounded_String;
  begin

    n := Length(KeyStr);

    KEY_LOOP:
    for i in 1..n loop
      if (Is_Alphanumeric(Element(KeyStr, i)) = False) then
        return False;
      end if;
    end loop KEY_LOOP;

    return True;

  end Validate_AlphaNumeric;


  Procedure ParseLineInput(Line : in SU.Unbounded_String; 
                           Key  : in out SU.Unbounded_String;
                           Value: in out SU.Unbounded_String;
                           Next : in out SU.Unbounded_String;
                           Ret  : in out Integer;
                           IsStr: in out Boolean) is
    Buf : SU.Unbounded_String;
  begin

    -- Validate input line
    --  The following cases will be bad:
    --   - Not seperate by two semicolons ";"
    --   - Space in the 1st and 3rd field
    --   - Not legitimate character sets in 1st and 3rd set

    -- Check the 1st ";"
    DELIM_LOC := SU.Index(Line, ";");
    if (DELIM_LOC <= 0) then
      Ret := -1;
      return;
    end if;

    Key := SU.To_Unbounded_String(SU.Slice(Line, 1, DELIM_LOC-1));
    Buf := SU.To_Unbounded_String(SU.Slice(Line, DELIM_LOC+1, Length(Line)));

    -- Check Empty key
    if (SU.To_String(Key) = "") then
      Ret := -1;
      return;
    end if;

    -- Validate the key
    if (Validate_AlphaNumeric(Key) = False) then
      Ret := -1;
      return;
    end if;

    -- Check the 2nd ";"
    DELIM_LOC := SU.Index(Buf, ";");
    if (DELIM_LOC <= 0) then
      Ret := -1;
      return;
    end if;

    if (DELIM_LOC = 1) then
      Value := SU.To_Unbounded_String("");
    else
      Value := SU.To_Unbounded_String(SU.Slice(Buf, 1, DELIM_LOC-1));
    end if;

    -- Check whether value is string or integer
    if (IsStr = False) then
      IsStr := Is_String(Value);
    end if;
    
    Next  := SU.To_Unbounded_String(SU.Slice(Buf, DELIM_LOC+1, Length(Buf)));

    -- Check the 3nd ";"
    DELIM_LOC := SU.Index(Next, ";");
    if (DELIM_LOC > 0) then
      Ret := -1;
      return;
    end if;

    -- Validate the pointer name to the next
    if (Validate_AlphaNumeric(Next) = False) then
      Ret := -1;
      return;
    end if;

    Ret := 0;
    return;
  end ParseLineInput;

-- Variable Declaration
  DataIdx : Integer := 0;

  Input_Key   : SU.Unbounded_String;
  Input_Value : SU.Unbounded_String;
  Input_Next  : SU.Unbounded_String;

  String_Flag : Boolean := False;

begin

  --
  -- Phase 1, get the input
  --   Exit Condition is an empty line
  --
  loop

    -- Handle EOF, exit the program when met
    --if End_Of_File then
    --  goto ExitProgram;
    --end if;

    SU.Text_IO.Get_Line(LineBuf);

    -- EMPTY line indicates the end of phase 1
    -- Exit the loop and proceed to phase 2
    if (SU.To_String(LineBuf) = "") then
      exit;
    end if;

    DataIdx := DataIdx + 1;

    -- Get Input
    ParseLineInput(LineBuf, DataList(DataIdx).Key, DataList(DataIdx).Value, DataList(DataIdx).Next, Ret, String_Flag);

    if (Ret = -1) then
      Put_Line("BAD");
      goto ExitProgram;
    end if;

  end loop;

  NUM_OF_NODES := DataIdx;

  --
  -- Phase 2, processing the command
  --

  -- Handle EOF, exit the loop when met
  loop
  --Put_Line("aaaa");
  --while (not End_Of_File) loop

    -- Handle EOF, exit the program when met
    SU.Text_IO.Get_Line(Str);
    Str := SU.To_Unbounded_String(Trim(Source => SU.To_String(Str), Side => Both));

    -- If it's empty string, print ERR without further processing
    if SU.To_String(Str) = "" then
      Put_Line("ERR");
      goto Continue;
    end if;

    --if End_Of_File then
    --  goto ExitProgram;
    --end if;

    -- Get the first space after the command
    SPACE_LOC := SU.Index(Str, " ");
    if (SPACE_LOC > 0) then
      Cmd := SU.To_Unbounded_String(SU.Slice(Str, 1, SPACE_LOC-1));
      --SU.Text_IO.Put_Line(Cmd);
    else
      Cmd := Str;
    end if;

    --SU.Text_IO.Put_Line(Cmd);

    -- if here is with argument, dont care about the extra arguments
    if (eq(SU.To_String(Cmd), "QUIT")) then
      exit;
    end if;

    -- get the parameter
    -- only 1 parameter is allowed for each command
    -- and it must be integer

    if (SPACE_LOC = 0) then
      Put_Line("ERR");
      goto Continue;
    end if;

    -- At this point, there are at least one argument
    Arg := SU.To_Unbounded_String(Trim(Source => SU.Slice(Str, SPACE_LOC, SU.Length(Str)), Side => Both));

    SPACE_LOC := SU.Index(Arg, " ");
    if (SPACE_LOC > 0) then
      Put_Line("ERR");
      goto Continue;
    end if;

    -- Argument alphanumeric check
    if (Validate_AlphaNumeric(Arg) = False) then
      Put_Line("ERR");
      goto Continue;
    end if;
    
    -- add global check : Validate the argument as a node name
    if (Validate_Node(DataList, Arg) = False) then
      Put_Line("ERR");
      goto Continue;
    end if;

    -- At this point, there should be with only one argument
    -- and the argument is with valid range(alphanumeric)
    -- and it should also be a existing and non-dup node

    if (eq(SU.To_String(Cmd), "COUNT")) then
      Ret := CMD_COUNT(DataList, Arg, True);
    elsif (eq(SU.To_String(Cmd), "SUM")) then
      CMD_SUM(DataList, Arg, String_Flag);
    elsif (eq(SU.To_String(Cmd), "UNUSED")) then
      CMD_UNUSED(DataList, Arg);
    elsif (eq(SU.To_String(Cmd), "LINKS")) then
      CMD_LINKS(DataList, Arg);
    else
      Put_Line("ERR");
    end if;

    <<Continue>>
    null;

  end loop;

  <<ExitProgram>>
  null;

exception
  when Error: END_ERROR =>
    if (NUM_OF_NODES = -1 and DataList(1).Key = "") then
      Put_Line("BAD");
    end if;

  when Error: CONSTRAINT_ERROR =>
    Put_Line("ERR");

end assignment2; 

