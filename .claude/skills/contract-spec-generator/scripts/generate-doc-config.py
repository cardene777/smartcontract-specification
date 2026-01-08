#!/usr/bin/env python3

"""
generate-doc-config.py

Contract Spec JSONとOpenAPI仕様書からdoc-config.jsonを生成

特徴:
- filtered.jsonから選択されたコントラクトリストを読み込み
- OpenAPI仕様書から説明を抽出
- コントラクト名のプレフィックスでカテゴリを自動分類
- プロジェクト情報はデフォルト値を設定

依存パッケージ:
  pip install pyyaml
"""

import json
import sys
from pathlib import Path
from typing import Dict

try:
    import yaml
except ImportError:
    print('エラー: PyYAMLが必要です', file=sys.stderr)
    print('インストール: pip install pyyaml', file=sys.stderr)
    sys.exit(1)


def categorize_contract(contract_name: str) -> str:
    """コントラクト名からカテゴリを判定"""
    if contract_name.startswith('Stablecoin'):
        return 'Stablecoin Contracts'
    if contract_name.startswith('Bank'):
        return 'Bank Management'
    if (contract_name.startswith('MultiSig') or
        contract_name.startswith('DualKey') or
        contract_name.startswith('AccessControl') or
        contract_name.startswith('RoleMultiSig')):
        return 'Access Control & MultiSig'
    return 'Other Contracts'


def extract_description(openapi_path: Path) -> Dict[str, str]:
    """OpenAPI仕様書から説明を抽出"""
    try:
        with open(openapi_path, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)

        description = spec.get('info', {}).get('description', '')

        return {
            'overview': description or f'{openapi_path.stem.replace(".openapi", "")}コントラクト',
            'detail': description or ''
        }
    except Exception as error:
        print(f'⚠️  Failed to extract description from {openapi_path}: {error}', file=sys.stderr)
        contract_name = openapi_path.stem.replace('.openapi', '')
        return {
            'overview': f'{contract_name}コントラクト',
            'detail': ''
        }


def generate_doc_config():
    """doc-config.jsonを生成"""
    print('📝 doc-config.json生成中...\n')

    FILTERED_JSON = Path('docs/contract/filtered.json')
    SPECS_DIR = Path('docs/contract/specs')
    OUTPUT_PATH = Path('docs/contract/doc-config.json')

    # filtered.jsonから選択されたコントラクトリストを読み込み
    if not FILTERED_JSON.exists():
        print(f'❌ エラー: {FILTERED_JSON} が見つかりません', file=sys.stderr)
        print('先に /generate-contract-specs を実行してください', file=sys.stderr)
        sys.exit(1)

    with open(FILTERED_JSON, 'r', encoding='utf-8') as f:
        filtered = json.load(f)

    contracts = filtered['selected']

    print(f'   対象コントラクト: {len(contracts)}個\n')

    # カテゴリ別にコントラクトを分類
    categories = {}
    descriptions = {}

    for contract_name in contracts:
        # カテゴリ判定
        category = categorize_contract(contract_name)

        if category not in categories:
            categories[category] = []
        categories[category].append(contract_name)

        # OpenAPI仕様書から説明を抽出
        openapi_path = SPECS_DIR / contract_name / f'{contract_name}.openapi.yaml'

        if openapi_path.exists():
            descriptions[contract_name] = extract_description(openapi_path)
        else:
            print(f'⚠️  OpenAPI仕様書が見つかりません: {openapi_path}', file=sys.stderr)
            descriptions[contract_name] = {
                'overview': f'{contract_name}コントラクト',
                'detail': ''
            }

    # doc-config.json生成
    config = {
        'projectTitle': 'Contract Documentation',
        'projectName': 'Avalanche Stablecoin',
        'tagline': 'Smart Contract Documentation',
        'projectDescription': 'Comprehensive documentation for Avalanche Stablecoin smart contracts',
        'githubOrg': 'your-org',
        'repoName': 'your-repo',
        'baseUrl': '/',
        'primaryColor': '#1890ff',
        'categories': categories,
        'descriptions': descriptions
    }

    # 出力ディレクトリ作成
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 保存
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f'✅ doc-config.jsonを生成しました: {OUTPUT_PATH}\n')
    print('📊 カテゴリ別コントラクト数:')
    for category, contract_list in categories.items():
        print(f'   - {category}: {len(contract_list)}個')
    print()
    print('⚠️  プロジェクト情報（projectTitle, githubOrg等）はデフォルト値です。')
    print('   必要に応じて docs/contract/doc-config.json を編集してください。\n')
    print('✅ 次のステップ: /generate-contract-docs でドキュメントを生成できます。')


if __name__ == '__main__':
    try:
        generate_doc_config()
    except Exception as error:
        print(f'致命的なエラー: {error}', file=sys.stderr)
        sys.exit(1)
