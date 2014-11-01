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

  NUM_OF_NODES : Integer;

  type LinkNode is record
    Key     : SU.Unbounded_String;
    Value   : SU.Unbounded_String;
    Next    : SU.Unbounded_String;
  end record;

  --type LinkList is array (Integer range <>) of LinkNode;
  type LinkList is array (1..12243) of LinkNode;

  --DataList : LinkList := ((1, SU.To_Unbounded_String("200"), 2), (2, SU.To_Unbounded_String("300"), 3), (3, SU.To_Unbounded_String("300"), 4));
  DataList : LinkList;

  use Ada.Text_IO;
  Function eq(Left, Right : String) return Boolean
    renames Ada.Strings.Equal_Case_Insensitive;

  --
  -- COUNT
  --
  Function CMD_COUNT(List : in LinkList; StartKey : in SU.Unbounded_String; PrintFlag : Boolean) return Integer is
    i : Integer := 1;
    n : Integer := 0;
    next : SU.Unbounded_String;
  begin

    -- Find the start node
    i := 1;
    LOOP_FIND_START_NODE:
    while SU.To_String(List(i).Key) /= "" loop
      if SU.To_String(List(i).Key) = SU.To_String(StartKey) then
        exit LOOP_FIND_START_NODE;
      end if;
      i := i + 1;
    end loop LOOP_FIND_START_NODE;

    -- For starting node Not Found
    if SU.To_String(List(i).Key) = "" then
      if PrintFlag = True then
        Put_Line("ERR");
      end if;
      return -1;
    end if;

    -- Count the items
    n := 1;

    next := List(i).Next;

    i := 1;

    LOOP_COUNT_NODES:
    while SU.To_String(List(i).Key) /= "" loop

      if SU.To_String(List(i).Key) = SU.To_String(next) then
        n := n + 1;
        next := List(i).Next;
        i := 1;
      else
        i := i + 1;
      end if;
    end loop LOOP_COUNT_NODES;

    if PrintFlag = True then
      Put_Line(Trim(Source => Integer'Image(n), Side => Both));
    end if;

    return n;

  end CMD_COUNT;

  --
  -- SUM
  --
  Procedure CMD_SUM(List : in LinkList; StartKey : in SU.Unbounded_String; IsString : Boolean) is
    i : Integer := 1;
    n : Integer := 0;
    sum : Integer := 0;
    sum_str : String := "";
    next : SU.Unbounded_String;
  begin

    -- Find the start node
    i := 1;
    LOOP_FIND_START_NODE:
    while SU.To_String(List(i).Key) /= "" loop
      if SU.To_String(List(i).Key) = SU.To_String(StartKey) then
        exit LOOP_FIND_START_NODE;
      end if;
      i := i + 1;
    end loop LOOP_FIND_START_NODE;

    -- For starting node Not Found
    if SU.To_String(List(i).Key) = "" then
      Put_Line("ERR");
      return;
    end if;

    -- Count the items
    n := 1;
    --sum_str := "";

    if IsString = False then
      sum := sum + Integer'Value(SU.To_String(List(i).Value));
    else
      sum_str := "xx";
    end if;

    next := List(i).Next;

    i := 1;

    LOOP_COUNT_NODES:
    while SU.To_String(List(i).Key) /= "" loop

      if SU.To_String(List(i).Key) = SU.To_String(next) then
        n := n + 1;

        if IsString = False then
          sum := sum + Integer'Value(SU.To_String(List(i).Value));
        else
          sum_str := "xx xx";
        end if;

        next := List(i).Next;
        i := 1;
      else
        i := i + 1;
      end if;
    end loop LOOP_COUNT_NODES;

    if IsString = False then
      Put_Line(Trim(Source => Integer'Image(sum), Side => Both));
    else
      Put_Line(sum_str);
    end if;

  end CMD_SUM;


  --
  -- UNUSED
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
  -- LINKS
  --
  Procedure CMD_LINKS(List : in LinkList; StartKey : in SU.Unbounded_String) is
  begin
    Put_Line("LINKS!!!");
  end CMD_LINKS;


  Function Check_List_Item(Line : in SU.Unbounded_String) return Boolean is
    i : Integer := 1;
    n : Integer := 0;
    next : SU.Unbounded_String;
  begin

    return True;

  end Check_List_Item;


  Procedure ParseLineInput(Line : in SU.Unbounded_String; 
                           Key  : in out SU.Unbounded_String;
                           Value: in out SU.Unbounded_String;
                           Next : in out SU.Unbounded_String;
                           Ret  : in out Integer) is
    Buf : SU.Unbounded_String;
  begin

    -- Validate input line
    --  The following cases will be bad:
    --   - Not seperate by two semicolons ";"
    --   - Space in the 1st and 3rd field
    --   - Not legitimate character sets in 1st and 3rd set
    if (Check_List_Item(Line) = False) then
      Ret := -1;
      return;
    end if;

    -- Check the 1st ";"
    DELIM_LOC := SU.Index(Line, ";");
    if (DELIM_LOC <= 0) then
      Ret := -1;
      return;
    end if;

    Key := SU.To_Unbounded_String(SU.Slice(Line, 1, DELIM_LOC-1));
    Buf := SU.To_Unbounded_String(SU.Slice(Line, DELIM_LOC+1, Length(Line)));

    -- Check the 1st ";"
    DELIM_LOC := SU.Index(Buf, ";");
    if (DELIM_LOC <= 0) then
      Ret := -1;
      return;
    end if;

    Value := SU.To_Unbounded_String(SU.Slice(Buf, 1, DELIM_LOC-1));
    Next  := SU.To_Unbounded_String(SU.Slice(Buf, DELIM_LOC+1, Length(Buf)));

    Ret := 0;
    return;
  end ParseLineInput;

-- Variable Declaration
  DataIdx : Integer := 0;

  Input_Key   : SU.Unbounded_String;
  Input_Value : SU.Unbounded_String;
  Input_Next  : SU.Unbounded_String;

begin

  --
  -- Phase 1, get the input
  --   Exit Condition is an empty line
  --
  loop
    SU.Text_IO.Get_Line(LineBuf);

    -- EMPTY line indicates the end of phase 1
    -- Exit the loop and proceed to phase 2
    if (SU.To_String(LineBuf) = "") then
      exit;
    end if;

    DataIdx := DataIdx + 1;

    -- Get Input
    ParseLineInput(LineBuf, DataList(DataIdx).Key, DataList(DataIdx).Value, DataList(DataIdx).Next, Ret);

    if (Ret = -1) then
      Put_Line("BAD");
      Abort_Task (Current_Task);
    end if;

    --DataList(DataIdx).Key   := SU.To_Unbounded_String("1");
    --DataList(DataIdx).Value := SU.To_Unbounded_String("100");
    --DataList(DataIdx).Next  := SU.To_Unbounded_String("2");

    Put_Line(SU.To_String(DataList(DataIdx).Key));

  end loop;

  NUM_OF_NODES := DataIdx;

  Put_Line("END of DATA!!");

  --
  -- Phase 2, processing the command
  --
  loop
    SU.Text_IO.Get_Line(Str);
    Str := SU.To_Unbounded_String(Trim(Source => SU.To_String(Str), Side => Both));

    -- Get the first space after the command
    SPACE_LOC := SU.Index(Str, " ");
    if (SPACE_LOC > 0) then
      Cmd := SU.To_Unbounded_String(SU.Slice(Str, 1, SPACE_LOC-1));
      --SU.Text_IO.Put_Line(Cmd);
    else
      Cmd := Str;
    end if;

    --SU.Text_IO.Put_Line(Cmd);

    --FIXME: if here is with argument, how to handle it??
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

    -- At this point, there should be with only one argument
    -- FIXME: still need numeric check
    
    if (eq(SU.To_String(Cmd), "COUNT")) then
      Ret := CMD_COUNT(DataList, Arg, True);
    elsif (eq(SU.To_String(Cmd), "SUM")) then
      CMD_SUM(DataList, Arg, False);
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

end assignment2; 

