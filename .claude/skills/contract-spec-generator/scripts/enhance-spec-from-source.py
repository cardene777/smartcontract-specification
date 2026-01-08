#!/usr/bin/env python3
"""
ソースコードから正しい説明を抽出してContract Spec JSONを強化（修正版）

機能:
- NatSpecコメント抽出
- 不適切なsummary検出と改善
- 関数名ベースのsummary自動生成
"""

import json
import re
from pathlib import Path
import sys
import os

def is_inappropriate_summary(summary):
    """
    summaryに実装詳細が含まれているかチェック

    Args:
        summary: チェックするsummary文字列

    Returns:
        True if 不適切, False if 適切
    """
    if not summary:
        return True

    # 実装詳細キーワード（小文字で統一）
    implementation_keywords = [
        'override', 'overrides', 'virtual',
        'multi-sig', 'multisig', 'multi sig',
        'diamond inheritance', 'inheritance',
        'to enforce', 'to allow', 'to enable', 'to resolve',
        'for compatibility', 'backward compat',
        'compatibility', 'compat'
    ]

    summary_lower = summary.lower()
    return any(keyword in summary_lower for keyword in implementation_keywords)

def extract_target_from_function(function_name, action_prefix, params):
    """
    関数名とパラメータから対象オブジェクトを推測

    Args:
        function_name: 関数名
        action_prefix: 動作プレフィックス（例: "revoke", "transfer"）
        params: パラメータリスト

    Returns:
        対象オブジェクトの説明（英語）
    """
    # 関数名から対象を抽出（camelCaseから）
    remaining = function_name[len(action_prefix):]

    if remaining:
        # camelCaseをスペース区切りに変換
        target = re.sub('([A-Z])', r' \1', remaining).strip().lower()

        # 特定のパターンを改善
        if 'role' in target.lower():
            if len(params) >= 2:
                return "a role from an account"
            else:
                return "a role"
        elif 'token' in target.lower() or 'balance' in target.lower():
            return "tokens"
        elif 'admin' in target.lower():
            return "the admin address"
        elif 'pauser' in target.lower():
            return "the pauser address"
        else:
            return target if target else "operation"

    # 関数名からの抽出に失敗した場合、パラメータから推測
    if params and len(params) > 0:
        first_param = params[0].get('name', '')
        if first_param:
            return f"the {first_param}"

    return "operation"

def generate_summary_from_function_name(function_name, params):
    """
    関数名とパラメータから適切なsummaryを生成

    Args:
        function_name: 関数名
        params: パラメータリスト [{"name": "role", "type": "bytes32"}, ...]

    Returns:
        生成されたsummary（英語）
    """
    # 関数名から動作を推測するパターンマップ
    action_patterns = {
        # Access control
        'grant': 'Grant',
        'revoke': 'Revoke',
        'renounce': 'Renounce',

        # Read operations
        'get': 'Get',
        'fetch': 'Fetch',
        'read': 'Read',
        'view': 'View',
        'check': 'Check',
        'has': 'Check if has',
        'is': 'Check if is',
        'can': 'Check if can',

        # Write operations
        'set': 'Set',
        'update': 'Update',
        'modify': 'Modify',

        # Token operations
        'transferFrom': 'Transfer from',
        'transfer': 'Transfer',
        'mint': 'Mint',
        'burn': 'Burn',
        'approve': 'Approve',

        # Lifecycle
        'initialize': 'Initialize',
        'pause': 'Pause',
        'unpause': 'Unpause',
        'enable': 'Enable',
        'disable': 'Disable',

        # Execution
        'execute': 'Execute',
        'call': 'Call',
        'delegate': 'Delegate call to',
    }

    # パターンマッチング（長いパターンから優先）
    for pattern in sorted(action_patterns.keys(), key=len, reverse=True):
        if function_name.startswith(pattern):
            action = action_patterns[pattern]
            target = extract_target_from_function(function_name, pattern, params)
            return f"{action} {target}"

    # パターンマッチできない場合は汎用的な説明
    if params and len(params) > 0:
        return f"Execute {function_name} function"
    else:
        return f"Execute {function_name}"

def improve_summary_if_needed(summary, function_name, params):
    """
    summaryが不適切な場合、関数名とパラメータから改善

    Args:
        summary: 元のsummary（@noticeから取得）
        function_name: 関数名
        params: パラメータリスト

    Returns:
        改善されたsummary
    """
    if is_inappropriate_summary(summary):
        # 不適切なので関数名から生成
        return generate_summary_from_function_name(function_name, params)
    else:
        # 適切なのでそのまま返す
        return summary

