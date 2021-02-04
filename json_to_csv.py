""" Converts a JSON file to CSV """
import argparse
from functools import reduce
import json
import sys


def encode_value(value, col_sep, encl='"'):
    """ convert a value to string and enclose with `encl`
        if it contains ','
    """
    if not isinstance(value, str):
        value = str(value)

    if col_sep in value:
        value = '{encl}{value}{encl}'.format(encl=encl, value=value)

    return value


def flatten(row, flat=None, prefix=None):
    """ convert nested objects to flat ones """
    flat = flat if flat else {}

    if not row:
        return flat

    key = next(iter(row))
    value = row.pop(key)

    if prefix:
        key = '{}.{}'.format(prefix, key)

    if not isinstance(value, dict):
        flat[key] = value
    else:
        flatten(value, flat, prefix=key)

    return flatten(row, flat, prefix=prefix)


def convert_json_to_csv(json_txt,
                        col_sep=',',
                        encl='"',
                        empty='',
                        crlf=False):
    """ convert a JSON string to csv """
    rows = json.loads(json_txt)
    rows = rows if isinstance(rows, list) else [rows]
    line_sep = '\n' if not crlf else '\r\n'

    # convert nested objects into flat objects with the new attributes in
    # the form "x.y.z"
    rows = list(map(flatten, rows))

    # collect the union set of the headers and sort it alphabetically.
    headers = sorted(reduce(lambda h, r: h | set(r.keys()), rows, set()))

    # fetch values for each row using `empty` for empty
    values = list(map(lambda r: [r.get(h, empty) for h in headers], rows))

    # join columns using `col_sep` and encode each value using `encode_value`
    output_lines = [
        col_sep.join([encode_value(value, col_sep, encl) for value in line])
        for line in ([headers] + values)
    ]

    return line_sep.join(output_lines)


def main():
    """ . """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        type=argparse.FileType('r', encoding='utf-8'))

    parser.add_argument('--col-sep',
                        help="Column separator, defaults to ','",
                        default=',')

    parser.add_argument('--crlf',
                        action='store_true',
                        help="Add CRLF at end lines, default False",
                        default=False)

    parser.add_argument('--encl',
                        help="Encloser char, defaults to '\"'",
                        default='"')

    parser.add_argument(
        '--empty',
        help="Value to use for empty strings defaults to empty string",
        default='')

    args = parser.parse_args(sys.argv[1:])

    try:
        csv = convert_json_to_csv(
            args.filename.read(),
            col_sep=args.col_sep,
            encl=args.encl,
            empty=args.empty,
            crlf=args.crlf)
    except json.JSONDecodeError as error:
        sys.exit('Error parsing JSON: {}'.format(error))
    else:
        print(csv)


if __name__ == '__main__':
    main()
