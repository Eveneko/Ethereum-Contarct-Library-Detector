# Ethereum Contarct Library Detector

ELDER - Ethereum Library DEtectoR

## ๐  Structure

```
./
โโโ LICENSE
โโโ README.md
โโโ contract
โโโ data
โโโ elder
โโโ elder_cli.py
โโโ requirements.txt
โโโ venv
```

## ๐จ Build

```
git clone https://github.com/Eveneko/Ethereum-Contarct-Library-Detector.git --depth 1

python3 -m venv venv
source venv/bin/activate    

pip install -r requirements.txt
```

## ๐ Run

```
$ python3 elder_cli.py
usage: elder_cli.py [-h] [-v] [-vv] {crawler} ...

ELDER - Ethereum Library DEtectoR

positional arguments:
  {crawler}      sub-command parser
    crawler      crawler parser

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  emit verbose debug output to stderr.
  -vv, --prolix  higher verbosity level, including extra debug messages from dataflow analysis and elsewhere.
```


## ๐งพ TODO

- [x] ETH contract crawler
- [ ] get CFG
- [ ] extract function 
- [ ] function tokenized
