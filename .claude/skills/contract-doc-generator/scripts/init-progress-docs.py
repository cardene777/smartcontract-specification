#!/usr/bin/env python3

"""
init-progress-docs.py

docs-reviewer エージェントの進捗管理を初期化

特徴:
  - filtered.json からコントラクトリストを読み込み
  - progress-docs.json を作成（全て pending）
  - 既存の progress-docs.json は上書きされる

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


# パス設定
PROGRESS_FILE = Path('docs/contract/progress-docs.json')


def init_progress(filtered_json_path: Path):
    """進捗管理を初期化"""
    if not filtered_json_path.exists():
        print(f'❌ エラー: {filtered_json_path} が見つかりません', file=sys.stderr)
        sys.exit(1)

    # filtered.json を読み込み
    with filtered_json_path.open('r', encoding='utf-8') as f:
        filtered = json.load(f)

    contracts = filtered.get('selected', [])

    if not contracts:
        print('⚠️  対象コントラクトがありません')
        sys.exit(0)

    # progress-docs.json を作成
    progress = {
        'total': len(contracts),
        'completed': 0,
        'status': 'in_progress',
        'startedAt': datetime.utcnow().isoformat() + 'Z',
        'contracts': {}
    }

    for contract in contracts:
        progress['contracts'][contract] = 'pending'

    # ファイルに書き込み
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_FILE.open('w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    print(f'✅ progress-docs.json を初期化しました: {PROGRESS_FILE}')
    print(f'   総コントラクト数: {len(contracts)}')
    print('')
    print('📋 対象コントラクト:')
    for idx, contract in enumerate(contracts, 1):
        print(f'   {idx}. {contract}')


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Initialize docs-reviewer progress')
    parser.add_argument('--filtered', required=True, help='Path to filtered.json')
    args = parser.parse_args()

    filtered_json_path = Path(args.filtered)

    try:
        init_progress(filtered_json_path)
    except Exception as error:
        print(f'❌ エラー: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
