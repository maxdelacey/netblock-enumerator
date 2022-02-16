#!/usr/bin/env python3

import netaddr
import argparse
import re
import sys

parser = argparse.ArgumentParser(
    description='Takes txt file as input containing ranges in the form "0.0.0.0 - 1.1.1.1" (one per line), converts to CIDR notation, and outputs to another txt file')
parser.add_argument(
    "-i",
    required=True,
    dest="infile",
    help="Input file")

parser.add_argument(
    "-o",
    required=False,
    dest="outfile",
    help="Output file")
args = parser.parse_args()

def main():

    try:
        infile = args.infile
        complete = []
        with open(infile, 'r') as f:
            lines = f.readlines()
        for range in lines:
            start_ip = range.split('-', 1)[0]
            range_end = range.split('-', 1)[1]
            end_ip = range_end.strip('\n')
            complete.append(netaddr.iprange_to_cidrs(start_ip, end_ip))

        pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)")
        compressed = ' '.join([str(elem) for elem in complete])
        result = re.findall(pattern, compressed)
        return '\n'.join(result)
    except:
        print('Something went wrong, check input file contains ranges in the form "0.0.0.0 - 1.1.1.1", one per line.')
        sys.exit(-1)
    

def write_output():

    if args.outfile:
        try:
            outfile = open(args.outfile, "wt")
            outfile.write(main())
            outfile.close()   
        except:
            pass 

if __name__ == '__main__':
    print(main())
    write_output()

