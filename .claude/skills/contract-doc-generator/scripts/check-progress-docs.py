#!/usr/bin/env python3

"""
check-progress-docs.py

docs-reviewer エージェントの進捗状況をチェック

特徴:
  - progress-docs.json を読み込み
  - 完了/未完了を表示
  - 全て完了の場合は exit 0、未完了がある場合は exit 1

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import json
import sys
from pathlib import Path


# パス設定
PROGRESS_FILE = Path('docs/contract/progress-docs.json')


def check_progress():
    """進捗状況をチェック"""
    if not PROGRESS_FILE.exists():
        print(f'❌ エラー: {PROGRESS_FILE} が見つかりません')
        print('先に init-progress-docs.py を実行してください')
        sys.exit(1)

    with PROGRESS_FILE.open('r', encoding='utf-8') as f:
        progress = json.load(f)

    print('📊 docs-reviewer エージェント進捗状況')
    print(f"総数: {progress['total']}")
    print(f"完了: {progress['completed']}")
    print(f"ステータス: {progress['status']}")

    # 未完了のコントラクトをリストアップ
    pending = [
        name for name, status in progress['contracts'].items()
        if status == 'pending'
    ]

    if pending:
        print(f"\n⏳ 未完了のコントラクト ({len(pending)}個):")
        for name in pending:
            print(f"  - {name}")
        print('')
        sys.exit(1)

    print('\n✅ 全てのドキュメントが完了しました！')
    if 'completedAt' in progress:
        print(f"完了時刻: {progress['completedAt']}")
    print('')
    sys.exit(0)


def main():
    """メイン処理"""
    try:
        check_progress()
    except Exception as error:
        print(f'❌ エラー: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
