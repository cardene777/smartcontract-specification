#!/usr/bin/env python3

"""
generate-contract-spec-json.py

SolidityソースコードとABIからContract Spec JSONを生成
- ABIから関数・イベント・エラー情報を抽出
- NatSpecコメントを解析
- エラー情報を構造化

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def extract_inherited_interfaces(source_code: str) -> List[str]:
    """継承しているinterfaceを検出"""
    match = re.search(r'contract\s+\w+\s+is\s+([^{]+)', source_code)
    if not match:
        return []

    inheritance_list = [s.strip() for s in match.group(1).split(',')]
    return [name for name in inheritance_list if re.match(r'^I[A-Z]', name)]


def load_interface_source(interface_name: str, contract_dir: Path) -> Optional[str]:
    """interfaceのソースコードを読み込み"""
    possible_paths = [
        contract_dir / 'interfaces' / f'{interface_name}.sol',
        contract_dir / f'{interface_name}.sol'
    ]

    for interface_path in possible_paths:
        if interface_path.exists():
            return interface_path.read_text(encoding='utf-8')

    return None


def translate_to_japanese(text: str) -> str:
    """英語を日本語に翻訳（簡易版）"""
    if not text:
        return ''

    translations = {
        'mint': 'ミント', 'Mint': 'ミント',
        'burn': 'バーン', 'Burn': 'バーン',
        'transfer': '転送', 'Transfer': '転送',
        'allowlist': 'アローリスト', 'Allowlist': 'アローリスト',
        'bucket': 'バケット', 'Bucket': 'バケット',
        'bank': '銀行', 'Bank': '銀行',
        'pause': '一時停止', 'Pause': '一時停止',
        'admin': '管理', 'Admin': '管理',
        'role': 'ロール', 'Role': 'ロール',
        'issuer': '発行者', 'Issuer': '発行者',
        'token': 'トークン', 'Token': 'トークン',
        'Handles': '処理します', 'Manages': '管理します', 'Controls': '制御します',
        'for': 'の', 'to': 'へ', 'from': 'から', 'with': 'と', 'and': 'および',
        'Contract': 'コントラクト', 'contract': 'コントラクト'
    }

    result = text
    for eng, jpn in translations.items():
        result = re.sub(rf'\b{eng}\b', jpn, result)

    return result


def extract_contract_description(source: str) -> str:
    """ソースコードからコントラクトの説明を抽出"""
    match = re.search(r'/\*\*[\s\S]*?@title\s+(.+?)[\n*]', source)
    return match.group(1).strip() if match else ''


def extract_error_description(source: str, error_name: str) -> str:
    """エラーの説明を抽出"""
    regex = re.compile(rf'//\s*(.+?)\n\s*error\s+{error_name}', re.MULTILINE)
    match = regex.search(source)
    return match.group(1).strip() if match else ''


def extract_function_documentation(source: str, function_name: str,
                                   interface_sources: Dict[str, str]) -> Dict[str, str]:
    """関数のドキュメントを抽出（interfaceも参照）"""
    sources = [source] + list(interface_sources.values())

    for src in sources:
        # 関数定義の位置を探す
        func_regex = re.compile(rf'function\s+{function_name}\s*\(', re.MULTILINE)
        func_match = func_regex.search(src)
        if not func_match:
            continue

        func_index = func_match.start()
        before_func = src[:func_index]

        # 直前のコメントブロックを探す（最後に出現するもの）
        comment_matches = list(re.finditer(r'/\*\*([\s\S]*?)\*/', before_func))
        if not comment_matches:
            continue

        last_comment = comment_matches[-1]
        comment_block = last_comment.group(1)

        # コメントブロックと関数の間に別の関数がないか確認
        between_text = before_func[last_comment.end():]
        if re.search(r'function\s+\w+\s*\(', between_text):
            continue  # 別の関数がある場合はスキップ

        documentation = {}
        notice_match = re.search(r'@notice\s+([^\n\r]+)', comment_block)
        dev_match = re.search(r'@dev\s+([^\n\r]+)', comment_block)

        if notice_match:
            documentation['notice'] = notice_match.group(1).strip()
        if dev_match:
            documentation['details'] = dev_match.group(1).strip()
        documentation['summary'] = documentation.get('notice') or documentation.get('details', '')

        return documentation

    return {'summary': '', 'details': '', 'notice': ''}


def extract_param_description(source: str, function_name: str, param_name: str,
                              param_index: int, interface_sources: Dict[str, str]) -> str:
    """パラメータの説明を抽出（interfaceも参照）"""
    sources = [source] + list(interface_sources.values())

    for src in sources:
        # 関数定義の位置を探す
        func_regex = re.compile(rf'function\s+{function_name}\s*\(', re.MULTILINE)
        func_match = func_regex.search(src)
        if not func_match:
            continue

        func_index = func_match.start()
        before_func = src[:func_index]

        # 直前のコメントブロックを探す（最後に出現するもの）
        comment_matches = list(re.finditer(r'/\*\*([\s\S]*?)\*/', before_func))
        if not comment_matches:
            continue

        last_comment = comment_matches[-1]
        comment_block = last_comment.group(1)

        # コメントブロックと関数の間に別の関数がないか確認
        between_text = before_func[last_comment.end():]
        if re.search(r'function\s+\w+\s*\(', between_text):
            continue

        # まず正確な名前でマッチを試みる
        param_regex = re.compile(rf'@param\s+{param_name}\s+([^\n\r]+)')
        param_match = param_regex.search(comment_block)

        if param_match:
            return param_match.group(1).strip()

        # 名前が一致しない場合、位置でマッチを試みる（interface と implementation でパラメータ名が異なる場合）
        all_params = list(re.finditer(r'@param\s+\w+\s+([^\n\r]+)', comment_block))
        if len(all_params) > param_index:
            return all_params[param_index].group(1).strip()

    return ''


def extract_function_errors(source: str, function_name: str,
                           custom_errors: Dict[str, Any]) -> List[Dict[str, Any]]:
    """関数ごとのエラー情報を抽出"""
    errors = []
    error_names: Set[str] = set()

    # 関数定義を抽出
    function_regex = re.compile(rf'function\s+{function_name}[\s\S]*?\{{([\s\S]*?)\n\s*\}}',
                               re.MULTILINE)
    match = function_regex.search(source)

    if not match:
        return errors

    function_body = match.group(1)

    # revert文からエラー名を抽出: revert ErrorName()
    for revert_match in re.finditer(r'revert\s+(\w+)\s*\(', function_body):
        error_names.add(revert_match.group(1))

    # require文からエラー名を抽出: require(condition, ErrorName())
    for require_match in re.finditer(r'require\s*\([^,]+,\s*(\w+)\s*\(', function_body):
        error_names.add(require_match.group(1))

    # エラー情報を構築
    for error_name in error_names:
        if error_name in custom_errors:
            description = custom_errors[error_name].get('description', '')
            errors.append({
                'name': error_name,
                'signature': custom_errors[error_name]['signature'],
                'parameters': custom_errors[error_name]['parameters'],
                'description': description,
                'exampleValue': {
                    'error': error_name,
                    'message': description or f'エラー: {error_name}'
                }
            })

    return errors


def find_solidity_files(directory: Path) -> List[Path]:
    """ディレクトリを再帰的に探索してSolidityファイルを取得"""
    file_list = []

    for item in directory.rglob('*.sol'):
        if item.is_file() and '.t.sol' not in item.name and '.s.sol' not in item.name:
            file_list.append(item)

    return file_list


def generate_contract_spec_json(contract_name: str, abi_path: Path,
                               source_path: Path, output_path: Path) -> Path:
    """ABIファイルとSolidityソースからContract Spec JSONを生成"""
    print(f'\n📝 Generating Contract Spec JSON for {contract_name}...')

    # ABIを読み込み
    with abi_path.open('r', encoding='utf-8') as f:
        abi_data = json.load(f)
    abi = abi_data.get('abi', abi_data)  # Forge形式とTruffle形式に対応

    source = source_path.read_text(encoding='utf-8')

    # 継承しているinterfaceを検出してソースを読み込み
    inherited_interfaces = extract_inherited_interfaces(source)
    interface_sources = {}

    # sourcePathから'src'ディレクトリを見つけてcontractDirを取得
    src_dir = None
    for parent in source_path.parents:
        if parent.name == 'src':
            src_dir = parent
            break
    if src_dir is None:
        src_dir = source_path.parent

    for interface_name in inherited_interfaces:
        interface_source = load_interface_source(interface_name, src_dir)
        if interface_source:
            interface_sources[interface_name] = interface_source

    # Contract Spec JSON構造を構築
    spec = {
        'contractName': contract_name,
        'version': '1.0.0',
        'generatedAt': datetime.utcnow().isoformat() + 'Z',
        'metadata': {
            'title': f'{contract_name}コントラクト',
            'description': extract_contract_description(source),
            'category': '未分類',
            'tags': []
        },
        'readFunctions': [],
        'writeFunctions': [],
        'events': [],
        'customErrors': {}
    }

    # カスタムエラーを抽出
    error_items = [item for item in abi if item.get('type') == 'error']
    for error_item in error_items:
        error_name = error_item['name']
        signature = f"{error_name}({','.join(i['type'] for i in error_item.get('inputs', []))})"

        spec['customErrors'][error_name] = {
            'signature': signature,
            'parameters': [
                {
                    'name': inp.get('name', ''),
                    'type': inp['type'],
                    'description': ''
                }
                for inp in error_item.get('inputs', [])
            ],
            'description': translate_to_japanese(extract_error_description(source, error_name))
        }

    # 関数を処理（読み取り/書き込みに分類）
    functions = [item for item in abi if item.get('type') == 'function']

    for func in functions:
        function_errors = extract_function_errors(source, func['name'], spec['customErrors'])
        documentation = extract_function_documentation(source, func['name'], interface_sources)
        is_read_only = func.get('stateMutability') in ('view', 'pure')

        function_spec = {
            'name': func['name'],
            'signature': f"{func['name']}({','.join(i['type'] for i in func.get('inputs', []))})",
            'stateMutability': func.get('stateMutability', 'nonpayable'),
            'visibility': 'external',
            'documentation': {
                'summary': documentation.get('summary', ''),
                'details': documentation.get('details', ''),
                'notice': documentation.get('notice', '')
            },
            'parameters': [
                {
                    'name': inp['name'],
                    'type': inp['type'],
                    'description': extract_param_description(
                        source, func['name'], inp['name'], idx, interface_sources
                    )
                }
                for idx, inp in enumerate(func.get('inputs', []))
            ],
            'returnValues': [
                {
                    'name': out.get('name') or f'return{idx}',
                    'type': out['type'],
                    'description': ''
                }
                for idx, out in enumerate(func.get('outputs', []))
            ],
            'errors': function_errors,
            'examples': []
        }

        # 読み取り専用関数と書き込み関数に分類
        if is_read_only:
            spec['readFunctions'].append(function_spec)
        else:
            spec['writeFunctions'].append(function_spec)

    # イベントを処理
    events = [item for item in abi if item.get('type') == 'event']

    for event in events:
        spec['events'].append({
            'name': event['name'],
            'signature': f"{event['name']}({','.join(i['type'] for i in event.get('inputs', []))})",
            'parameters': [
                {
                    'name': inp['name'],
                    'type': inp['type'],
                    'indexed': inp.get('indexed', False)
                }
                for inp in event.get('inputs', [])
            ]
        })

    # ファイル出力
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)

    print(f'✅ Contract Spec JSON generated: {output_path}')
    print(f'   - Read Functions: {len(spec["readFunctions"])}')
    print(f'   - Write Functions: {len(spec["writeFunctions"])}')
    print(f'   - Events: {len(spec["events"])}')
    print(f'   - Custom Errors: {len(spec["customErrors"])}')

    return output_path


def main():
    """メイン処理"""
    # パス設定（環境変数で上書き可能）
    CONTRACT_DIR = Path(os.getenv('CONTRACT_DIR', 'packages/contract/src'))
    ABI_DIR = Path(os.getenv('ABI_DIR', 'packages/contract/out'))
    OUTPUT_DIR = Path(os.getenv('IR_DIR', 'docs/contract/ir'))
    FILTERED_JSON = Path(os.getenv('FILTERED_JSON', 'docs/contract/filtered.json'))

    print('📦 Contract Spec JSON生成中...\n')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # filtered.jsonから選択されたコントラクトリストを読み込み
    target_contracts = None
    if FILTERED_JSON.exists():
        with FILTERED_JSON.open('r', encoding='utf-8') as f:
            filtered = json.load(f)
        target_contracts = set(filtered.get('selected', []))
        print(f'   対象コントラクト: {len(target_contracts)}個（filtered.jsonから読み込み）\n')
    else:
        print('   ⚠️  filtered.jsonが見つかりません。全コントラクトを処理します。\n')

    # サブディレクトリを含めて全てのSolidityファイルを取得
    solidity_files = find_solidity_files(CONTRACT_DIR)

    results = []

    for source_path in solidity_files:
        contract_name = source_path.stem

        # filtered.jsonに含まれているかチェック（存在する場合のみ）
        if target_contracts and contract_name not in target_contracts:
            continue

        abi_path = ABI_DIR / f'{contract_name}.sol' / f'{contract_name}.json'
        output_path = OUTPUT_DIR / f'{contract_name}.json'

        if not abi_path.exists():
            print(f'⚠️  Skipping {contract_name}: ABI not found at {abi_path}')
            continue

        try:
            output = generate_contract_spec_json(contract_name, abi_path, source_path, output_path)
            results.append({'contractName': contract_name, 'success': True, 'outputPath': str(output)})
        except Exception as error:
            print(f'❌ エラー（{contract_name}の処理中）: {error}', file=sys.stderr)
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

    print('\n✅ 全Contract Spec JSONの生成が完了しました！')
    print(f'📂 Output directory: {OUTPUT_DIR}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'致命的なエラー: {error}', file=sys.stderr)
        sys.exit(1)
