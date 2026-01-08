#!/usr/bin/env python3
"""
analyze-errors.py

Solidityソースコードからエラー・イベント情報を抽出してContract Spec JSONに追加

Phase 2完全実装:
- 関数内エラー検出（revert, require）
- modifier内エラー追跡
- 継承チェーン全体の解析
- イベント情報抽出
- NatSpecコメント対応
"""

import os
import re
import json
from pathlib import Path


def find_solidity_files(directory):
    """ディレクトリ内の全Solidityファイルを取得"""
    sol_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sol'):
                sol_files.append(os.path.join(root, file))
    return sol_files


def extract_inheritance_chain(source):
    """継承チェーンを抽出（contract X is A, B, C）"""
    match = re.search(r'(?:contract|abstract\s+contract)\s+\w+\s+is\s+([^{]+)', source)
    if match:
        parents = match.group(1).strip().split(',')
        return [p.strip() for p in parents]
    return []


def extract_custom_errors(source):
    """カスタムエラー定義を抽出"""
    errors = {}

    # error ErrorName(type param, ...) パターン
    pattern = r'(?:\/\/\/?\s*(.+?)\n)?\s*error\s+(\w+)\s*\(([^)]*)\)'

    for match in re.finditer(pattern, source):
        comment = match.group(1) or ''
        error_name = match.group(2)
        params_str = match.group(3).strip()

        # パラメータ解析
        parameters = []
        if params_str:
            for param in params_str.split(','):
                param = param.strip()
                if param:
                    parts = param.split()
                    if len(parts) >= 2:
                        param_type = parts[0]
                        param_name = parts[1]
                        parameters.append({
                            'name': param_name,
                            'type': param_type,
                            'description': ''
                        })

        # シグネチャ生成
        param_types = ','.join([p['type'] for p in parameters])
        signature = f"{error_name}({param_types})"

        errors[error_name] = {
            'name': error_name,
            'signature': signature,
            'parameters': parameters,
            'description': comment.strip() if comment else '',
            'exampleValue': {
                'error': error_name,
                'message': ''  # AIが後で埋める
            }
        }

    return errors


def extract_modifiers(source):
    """modifier定義とその中で使用されるエラーを抽出"""
    modifiers = {}

    # modifier名の抽出
    modifier_pattern = r'modifier\s+(\w+)\s*\([^)]*\)\s*\{([^}]+)\}'

    for match in re.finditer(modifier_pattern, source, re.DOTALL):
        modifier_name = match.group(1)
        modifier_body = match.group(2)

        # modifier内で使用されるエラーを抽出
        errors_in_modifier = []

        # revert ErrorName() パターン
        revert_pattern = r'revert\s+(\w+)\s*\('
        for revert_match in re.finditer(revert_pattern, modifier_body):
            errors_in_modifier.append(revert_match.group(1))

        # require(..., "ErrorMessage") パターン
        require_pattern = r'require\s*\([^,]+,\s*["\']([^"\']+)["\']\s*\)'
        for req_match in re.finditer(require_pattern, modifier_body):
            # requireメッセージからエラー名を推測（実際のエラーではないが参考情報）
            pass

        modifiers[modifier_name] = errors_in_modifier

    return modifiers


def extract_function_body(source, function_name):
    """関数本体を括弧のバランスを数えて正確に抽出"""
    # 関数定義の開始位置を探す
    func_start_pattern = rf'function\s+{function_name}\s*\('
    match = re.search(func_start_pattern, source)

    if not match:
        return None, None

    # 関数定義の開始位置
    start_pos = match.start()

    # 開始括弧 { を探す
    brace_start = source.find('{', match.end())
    if brace_start == -1:
        return None, None

    # modifiers部分（関数シグネチャから { の間）
    modifiers_str = source[match.end():brace_start]

    # 括弧のバランスを数えて関数本体の終了位置を見つける
    brace_count = 1
    pos = brace_start + 1

    while pos < len(source) and brace_count > 0:
        if source[pos] == '{':
            brace_count += 1
        elif source[pos] == '}':
            brace_count -= 1
        pos += 1

    if brace_count != 0:
        return None, None

    # 関数本体（括弧の中身）
    func_body = source[brace_start + 1:pos - 1]

    return modifiers_str, func_body


