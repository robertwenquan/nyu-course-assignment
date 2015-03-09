#!/usr/bin/awk -f

BEGIN{
  FS = ","
}

{
  key = $1
  val = $2

  if (LIST[key] == "") {
    LIST[key] = key "|" val
  } else {
    LIST[key] = LIST[key] "," val
  }
}

END {
  for (key in LIST)
  {
    print LIST[key] "|-1|WAIT|na"
  }
}
