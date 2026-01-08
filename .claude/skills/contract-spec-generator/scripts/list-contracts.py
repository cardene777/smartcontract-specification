#!/usr/bin/env python3

"""
list-contracts.py

Solidityソースディレクトリからコントラクト一覧を取得

機能:
  - メインコントラクト（直接定義されたコントラクト）を抽出
  - 継承元コントラクトを解析
  - 継承関係のマップを生成
  - JSON形式で出力

使用方法:
  python3 list-contracts.py --contract-dir <dir> [--output <file>]

例:
  python3 list-contracts.py --contract-dir packages/contract/src --output docs/contract/contracts.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set


def find_solidity_files(directory: str) -> List[str]:
    """Solidityファイルを再帰的に検索"""
    solidity_files = []
    dir_path = Path(directory)

    if not dir_path.exists():
        return solidity_files

    for sol_file in dir_path.rglob("*.sol"):
        solidity_files.append(str(sol_file))

    return sorted(solidity_files)


def extract_main_contracts(sol_files: List[str]) -> List[str]:
    """メインコントラクト（直接定義されたコントラクト）を抽出"""
    contracts = set()

    for sol_file in sol_files:
        contract_name = Path(sol_file).stem

        with open(sol_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # contract, abstract contract, library, interface を検出
        pattern = r'^\s*(contract|abstract\s+contract|library|interface)\s+(\w+)'
        match = re.search(pattern, content, re.MULTILINE)

        if match:
            contracts.add(contract_name)

    return sorted(list(contracts))


def extract_inherited_contracts(sol_files: List[str]) -> List[str]:
    """継承元コントラクトを抽出"""
    inherited = set()

    for sol_file in sol_files:
        with open(sol_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # "contract X is Y, Z {" のパターンから継承元を抽出
        pattern = r'^\s*(contract|abstract\s+contract|library|interface)\s+\w+\s+is\s+([^{]+)'

        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                inheritance_list = match.group(2)
                # カンマ区切りで分割し、空白を除去
                parents = [s.strip() for s in inheritance_list.split(',')]
                for parent in parents:
                    if parent:
                        inherited.add(parent)

    return sorted(list(inherited))


def build_inheritance_map(sol_files: List[str]) -> Dict[str, List[str]]:
    """継承関係マップを生成"""
    inheritance_map = {}

    for sol_file in sol_files:
        contract_name = Path(sol_file).stem

        with open(sol_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # "contract X is Y, Z {" のパターンから継承元を抽出
        pattern = r'^\s*(contract|abstract\s+contract|library|interface)\s+(\w+)\s+is\s+([^{]+)'

        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                name = match.group(2)
                inheritance_list = match.group(3)
                parents = [s.strip() for s in inheritance_list.split(',') if s.strip()]

                if name == contract_name and parents:
                    inheritance_map[contract_name] = parents

    return inheritance_map


def main():
    parser = argparse.ArgumentParser(description='Solidityソースディレクトリからコントラクト一覧を取得')
    parser.add_argument('--contract-dir', required=True, help='Solidityソースディレクトリ')
    parser.add_argument('--output', help='出力ファイルパス')

    args = parser.parse_args()

    if not os.path.exists(args.contract_dir):
        print(f'エラー: ディレクトリが見つかりません: {args.contract_dir}', file=sys.stderr)
        sys.exit(1)

    print('🔍 コントラクト一覧を取得中...\n')

    # Solidityファイルを検索
    sol_files = find_solidity_files(args.contract_dir)
    print(f'   検出されたSolidityファイル: {len(sol_files)}')

    # メインコントラクトを抽出
    main_contracts = extract_main_contracts(sol_files)
    print(f'   メインコントラクト: {len(main_contracts)}')

    # 継承元コントラクトを抽出
    inherited_contracts = extract_inherited_contracts(sol_files)
    print(f'   継承元コントラクト: {len(inherited_contracts)}')

    # 継承関係マップを生成
    inheritance_map = build_inheritance_map(sol_files)

    # 全コントラクトリスト（重複削除）
    all_contracts = sorted(list(set(main_contracts + inherited_contracts)))
    print(f'   全コントラクト（重複削除後）: {len(all_contracts)}\n')

    # 結果をJSON形式で生成
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'sourceDirectory': args.contract_dir,
        'mainContracts': main_contracts,
        'inheritedContracts': inherited_contracts,
        'allContracts': all_contracts,
        'inheritanceMap': inheritance_map,
        'summary': {
            'totalSolidityFiles': len(sol_files),
            'mainContractsCount': len(main_contracts),
            'inheritedContractsCount': len(inherited_contracts),
            'allContractsCount': len(all_contracts)
        }
    }

    # 出力
    if args.output:
        # 出力ディレクトリが存在しない場合は作成
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f'✅ コントラクト一覧を保存: {args.output}')
    else:
        # 標準出力に出力
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'致命的なエラー: {error}', file=sys.stderr)
        sys.exit(1)
