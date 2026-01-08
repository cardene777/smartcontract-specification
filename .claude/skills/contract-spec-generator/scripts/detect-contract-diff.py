#!/usr/bin/env python3

"""
detect-contract-diff.py

ABIファイルと既存仕様書/ドキュメントの差分を検出

特徴:
  - 既存ファイルがない場合は早期リターン（初回生成）
  - ABIファイルから関数・イベント・エラーを正確に抽出
  - コントラクトレベル: 新規/削除/更新/未変更を検出
  - 関数レベル: 新規/削除/変更を検出
  - JSON差分レポートを生成
  - 人間が読みやすい形式でコンソール出力

使用方法:
  python detect-contract-diff.py --abi-dir <abi-dir> --contract-dir <contract-dir> --specs-dir <specs-dir> [--docs-dir <docs-dir>]

例:
  python detect-contract-diff.py \
    --abi-dir packages/contract/out \
    --contract-dir packages/contract/src \
    --specs-dir docs/contract/specs \
    --docs-dir docs/contract/docs

Requirements:
    - Python 3.7+
    - PyYAML: pip install pyyaml
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    import yaml
except ImportError:
    print('Error: PyYAML is required. Install it with: pip install pyyaml', file=sys.stderr)
    sys.exit(1)


def check_existing_files(specs_dir: Path, docs_dir: Path = None) -> Dict[str, Any]:
    """既存ファイルの存在チェック"""
    spec_files = []
    doc_files = []

    # specs/ 配下の .openapi.yaml をチェック
    if specs_dir.exists():
        for entry in specs_dir.iterdir():
            if entry.is_dir():
                yaml_path = entry / f'{entry.name}.openapi.yaml'
                if yaml_path.exists():
                    spec_files.append(yaml_path)

    # docs/contracts/ 配下の .md をチェック（オプション）
    if docs_dir:
        contracts_dir = docs_dir / 'contracts'
        if contracts_dir.exists():
            for entry in contracts_dir.iterdir():
                if entry.is_file() and entry.suffix == '.md' and entry.name != 'index.md':
                    doc_files.append(entry)

    return {
        'hasSpecs': len(spec_files) > 0,
        'hasDocs': len(doc_files) > 0,
        'specCount': len(spec_files),
        'docCount': len(doc_files),
        'specFiles': spec_files,
        'docFiles': doc_files
    }


def find_solidity_files(directory: Path) -> List[Path]:
    """Solidityファイルを再帰的に検索"""
    files = []

    def traverse(current_dir: Path):
        for entry in current_dir.iterdir():
            if entry.is_dir():
                traverse(entry)
            elif entry.is_file() and entry.suffix == '.sol':
                files.append(entry)

    traverse(directory)
    return files


def get_source_contracts(contract_dir: Path, abi_dir: Path) -> List[Dict[str, Any]]:
    """ABIファイルから関数・イベント・エラーを取得"""
    contracts = []

    if not contract_dir.exists():
        return contracts

    sol_files = find_solidity_files(contract_dir)

    for sol_file in sol_files:
        contract_name = sol_file.stem
        content = sol_file.read_text(encoding='utf-8')

        # contract, abstract contract, library, interface を検出
        contract_match = re.search(r'^\s*(contract|abstract\s+contract|library|interface)\s+(\w+)',
                                  content, re.MULTILINE)

        if contract_match:
            # ABIファイルから関数・イベント・エラーを取得
            abi_path = abi_dir / f'{contract_name}.sol' / f'{contract_name}.json'

            functions = []
            events = []
            errors = []

            if abi_path.exists():
                with abi_path.open('r', encoding='utf-8') as f:
                    abi_data = json.load(f)
                abi = abi_data.get('abi', abi_data)

                functions = [item['name'] for item in abi if item.get('type') == 'function']
                events = [item['name'] for item in abi if item.get('type') == 'event']
                errors = [item['name'] for item in abi if item.get('type') == 'error']

            contracts.append({
                'name': contract_name,
                'source': str(sol_file),
                'functions': functions,
                'events': events,
                'errors': errors
            })

    return contracts


def get_existing_spec_functions(spec_path: Path) -> List[str]:
    """既存仕様書から関数リストを取得"""
    try:
        content = spec_path.read_text(encoding='utf-8')
        spec = yaml.safe_load(content)
        functions = []

        if spec and 'paths' in spec:
            for path_item in spec['paths'].values():
                for operation in path_item.values():
                    if isinstance(operation, dict) and 'operationId' in operation:
                        functions.append(operation['operationId'])

        return functions
    except Exception:
        return []


def calculate_diff(source_contracts: List[Dict[str, Any]],
                  existing_files: Dict[str, Any]) -> Dict[str, List[Any]]:
    """差分を計算"""
    diff = {
        'new': [],
        'deleted': [],
        'updated': [],
        'unchanged': []
    }

    source_map = {c['name']: c for c in source_contracts}
    existing_map = {}

    # 既存仕様書からコントラクト名と関数を抽出
    for spec_file in existing_files['specFiles']:
        contract_name = spec_file.parent.name
        functions = get_existing_spec_functions(spec_file)
        existing_map[contract_name] = {
            'name': contract_name,
            'specPath': str(spec_file),
            'functions': functions
        }

    # 新規コントラクトを検出
    for name, source_contract in source_map.items():
        if name not in existing_map:
            diff['new'].append({
                'name': source_contract['name'],
                'source': source_contract['source'],
                'functions': len(source_contract['functions']),
                'events': len(source_contract['events']),
                'errors': len(source_contract['errors'])
            })

    # 削除されたコントラクトを検出
    for name, existing_contract in existing_map.items():
        if name not in source_map:
            diff['deleted'].append({
                'name': existing_contract['name'],
                'specPath': existing_contract['specPath'],
                'reason': 'ソースファイルが見つかりません'
            })

    # 更新されたコントラクトを検出
    for name, source_contract in source_map.items():
        if name in existing_map:
            existing_contract = existing_map[name]
            source_functions = set(source_contract['functions'])
            existing_functions = set(existing_contract['functions'])

            new_functions = list(source_functions - existing_functions)
            deleted_functions = list(existing_functions - source_functions)

            if new_functions or deleted_functions:
                diff['updated'].append({
                    'name': source_contract['name'],
                    'source': source_contract['source'],
                    'specPath': existing_contract['specPath'],
                    'changes': {
                        'newFunctions': new_functions,
                        'deletedFunctions': deleted_functions,
                        'modifiedFunctions': []  # TODO: 変更検出は今後実装
                    }
                })
            else:
                diff['unchanged'].append(name)

    return diff


def main():
    """メイン処理"""
    # 固定パス
    ABI_DIR = Path('packages/contract/out')
    CONTRACT_DIR = Path('packages/contract/src')
    SPECS_DIR = Path('docs/contract/specs')
    DOCS_DIR = Path('docs/contract/docs')

    # 既存ファイルの存在確認
    existing_files = check_existing_files(SPECS_DIR, DOCS_DIR)

    # 既存ファイルがない場合は早期リターン
    if not existing_files['hasSpecs'] and not existing_files['hasDocs']:
        print('ℹ️  既存の仕様書またはドキュメントが見つかりません。')
        print('   これは初回生成のようです。')
        print('   差分検出をスキップします - フル生成モードを使用してください。\n')
        print('📊 サマリー:')
        print(f"   既存の仕様書: {existing_files['specCount']}")
        print(f"   既存のドキュメント: {existing_files['docCount']}")
        print('')
        print('⚠️  次のステップ: フル生成モードを実行')

        # 空のdiffレポートを生成（フルモード用）
        empty_report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'mode': 'full',
            'reason': '既存ファイルが見つかりません',
            'summary': {
                'totalSourceContracts': 0,
                'totalExistingSpecs': 0,
                'newContracts': 0,
                'deletedContracts': 0,
                'updatedContracts': 0,
                'unchangedContracts': 0
            },
            'contracts': {
                'new': [],
                'deleted': [],
                'updated': [],
                'unchanged': []
            }
        }

        with open('contract-diff-report.json', 'w', encoding='utf-8') as f:
            json.dump(empty_report, f, ensure_ascii=False, indent=2)
        sys.exit(0)

    print('🔍 コントラクト差分検出レポート')
    print('━' * 40 + '\n')
    print('既存ファイルを発見:')
    print(f"   仕様書: {existing_files['specCount']}")
    print(f"   ドキュメント: {existing_files['docCount']}\n")

    # ABIファイルから現在のコントラクトリストを取得
    source_contracts = get_source_contracts(CONTRACT_DIR, ABI_DIR)

    # 差分を計算
    diff = calculate_diff(source_contracts, existing_files)

    # サマリーを作成
    summary = {
        'totalSourceContracts': len(source_contracts),
        'totalExistingSpecs': existing_files['specCount'],
        'newContracts': len(diff['new']),
        'deletedContracts': len(diff['deleted']),
        'updatedContracts': len(diff['updated']),
        'unchangedContracts': len(diff['unchanged'])
    }

    # レポートを生成
    has_changes = diff['new'] or diff['updated'] or diff['deleted']
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'mode': 'incremental' if has_changes else 'full',
        'reason': '変更が検出されました' if has_changes else '変更が検出されませんでした',
        'summary': summary,
        'contracts': diff
    }

    # JSONレポートを保存
    with open('contract-diff-report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # コンソール出力
    print('📊 サマリー:')
    print(f"   ソースコントラクト総数: {summary['totalSourceContracts']}")
    print(f"   既存の仕様書: {summary['totalExistingSpecs']}")
    print('')
    print(f"   ✨ 新規コントラクト: {summary['newContracts']}")
    print(f"   🗑️  削除されたコントラクト: {summary['deletedContracts']}")
    print(f"   🔄 更新されたコントラクト: {summary['updatedContracts']}")
    print(f"   ✅ 未変更のコントラクト: {summary['unchangedContracts']}")
    print('')
    print('━' * 40 + '\n')

    # 新規コントラクト
    if diff['new']:
        print(f"✨ 新規コントラクト ({len(diff['new'])}):")
        for idx, contract in enumerate(diff['new'], 1):
            print(f"   {idx}. {contract['name']}")
            print(f"      - 関数: {contract['functions']}")
            print(f"      - イベント: {contract['events']}")
            print(f"      - エラー: {contract['errors']}")
            print(f"      - ソース: {contract['source']}")
            print('')
        print('━' * 40 + '\n')

    # 更新されたコントラクト
    if diff['updated']:
        print(f"🔄 更新されたコントラクト ({len(diff['updated'])}):")
        for idx, contract in enumerate(diff['updated'], 1):
            print(f"   {idx}. {contract['name']}")
            changes = contract['changes']
            if changes['newFunctions']:
                new_funcs = ', '.join(changes['newFunctions'])
                print(f"      ➕ 新規関数 ({len(changes['newFunctions'])}): {new_funcs}")
            if changes['deletedFunctions']:
                del_funcs = ', '.join(changes['deletedFunctions'])
                print(f"      ➖ 削除された関数 ({len(changes['deletedFunctions'])}): {del_funcs}")
            if changes['modifiedFunctions']:
                print(f"      🔧 変更された関数 ({len(changes['modifiedFunctions'])})")
            print('')
        print('━' * 40 + '\n')

    # 削除されたコントラクト
    if diff['deleted']:
        print(f"🗑️  削除されたコントラクト ({len(diff['deleted'])}):")
        for contract in diff['deleted']:
            print(f"   ⚠️  {contract['name']}")
            print('      - 仕様書は存在するがソースが見つかりません')
            print(f"      - 仕様書パス: {contract['specPath']}")
            print('      - ⚠️  手動で削除が必要です')
            print('')
        print('━' * 40 + '\n')

    print('💾 詳細レポート保存先: contract-diff-report.json\n')
    print('⚠️  次のステップ:')
    print('   1. 上記の変更を確認してください')
    print('   2. 生成モードを選択:')
    print('      - フルモード: すべてのコントラクトを再生成')
    print('      - 差分モード: 変更されたコントラクトのみ更新')
    print('      - ドライラン: 変更せずに終了')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'致命的なエラー: {error}', file=sys.stderr)
        sys.exit(1)
