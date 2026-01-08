#!/usr/bin/env python3

"""
filter-contracts.py

コントラクトリストから不要なコントラクトを除外

機能:
  - スコープ選択（main/related/all）に応じてコントラクトをフィルタ
  - テスト、モック、インターフェース等の除外カテゴリを適用
  - 除外されたコントラクトをカテゴリ別に記録
  - JSON形式で出力

使用方法:
  python3 filter-contracts.py --input <file> --scope <main|related|all> [--output <file>]

例:
  python3 filter-contracts.py \
    --input docs/contract/contracts.json \
    --scope main \
    --output docs/contract/filtered.json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# 除外パターン定義
EXCLUDE_PATTERNS = {
    'test': [
        re.compile(r'Test$'),           # *Test
        re.compile(r'TestBase$'),       # *TestBase
        re.compile(r'TestImpl$')        # *TestImpl
    ],
    'mock': [
        re.compile(r'^Mock')            # Mock*
    ],
    'interface': [
        re.compile(r'^I[A-Z]')          # I* (大文字で始まる)
    ],
    'library': [
        re.compile(r'Lib$')             # *Lib
    ],
    'helper': [
        re.compile(r'Helper'),          # *Helper*
        re.compile(r'Utils$')           # *Utils
    ],
    'script': [
        re.compile(r'Script$'),         # *Script
        re.compile(r'^Deploy'),         # Deploy*
        re.compile(r'^Upgrade')         # Upgrade*
    ],
    'forge': [
        re.compile(r'^Vm'),             # Vm*
        re.compile(r'^console'),        # console*
        re.compile(r'^std'),            # std*
        re.compile(r'^Common')          # Common*
    ]
}


def categorize_contract(contract_name: str) -> str:
    """コントラクトが除外パターンに一致するか判定"""
    for category, patterns in EXCLUDE_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(contract_name):
                return category
    return None  # 除外対象外


def filter_contracts(contracts: List[str]) -> Tuple[List[str], Dict[str, List[str]]]:
    """コントラクトリストをフィルタリング"""
    selected = []
    excluded = {
        'test': [],
        'mock': [],
        'interface': [],
        'library': [],
        'helper': [],
        'script': [],
        'forge': []
    }

    for contract in contracts:
        category = categorize_contract(contract)

        if category:
            # 除外対象
            excluded[category].append(contract)
        else:
            # 選択対象
            selected.append(contract)

    return sorted(selected), excluded


def get_contracts_by_scope(contracts_data: dict, scope: str) -> List[str]:
    """スコープに応じたコントラクトリストを取得"""
    if scope == 'main':
        return contracts_data['mainContracts']
    elif scope == 'related':
        # メインコントラクト + 直接継承されているコントラクト
        main_set = set(contracts_data['mainContracts'])
        related_set = set(contracts_data['mainContracts'])

        # 継承マップから直接の親を追加
        inheritance_map = contracts_data.get('inheritanceMap', {})
        for parents in inheritance_map.values():
            for parent in parents:
                if parent in main_set:
                    related_set.add(parent)

        return sorted(list(related_set))
    elif scope == 'all':
        return contracts_data['allContracts']
    else:
        raise ValueError(f'不明なスコープ: {scope} (main/related/all のいずれかを指定)')


def main():
    parser = argparse.ArgumentParser(description='コントラクトリストから不要なコントラクトを除外')
    parser.add_argument('--input', required=True, help='入力ファイルパス')
    parser.add_argument('--scope', required=True, choices=['main', 'related', 'all'], help='スコープ')
    parser.add_argument('--output', help='出力ファイルパス')

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f'エラー: 入力ファイルが見つかりません: {args.input}', file=sys.stderr)
        sys.exit(1)

    print('🔍 コントラクトをフィルタリング中...\n')

    # 入力JSONを読み込み
    with open(args.input, 'r', encoding='utf-8') as f:
        contracts_data = json.load(f)

    # スコープに応じたコントラクトリストを取得
    scoped_contracts = get_contracts_by_scope(contracts_data, args.scope)
    print(f'   スコープ: {args.scope}')
    print(f'   対象コントラクト: {len(scoped_contracts)}')

    # フィルタリング実行
    selected, excluded = filter_contracts(scoped_contracts)

    # 除外数を計算
    excluded_count = sum(len(v) for v in excluded.values())

    print(f'   除外されたコントラクト: {excluded_count}')
    print(f'   最終的な選択コントラクト: {len(selected)}\n')

    # 除外の詳細を表示
    if excluded_count > 0:
        print('📋 除外されたコントラクト（カテゴリ別）:')
        for category, contracts in excluded.items():
            if contracts:
                print(f'   {category}: {len(contracts)}個')
                for c in contracts:
                    print(f'      - {c}')
        print('')

    # 結果をJSON形式で生成
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'scope': args.scope,
        'selected': selected,
        'excluded': excluded,
        'summary': {
            'totalInput': len(scoped_contracts),
            'selectedCount': len(selected),
            'excludedCount': excluded_count,
            'excludedBreakdown': {k: len(v) for k, v in excluded.items()}
        }
    }

    # 出力
    if args.output:
        # 出力ディレクトリが存在しない場合は作成
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f'✅ フィルタ結果を保存: {args.output}')
    else:
        # 標準出力に出力
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'致命的なエラー: {error}', file=sys.stderr)
        sys.exit(1)
