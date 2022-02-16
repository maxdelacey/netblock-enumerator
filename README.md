# Netblock-Enumerator

Netblock-Enumerator is a simple command line tool written in python which queries WhoisXMLAPI for netblocks associated with a given organisation name.

Range2cidr will take a list of netblocks in the format "0.0.0.0 - 1.1.1.1" (one per line) and output the CIDR ranges.

## Installation

```
git clone https://github.com/0x680/netblock-enumerator.git

pip install requirements.txt 
```

## Usage - netblock-enumerator

You will need to register for an API key here: https://ip-netblocks.whoisxmlapi.com/api/signup

Allows for up to 1000 requests a month unpaid.

```
python3 netblock-enumerator.py [-h] -n ORG [-oC] [-oJ]

Queries WhoisXMLAPI with the specified organisation name and returns all
associated netblocks.

optional arguments:
  -h, --help  show this help message and exit
  -n ORG      Name of organisation to query.
  -oC         Ouput results to CSV in current directory. No need to specify
              filename.
  -oJ         Ouput full results to JSON in current directory. No need to
              specify filename.
```

## Usage - range2cidr

```
python3 range2cidr.py [-h] [-o OUTFILE] infile

Takes txt file as input containing ranges in the form "0.0.0.0 - 1.1.1.1" (one per line), converts to CIDR notation, and outputs to txt file

positional arguments:
  infile      Input file

optional arguments:
  -h, --help  show this help message and exit
  -o OUTFILE  Output file
```

## Output

Output will be printed to the command line. At this point it will have been trimmed to return only (hopefully) relevant information (i.e. the netblock, netblock name, description and/or registered organisation details). 

There is also the option to output to CSV or JSON. CSV output is also a cutdown version of the response. 

JSON output will be the full JSON response from the API.


#### Example

Command line output should look something like this:

```
Netblock                                                  Block Name                             Description    Organisation Name
--------------------------------------------------------  -------------------------------------  -------------  -------------------
50.220.179.216 - 50.220.179.223                           GOOGLE                                 None           Google
216.117.22.196 - 216.117.22.199                           CYRUSONE--C0000245-216-117-22-196-30   None           Google
68.112.55.16 - 68.112.55.23                               GGL-68-112-55-16                       None           Google
76.74.83.192 - 76.74.83.255                               GOOGLE-GTT                             None           Google
208.116.164.0 - 208.116.164.63                            GOOGLE-GTT                             None           Google
...
```

## Working with the output

Currently the output will be in ranges, not CIDR notation. To get just the relevant ranges quickly redirect terminal output to a text file and run:

```
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3} - ([0-9]{1,3}[\.]){3}[0-9]{1,3}" output.txt > ranges.txt

```
Then run range2cidr.py:

```
python range2cidr.py -i ranges.txt -o cidrs.txt
```
