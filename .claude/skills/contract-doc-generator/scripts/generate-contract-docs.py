#!/usr/bin/env python3

"""
generate-contract-docs.py

OpenAPI仕様書からMarkdownドキュメントとsidebars.jsを自動生成するスクリプト

特徴:
  - OpenAPI YAML仕様書からMarkdownドキュメントを自動生成
  - doc-config.jsonからカテゴリ定義を読み込み（プロジェクト固有設定）
  - sidebars.jsを自動生成（カテゴリ別グルーピング）
  - 概要セクション、API仕様書リンクを含む基本構造を生成

使用方法:
  python generate-contract-docs.py --specs-dir <specs-dir> --docs-dir <docs-dir> --config <config-path>

例:
  python generate-contract-docs.py \
    --specs-dir docs/contract/specs \
    --docs-dir docs/contract/docs \
    --config docs/contract/doc-config.json

Requirements:
    - Python 3.7+
    - PyYAML: pip install pyyaml
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print('Error: PyYAML is required. Install it with: pip install pyyaml', file=sys.stderr)
    sys.exit(1)


def load_config(config_path: Path) -> Dict[str, Any]:
    """doc-config.jsonを読み込み"""
    if not config_path.exists():
        print(f'Error: Config file not found: {config_path}', file=sys.stderr)
        print('\nPlease create a doc-config.json file with the following structure:', file=sys.stderr)
        example_config = {
            "categories": {
                "Category Name 1": ["Contract1", "Contract2"],
                "Category Name 2": ["Contract3", "Contract4"]
            },
            "descriptions": {
                "Contract1": {
                    "overview": "Short description",
                    "detail": "Detailed description"
                }
            }
        }
        print(json.dumps(example_config, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    try:
        with config_path.open('r', encoding='utf-8') as f:
            config = json.load(f)

        # 必須フィールドのチェック
        if not config.get('categories') or not isinstance(config['categories'], dict):
            print('Error: Config file must contain "categories" object', file=sys.stderr)
            sys.exit(1)

        return config
    except json.JSONDecodeError as error:
        print(f'Error parsing config file: {error}', file=sys.stderr)
        sys.exit(1)


def categorize_contract(contract_name: str, categories: Dict[str, List[str]]) -> Optional[str]:
    """コントラクト名からカテゴリを取得"""
    for category, contracts in categories.items():
        if contract_name in contracts:
            return category

    print(f'⚠️  Contract "{contract_name}" not found in doc-config.json - skipping')
    return None


def find_contracts(specs_dir: Path) -> List[Dict[str, Path]]:
    """OpenAPI仕様書ディレクトリから全てのコントラクトを検出"""
    contracts = []

    if not specs_dir.exists():
        print(f'Error: Specs directory not found: {specs_dir}', file=sys.stderr)
        sys.exit(1)

    for entry in specs_dir.iterdir():
        if entry.is_dir():
            contract_name = entry.name
            yaml_path = entry / f'{contract_name}.openapi.yaml'

            if yaml_path.exists():
                contracts.append({
                    'name': contract_name,
                    'yamlPath': yaml_path
                })

    return contracts


def load_openapi_spec(yaml_path: Path) -> Optional[Dict[str, Any]]:
    """OpenAPI仕様書を読み込み"""
    try:
        content = yaml_path.read_text(encoding='utf-8')
        return yaml.safe_load(content)
    except Exception as error:
        print(f'Error loading OpenAPI spec: {yaml_path} - {error}', file=sys.stderr)
        return None


def generate_functions_table(functions: List[Dict[str, Any]], contract_spec_json: Optional[Dict[str, Any]]) -> str:
    """関数の一覧を表形式で生成（読み取り/書き込みに分類）"""
    if not functions:
        return "なし（関数は定義されていません）\n"

    # Contract Spec JSONから既に分類済みの関数を取得
    read_functions = contract_spec_json.get('readFunctions', []) if contract_spec_json else []
    write_functions = contract_spec_json.get('writeFunctions', []) if contract_spec_json else []

    # OpenAPI関数データとマージ
    read_functions_data = [
        {
            'name': func_detail['name'],
            'description': func_detail.get('documentation', {}).get('summary') or func_detail.get('documentation', {}).get('details', '')
        }
        for func_detail in read_functions
    ]

    write_functions_data = [
        {
            'name': func_detail['name'],
            'description': func_detail.get('documentation', {}).get('summary') or func_detail.get('documentation', {}).get('details', '')
        }
        for func_detail in write_functions
    ]

    result = ''

    # 書き込み関数
    if write_functions_data:
        result += '<details>\n'
        result += f'<summary><strong>📝 書き込み関数（{len(write_functions_data)}）</strong></summary>\n\n'
        result += '| 関数名 | 説明 |\n'
        result += '|--------|------|\n'
        for func in write_functions_data:
            result += f"| `{func['name']}` | {func['description']} |\n"
        result += '\n</details>\n\n'

    # 読み取り関数
    if read_functions_data:
        result += '<details>\n'
        result += f'<summary><strong>📖 読み取り関数（{len(read_functions_data)}）</strong></summary>\n\n'
        result += '| 関数名 | 説明 |\n'
        result += '|--------|------|\n'
        for func in read_functions_data:
            result += f"| `{func['name']}` | {func['description']} |\n"
        result += '\n</details>\n\n'

    return result


def generate_table(items: List[Dict[str, Any]], item_type: str) -> str:
    """イベント/エラーの一覧を表形式で生成"""
    if not items:
        return f"なし（{item_type}は定義されていません）\n\n"

    emoji = '📡' if item_type == 'イベント' else '⚠️'

    result = '<details>\n'
    result += f'<summary><strong>{emoji} {item_type}（{len(items)}）</strong></summary>\n\n'
    result += '| 名前 | 説明 |\n'
    result += '|------|------|\n'

    for item in items:
        name = item.get('name', 'N/A')
        description = (item.get('description', '説明なし')).replace('\n', ' ')
        result += f'| `{name}` | {description} |\n'

    result += '\n</details>\n\n'
    return result


def extract_api_elements(spec: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """関数、イベント、エラーを抽出"""
    functions = []
    events = []
    errors = []

    if spec.get('paths'):
        for path_key, path_item in spec['paths'].items():
            for method, operation in path_item.items():
                if isinstance(operation, dict) and operation.get('operationId'):
                    element = {
                        'name': operation['operationId'],
                        'description': operation.get('description') or operation.get('summary', ''),
                        'method': method.upper(),
                        'path': path_key
                    }

                    # タグで分類
                    tags = operation.get('tags', [])
                    if 'Events' in tags:
                        events.append(element)
                    elif 'Errors' in tags:
                        errors.append(element)
                    else:
                        functions.append(element)

    return {'functions': functions, 'events': events, 'errors': errors}


def get_contract_description(contract_name: str, config: Dict[str, Any]) -> str:
    """コントラクトの説明を取得"""
    if config.get('descriptions') and config['descriptions'].get(contract_name):
        desc = config['descriptions'][contract_name]
        return desc.get('detail') or desc.get('overview', f'{contract_name}コントラクトの仕様書です。')
    return f'{contract_name}コントラクトの仕様書です。'


def generate_markdown(contract: Dict[str, Any], spec: Dict[str, Any], category: str,
                     config: Dict[str, Any], contract_spec_json: Optional[Dict[str, Any]]) -> str:
    """Markdownドキュメントを生成"""
    name = contract['name']
    info = spec.get('info', {})
    title = info.get('title', name)
    description = get_contract_description(name, config)

    # 関数をOpenAPI specから抽出
    api_elements = extract_api_elements(spec)
    functions = api_elements['functions']

    # イベントとエラーをContract Spec JSONから抽出
    events = contract_spec_json.get('events', []) if contract_spec_json else []
    custom_errors = contract_spec_json.get('customErrors', {}) if contract_spec_json else {}

    # Markdown生成
    markdown = f"""---
