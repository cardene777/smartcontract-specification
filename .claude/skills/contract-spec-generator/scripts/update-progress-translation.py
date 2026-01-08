#!/usr/bin/env python3

"""
update-progress-translation.py

翻訳進捗を更新し、全完了時に終了コード0を返す

使用方法:
  python3 update-progress-translation.py --contract StablecoinCore
"""

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROGRESS_PATH = PROJECT_ROOT / 'docs' / 'contract' / 'progress-translation.json'


def main():
    parser = argparse.ArgumentParser(description='翻訳進捗を更新')
    parser.add_argument('--contract', required=True, help='コントラクト名')

    args = parser.parse_args()
    contract_name = args.contract

    if not PROGRESS_PATH.exists():
        print('❌ Error: progress-translation.json not found', file=sys.stderr)
        sys.exit(1)

    with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    # コントラクトの状態を完了に更新
    if contract_name in progress['contracts']:
        progress['contracts'][contract_name]['status'] = 'completed'

    # 完了数を再計算
    completed = sum(1 for c in progress['contracts'].values() if c['status'] == 'completed')
    total = progress['total']

    progress['completed'] = completed

    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

    remaining = total - completed

    print(f'✅ {contract_name}: 翻訳完了')
    print(f'📊 進捗: {completed}/{total} (残り{remaining}個)')

    if remaining == 0:
        print('')
        print('🎉 全翻訳完了！')
        sys.exit(0)  # All complete
    else:
        sys.exit(1)  # Still incomplete


if __name__ == '__main__':
    main()
