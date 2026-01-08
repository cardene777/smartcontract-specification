#!/usr/bin/env python3

"""
generate-api-pages.py

sidebars.jsから全コントラクトのAPI仕様書ページ（.mdx）を自動生成

特徴:
  - sidebars.jsを読み込んでコントラクトリストを抽出
  - 各コントラクトのAPI仕様書ページ（.mdx）を生成
  - SwaggerUIコンポーネントを埋め込み

使用方法:
  python generate-api-pages.py \
    --sidebars-path <sidebars-path> \
    --output-dir <output-dir>

例:
  python generate-api-pages.py \
    --sidebars-path docs/contract/docs/sidebars.js \
    --output-dir docs/contract/site/docs/api

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


def find_project_root(start_path: Path = None) -> Path:
    """プロジェクトルートを検出（.git または package.json を探す）"""
    if start_path is None:
        start_path = Path(__file__).parent

    current_path = start_path.resolve()

    while current_path != current_path.parent:
        if (current_path / '.git').exists() or (current_path / 'package.json').exists():
            return current_path
        current_path = current_path.parent

    # 見つからない場合は現在のディレクトリを返す
    return Path.cwd()


PROJECT_ROOT = find_project_root()


def extract_contracts_from_sidebars(sidebars_path: Path) -> List[str]:
    """sidebars.jsを読み込んでコントラクトリストを抽出"""
    if not sidebars_path.exists():
        print(f'Error: sidebars.js not found: {sidebars_path}', file=sys.stderr)
        sys.exit(1)

    content = sidebars_path.read_text(encoding='utf-8')
    contracts = []

    # contracts/ で始まるアイテムを抽出（正規表現で）
    # 例: "contracts/StablecoinCore"
    pattern = r'"contracts/([^"]+)"'
    matches = re.findall(pattern, content)

    contracts = list(set(matches))  # 重複削除
    contracts.sort()  # アルファベット順にソート

    return contracts


def generate_api_page(contract_name: str, position: int) -> str:
    """API仕様書ページ（.mdx）を生成"""
    return f"""---
id: {contract_name}
title: {contract_name} API仕様書
sidebar_position: {position}
---

import SwaggerUI from '@site/src/components/SwaggerUI';

# {contract_name} API仕様書

<SwaggerUI specUrl="/specs/{contract_name}/{contract_name}.openapi.yaml" />
"""


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description='Generate API pages from sidebars.js')
    parser.add_argument('--sidebars-path', help='sidebars.js path')
    parser.add_argument('--output-dir', help='Output directory for API pages')
    args = parser.parse_args()

    # パスの設定（引数がない場合はデフォルト値を使用）
    SIDEBARS_PATH = Path(args.sidebars_path or PROJECT_ROOT / 'docs/contract/docs/sidebars.js')
    OUTPUT_DIR = Path(args.output_dir or PROJECT_ROOT / 'docs/contract/site/docs/api')

    print('📝 Generating API pages...\n')
    print(f'Sidebars path: {SIDEBARS_PATH}')
    print(f'Output directory: {OUTPUT_DIR}\n')

    # sidebars.jsからコントラクトリストを抽出
    contracts = extract_contracts_from_sidebars(SIDEBARS_PATH)

    if not contracts:
        print('Error: No contracts found in sidebars.js', file=sys.stderr)
        sys.exit(1)

    print(f'Found {len(contracts)} contracts:\n')
    for contract in contracts:
        print(f'  - {contract}')
    print('')

    # 出力ディレクトリ作成
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 各コントラクトのAPI仕様書ページを生成
    success_count = 0

    for idx, contract_name in enumerate(contracts, start=1):
        try:
            content = generate_api_page(contract_name, idx)
            output_path = OUTPUT_DIR / f'{contract_name}.mdx'

            output_path.write_text(content, encoding='utf-8')
            print(f'  ✓ {contract_name}.mdx')
            success_count += 1
        except Exception as error:
            print(f'  ✗ {contract_name}: {error}', file=sys.stderr)

    print('')
    print(f'✅ API pages generation complete!')
    print(f'   Success: {success_count}/{len(contracts)} pages')
    print(f'   Output directory: {OUTPUT_DIR}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