id: {name}
title: {title}
sidebar_label: {name}
---

# {title}

{description}

## 📖 API仕様書

詳細なAPI仕様は以下のリンクから確認できます。

📋 [{name} API仕様書を見る](/docs/api/{name}/{name.lower()}コントラクト)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| コントラクト名 | {name} |
| カテゴリ | {category} |
| バージョン | {info.get('version', '1.0.0')} |

## 📚 概要

このコントラクトは以下の機能を提供します。

（※ このセクションはAIエンハンスで詳細化する必要があります）

## 🔧 主要機能

このセクションでは、コントラクトの主要な機能について詳細に説明します。

（※ このセクションはAIエンハンスで以下を追加する必要があります）
- 各主要機能の詳細説明（h3見出しごと）
- 必要に応じてシーケンス図（mermaid記法）

## 📋 機能一覧

{generate_functions_table(functions, contract_spec_json)}

{generate_table(events, 'イベント')}

{generate_table([
    {
        'name': err.get('signature', '').split('(')[0] if err.get('signature') else 'Unknown',
        'description': err.get('description', '')
    }
    for err in custom_errors.values()
], 'エラー')}
"""

    return markdown


def generate_sidebars(contracts: List[Dict[str, Any]], categories: Dict[str, List[str]]) -> str:
    """sidebars.jsを生成"""
    # カテゴリごとにグループ化
    grouped = {}

    for contract in contracts:
        category = contract.get('category')
        if category:
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(f"contracts/{contract['name']}")

    # sidebars.js生成
    sidebars_content = """module.exports = {
  docsSidebar: [
    "overview",
    "architecture",
    "roles",
    "security",
    "testing",
    "upgrade",
    "audit",
"""

    for category, items in grouped.items():
        sidebars_content += '    {\n'
        sidebars_content += '        "type": "category",\n'
        sidebars_content += f'        "label": "{category}",\n'
        sidebars_content += '        "items": [\n'

        for item in items:
            sidebars_content += f'            "{item}",\n'

        sidebars_content += '        ]\n'
        sidebars_content += '    },\n'

    sidebars_content += """  ],
};
"""

    return sidebars_content


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description='Generate contract documentation from OpenAPI specs')
    parser.add_argument('--specs-dir', help='Specs directory path')
    parser.add_argument('--docs-dir', help='Docs output directory path')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--ir-dir', help='Contract Spec JSON directory path')
    args = parser.parse_args()

    # パスの設定（引数がない場合はデフォルト値を使用）
    SPECS_DIR = Path(args.specs_dir or 'docs/contract/specs')
    DOCS_DIR = Path(args.docs_dir or 'docs/contract/docs')
    CONFIG_PATH = Path(args.config or 'docs/contract/doc-config.json')
    CONTRACT_SPEC_JSON_DIR = Path(args.ir_dir or SPECS_DIR.parent / 'ir')

    print('📝 Generating contract documentation...\n')
    print(f'Specs directory: {SPECS_DIR}')
    print(f'Docs output directory: {DOCS_DIR}')
    print(f'Config file: {CONFIG_PATH}\n')

    # Config読み込み
    config = load_config(CONFIG_PATH)
    categories = config['categories']

    print('📂 Categories defined in config:')
    for category, contracts in categories.items():
        print(f'  - {category}: {len(contracts)} contracts')
    print('')

    # コントラクト検出
    contracts = find_contracts(SPECS_DIR)

    if not contracts:
        print('Error: No contracts found in specs directory', file=sys.stderr)
        sys.exit(1)

    print(f'Found {len(contracts)} contracts in specs directory:\n')

    # 各コントラクトにカテゴリを割り当て
    for contract in contracts:
        contract['category'] = categorize_contract(contract['name'], categories)

    # カテゴリが見つからなかったコントラクトをフィルター
    valid_contracts = [c for c in contracts if c.get('category')]

    # カテゴリ別集計
    category_count = {}
    for contract in valid_contracts:
        category = contract['category']
        category_count[category] = category_count.get(category, 0) + 1

    print('📊 Contract distribution by category:')
    for category, count in category_count.items():
        print(f'  - {category}: {count} contracts')
    print('')

    # 出力ディレクトリ作成
    contracts_dir = DOCS_DIR / 'contracts'
    contracts_dir.mkdir(parents=True, exist_ok=True)

    # 各コントラクトのMarkdown生成
    success_count = 0
    error_count = 0

    print('📄 Generating Markdown files:\n')
    for contract in valid_contracts:
        try:
            spec = load_openapi_spec(contract['yamlPath'])

            if not spec:
                print(f"  ✗ {contract['name']}: Failed to load OpenAPI spec")
                error_count += 1
                continue

            # Contract Spec JSON (IR) を読み込み
            contract_spec_json = None
            spec_json_path = CONTRACT_SPEC_JSON_DIR / f"{contract['name']}.json"

            if spec_json_path.exists():
                with spec_json_path.open('r', encoding='utf-8') as f:
                    contract_spec_json = json.load(f)

            markdown = generate_markdown(contract, spec, contract['category'], config, contract_spec_json)
            output_path = contracts_dir / f"{contract['name']}.md"

            output_path.write_text(markdown, encoding='utf-8')
            print(f"  ✓ {contract['name']} ({contract['category']})")
            success_count += 1
        except Exception as error:
            print(f"  ✗ {contract['name']}: {error}", file=sys.stderr)
            error_count += 1

    print('')

    # sidebars.js生成
    try:
        sidebars_content = generate_sidebars(valid_contracts, categories)
        sidebars_path = DOCS_DIR / 'sidebars.js'
        sidebars_path.write_text(sidebars_content, encoding='utf-8')
        print(f'✓ sidebars.js generated: {sidebars_path}')
    except Exception as error:
        print(f'✗ Failed to generate sidebars.js: {error}', file=sys.stderr)
        error_count += 1

    print('')
    print('✅ Documentation generation complete!')
    print(f'   Success: {success_count} contracts')
    if error_count > 0:
        print(f'   Errors: {error_count} contracts')
    print('')
    print('⚠️  Next step: Run AI enhancement (Step 2.2) to complete the documentation')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
