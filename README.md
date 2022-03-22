# Ethereum Contarct Library Detector

ELDER - Ethereum Library DEtectoR

## 🏠 Structure

```
./
├── LICENSE
├── README.md
├── contract
├── data
├── elder
├── elder_cli.py
├── requirements.txt
└── venv
```

## 🔨 Build

```
git clone https://github.com/Eveneko/Ethereum-Contarct-Library-Detector.git --depth 1

python3 -m venv venv
source venv/bin/activate    

pip install -r requirements.txt
```

## 🚀 Run

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


## 🧾 TODO

- [x] ETH contract crawler
- [ ] get CFG
- [ ] extract function 
- [ ] function tokenized
