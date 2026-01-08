#!/usr/bin/env python3

"""
enhance-openapi-examples.py

OpenAPI仕様書の500エラーレスポンスに個別Examplesを自動追加するスクリプト

特徴:
  - 全OpenAPI YAML仕様書をスキャン
  - 500エラーレスポンスを検出
  - エラー名に基づいた適切なExampleを生成
  - 冪等性を保証（既存examplesはスキップ）
  - 統計サマリーを出力

使用方法:
  python enhance-openapi-examples.py --specs-dir <specs-dir>

例:
  python enhance-openapi-examples.py --specs-dir docs/contract/specs

Requirements:
    - Python 3.7+
    - PyYAML: pip install pyyaml
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print('Error: PyYAML is required. Install it with: pip install pyyaml', file=sys.stderr)
    sys.exit(1)


def generate_error_example(error_name: str, error_schema: Dict[str, Any]) -> Dict[str, Any]:
    """エラー名とスキーマから適切なExampleを生成"""
    example = {
        'summary': f"{error_name} - {error_schema.get('description', 'Error occurred')}",
        'value': {
            'error': error_name,
            'message': error_schema.get('description', f'{error_name} occurred'),
            'code': 500
        }
    }

    # エラー名パターンに応じた追加フィールド
    if any(keyword in error_name for keyword in ['Unauthorized', 'NotAuthorized', 'AccessDenied']):
        example['value']['details'] = {
            'requiredRole': 'ADMIN_ROLE',
            'currentRole': 'USER_ROLE',
            'caller': '0x1234567890123456789012345678901234567890'
        }
    elif any(keyword in error_name for keyword in ['InvalidAmount', 'InsufficientBalance', 'AmountTooLarge']):
        example['value']['details'] = {
            'requestedAmount': '1000000000000000000',
            'availableAmount': '500000000000000000',
            'unit': 'wei'
        }
    elif 'Paused' in error_name:
        example['value']['details'] = {
            'status': 'paused',
            'pausedAt': '2024-01-15T10:30:00Z',
            'pausedBy': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0'
        }
    elif 'ZeroAddress' in error_name:
        example['value']['details'] = {
            'providedAddress': '0x0000000000000000000000000000000000000000',
            'parameter': 'account'
        }
    elif any(keyword in error_name for keyword in ['InvalidParameter', 'InvalidInput']):
        example['value']['details'] = {
            'parameter': 'amount',
            'providedValue': '0',
            'expectedCondition': 'greater than 0'
        }
    elif any(keyword in error_name for keyword in ['Expired', 'Deadline']):
        example['value']['details'] = {
            'deadline': '2024-01-15T10:00:00Z',
            'currentTime': '2024-01-15T11:00:00Z'
        }
    elif any(keyword in error_name for keyword in ['AlreadyExists', 'Duplicate']):
        example['value']['details'] = {
            'existingValue': 'existing_value',
            'attemptedValue': 'new_value'
        }
    elif any(keyword in error_name for keyword in ['NotFound', 'DoesNotExist']):
        example['value']['details'] = {
            'searchedValue': 'searched_value',
            'searchedIn': 'registry'
        }
    elif 'Reentrancy' in error_name:
        example['value']['details'] = {
            'status': 'locked',
            'caller': '0x1234567890123456789012345678901234567890'
        }

    return example


def enhance_examples(spec: Dict[str, Any]) -> Dict[str, Any]:
    """OpenAPI仕様書のpathsから500エラーを持つoperationを検出し、Examplesを追加"""
    stats = {
        'functionsProcessed': 0,
        'functionsWith500': 0,
        'examplesAdded': 0,
        'functionsSkipped': 0,
        'enhancedOperations': []
    }

    if not spec or 'paths' not in spec:
        return stats

    for path_key, path_item in spec['paths'].items():
        for method, operation in path_item.items():
            if not isinstance(operation, dict) or 'operationId' not in operation:
                continue

            stats['functionsProcessed'] += 1
            operation_id = operation['operationId']

            # 500エラーレスポンスをチェック
            if 'responses' not in operation or '500' not in operation['responses']:
                continue

            stats['functionsWith500'] += 1

            response_500 = operation['responses']['500']
            if 'content' not in response_500 or 'application/json' not in response_500['content']:
                continue

            json_content = response_500['content']['application/json']

            # 既にexamplesが存在する場合はスキップ
            if 'examples' in json_content and json_content['examples']:
                stats['functionsSkipped'] += 1
                continue

            # schemaからエラー定義を抽出
            schema = json_content.get('schema')
            if not schema or 'oneOf' not in schema:
                continue

            # examplesオブジェクトを作成
            examples = {}
            example_count = 0

            for error_ref in schema['oneOf']:
                if '$ref' not in error_ref:
                    continue

                # $ref から エラー名を抽出 (例: "#/components/schemas/UnauthorizedError" → "UnauthorizedError")
                error_name = error_ref['$ref'].split('/')[-1]

                # components.schemasからエラー定義を取得
                error_schema = spec.get('components', {}).get('schemas', {}).get(error_name)
                if not error_schema:
                    continue

                # Exampleを生成
                example = generate_error_example(error_name, error_schema)
                examples[error_name] = example
                example_count += 1

            if example_count > 0:
                # examplesを追加
                json_content['examples'] = examples
                stats['examplesAdded'] += example_count
                stats['enhancedOperations'].append({
                    'operationId': operation_id,
                    'count': example_count,
                    'errors': list(examples.keys())
                })

    return stats


def find_contracts(specs_dir: Path) -> List[Dict[str, Path]]:
    """specsディレクトリから全てのコントラクトを検出"""
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


def load_openapi_spec(yaml_path: Path) -> Dict[str, Any]:
    """OpenAPI仕様書を読み込み"""
    try:
        content = yaml_path.read_text(encoding='utf-8')
        return yaml.safe_load(content)
    except Exception as error:
        print(f'Error loading OpenAPI spec: {yaml_path} - {error}', file=sys.stderr)
        return None


def save_openapi_spec(yaml_path: Path, spec: Dict[str, Any]) -> bool:
    """OpenAPI仕様書を書き込み"""
    try:
        yaml_content = yaml.dump(spec, allow_unicode=True, default_flow_style=False,
                                sort_keys=False, width=float('inf'))
        yaml_path.write_text(yaml_content, encoding='utf-8')
        return True
    except Exception as error:
        print(f'Error saving OpenAPI spec: {yaml_path} - {error}', file=sys.stderr)
        return False


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Enhance OpenAPI Examples')
    parser.add_argument('--specs-dir', required=True, help='Specs directory path')
    args = parser.parse_args()

    specs_dir = Path(args.specs_dir)

    print('📝 Enhancing OpenAPI Examples...\n')
    print(f'Specs directory: {specs_dir}')

    # コントラクト検出
    contracts = find_contracts(specs_dir)

    if not contracts:
        print('Error: No contracts found in specs directory', file=sys.stderr)
        sys.exit(1)

    print(f'Total contracts found: {len(contracts)}\n')
    print('━' * 40 + '\n')

    # 統計
    total_functions_processed = 0
    total_functions_with_500 = 0
    total_examples_added = 0
    total_functions_skipped = 0
    success_count = 0
    error_count = 0

    # 各コントラクトを処理
    for contract in contracts:
        try:
            spec = load_openapi_spec(contract['yamlPath'])

            if not spec:
                print(f"✗ {contract['name']}: Failed to load OpenAPI spec")
                error_count += 1
                continue

            # Examplesを追加
            stats = enhance_examples(spec)

            # 結果を保存
            if stats['examplesAdded'] > 0:
                saved = save_openapi_spec(contract['yamlPath'], spec)
                if not saved:
                    print(f"✗ {contract['name']}: Failed to save OpenAPI spec")
                    error_count += 1
                    continue

            # 統計を更新
            total_functions_processed += stats['functionsProcessed']
            total_functions_with_500 += stats['functionsWith500']
            total_examples_added += stats['examplesAdded']
            total_functions_skipped += stats['functionsSkipped']

            # 出力
            print(f"Processing: {contract['name']}/{contract['name']}.openapi.yaml")
            for op in stats['enhancedOperations']:
                errors_str = ', '.join(op['errors'])
                print(f"  ✓ {op['operationId']}: Added {op['count']} error examples ({errors_str})")
            if stats['functionsSkipped'] > 0:
                print(f"  ⊘ {stats['functionsSkipped']} function(s): Examples already exist, skipping")
            print('')

            success_count += 1
        except Exception as error:
            print(f"✗ {contract['name']}: {error}", file=sys.stderr)
            error_count += 1

    print('━' * 40 + '\n')
    print('✅ Enhancement complete!\n')
    print('📊 Summary:')
    print(f'   Total contracts processed: {len(contracts)}')
    print(f'   Successful: {success_count}')
    if error_count > 0:
        print(f'   Errors: {error_count}')
    print(f'   Total functions processed: {total_functions_processed}')
    print(f'   Functions with 500 errors: {total_functions_with_500}')
    print(f'   Examples added: {total_examples_added}')
    print(f'   Functions skipped (already has examples): {total_functions_skipped}')
    print('')
    print('⚠️  Next step: AI should verify the generated examples')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
