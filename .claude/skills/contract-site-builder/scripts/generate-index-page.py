#!/usr/bin/env python3

"""
generate-index-page.py

sidebars.jsとMarkdownドキュメントからindex.tsxを自動生成するスクリプト

特徴:
  - sidebars.jsを読み込んでカテゴリとコントラクトリストを抽出
  - 各コントラクトのMarkdownから説明を抽出
  - カテゴリ別コントラクトデータ配列を生成
  - トップページ用のindex.tsxを生成

使用方法:
  python generate-index-page.py \
    --sidebars-path <sidebars-path> \
    --docs-dir <docs-dir> \
    --config <config-path> \
    --output-path <output-path>

例:
  python generate-index-page.py \
    --sidebars-path docs/contract/docs/sidebars.js \
    --docs-dir docs/contract/docs \
    --config docs/contract/doc-config.json \
    --output-path docs/contract/site/src/pages/index.tsx

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import argparse
import json
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

    return Path.cwd()


PROJECT_ROOT = find_project_root()


def load_config(config_path: Path) -> Dict[str, Any]:
    """doc-config.jsonを読み込み"""
    if not config_path.exists():
        print(f'Error: Config file not found: {config_path}', file=sys.stderr)
        sys.exit(1)

    try:
        with config_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as error:
        print(f'Error parsing config file: {error}', file=sys.stderr)
        sys.exit(1)


def extract_contracts_from_sidebars(sidebars_path: Path) -> Dict[str, Any]:
    """sidebars.jsを読み込んでカテゴリとコントラクトリストを抽出"""
    if not sidebars_path.exists():
        print(f'Error: sidebars.js not found: {sidebars_path}', file=sys.stderr)
        sys.exit(1)

    content = sidebars_path.read_text(encoding='utf-8')

    contracts = []
    categories = []

    # カテゴリパターンを抽出（正規表現で）
    category_pattern = r'\{\s*["\']?type["\']?\s*:\s*["\']category["\']\s*,\s*["\']?label["\']?\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']?items["\']?\s*:\s*\[(.*?)\]'

    for match in re.finditer(category_pattern, content, re.DOTALL):
        label = match.group(1)
        items_str = match.group(2)

        # API仕様書カテゴリはスキップ
        if label == 'API仕様書':
            continue

        # アイテムを抽出
        item_pattern = r'["\']contracts/([^"\']+)["\']'
        category_contracts = []

        for item_match in re.finditer(item_pattern, items_str):
            contract_name = item_match.group(1)
            category_contracts.append({
                'name': contract_name,
                'path': f'contracts/{contract_name}'
            })

        if category_contracts:
            categories.append({
                'label': label,
                'contracts': category_contracts
            })
            contracts.extend(category_contracts)

    return {'contracts': contracts, 'categories': categories}


def escape_description(desc: str) -> str:
    """description文字列をエスケープして1行に変換"""
    return (desc
            .replace('\n', ' ')       # 改行を半角スペースに変換
            .replace('  ', ' ')       # 連続する空白を1つに（複数回適用）
            .replace('  ', ' ')
            .strip()                   # 前後の空白を削除
            .replace("'", "\\'"))      # シングルクォートをエスケープ


def extract_description_from_markdown(markdown_path: Path, contract_name: str, config: Dict[str, Any]) -> str:
    """Markdownファイルから説明を抽出"""
    description = ''

    # まずconfigから説明を取得
    if config.get('descriptions') and config['descriptions'].get(contract_name):
        desc = config['descriptions'][contract_name]
        description = desc.get('overview') or desc.get('detail', f'{contract_name}コントラクトの仕様書です。')
    # configになければMarkdownから抽出
    elif markdown_path.exists():
        try:
            content = markdown_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            in_frontmatter = False
            frontmatter_ended = False

            for line in lines:
                if line.strip() == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        in_frontmatter = False
                        frontmatter_ended = True
                    continue

                if frontmatter_ended and not in_frontmatter:
                    # 見出し行をスキップ
                    if line.startswith('#'):
                        continue

                    # 空行をスキップ
                    if line.strip() == '':
                        continue

                    # 最初の有効な段落を取得
                    if len(line.strip()) > 0:
                        description = line.strip()
                        break

            # 説明が見つからない場合はデフォルト
            if not description:
                description = f'{contract_name}コントラクトの仕様書です。'
        except Exception as error:
            print(f'Error reading markdown: {markdown_path}', error, file=sys.stderr)
            description = f'{contract_name}コントラクトの仕様書です。'
    # Markdownファイルがない場合もデフォルト
    else:
        description = f'{contract_name}コントラクトの仕様書です。'

    # 説明が長すぎる場合は切り詰める（2行分: 約80文字）
    if len(description) > 80:
        description = description[:77] + '...'

    return description


def generate_contracts_data(categories: List[Dict[str, Any]], docs_dir: Path, config: Dict[str, Any]) -> str:
    """カテゴリ別コントラクトデータを生成"""
    data_lines = []

    for category in categories:
        data_lines.append('  {')
        data_lines.append(f"    category: '{category['label']}',")
        data_lines.append('    items: [')

        for contract in category['contracts']:
            markdown_path = docs_dir / 'contracts' / f"{contract['name']}.md"
            description = extract_description_from_markdown(markdown_path, contract['name'], config)

            data_lines.append('      {')
            data_lines.append(f"        name: '{contract['name']}',")
            data_lines.append(f"        path: '/docs/api/{contract['name']}',")
            data_lines.append(f"        description: '{escape_description(description)}',")
            data_lines.append('      },')

        data_lines.append('    ],')
        data_lines.append('  },')

    return '\n'.join(data_lines)


def generate_index_tsx(config: Dict[str, Any], contracts: List[Dict[str, Any]],
                       categories: List[Dict[str, Any]], docs_dir: Path) -> str:
    """index.tsxを生成"""
    project_description = config.get('projectDescription') or config.get('tagline', 'スマートコントラクト仕様書')
    total_contracts = len(contracts)
    contracts_data = generate_contracts_data(categories, docs_dir, config)

    return f"""import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

