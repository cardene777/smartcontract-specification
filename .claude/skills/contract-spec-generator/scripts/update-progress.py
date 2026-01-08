#!/usr/bin/env python3

"""
update-progress.py

進捗カウンター更新スクリプト（超軽量版）

処理時間: 0.1秒以内
処理内容: progress.jsonの該当コントラクトをcompletedに更新するだけ

使用方法:
  python3 update-progress.py --contract StablecoinCore
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROGRESS_PATH = PROJECT_ROOT / 'docs' / 'contract' / 'progress.json'


def main():
    parser = argparse.ArgumentParser(description='進捗カウンター更新')
    parser.add_argument('--contract', required=True, help='コントラクト名')

    args = parser.parse_args()
    contract_name = args.contract

    # progress.jsonを読み込み
    if not PROGRESS_PATH.exists():
        print(f'❌ Error: {PROGRESS_PATH} not found', file=sys.stderr)
        sys.exit(1)

    with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    # コントラクトが存在するかチェック
    if contract_name not in progress['contracts']:
        print(f'❌ Error: Contract {contract_name} not found in progress.json', file=sys.stderr)
        print('   Available contracts:', file=sys.stderr)
        for name in progress['contracts'].keys():
            print(f'     - {name}', file=sys.stderr)
        sys.exit(1)

    # 既に完了している場合はスキップ
    if progress['contracts'][contract_name] == 'completed':
        print(f'⏭️  Contract {contract_name} is already marked as completed')

        # 進捗状況を出力（スキップした場合も）
        total = progress['total']
        completed = sum(1 for s in progress['contracts'].values() if s == 'completed')
        remaining = total - completed

        print(f'📊 進捗: {completed}/{total} (残り{remaining}個)')

        if 0 < remaining <= 3:
            print('⚠️  残り3個以下: check-and-proceed.jsの実行を推奨')

        sys.exit(0)

    # ステータス更新
    progress['contracts'][contract_name] = 'completed'
    progress['completed'] += 1

    # 全て完了した場合、ステータスを更新
    if progress['completed'] == progress['total']:
        progress['status'] = 'completed'
        progress['completedAt'] = datetime.utcnow().isoformat() + 'Z'

    # 保存
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

    # 進捗状況を出力
    total = progress['total']
    completed = progress['completed']
    remaining = total - completed

    print(f'✅ {contract_name}: 完了')
    print(f'📊 進捗: {completed}/{total} (残り{remaining}個)')

    # 終了コードで情報を渡す
    if remaining == 0:
        print('')
        print('🎉 全完了！全てのチェックリストが埋まりました')
        print('')
        print('💡 メインエージェントがPhase 4へ進みます')
        sys.exit(0)  # 全完了
    else:
        sys.exit(1)  # まだ未完了


if __name__ == '__main__':
    main()
