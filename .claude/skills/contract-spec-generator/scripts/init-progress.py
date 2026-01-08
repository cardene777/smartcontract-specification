#!/usr/bin/env python3

"""
init-progress.py

spec-reviewerエージェントの進捗管理ファイルを初期化

使用方法:
  python3 init-progress.py --filtered <filtered.json>

例:
  python3 init-progress.py --filtered docs/contract/filtered.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


PROGRESS_FILE = 'docs/contract/progress.json'


def init_progress(filtered_json_path: str):
    """進捗管理ファイルを初期化"""
    print('📊 進捗管理ファイルを初期化中...\n')

    # filtered.jsonを読み込み
    if not os.path.exists(filtered_json_path):
        print(f'❌ Error: Filtered JSON not found: {filtered_json_path}', file=sys.stderr)
        sys.exit(1)

    with open(filtered_json_path, 'r', encoding='utf-8') as f:
        filtered = json.load(f)

    contracts = filtered.get('selected', [])

    if not contracts:
        print('❌ Error: No contracts found in filtered.json', file=sys.stderr)
        sys.exit(1)

    # 進捗オブジェクトを作成
    progress = {
        'total': len(contracts),
        'completed': 0,
        'status': 'in_progress',
        'startedAt': datetime.utcnow().isoformat() + 'Z',
        'contracts': {contract: 'pending' for contract in contracts}
    }

    # ディレクトリが存在しない場合は作成
    progress_path = Path(PROGRESS_FILE)
    progress_path.parent.mkdir(parents=True, exist_ok=True)

    # 進捗ファイルを保存
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

    print('✅ 進捗管理ファイルを初期化しました')
    print(f'   ファイル: {PROGRESS_FILE}')
    print(f'   総コントラクト数: {len(contracts)}')
    print('')
    print('📋 対象コントラクト:')
    for contract in contracts:
        print(f'   - {contract}')


def main():
    parser = argparse.ArgumentParser(description='spec-reviewerエージェントの進捗管理ファイルを初期化')
    parser.add_argument('--filtered', required=True, help='filtered.jsonのパス')

    args = parser.parse_args()
    init_progress(args.filtered)


if __name__ == '__main__':
    main()