interface ContractCard {{
  name: string;
  description: string;
  path: string;
}}

interface ContractCategory {{
  category: string;
  items: ContractCard[];
}}

const contractsData: ContractCategory[] = [
{contracts_data}
];

function ContractCard({{ name, description, path }}: ContractCard) {{
  return (
    <div className={{clsx('col col--4', styles.contractCard)}}>
      <div className="card">
        <div className="card__header">
          <h3>{{name}}</h3>
        </div>
        <div className="card__body">
          <p>{{description}}</p>
        </div>
        <div className="card__footer">
          <Link
            className="button button--primary button--block"
            to={{path}}>
            仕様書を見る
          </Link>
        </div>
      </div>
    </div>
  );
}}

function CategorySection({{ category, items }}: ContractCategory) {{
  return (
    <section className={{styles.categorySection}}>
      <div className="container">
        <h2 className={{styles.categoryTitle}}>{{category}}</h2>
        <div className="row">
          {{items.map((contract, idx) => (
            <ContractCard key={{idx}} {{...contract}} />
          ))}}
        </div>
      </div>
    </section>
  );
}}

export default function Home(): JSX.Element {{
  const {{siteConfig}} = useDocusaurusContext();
  return (
    <Layout
      title={{`${{siteConfig.title}}`}}
      description="{project_description}">
      <header className={{clsx('hero hero--primary', styles.heroBanner)}}>
        <div className="container">
          <h1 className="hero__title">{{siteConfig.title}}</h1>
          <p className="hero__subtitle">{{siteConfig.tagline}}</p>
          <p className={{styles.contractCount}}>全{total_contracts}個のスマートコントラクト仕様書</p>
        </div>
      </header>
      <main>
        {{contractsData.map((category, idx) => (
          <CategorySection key={{idx}} {{...category}} />
        ))}}
      </main>
    </Layout>
  );
}}
"""


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description='Generate index.tsx from sidebars and Markdown docs')
    parser.add_argument('--sidebars-path', help='sidebars.js path')
    parser.add_argument('--docs-dir', help='Docs directory path')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--output-path', help='Output index.tsx path')
    args = parser.parse_args()

    # パスの設定
    SIDEBARS_PATH = Path(args.sidebars_path or PROJECT_ROOT / 'docs/contract/docs/sidebars.js')
    DOCS_DIR = Path(args.docs_dir or PROJECT_ROOT / 'docs/contract/docs')
    CONFIG_PATH = Path(args.config or PROJECT_ROOT / 'docs/contract/doc-config.json')
    OUTPUT_PATH = Path(args.output_path or PROJECT_ROOT / 'docs/contract/site/src/pages/index.tsx')

    print('📝 Generating index.tsx...\n')
    print(f'Sidebars path: {SIDEBARS_PATH}')
    print(f'Docs directory: {DOCS_DIR}')
    print(f'Config path: {CONFIG_PATH}')
    print(f'Output path: {OUTPUT_PATH}\n')

    # Config読み込み
    config = load_config(CONFIG_PATH)

    # sidebars.jsから抽出
    result = extract_contracts_from_sidebars(SIDEBARS_PATH)
    contracts = result['contracts']
    categories = result['categories']

    print(f'Found {len(contracts)} contracts in {len(categories)} categories:\n')
    for category in categories:
        print(f"  - {category['label']}: {len(category['contracts'])} contracts")
    print('')

    # index.tsx生成
    index_content = generate_index_tsx(config, contracts, categories, DOCS_DIR)

    # 出力ディレクトリ作成
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ファイル出力
    OUTPUT_PATH.write_text(index_content, encoding='utf-8')

    print(f'✅ index.tsx generated: {OUTPUT_PATH}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
