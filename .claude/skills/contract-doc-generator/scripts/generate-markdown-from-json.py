#!/usr/bin/env python3

"""
generate-markdown-from-json.py

Contract Spec JSONからMarkdownドキュメントとsidebars.jsを生成

特徴:
  - Contract Spec JSONから詳細なMarkdownドキュメントを生成
  - カテゴリ別にsidebars.jsを自動生成
  - 関数、イベント、エラーの詳細情報を含む

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def generate_markdown_from_json(spec_path: Path, output_path: Path) -> Path:
    """Contract Spec JSONからMarkdownドキュメントを生成"""
    with spec_path.open('r', encoding='utf-8') as f:
        spec = json.load(f)

    markdown = f"""---
title: {spec['contractName']}
sidebar_label: {spec['contractName']}
---

# {spec['contractName']}

{spec['metadata']['description']}

"""

    # メタデータ情報
    if spec['metadata'].get('category') or spec['metadata'].get('tags'):
        markdown += "## メタデータ\n\n"
        if spec['metadata'].get('category'):
            markdown += f"- **カテゴリ**: {spec['metadata']['category']}\n"
        if spec['metadata'].get('tags'):
            markdown += f"- **タグ**: {', '.join(spec['metadata']['tags'])}\n"
        if spec['metadata'].get('inheritance'):
            markdown += f"- **継承**: {', '.join(spec['metadata']['inheritance'])}\n"
        markdown += '\n'

    # 関数一覧（読み取りと書き込みを統合）
    all_functions = spec.get('readFunctions', []) + spec.get('writeFunctions', [])

    if all_functions:
        markdown += "## 関数一覧\n\n"

        for func in all_functions:
            markdown += f"### {func['name']}\n\n"

            if func['documentation'].get('summary'):
                markdown += f"{func['documentation']['summary']}\n\n"

            if func['documentation'].get('details'):
                markdown += f"{func['documentation']['details']}\n\n"

            # シグネチャ
            markdown += f"**シグネチャ**: `{func['signature']}`\n\n"

            # モディファイア
            if func.get('modifiers'):
                modifiers_str = ', '.join(f"`{m}`" for m in func['modifiers'])
                markdown += f"**モディファイア**: {modifiers_str}\n\n"

            # パラメータ
            if func.get('parameters'):
                markdown += "**パラメータ:**\n\n"
                for param in func['parameters']:
                    markdown += f"- `{param['name']}` (`{param['type']}`): {param.get('description', '')}\n"
                markdown += '\n'

            # 戻り値
            if func.get('returnValues'):
                markdown += "**戻り値:**\n\n"
                for ret in func['returnValues']:
                    markdown += f"- `{ret['name']}` (`{ret['type']}`): {ret.get('description', '')}\n"
                markdown += '\n'

            # エラー
            if func.get('errors'):
                markdown += "**エラー:**\n\n"
                for error in func['errors']:
                    markdown += f"- `{error['name']}`: {error.get('description', '')}\n"
                    if error.get('triggerCondition'):
                        markdown += f"  - 発生条件: {error['triggerCondition']}\n"
                markdown += '\n'

            # 制約条件
            if func.get('constraints'):
                markdown += "**制約条件:**\n\n"
                # 配列とオブジェクトの両方に対応
                if isinstance(func['constraints'], list):
                    for constraint in func['constraints']:
                        markdown += f"- {constraint}\n"
                else:
                    for param_name, constraint in func['constraints'].items():
                        markdown += f"- `{param_name}`:\n"
                        if constraint.get('min'):
                            markdown += f"  - 最小値: {constraint['min']}\n"
                        if constraint.get('max'):
                            markdown += f"  - 最大値: {constraint['max']}\n"
                        if constraint.get('description'):
                            markdown += f"  - {constraint['description']}\n"
                markdown += '\n'

            # 前提条件
            if func.get('preconditions'):
                markdown += "**前提条件:**\n\n"
                for condition in func['preconditions']:
                    markdown += f"- {condition}\n"
                markdown += '\n'

            # 関連関数
            if func.get('relatedFunctions'):
                markdown += "**関連関数:**\n\n"
                for related in func['relatedFunctions']:
                    # 文字列の配列とオブジェクトの配列の両方に対応
                    if isinstance(related, str):
                        markdown += f"- [`{related}`](#{related.lower()})\n"
                    else:
                        markdown += f"- [`{related['name']}`](#{related['name'].lower()}) ({related.get('relationship', '')}): {related.get('description', '')}\n"
                markdown += '\n'

            # 使用例
            if func.get('examples'):
                markdown += "**使用例:**\n\n"
                for example in func['examples']:
                    markdown += f"<details>\n<summary>{example.get('title', 'Example')}</summary>\n\n"
                    if example.get('description'):
                        markdown += f"{example['description']}\n\n"
                    markdown += "```json\n"
                    markdown += f"// 入力\n{json.dumps(example.get('input', {}), ensure_ascii=False, indent=2)}\n\n"
                    if example.get('output'):
                        markdown += f"// 出力\n{json.dumps(example['output'], ensure_ascii=False, indent=2)}\n"
                    if example.get('expectedError'):
                        markdown += f'// 期待されるエラー\n"{example["expectedError"]}"\n'
                    markdown += "```\n\n"
                    if example.get('notes'):
                        markdown += f"> **Note**: {example['notes']}\n\n"
                    markdown += "</details>\n\n"

            markdown += "---\n\n"

    # イベント一覧
    events = spec.get('events', [])
    if events:
        markdown += "## イベント一覧\n\n"
        for event in events:
            markdown += f"### {event['name']}\n\n"

            if event.get('documentation', {}).get('summary'):
                markdown += f"{event['documentation']['summary']}\n\n"

            markdown += f"**シグネチャ**: `{event['signature']}`\n\n"

            markdown += "**パラメータ:**\n\n"
            for param in event.get('parameters', []):
                indexed = ' (indexed)' if param.get('indexed') else ''
                markdown += f"- `{param['name']}` (`{param['type']}`){indexed}"
                if param.get('description'):
                    markdown += f": {param['description']}"
                markdown += '\n'
            markdown += '\n'

            if event.get('useCases'):
                markdown += "**ユースケース:**\n\n"
                for use_case in event['useCases']:
                    markdown += f"- {use_case}\n"
                markdown += '\n'

            if event.get('emittedBy'):
                emitted_by_str = ', '.join(f"`{f}()`" for f in event['emittedBy'])
                markdown += f"**発火元:** {emitted_by_str}\n\n"

            markdown += "---\n\n"

    # カスタムエラー一覧
    custom_errors = spec.get('customErrors', {})
    if custom_errors:
        markdown += "## カスタムエラー一覧\n\n"
        for error_name, error in custom_errors.items():
            markdown += f"### {error_name}\n\n"
            markdown += f"{error.get('description', '')}\n\n"
            markdown += f"**シグネチャ**: `{error.get('signature', '')}`\n\n"

            if error.get('parameters'):
                markdown += "**パラメータ:**\n\n"
                for param in error['parameters']:
                    markdown += f"- `{param['name']}` (`{param['type']}`)"
                    if param.get('description'):
                        markdown += f": {param['description']}"
                    markdown += '\n'
                markdown += '\n'

            if error.get('triggerCondition'):
                markdown += f"**発生条件**: {error['triggerCondition']}\n\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding='utf-8')
    print(f'✅ Markdown generated: {output_path.name}')

    return output_path


def generate_sidebars_js(contracts_by_category: Dict[str, List[str]], output_path: Path) -> Path:
    """sidebars.jsを生成"""
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

    for category, contracts in contracts_by_category.items():
        sidebars_content += '    {\n'
        sidebars_content += '      "type": "category",\n'
        sidebars_content += f'      "label": "{category}",\n'
        sidebars_content += '      "items": [\n'

        for contract in contracts:
            sidebars_content += f'        "contracts/{contract}",\n'

        sidebars_content += '      ]\n'
        sidebars_content += '    },\n'

    sidebars_content += """  ],
};
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(sidebars_content, encoding='utf-8')
    print(f'✅ sidebars.js generated: {output_path}')

    return output_path


