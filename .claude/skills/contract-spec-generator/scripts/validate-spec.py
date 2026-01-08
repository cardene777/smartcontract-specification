#!/usr/bin/env python3

"""
Contract Spec JSON 品質検証スクリプト

Subagent処理完了後に、Contract Spec JSONの品質を検証します。

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


# パス設定（環境変数で上書き可能）
import os
IR_DIR = Path(os.getenv('IR_DIR', 'docs/contract/ir'))
FILTERED_JSON = Path(os.getenv('FILTERED_JSON', 'docs/contract/filtered.json'))
REPORT_PATH = Path(os.getenv('REPORT_PATH', 'docs/contract/validation-report.json'))


def validate_contract_spec(contract_name: str, spec_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """単一コントラクトの検証"""
    errors = []
    warnings = []

    # 1. メタデータチェック
    if 'metadata' not in spec_data:
        errors.append('メタデータが存在しません')
    else:
        metadata = spec_data['metadata']
        if not metadata.get('description', '').strip():
            errors.append('メタデータの説明が空です')
        if not metadata.get('category', '').strip():
            warnings.append('メタデータのカテゴリが空です')

    # 2. 読み取り関数チェック
    read_functions = spec_data.get('readFunctions', [])
    if read_functions:
        for func in read_functions:
            func_name = func.get('name', '(無名関数)')

            # サマリーチェック
            doc = func.get('documentation', {})
            if not doc.get('summary', '').strip():
                errors.append(f'読み取り関数 {func_name}: サマリーが空です')

            # パラメータチェック
            for param in func.get('parameters', []):
                if not param.get('description', '').strip():
                    param_name = param.get('name', '?')
                    warnings.append(f'読み取り関数 {func_name}.{param_name}: パラメータ説明が空です')

            # 戻り値チェック
            for ret in func.get('returnValues', []):
                if not ret.get('description', '').strip():
                    warnings.append(f'読み取り関数 {func_name}: 戻り値説明が空です')

    # 3. 書き込み関数チェック
    write_functions = spec_data.get('writeFunctions', [])
    if write_functions:
        for func in write_functions:
            func_name = func.get('name', '(無名関数)')

            # サマリーチェック
            doc = func.get('documentation', {})
            if not doc.get('summary', '').strip():
                errors.append(f'書き込み関数 {func_name}: サマリーが空です')

            # パラメータチェック
            for param in func.get('parameters', []):
                if not param.get('description', '').strip():
                    param_name = param.get('name', '?')
                    warnings.append(f'書き込み関数 {func_name}.{param_name}: パラメータ説明が空です')

            # エラーケースチェック
            if not func.get('errors'):
                warnings.append(f'書き込み関数 {func_name}: エラーケースが定義されていません')

    # 4. カスタムエラーチェック
    custom_errors = spec_data.get('customErrors', {})
    for error_name, error_data in custom_errors.items():
        if not error_data.get('description', '').strip():
            warnings.append(f'カスタムエラー {error_name}: 説明が空です')

        for param in error_data.get('parameters', []):
            if not param.get('description', '').strip():
                param_name = param.get('name', '?')
                warnings.append(f'カスタムエラー {error_name}.{param_name}: パラメータ説明が空です')

    # 5. イベントチェック
    events = spec_data.get('events', [])
    for event in events:
        event_name = event.get('name', '(無名イベント)')

        event_doc = event.get('documentation', {})
        if not event_doc.get('summary', '').strip():
            warnings.append(f'イベント {event_name}: サマリーが空です')

        for param in event.get('parameters', []):
            if not param.get('description', '').strip():
                param_name = param.get('name', '?')
                warnings.append(f'イベント {event_name}.{param_name}: パラメータ説明が空です')

    return errors, warnings


def main():
    """メイン処理"""
    print('📋 Contract Spec JSON 検証を開始します...\n')

    # filtered.json を読み込み
    if not FILTERED_JSON.exists():
        print(f'❌ エラー: {FILTERED_JSON} が見つかりません', file=sys.stderr)
        sys.exit(1)

    with FILTERED_JSON.open('r', encoding='utf-8') as f:
        filtered = json.load(f)
    contracts = filtered.get('selected', [])

    if not contracts:
        print('⚠️  対象コントラクトがありません')
        sys.exit(0)

    print(f'対象コントラクト: {len(contracts)}個\n')

    results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }

    # 各コントラクトを検証
    for contract_name in contracts:
        spec_path = IR_DIR / f'{contract_name}.json'

        if not spec_path.exists():
            results['failed'].append({
                'contract': contract_name,
                'errors': [f'Contract Spec JSON ファイルが見つかりません: {spec_path}'],
                'warnings': []
            })
            continue

        try:
            with spec_path.open('r', encoding='utf-8') as f:
                spec_data = json.load(f)
            errors, warnings = validate_contract_spec(contract_name, spec_data)

            if errors:
                results['failed'].append({
                    'contract': contract_name,
                    'errors': errors,
                    'warnings': warnings
                })
            else:
                results['passed'].append(contract_name)
                if warnings:
                    results['warnings'].append({
                        'contract': contract_name,
                        'warnings': warnings
                    })
        except json.JSONDecodeError as error:
            results['failed'].append({
                'contract': contract_name,
                'errors': [f'JSON パースエラー: {error}'],
                'warnings': []
            })

    # レポート保存
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open('w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # コンソール出力
    print('=' * 60)
    print(f'✅ 検証成功: {len(results["passed"])}/{len(contracts)}個')
    print(f'❌ 検証失敗: {len(results["failed"])}個')
    print(f'⚠️  警告あり: {len(results["warnings"])}個')
    print('=' * 60)

    # 失敗詳細
    if results['failed']:
        print('\n❌ 検証失敗詳細:\n')
        for item in results['failed']:
            print(f"{item['contract']}:")
            for err in item['errors']:
                print(f'  - {err}')
            print()

    # 警告詳細
    if results['warnings']:
        print('\n⚠️  警告詳細:\n')
        for item in results['warnings']:
            print(f"{item['contract']}:")
            for warn in item['warnings']:
                print(f'  - {warn}')
            print()

    print(f'\n📄 検証レポート: {REPORT_PATH}\n')

    # 終了コード
    if results['failed']:
        print('❌ 検証失敗により終了します')
        sys.exit(1)
    else:
        print('✅ 全ての検証が成功しました')
        sys.exit(0)


if __name__ == '__main__':
    main()