def extract_natspec_from_source(sol_path):
    """ソースコードからNatSpecコメントを抽出"""
    
    with open(sol_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    natspec = {}
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # /// コメントブロックの開始
        if line.startswith('///'):
            doc_lines = []
            
            # コメントブロックを収集
            while i < len(lines) and lines[i].strip().startswith('///'):
                doc_lines.append(lines[i].strip())
                i += 1
            
            # 次の非空行を探す
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            if i >= len(lines):
                break
            
            definition = lines[i].strip()
            
            # 関数名または変数名を抽出
            name = None
            
            # function functionName(...) 
            func_match = re.match(r'function\s+(\w+)', definition)
            if func_match:
                name = func_match.group(1)
            
            # bytes32 public constant VARIABLE_NAME
            const_match = re.match(r'(?:bytes32|uint256|address|bool)\s+public\s+constant\s+(\w+)', definition)
            if const_match:
                name = const_match.group(1)
            
            if name:
                notice = ''
                dev = ''
                params = {}
                returns = {}
                
                for doc_line in doc_lines:
                    doc_line = doc_line.replace('///', '').strip()
                    
                    if doc_line.startswith('@notice'):
                        notice = doc_line.replace('@notice', '').strip()
                    elif doc_line.startswith('@dev'):
                        dev = doc_line.replace('@dev', '').strip()
                    elif doc_line.startswith('@param'):
                        parts = doc_line.replace('@param', '').strip().split(' ', 1)
                        if len(parts) == 2:
                            params[parts[0]] = parts[1]
                    elif doc_line.startswith('@return'):
                        parts = doc_line.replace('@return', '').strip().split(' ', 1)
                        if len(parts) == 2:
                            returns[parts[0]] = parts[1]
                        elif len(parts) == 1:
                            returns['_default'] = parts[0]
                
                natspec[name] = {
                    'notice': notice,
                    'dev': dev,
                    'params': params,
                    'returns': returns
                }
        
        i += 1
    
    return natspec

def enhance_contract_from_source(spec_data, natspec):
    """NatSpecを使ってContract Spec JSONを強化（強制上書き + summary品質改善）"""

    modified = False

    # Read Functions
    for func in spec_data.get('readFunctions', []):
        func_name = func['name']
        func_params = func.get('parameters', [])

        if func_name in natspec:
            doc = func.setdefault('documentation', {})
            ns = natspec[func_name]

            # summary品質チェック + 改善
            if ns['notice']:
                # 不適切なsummaryを検出して改善
                improved_summary = improve_summary_if_needed(
                    ns['notice'],
                    func_name,
                    func_params
                )
                doc['summary'] = improved_summary
                doc['notice'] = improved_summary
                modified = True

            if ns['dev']:
                doc['details'] = ns['dev']
                modified = True

            # パラメータ
            for param in func.get('parameters', []):
                param_name = param.get('name', '')
                if param_name in ns['params']:
                    param['description'] = ns['params'][param_name]
                    modified = True

            # 戻り値
            for ret in func.get('returnValues', []):
                ret_name = ret.get('name', '')
                if ret_name in ns['returns']:
                    ret['description'] = ns['returns'][ret_name]
                    modified = True
                elif '_default' in ns['returns']:
                    ret['description'] = ns['returns']['_default']
                    modified = True
        else:
            # NatSpecがない場合も関数名からsummaryを生成
            doc = func.setdefault('documentation', {})
            if not doc.get('summary'):
                generated_summary = generate_summary_from_function_name(func_name, func_params)
                doc['summary'] = generated_summary
                modified = True

    # Write Functions
    for func in spec_data.get('writeFunctions', []):
        func_name = func['name']
        func_params = func.get('parameters', [])

        if func_name in natspec:
            doc = func.setdefault('documentation', {})
            ns = natspec[func_name]

            # summary品質チェック + 改善
            if ns['notice']:
                # 不適切なsummaryを検出して改善
                improved_summary = improve_summary_if_needed(
                    ns['notice'],
                    func_name,
                    func_params
                )
                doc['summary'] = improved_summary
                doc['notice'] = improved_summary
                modified = True

            if ns['dev']:
                doc['details'] = ns['dev']
                modified = True

            # パラメータ
            for param in func.get('parameters', []):
                param_name = param.get('name', '')
                if param_name in ns['params']:
                    param['description'] = ns['params'][param_name]
                    modified = True
        else:
            # NatSpecがない場合も関数名からsummaryを生成
            doc = func.setdefault('documentation', {})
            if not doc.get('summary'):
                generated_summary = generate_summary_from_function_name(func_name, func_params)
                doc['summary'] = generated_summary
                modified = True

    return spec_data, modified

def find_source_file(contract_name, source_dir):
    """コントラクトのソースファイルを検索"""
    
    for sol_file in Path(source_dir).rglob(f'{contract_name}.sol'):
        return sol_file
    
    return None

def main():
    # パス設定（環境変数で上書き可能）
    ir_dir = Path(os.getenv('IR_DIR', 'docs/contract/ir'))
    source_dir = Path(os.getenv('CONTRACT_DIR', 'packages/contract/src'))
    filtered_json = Path(os.getenv('FILTERED_JSON', 'docs/contract/filtered.json'))
    
    with open(filtered_json, 'r', encoding='utf-8') as f:
        filtered = json.load(f)
    
    contracts = filtered['selected']
    
    print(f'📋 対象コントラクト: {len(contracts)}個')
    print(f'{"="*60}\n')
    
    enhanced_count = 0
    
    for contract_name in contracts:
        json_path = ir_dir / f'{contract_name}.json'
        sol_path = find_source_file(contract_name, source_dir)
        
        if not json_path.exists() or not sol_path:
            continue
        
        print(f'📝 {contract_name}')
        print(f'   ソース: {sol_path}')
        
        # ソースコードからNatSpecを抽出
        natspec = extract_natspec_from_source(sol_path)
        print(f'   NatSpec抽出: {len(natspec)}個')
        
        if natspec:
            # 最初の5個だけ表示
            print(f'   要素: {", ".join(list(natspec.keys())[:5])}')
        
        # Contract Spec JSONを読み込み
        with open(json_path, 'r', encoding='utf-8') as f:
            spec_data = json.load(f)
        
        # NatSpecで強化
        enhanced_spec, modified = enhance_contract_from_source(spec_data, natspec)
        
        # 保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_spec, f, indent=2, ensure_ascii=False)
        
        if modified:
            print(f'   ✅ NatSpecで上書きしました')
            enhanced_count += 1
        else:
            print(f'   ⏭️  NatSpecなし（元の説明を維持）')
        
        print()
    
    print(f'{"="*60}')
    print(f'✅ 完了: {enhanced_count}個のコントラクトをNatSpecで更新')

if __name__ == '__main__':
    main()
