#!/usr/bin/env python3

"""
validate-docs.py

Markdown ドキュメントの品質検証スクリプト

特徴:
  - 必須セクションのチェック（概要、主要機能、要素一覧）
  - 主要機能の数をチェック（3-5個を推奨）
  - Mermaid図の存在チェック
  - 空の見出しの検出
  - 過剰な空行の検出

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# パス設定（環境変数で上書き可能）
DOCS_DIR = Path(os.getenv('DOCS_DIR', 'docs/contract/docs'))
FILTERED_JSON = Path(os.getenv('FILTERED_JSON', 'docs/contract/filtered.json'))
REPORT_PATH = Path(os.getenv('REPORT_PATH', 'docs/contract/validation-report-docs.json'))


def check_required_sections(content: str) -> Tuple[List[str], List[str]]:
    """必須セクションのチェック"""
    errors = []
    warnings = []

    required_sections = [
        {'pattern': re.compile(r'^##\s+.*概要', re.MULTILINE), 'name': '概要'},
        {'pattern': re.compile(r'^##\s+.*主要機能', re.MULTILINE), 'name': '主要機能'},
        {'pattern': re.compile(r'^##\s+.*(要素一覧|機能一覧)', re.MULTILINE), 'name': '要素一覧'}
    ]

    for section in required_sections:
        if not section['pattern'].search(content):
            errors.append(f"必須セクション「{section['name']}」が見つかりません")

    return errors, warnings


def check_main_features(content: str) -> Tuple[List[str], List[str]]:
    """主要機能の数をチェック"""
    errors = []
    warnings = []

    # 主要機能セクションを検出
    main_features_match = re.search(r'^##\s+.*主要機能\s*$(.*?)(?=^##\s|\Z)', content, re.MULTILINE | re.DOTALL)

    if not main_features_match:
        errors.append('主要機能セクションが見つかりません')
        return errors, warnings

    features_section = main_features_match.group(1)

    # h3見出しをカウント（主要機能の数）
    feature_count = len(re.findall(r'^###\s+', features_section, re.MULTILINE))

    if feature_count == 0:
        errors.append('主要機能が1つも記述されていません（0個）')
    elif feature_count < 3:
        warnings.append(f'主要機能が少なすぎます（{feature_count}個、推奨: 3-5個）')
    elif feature_count > 5:
        warnings.append(f'主要機能が多すぎます（{feature_count}個、推奨: 3-5個）')

    return errors, warnings


def check_mermaid_diagrams(content: str) -> Tuple[List[str], List[str]]:
    """Mermaid図の存在チェック"""
    errors = []
    warnings = []

    has_mermaid = bool(re.search(r'```mermaid', content, re.MULTILINE))

    if not has_mermaid:
        warnings.append('Mermaid図が見つかりません（推奨: 主要機能に少なくとも1つの図を追加）')

    return errors, warnings


def check_empty_headings(content: str) -> Tuple[List[str], List[str]]:
    """空の見出しの検出"""
    errors = []
    warnings = []

    # 見出しの後に内容がない場合を検出
    empty_heading_pattern = re.compile(r'^(#{2,})\s+(.+?)\s*$\s*^(#{2,}|\Z)', re.MULTILINE)

    for match in empty_heading_pattern.finditer(content):
        heading_level = match.group(1)
        heading_text = match.group(2)
        next_item = match.group(3)

        # 次の項目が同じレベル以上の見出しの場合、内容が空
        if next_item and next_item.startswith('#'):
            warnings.append(f'空の見出しを検出: "{heading_text}"')

    return errors, warnings


def check_excessive_blank_lines(content: str) -> Tuple[List[str], List[str]]:
    """過剰な空行の検出"""
    errors = []
    warnings = []

    # 3行以上連続する空行を検出
    excessive_blank_lines = re.findall(r'\n\s*\n\s*\n\s*\n', content)

    if excessive_blank_lines:
        warnings.append(f'過剰な空行を検出（{len(excessive_blank_lines)}箇所）')

    return errors, warnings


def check_incomplete_placeholders(content: str) -> Tuple[List[str], List[str]]:
    """AIエンハンス用プレースホルダーの検出"""
    errors = []
    warnings = []

    placeholder_patterns = [
        r'このセクションはAIエンハンスで',
        r'\(\*+ この',
        r'TODO:',
        r'FIXME:'
    ]

    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            warnings.append(f'未完成のプレースホルダーを検出: "{pattern}" ({len(matches)}箇所)')

    return errors, warnings


def validate_markdown(file_path: Path) -> Dict[str, any]:
    """Markdownファイルを検証"""
    content = file_path.read_text(encoding='utf-8')

    all_errors = []
    all_warnings = []

    # 各種チェック
    checks = [
        check_required_sections,
        check_main_features,
        check_mermaid_diagrams,
        check_empty_headings,
        check_excessive_blank_lines,
        check_incomplete_placeholders
    ]

    for check in checks:
        errors, warnings = check(content)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    return {
        'errors': all_errors,
        'warnings': all_warnings
    }


def main():
    """メイン処理"""
    print('📋 Markdown ドキュメント検証を開始します...\n')

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
    contracts_dir = DOCS_DIR / 'contracts'

    for contract_name in contracts:
        md_path = contracts_dir / f'{contract_name}.md'

        if not md_path.exists():
            results['failed'].append({
                'contract': contract_name,
                'errors': [f'Markdownファイルが見つかりません: {md_path}'],
                'warnings': []
            })
            continue

        try:
            validation_result = validate_markdown(md_path)

            if validation_result['errors']:
                results['failed'].append({
                    'contract': contract_name,
                    'errors': validation_result['errors'],
                    'warnings': validation_result['warnings']
                })
            else:
                results['passed'].append(contract_name)
                if validation_result['warnings']:
                    results['warnings'].append({
                        'contract': contract_name,
                        'warnings': validation_result['warnings']
                    })
        except Exception as error:
            results['failed'].append({
                'contract': contract_name,
                'errors': [f'検証エラー: {error}'],
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