def extract_function_calls(func_body):
    """関数本体から関数呼び出しを抽出"""
    calls = []

    # 関数呼び出しパターン: word(
    call_pattern = r'(\w+)\s*\('

    # 除外するキーワード
    excluded_keywords = {
        'if', 'for', 'while', 'require', 'assert', 'revert',
        'uint', 'uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256',
        'int', 'int8', 'int16', 'int32', 'int64', 'int128', 'int256',
        'bytes', 'bytes1', 'bytes2', 'bytes4', 'bytes8', 'bytes16', 'bytes32',
        'address', 'bool', 'string',
        'emit', 'return', 'new', 'delete'
    }

    for match in re.finditer(call_pattern, func_body):
        func_name = match.group(1)

        # 除外キーワードをスキップ
        if func_name in excluded_keywords:
            continue

        # 大文字で始まる名前（型や構造体）をスキップ
        if func_name[0].isupper():
            continue

        if func_name not in calls:
            calls.append(func_name)

    return calls


def find_function_in_sources(func_name, all_sources, contract_name=None, inheritance_chain=None):
    """関数定義を継承チェーン全体から探す"""
    if inheritance_chain is None:
        inheritance_chain = []

    # まず指定されたコントラクトで探す
    if contract_name:
        for src_path, src_content in all_sources.items():
            # コントラクト定義を探す
            contract_match = re.search(
                rf'(?:contract|abstract\s+contract)\s+{contract_name}\b',
                src_content
            )
            if contract_match:
                # そのコントラクト内で関数定義を探す
                modifiers_str, func_body = extract_function_body(src_content, func_name)
                if func_body is not None:
                    return src_content, func_body

                # 見つからなければ継承元を探す
                parents = extract_inheritance_chain(src_content)
                for parent in parents:
                    if parent not in inheritance_chain:
                        result_source, result_body = find_function_in_sources(
                            func_name,
                            all_sources,
                            parent,
                            inheritance_chain + [contract_name]
                        )
                        if result_body is not None:
                            return result_source, result_body

    # すべてのソースから探す（フォールバック）
    for src_path, src_content in all_sources.items():
        modifiers_str, func_body = extract_function_body(src_content, func_name)
        if func_body is not None:
            return src_content, func_body

    return None, None


def collect_errors_recursively(
    func_name,
    source,
    all_sources,
    contract_name,
    custom_errors,
    modifiers_map,
    visited=None
):
    """関数が発生させる可能性のある全エラーを再帰的に収集"""
    if visited is None:
        visited = set()

    # 無限再帰を防ぐ
    if func_name in visited:
        return []

    visited.add(func_name)
    errors = []

    # 関数本体を取得
    modifiers_str, func_body = extract_function_body(source, func_name)

    if not func_body:
        # 現在のソースで見つからない場合、継承チェーンから探す
        source, func_body = find_function_in_sources(func_name, all_sources, contract_name)
        if not func_body:
            return errors

        # modifiers_strも再取得
        modifiers_str, _ = extract_function_body(source, func_name)

    # modifier内のエラーを収集
    if modifiers_str:
        modifier_pattern = r'(\w+)\s*(?:\([^)]*\))?'
        for mod_match in re.finditer(modifier_pattern, modifiers_str):
            modifier_name = mod_match.group(1)
            # 予約語をスキップ
            if modifier_name in ['public', 'private', 'internal', 'external', 'pure', 'view', 'payable', 'virtual', 'override', 'returns']:
                continue

            # modifierで使用されるエラーを追加
            if modifier_name in modifiers_map:
                for error in modifiers_map[modifier_name]:
                    if error not in errors:
                        errors.append(error)

    # 直接的なエラー（revert）を収集
    revert_pattern = r'revert\s+(\w+)\s*\('
    for revert_match in re.finditer(revert_pattern, func_body):
        error_name = revert_match.group(1)
        if error_name not in errors:
            errors.append(error_name)

    # 関数呼び出しを抽出
    function_calls = extract_function_calls(func_body)

    # 各関数呼び出しから再帰的にエラーを収集
    for called_func in function_calls:
        # 呼び出された関数のエラーを再帰的に収集
        called_errors = collect_errors_recursively(
            called_func,
            source,
            all_sources,
            contract_name,
            custom_errors,
            modifiers_map,
            visited
        )

        for error in called_errors:
            if error not in errors:
                errors.append(error)

    return errors


def extract_function_errors(source, function_name, modifiers_map, all_sources=None, contract_name=None, custom_errors=None):
    """関数内で発生する可能性のあるエラーを抽出（関数呼び出しチェーンも追跡）"""
    if all_sources is None or custom_errors is None:
        # 後方互換性のため、古いロジックにフォールバック
        errors = []

        # 関数定義を探す
        modifiers_str, func_body = extract_function_body(source, function_name)

        if not func_body:
            return errors

        # modifier名を抽出
        modifier_pattern = r'(\w+)\s*(?:\([^)]*\))?'
        for mod_match in re.finditer(modifier_pattern, modifiers_str):
            modifier_name = mod_match.group(1)
            # 予約語をスキップ
            if modifier_name in ['public', 'private', 'internal', 'external', 'pure', 'view', 'payable', 'virtual', 'override', 'returns']:
                continue

            # modifierで使用されるエラーを追加
            if modifier_name in modifiers_map:
                errors.extend(modifiers_map[modifier_name])

        # 関数本体内のエラーを抽出
        # revert ErrorName() パターン
        revert_pattern = r'revert\s+(\w+)\s*\('
        for revert_match in re.finditer(revert_pattern, func_body):
            error_name = revert_match.group(1)
            if error_name not in errors:
                errors.append(error_name)

        return errors

    # 新しいロジック：関数呼び出しチェーンを追跡
    return collect_errors_recursively(
        function_name,
        source,
        all_sources,
        contract_name,
        custom_errors,
        modifiers_map
    )


