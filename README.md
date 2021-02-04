# json_to_csv
Converts a JSON file to CSV
usage: json_to_csv.py [-h] [--col-sep COL_SEP] [--crlf] [--encl ENCL]
                      [--empty EMPTY]
                      filename

positional arguments:
  filename

optional arguments:
  -h, --help         show this help message and exit
  --col-sep COL_SEP  Column separator, defaults to ','
  --crlf             Add CRLF at end lines, default False
  --encl ENCL        Encloser char, defaults to '"'
  --empty EMPTY      Value to use for empty strings defaults to empty string
