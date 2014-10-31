with Ada.Text_IO;                         use  Ada.Text_IO;
with Ada.Strings.Equal_Case_Insensitive;
with Ada.Strings.Unbounded;
with Ada.Strings.Unbounded.Text_IO;
with Ada.Characters.Handling;             use Ada.Characters.Handling;
with Ada.Strings;                         use Ada.Strings;
with Ada.Strings.Fixed;                   use Ada.Strings.Fixed;
with Ada.Integer_Text_IO;                 use Ada.Integer_Text_IO;

procedure stdio is

  package SU renames Ada.Strings.Unbounded;

  Str : SU.Unbounded_String;
  Cmd : SU.Unbounded_String;
  Arg : SU.Unbounded_String;
  SPACE_LOC : Integer;

  -- Function return value
  Ret : Integer;

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


begin

  --
  -- Phase 1, get the input
  --

  DataList(1) := (SU.To_Unbounded_String("1"), SU.To_Unbounded_String("100"), SU.To_Unbounded_String("2"));
  DataList(2) := (SU.To_Unbounded_String("2"), SU.To_Unbounded_String("200"), SU.To_Unbounded_String("3"));
  DataList(3) := (SU.To_Unbounded_String("3"), SU.To_Unbounded_String("300"), SU.To_Unbounded_String("4"));
  DataList(4) := (SU.To_Unbounded_String("4"), SU.To_Unbounded_String("400"), SU.To_Unbounded_String(""));

  NUM_OF_NODES := 4;

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

end stdio; 

