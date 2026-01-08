#!/usr/bin/env python3

"""
generate-openapi-from-json.py

Contract Spec JSONからOpenAPI 3.0仕様書を生成

特徴:
- エラー情報が構造化されているため、500エラーのExampleが自動生成される
- JSON Schemaからの変換が簡単（型マッピング不要）
- NatSpecドキュメントがそのまま使える

Requirements:
    - Python 3.7+
    - PyYAML: pip install pyyaml
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print('Error: PyYAML is required. Install it with: pip install pyyaml', file=sys.stderr)
    sys.exit(1)


def map_solidity_to_json_type(solidity_type: str) -> str:
    """Solidity型をJSON Schema型にマッピング"""
    if solidity_type == 'address':
        return 'string'
    if solidity_type == 'bool':
        return 'boolean'
    if solidity_type.startswith('uint') or solidity_type.startswith('int'):
        return 'string'
    if solidity_type == 'string':
        return 'string'
    if solidity_type == 'bytes':
        return 'string'
    if solidity_type.endswith('[]'):
        return 'array'
    return 'string'


def to_camel_case(text: str) -> str:
    """関数名をcamelCaseに変換（operationId用）"""
    # 先頭を小文字に
    return text[0].lower() + text[1:] if text else text


def build_responses(func: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    """レスポンススキーマを構築"""
    responses = {
        '200': {
            'description': 'Successful operation',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {}
                    }
                }
            }
        }
    }

    # 戻り値がある場合
    if func.get('returnValues'):
        for ret in func['returnValues']:
            responses['200']['content']['application/json']['schema']['properties'][ret['name']] = {
                'type': map_solidity_to_json_type(ret['type']),
                'description': ret.get('description', '')
            }

    # 500エラーレスポンス
    # errorsが空で書き込み関数の場合、customErrorsから全エラーを使用
    error_list = func.get('errors', [])
    custom_errors = spec.get('customErrors', {})

    if not error_list and custom_errors:
        # 書き込み関数（view/pureでない）の場合のみ
        if func.get('stateMutability') not in ('view', 'pure'):
            # customErrorsから名前付きエラーオブジェクトを生成
            error_list = [
                {
                    'name': name,
                    'signature': error.get('signature', ''),
                    'parameters': error.get('parameters', []),
                    'description': error.get('description', ''),
                    'exampleValue': {
                        'error': name,
                        'message': error.get('description', '')
                    }
                }
                for name, error in custom_errors.items()
            ]

    if error_list:
        # エラー一覧を生成（エラー名を太字、説明を別行に表示）
        error_descriptions = []
        for e in error_list:
            if isinstance(e, str):
                # 文字列形式の場合、" - " で分割（後方互換性のため）
                parts = e.split(' - ')
                error_name = parts[0]
                error_description = ' - '.join(parts[1:]) if len(parts) > 1 else ''
            else:
                # オブジェクト形式（推奨）
                error_name = e.get('name', '')
                error_description = e.get('description', '')

            # spec.customErrorsから説明を取得
            if not error_description and error_name in custom_errors:
                error_description = custom_errors[error_name].get('description', '')

            # エラー名を太字、説明を次の行に
            if error_description:
                error_descriptions.append(f'・**{error_name}**<br>{error_description}<br>')
            else:
                error_descriptions.append(f'・**{error_name}**<br>')

        error_descriptions_text = ''.join(error_descriptions)

        # descriptionの生成
        is_from_custom_errors = (not func.get('errors') and error_list)
        description_prefix = (
            'このコントラクトで定義されている全カスタムエラーが発生する可能性があります。<br>'
            if is_from_custom_errors else
            'この関数で発生する可能性のあるエラーの一覧です。<br>'
        )

        responses['500'] = {
            'description': f'{description_prefix}{error_descriptions_text}',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/ErrorResponse'
                    },
                    'examples': {}
                }
            }
        }

        # 各エラーのExampleを追加
        for error in error_list:
            if isinstance(error, str):
                # 文字列形式の場合、" - " で分割（後方互換性のため）
                parts = error.split(' - ')
                error_name = parts[0]
                error_description = ' - '.join(parts[1:]) if len(parts) > 1 else ''
                error_example = None
            else:
                # オブジェクト形式（推奨）
                error_name = error.get('name', '')
                error_description = error.get('description', '')
                error_example = error.get('exampleValue')

            # spec.customErrorsから説明を取得
            if not error_description and error_name in custom_errors:
                error_description = custom_errors[error_name].get('description', '')

            responses['500']['content']['application/json']['examples'][error_name] = {
                'summary': error_name,
                'value': error_example or {
                    'error': error_name,
                    'message': error_description or error_name
                }
            }

    return responses


def generate_openapi_from_json(spec_path: Path, output_path: Path) -> Path:
    """OpenAPI仕様書を生成"""
    print(f'\n📝 Generating OpenAPI spec from {spec_path.name}...')

    # Contract Spec JSONを読み込み
    with spec_path.open('r', encoding='utf-8') as f:
        spec = json.load(f)

    # OpenAPI基本構造
    openapi = {
        'openapi': '3.0.0',
        'info': {
            'title': spec.get('metadata', {}).get('title') or f"{spec['contractName']} API",
            'description': spec.get('metadata', {}).get('description', ''),
            'version': spec.get('version', '1.0.0')
        },
        'servers': [
            {
                'url': 'https://api.example.com/v1',
                'description': 'Production server'
            }
        ],
        'paths': {},
        'components': {
            'schemas': {
                'ErrorResponse': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    }

    # 読み取り関数を処理（GET）
    read_functions = spec.get('readFunctions', [])
    for func in read_functions:
        path_key = f"/{func['name']}"
        parameters = [
            {
                'name': param['name'],
                'in': 'query',
                'required': True,
                'schema': {
                    'type': map_solidity_to_json_type(param['type'])
                },
                'description': param.get('description', '')
            }
            for param in func.get('parameters', [])
        ]

        responses = build_responses(func, spec)

        openapi['paths'][path_key] = {
            'get': {
                'summary': func.get('documentation', {}).get('summary') or func['name'],
                'description': func.get('documentation', {}).get('details', ''),
                'operationId': to_camel_case(func['name']),
                'tags': ['Read Functions'],
                'parameters': parameters,
                'responses': responses
            }
        }

    # 書き込み関数を処理（POST）
    write_functions = spec.get('writeFunctions', [])
    for func in write_functions:
        path_key = f"/{func['name']}"
        request_body = {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'required': [p['name'] for p in func.get('parameters', [])],
                        'properties': {}
                    }
                }
            }
        }

        for param in func.get('parameters', []):
            request_body['content']['application/json']['schema']['properties'][param['name']] = {
                'type': map_solidity_to_json_type(param['type']),
                'description': param.get('description', '')
            }

        responses = build_responses(func, spec)

        openapi['paths'][path_key] = {
            'post': {
                'summary': func.get('documentation', {}).get('summary') or func['name'],
                'description': func.get('documentation', {}).get('details', ''),
                'operationId': to_camel_case(func['name']),
                'tags': ['Write Functions'],
                'requestBody': request_body,
                'responses': responses
            }
        }

    # YAML出力
    yaml_content = yaml.dump(openapi, allow_unicode=True, default_flow_style=False,
                            sort_keys=False, width=float('inf'))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml_content, encoding='utf-8')

    all_functions = read_functions + write_functions
    functions_with_errors = sum(1 for f in all_functions if f.get('errors'))

    print(f'✅ OpenAPI spec generated: {output_path.name}')
    print(f'   - Paths: {len(openapi["paths"])}')
    print(f'   - Read Functions (GET): {len(read_functions)}')
    print(f'   - Write Functions (POST): {len(write_functions)}')
    print(f'   - Functions with errors: {functions_with_errors}')

    return output_path


def main():
    """メイン処理"""
    # パス設定（環境変数で上書き可能）
    IR_DIR = Path(os.getenv('IR_DIR', 'docs/contract/ir'))
    OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', 'docs/contract/specs'))

    print('📝 OpenAPI仕様書生成中（Contract Spec JSONから）...\n')

    spec_dir = IR_DIR
    print(f'   使用するディレクトリ: {spec_dir}\n')

    if not spec_dir.exists():
        print(f'❌ エラー: ディレクトリが見つかりません: {spec_dir}', file=sys.stderr)
        print('先に generate-contract-spec-json.py を実行してください', file=sys.stderr)
        sys.exit(1)

    files = list(spec_dir.glob('*.json'))

    if not files:
        print(f'❌ エラー: {spec_dir} にJSONファイルが見つかりません', file=sys.stderr)
        sys.exit(1)

    print(f'   対象ファイル: {len(files)}個\n')

    results = []

    for file_path in files:
        contract_name = file_path.stem
        output_path = OUTPUT_DIR / contract_name / f'{contract_name}.openapi.yaml'

        try:
            output = generate_openapi_from_json(file_path, output_path)
            results.append({'contractName': contract_name, 'success': True, 'outputPath': str(output)})
        except Exception as error:
            print(f'❌ Error processing {contract_name}: {error}', file=sys.stderr)
            results.append({'contractName': contract_name, 'success': False, 'error': str(error)})

    print('\n' + '=' * 60)
    print('📊 生成サマリー')
    print('=' * 60)
    print(f'総コントラクト数: {len(results)}')
    print(f'成功: {sum(1 for r in results if r["success"])}')
    print(f'失敗: {sum(1 for r in results if not r["success"])}')

    if any(r['success'] for r in results):
        print('\n✅ 生成されたファイル:')
        for r in results:
            if r['success']:
                print(f'   - {r["outputPath"]}')

    print('\n✅ 全OpenAPI仕様書の生成が完了しました！')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'致命的なエラー: {error}', file=sys.stderr)
        sys.exit(1)