def main():
    """メイン処理"""
    REVIEWED_DIR = Path('docs/contract/contract-specs-reviewed')
    DOCS_OUTPUT_DIR = Path('docs/contract/docs/contracts')
    SIDEBARS_OUTPUT_PATH = Path('docs/contract/docs/sidebars.js')

    print('📝 Generating Markdown docs from reviewed JSONs...\n')

    # レビュー済みディレクトリが存在しない場合は通常のディレクトリを使用
    spec_dir = REVIEWED_DIR if REVIEWED_DIR.exists() else Path('docs/contract/contract-specs')
    print(f'Using spec directory: {spec_dir}\n')

    if not spec_dir.exists():
        print(f'❌ Error: Spec directory not found: {spec_dir}', file=sys.stderr)
        print('Please run generate-contract-spec-json.py first', file=sys.stderr)
        sys.exit(1)

    # 出力ディレクトリ作成
    DOCS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = [f for f in spec_dir.iterdir() if f.suffix == '.json']

    if not files:
        print(f'❌ Error: No JSON files found in {spec_dir}', file=sys.stderr)
        sys.exit(1)

    results = []
    contracts_by_category = {}

    for file in files:
        contract_name = file.stem
        output_path = DOCS_OUTPUT_DIR / f'{contract_name}.md'

        try:
            output = generate_markdown_from_json(file, output_path)
            results.append({'contractName': contract_name, 'success': True, 'outputPath': str(output)})

            # カテゴリ別に整理
            with file.open('r', encoding='utf-8') as f:
                spec = json.load(f)
            category = spec.get('metadata', {}).get('category', 'Uncategorized')
            if category not in contracts_by_category:
                contracts_by_category[category] = []
            contracts_by_category[category].append(contract_name)
        except Exception as error:
            print(f'❌ Error processing {contract_name}: {error}', file=sys.stderr)
            results.append({'contractName': contract_name, 'success': False, 'error': str(error)})

    # sidebars.js生成
    print('\n📝 Generating sidebars.js...\n')
    generate_sidebars_js(contracts_by_category, SIDEBARS_OUTPUT_PATH)

    print('\n' + '=' * 60)
    print('📊 Generation Summary')
    print('=' * 60)
    print(f'Total contracts: {len(results)}')
    print(f'Success: {sum(1 for r in results if r["success"])}')
    print(f'Failed: {sum(1 for r in results if not r["success"])}')

    if any(r['success'] for r in results):
        print('\n✅ Generated files:')
        for r in results:
            if r['success']:
                print(f'   - {r["outputPath"]}')

    print(f'\n✅ All Markdown docs generated!')
    print(f'📂 Output directory: {DOCS_OUTPUT_DIR}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
