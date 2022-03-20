# Ethereum Contarct Library Detector

## 🚀 Structure

```
./
├── LICENSE
├── README.md
├── contract
├── crawler
├── data
├── log
└── venv
```

## 🔨 Build

```
git clone https://github.com/Eveneko/Ethereum-Contarct-Library-Detector.git --depth 1

python3 -m venv venv
source venv/bin/activate    

pip install -r requirements.txt
```

## 🕷️ Crawler

clean results and regenerate

```
python3 crawler/crawler.py --overwrite
```

## 🧾 TODO

- [x] ETH contract crawler
- [ ] get CFG
- [ ] function tokenized
