#!/usr/bin/awk -f

BEGIN{
  FS = ","
}

{
  key = $1
  val = $2

  if (LIST[key] == "") {
    LIST[key] = key "\t" val
  } else {
    LIST[key] = LIST[key] "," val
  }
}

END {
  n = length(LIST)
  asort(LIST)
  for (key=0;key<n;key++)
  {
    if (LIST[key] == "") {
      continue
    }

    if (substr(LIST[key], 0, 2) == "1\t") {
      print LIST[key] "|0|TODO|root"
    }
    else {
      print LIST[key] "|-1|WAIT|na"
    }
  }
}
