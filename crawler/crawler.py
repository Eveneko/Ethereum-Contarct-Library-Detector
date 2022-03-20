#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from bs4 import BeautifulSoup
import csv
import json
import os
import requests
import shutil
import time


DEDAUB_LATEST_URL = 'https://library.dedaub.com/api/contracts'
DEDAUB_HOTTEST_URL = 'https://library.dedaub.com/api/hot_contracts'
DEDAUB_CONTRACTS_URL = 'https://library.dedaub.com/api/contracts/Ethereum/'
ETHERSCAN_CONTRACTS_VERIFIED_URL = 'https://etherscan.io/contractsVerified/'

CONTRACT_CSV = './data/contract.csv'
CONTRACT_FOLDER = './contract/'
fieldnames = ['Address', 'Contract Name', 'Compiler', 'Version', 'Balance', 'Txns', 'Verified']
POROSITY_EXECUTABLE = './porosity/porosity/porosity/porosity'

global_args = None


def get_hottest_contract_list():
    url = DEDAUB_HOTTEST_URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
        'Accept-Language': 'en-US,en;q=0.9',
        'Host': 'library.dedaub.com'
    }
    resp = requests.get(url=url, headers=headers, timeout=30)
    
    return resp.json()


def get_latest_contract_list():
    url = DEDAUB_LATEST_URL
    params = {
        'n': 'Ethereum',
        'q': '',
        't': 'address',
        's': 'block_number',
        'o': 'desc',
        'p': '2',
        'c': 'undefined',
        'has_source': '1',
        'has_decompiled': '1',
        'w': '',
        'block': 'undefined',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
        'Accept-Language': 'en-US,en;q=0.9',
        'Host': 'library.dedaub.com'
    }

    resp = requests.get(url=url, params=params, headers=headers, timeout=30)

    return resp.json()


def etherscan_contracts_verified():
    if not os.path.exists(CONTRACT_CSV):
        with open(CONTRACT_CSV, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    exist_contract_list = set()

    with open(CONTRACT_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        for row in reader:
            exist_contract_list.add(row['Address'])

    new_contract_count = 0

    with open(CONTRACT_CSV, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for i in range(1, 6):
            url = f'{ETHERSCAN_CONTRACTS_VERIFIED_URL}{i}?ps=100'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'etherscan.io'
            }
            resp = requests.get(url=url, headers=headers)
            print(f'[Status: {resp.status_code}] URL: {url}')

            content = resp.content
            soup = BeautifulSoup(content, 'html.parser')

            for row in soup.select('table.table-hover tbody tr'):
                cells = row.findAll('td')
                cells = map(lambda x: x.text, cells)
                address, contract_name, compiler, version, balance, txns, setting, verified, audited, license = cells
                if address.strip() not in exist_contract_list:
                    writer.writerow({
                        'Address': address.strip(),
                        'Contract Name': contract_name.strip(),
                        'Compiler': compiler.strip(),
                        'Version': version.strip(),
                        'Balance': balance.strip(),
                        'Txns': txns.strip(),
                        'Verified': verified.strip(),
                    })
                    new_contract_count = new_contract_count + 1
        
    print(f'[New] {new_contract_count} contracts')


def get_contract_details_from_address():
    if global_args.overwrite:
        try:
            shutil.rmtree(CONTRACT_FOLDER)
            os.mkdir(CONTRACT_FOLDER)
            print(f'[Overwrite] Remove all results and regenerate')
        except OSError as e:
            print(f'[Error] {e.filename} - {e.strerror}')


    with open(CONTRACT_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        next(reader)

        for row in reader:
            address = row['Address']
            contract_name = row['Contract Name']
            folder_name = f'{contract_name}_{address}'
            folder_path = os.path.join(CONTRACT_FOLDER, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            url = DEDAUB_CONTRACTS_URL + address
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'library.dedaub.com'
            }

            resp = requests.get(url=url, headers=headers, timeout=30)
            resp_dict = resp.json()

            bytecode = resp_dict['bytecode']
            decompiled = resp_dict['decompiled']
            disassembled = resp_dict['disassembled']
            source = resp_dict['source']

            bytecode_file = os.path.join(folder_path, 'bytecode')
            decompiled_file = os.path.join(folder_path, 'decompiled')
            disassembled_file = os.path.join(folder_path, 'disassembled')
            source_file = os.path.join(folder_path, 'source')
            cfg_dot_file = os.path.join(folder_path, "cfg.dot")
            cfg_pdf_file = os.path.join(folder_path, "cfg.pdf")

            if not os.path.exists(bytecode_file) and bytecode:
                    with open(bytecode_file, 'w') as f:
                        f.write(bytecode)

                # generate CFG
                # if not os.path.exists(cfg_dot_file) or not os.path.exists(cfg_pdf_file) :
                #     os.system(f'{POROSITY_EXECUTABLE} --code-file {os.path.join(folder_path, "bytecode")} --cfg-full > {cfg_dot_file}')
                #     os.system(f'dot -Tpdf {os.path.join(folder_path, "cfg.dot")} -o {cfg_pdf_file}')

            if not os.path.exists(decompiled_file) and decompiled:
                with open(decompiled_file, 'w') as f:
                    f.write(decompiled)

            if not os.path.exists(disassembled_file) and disassembled:
                with open(disassembled_file, 'w') as f:
                    f.write(disassembled)

            if not os.path.exists(source_file) and source:
                with open(source_file, 'w') as f:
                    f.write(source)

            print(f'[Complete] {contract_name}({address})')


def main():
    parser = argparse.ArgumentParser(description='library.dedaub.com scrapy')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()

    global global_args

    global_args = args

    etherscan_contracts_verified()

    get_contract_details_from_address()


if __name__ == '__main__':
    main()
