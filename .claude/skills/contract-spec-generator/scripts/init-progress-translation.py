#!/usr/bin/env python3

"""
init-progress-translation.py

翻訳用の進捗管理JSONを初期化

使用方法:
  python3 init-progress-translation.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
FILTERED_JSON_PATH = PROJECT_ROOT / 'docs' / 'contract' / 'filtered.json'
PROGRESS_PATH = PROJECT_ROOT / 'docs' / 'contract' / 'progress-translation.json'


def main():
    if not FILTERED_JSON_PATH.exists():
        print(f'❌ Error: {FILTERED_JSON_PATH} not found', file=sys.stderr)
        sys.exit(1)

    with open(FILTERED_JSON_PATH, 'r', encoding='utf-8') as f:
        filtered = json.load(f)

    contracts = filtered.get('selected', [])

    if not contracts:
        print('❌ Error: No contracts found in filtered.json', file=sys.stderr)
        sys.exit(1)

    progress = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'total': len(contracts),
        'completed': 0,
        'contracts': {contract: {'status': 'pending'} for contract in contracts}
    }

    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

    print(f'✅ 翻訳進捗管理を初期化: {len(contracts)}個のコントラクト')


if __name__ == '__main__':
    main()
