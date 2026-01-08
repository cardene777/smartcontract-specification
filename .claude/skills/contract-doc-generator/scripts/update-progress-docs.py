#!/usr/bin/env python3

"""
update-progress-docs.py

docs-reviewer エージェントの進捗を更新

特徴:
  - 指定されたコントラクトを completed にマーク
  - 全て完了した場合は status を 'completed' に変更
  - 完了済みの場合は警告を表示

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


def update_progress(contract_name: str):
    """進捗を更新"""
    if not PROGRESS_FILE.exists():
        print(f'❌ エラー: {PROGRESS_FILE} が見つかりません', file=sys.stderr)
        print('先に init-progress-docs.py を実行してください', file=sys.stderr)
        sys.exit(1)

    # progress-docs.json を読み込み
    with PROGRESS_FILE.open('r', encoding='utf-8') as f:
        progress = json.load(f)

    # コントラクトが存在するかチェック
    if contract_name not in progress['contracts']:
        print(f'⚠️  警告: コントラクト "{contract_name}" が進捗リストに見つかりません')
        sys.exit(0)

    # 既に completed の場合は警告
    if progress['contracts'][contract_name] == 'completed':
        print(f'⚠️  警告: コントラクト "{contract_name}" は既に完了済みです')
        sys.exit(0)

    # 進捗を更新
    progress['contracts'][contract_name] = 'completed'
    progress['completed'] += 1

    # 全て完了した場合
    if progress['completed'] == progress['total']:
        progress['status'] = 'completed'
        progress['completedAt'] = datetime.utcnow().isoformat() + 'Z'
        print(f'🎉 全てのドキュメントが完了しました！')
        print(f'   完了時刻: {progress["completedAt"]}')
    else:
        remaining = progress['total'] - progress['completed']
        print(f'✅ {contract_name} の進捗を更新しました')
        print(f'   完了: {progress["completed"]}/{progress["total"]}')
        print(f'   残り: {remaining}件')

    # ファイルに書き込み
    with PROGRESS_FILE.open('w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Update docs-reviewer progress')
    parser.add_argument('--contract', required=True, help='Contract name to mark as completed')
    args = parser.parse_args()

    try:
        update_progress(args.contract)
    except Exception as error:
        print(f'❌ エラー: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