def extract_events(source):
    """イベント定義とNatSpecを抽出"""
    events = {}

    # NatSpecコメント + event定義パターン
    pattern = r'((?:\/\*\*[\s\S]*?\*\/|\/\/\/[^\n]*\n)*)\s*event\s+(\w+)\s*\(([^)]*)\)'

    for match in re.finditer(pattern, source):
        natspec = match.group(1)
        event_name = match.group(2)
        params_str = match.group(3).strip()

        # NatSpecを解析
        summary = ''
        param_docs = {}

        if natspec:
            # @notice抽出
            notice_match = re.search(r'@notice\s+([^\n@]+)', natspec)
            if notice_match:
                summary = notice_match.group(1).strip()

            # @param抽出
            for param_match in re.finditer(r'@param\s+(\w+)\s+([^\n@]+)', natspec):
                param_name = param_match.group(1)
                param_desc = param_match.group(2).strip()
                param_docs[param_name] = param_desc

        # パラメータ解析
        parameters = []
        if params_str:
            for param in params_str.split(','):
                param = param.strip()
                if param:
                    # "indexed" キーワードを処理
                    param = param.replace('indexed', '').strip()
                    parts = param.split()
                    if len(parts) >= 2:
                        param_type = parts[0]
                        param_name = parts[1]
                        param_desc = param_docs.get(param_name, '')

                        parameters.append({
                            'name': param_name,
                            'type': param_type,
                            'description': param_desc
                        })

        # シグネチャ生成
        param_types = ','.join([p['type'] for p in parameters])
        signature = f"{event_name}({param_types})"

        events[event_name] = {
            'name': event_name,
            'signature': signature,
            'parameters': parameters,
            'documentation': {
                'summary': summary,
                'notice': summary,
                'details': ''
            }
        }

    return events


def collect_from_inheritance_tree(contract_name, all_sources, collector_func, visited=None):
    """継承ツリー全体から情報を再帰的に収集"""
    if visited is None:
        visited = set()

    if contract_name in visited:
        return {}

    visited.add(contract_name)
    collected = {}

    # 現在のコントラクトのソースを探す
    for src_path, src_content in all_sources.items():
        contract_match = re.search(rf'(?:contract|abstract\s+contract|interface)\s+{contract_name}\b', src_content)
        if contract_match:
            # 現在のコントラクトから情報を収集
            collected.update(collector_func(src_content))

            # 継承チェーンを取得
            inheritance_chain = extract_inheritance_chain(src_content)

            # 各親から再帰的に収集
            for parent in inheritance_chain:
                parent_collected = collect_from_inheritance_tree(parent, all_sources, collector_func, visited)
                collected.update(parent_collected)

            break

    return collected


def analyze_contract(contract_path, all_sources):
    """単一コントラクトを解析"""
    with open(contract_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # コントラクト名を抽出
    contract_match = re.search(r'(?:contract|abstract\s+contract)\s+(\w+)', source)
    if not contract_match:
        return None

    contract_name = contract_match.group(1)

    # 継承チェーンを解析（直接の親のみ）
    inheritance_chain = extract_inheritance_chain(source)

    # 継承ツリー全体からカスタムエラーを収集
    custom_errors = collect_from_inheritance_tree(contract_name, all_sources, extract_custom_errors)

    # 継承ツリー全体からmodifierを収集
    modifiers_map = collect_from_inheritance_tree(contract_name, all_sources, extract_modifiers)

    # 継承ツリー全体からイベントを収集
    events = collect_from_inheritance_tree(contract_name, all_sources, extract_events)

    return {
        'contract_name': contract_name,
        'custom_errors': custom_errors,
        'modifiers': modifiers_map,
        'events': events,
        'source': source,
        'inheritance_chain': inheritance_chain
    }


def enhance_contract_spec(spec_path, analysis, all_sources):
    """Contract Spec JSONにエラー・イベント情報を追加"""
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    modified = False

    # カスタムエラーセクションを更新
    if 'customErrors' not in spec:
        spec['customErrors'] = {}

    for error_name, error_info in analysis['custom_errors'].items():
        if error_name not in spec['customErrors']:
            spec['customErrors'][error_name] = error_info
            modified = True

    # 書き込み関数にエラー情報を追加
    for func in spec.get('writeFunctions', []):
        func_name = func['name']

        # 関数内で使用されるエラーを抽出（関数呼び出しチェーンも追跡）
        func_errors = extract_function_errors(
            analysis['source'],
            func_name,
            analysis['modifiers'],
            all_sources,
            analysis['contract_name'],
            analysis['custom_errors']
        )

        # エラー情報を構築
        error_list = []
        for error_name in func_errors:
            if error_name in analysis['custom_errors']:
                error_info = analysis['custom_errors'][error_name]
                error_list.append({
                    'name': error_info['name'],
                    'signature': error_info['signature'],
                    'parameters': error_info['parameters'],
                    'description': error_info['description'],
                    'exampleValue': error_info['exampleValue']
                })

        # 既存のerrorsが空配列の場合のみ追加
        if not func.get('errors'):
            func['errors'] = error_list
            if error_list:
                modified = True

    # イベント情報を更新
    if 'events' not in spec:
        spec['events'] = []

    # 既存イベントを更新
    existing_event_names = {e['name'] for e in spec['events']}

    for event_name, event_info in analysis['events'].items():
        # 既存イベントを更新
        found = False
        for event in spec['events']:
            if event['name'] == event_name:
                # サマリーが空の場合のみ更新
                if not event.get('documentation', {}).get('summary'):
                    event['documentation'] = event_info['documentation']
                    modified = True

                # パラメータ説明が空の場合のみ更新
                for i, param in enumerate(event.get('parameters', [])):
                    if not param.get('description') and i < len(event_info['parameters']):
                        param['description'] = event_info['parameters'][i]['description']
                        modified = True

                found = True
                break

        # 新規イベントを追加
        if not found:
            spec['events'].append(event_info)
            modified = True

    # 保存
    if modified:
        with open(spec_path, 'w', encoding='utf-8') as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)

    return modified


def main():
    # パス設定
    CONTRACT_DIR = os.getenv('CONTRACT_DIR', 'packages/contract/src')
    IR_DIR = os.getenv('IR_DIR', 'docs/contract/ir')
    FILTERED_JSON = os.getenv('FILTERED_JSON', 'docs/contract/filtered.json')

    # 対象コントラクトを取得
    if os.path.exists(FILTERED_JSON):
        with open(FILTERED_JSON, 'r') as f:
            filtered = json.load(f)
            target_contracts = filtered.get('selected', [])
    else:
        print(f"❌ エラー: {FILTERED_JSON} が見つかりません")
        return

    print(f"📋 対象コントラクト: {len(target_contracts)}個")
    print("=" * 60)
    print()

    # 全Solidityファイルを読み込み（継承解析用）
    all_sources = {}
    sol_files = find_solidity_files(CONTRACT_DIR)
    for sol_path in sol_files:
        with open(sol_path, 'r', encoding='utf-8') as f:
            all_sources[sol_path] = f.read()

    # 各コントラクトを解析
    for contract_name in target_contracts:
        print(f"📝 {contract_name}")

        # ソースファイルを探す
        source_path = None
        for sol_path in sol_files:
            with open(sol_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(rf'(?:contract|abstract\s+contract)\s+{contract_name}\b', content):
                    source_path = sol_path
                    break

        if not source_path:
            print(f"   ⚠️  ソースファイルが見つかりません")
            continue

        # 解析実行
        analysis = analyze_contract(source_path, all_sources)

        if not analysis:
            print(f"   ⚠️  コントラクト定義が見つかりません")
            continue

        print(f"   ソース: {source_path}")
        print(f"   カスタムエラー: {len(analysis['custom_errors'])}個")
        print(f"   Modifier: {len(analysis['modifiers'])}個")
        print(f"   イベント: {len(analysis['events'])}個")
        print(f"   継承: {', '.join(analysis['inheritance_chain']) if analysis['inheritance_chain'] else 'なし'}")

        # Contract Spec JSONを更新
        spec_path = os.path.join(IR_DIR, f"{contract_name}.json")
        if os.path.exists(spec_path):
            modified = enhance_contract_spec(spec_path, analysis, all_sources)
            if modified:
                print(f"   ✅ エラー・イベント情報を追加しました")
            else:
                print(f"   ℹ️  更新不要（既に情報あり）")
        else:
            print(f"   ⚠️  Contract Spec JSONが見つかりません: {spec_path}")

        print()

    print("=" * 60)
    print(f"✅ 完了: {len(target_contracts)}個のコントラクトを解析")


if __name__ == '__main__':
    main()
