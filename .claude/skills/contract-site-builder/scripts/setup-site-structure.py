#!/usr/bin/env python3

"""
setup-site-structure.py

Docusaurus初期化後のサイト構造を設定するスクリプト

特徴:
  - 事前チェック（docs, specs, site, sidebars.js, doc-config.json）
  - デフォルトファイルの削除（docs/, blog/, docusaurus.config.ts）
  - シンボリックリンクの作成（docs, specs, sidebars.js）
  - package.jsonの修正（ブラウザ自動起動を無効化）
  - SwaggerUIコンポーネントのコピー
  - 依存関係のインストール（swagger-ui-react）

使用方法:
  python setup-site-structure.py \
    --site-dir <site-dir> \
    --docs-dir <docs-dir> \
    --specs-dir <specs-dir>

例:
  python setup-site-structure.py \
    --site-dir docs/contract/site \
    --docs-dir docs/contract/docs \
    --specs-dir docs/contract/specs

Requirements:
    - Python 3.7+
    - npm (for installing dependencies)
    - No external Python dependencies
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


def find_project_root(start_path: Path = None) -> Path:
    """プロジェクトルートを検出（.git または package.json を探す）"""
    if start_path is None:
        start_path = Path(__file__).parent

    current_path = start_path.resolve()

    while current_path != current_path.parent:
        if (current_path / '.git').exists() or (current_path / 'package.json').exists():
            return current_path
        current_path = current_path.parent

    return Path.cwd()


PROJECT_ROOT = find_project_root()


def pre_check(docs_dir: Path, specs_dir: Path, site_dir: Path, doc_config_path: Path) -> bool:
    """事前チェック"""
    print('🔍 Pre-check: Validating prerequisites...\n')

    checks = [
        {'path': docs_dir, 'name': 'Docs directory', 'required': 'contract-doc-generator skill'},
        {'path': specs_dir, 'name': 'Specs directory', 'required': 'contract-spec-generator skill'},
        {'path': site_dir, 'name': 'Site directory', 'required': 'Docusaurus initialization'},
        {'path': docs_dir / 'sidebars.js', 'name': 'sidebars.js', 'required': 'contract-doc-generator skill'},
        {'path': doc_config_path, 'name': 'doc-config.json', 'required': 'configuration file'}
    ]

    all_passed = True

    for check in checks:
        if check['path'].exists():
            print(f"  ✓ {check['name']}: {check['path']}")
        else:
            print(f"  ✗ {check['name']}: NOT FOUND - {check['path']}", file=sys.stderr)
            print(f"    Required by: {check['required']}", file=sys.stderr)
            all_passed = False

    print('')

    if not all_passed:
        print('❌ Pre-check failed. Please ensure all prerequisites are in place.', file=sys.stderr)
        return False

    print('✅ Pre-check passed!\n')
    return True


def remove_default_files(site_dir: Path) -> None:
    """Docusaurusデフォルトファイルを削除"""
    print('🗑️  Removing default Docusaurus files...\n')

    files_to_remove = [
        site_dir / 'docs',
        site_dir / 'blog',
        site_dir / 'docusaurus.config.ts',
        site_dir / 'sidebars.ts',  # TypeScriptサイドバーファイルを削除（JSシンボリックリンクと競合するため）
        site_dir / 'src/components/HomepageFeatures',  # デフォルトのHomepageFeatures
        site_dir / 'src/pages/markdown-page.md',  # デフォルトのmarkdownページ
    ]

    for file_path in files_to_remove:
        if file_path.exists():
            if file_path.is_dir():
                shutil.rmtree(file_path)
                print(f'  ✓ Removed directory: {file_path.name}')
            else:
                file_path.unlink()
                print(f'  ✓ Removed file: {file_path.name}')

    print('')


def create_symlink(target: Path, link_path: Path) -> None:
    """シンボリックリンクを作成"""
    full_link_path = link_path.resolve()

    # 既存のシンボリックリンクがあれば削除
    if full_link_path.exists() or full_link_path.is_symlink():
        if full_link_path.is_symlink():
            full_link_path.unlink()
            print(f'  ℹ️  Removed existing symlink: {full_link_path.name}')

    # シンボリックリンク作成
    os.symlink(target.resolve(), full_link_path)
    print(f'  ✓ Created symlink: {full_link_path.name} -> {target}')


def create_symlinks(site_dir: Path, docs_dir: Path, specs_dir: Path) -> None:
    """必要なシンボリックリンクを作成"""
    print('🔗 Creating symlinks...\n')

    # docs ディレクトリへのシンボリックリンク
    create_symlink(docs_dir, site_dir / 'docs')

    # static/specs ディレクトリへのシンボリックリンク
    static_dir = site_dir / 'static'
    static_dir.mkdir(parents=True, exist_ok=True)
    create_symlink(specs_dir, static_dir / 'specs')

    # sidebars.js へのシンボリックリンク
    create_symlink(docs_dir / 'sidebars.js', site_dir / 'sidebars.js')

    print('')


def fix_package_json(site_dir: Path) -> None:
    """package.jsonを修正（ブラウザ自動起動無効化、sync/prebuildスクリプト追加）"""
    print('📦 Fixing package.json...\n')

    package_json_path = site_dir / 'package.json'

    if not package_json_path.exists():
        print('  ⚠️  package.json not found, skipping...', file=sys.stderr)
        return

    try:
        with package_json_path.open('r', encoding='utf-8') as f:
            package_data = json.load(f)

        modified = False

        if 'scripts' not in package_data:
            package_data['scripts'] = {}

        # scripts.start を修正（--no-open 追加）
        if 'start' in package_data['scripts']:
            original = package_data['scripts']['start']
            if '--no-open' not in original:
                package_data['scripts']['start'] = f"{original} --no-open"
                print(f'  ✓ Modified start script: {package_data["scripts"]["start"]}')
                modified = True
            else:
                print('  ℹ️  --no-open already present in start script')
        else:
            print('  ⚠️  start script not found in package.json', file=sys.stderr)

        # sync スクリプトを追加（SSGビルド用にファイルをコピー）
        sync_script = "rm -rf docs static/specs sidebars.js && cp -R ../docs ./docs && mkdir -p static && cp -R ../specs ./static/specs && cp ../docs/sidebars.js ./sidebars.js && rm -rf docs/docs 2>/dev/null || true"
        if 'sync' not in package_data['scripts']:
            package_data['scripts']['sync'] = sync_script
            print('  ✓ Added sync script')
            modified = True
        else:
            print('  ℹ️  sync script already exists')

        # prebuild スクリプトを追加（ビルド前に自動でsyncを実行）
        if 'prebuild' not in package_data['scripts']:
            package_data['scripts']['prebuild'] = 'npm run sync'
            print('  ✓ Added prebuild script')
            modified = True
        else:
            print('  ℹ️  prebuild script already exists')

        # 変更があればファイルに書き戻し
        if modified:
            with package_json_path.open('w', encoding='utf-8') as f:
                json.dump(package_data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # 末尾に改行を追加
            print('  ✓ package.json updated successfully')

    except Exception as error:
        print(f'  ✗ Error modifying package.json: {error}', file=sys.stderr)

    print('')


def copy_swagger_ui_component(site_dir: Path, project_root: Path) -> None:
    """SwaggerUIコンポーネントをコピー"""
    print('📄 Copying SwaggerUI component...\n')

    # ソースパス
    source_path = project_root / '.claude/skills/contract-site-builder/templates/components/SwaggerUI.tsx'

    # デスティネーションパス
    dest_dir = site_dir / 'src/components'
    dest_path = dest_dir / 'SwaggerUI.tsx'

    if not source_path.exists():
        print(f'  ⚠️  Source component not found: {source_path}', file=sys.stderr)
        print('  Please ensure the component template exists', file=sys.stderr)
        return

    # ディレクトリ作成
    dest_dir.mkdir(parents=True, exist_ok=True)

    # ファイルコピー
    shutil.copy2(source_path, dest_path)
    print(f'  ✓ Copied: SwaggerUI.tsx')
    print(f'    From: {source_path}')
    print(f'    To:   {dest_path}')

    print('')


def install_dependencies(site_dir: Path) -> None:
    """依存関係をインストール"""
    print('📦 Installing dependencies...\n')

    try:
        # React 18にダウングレード（Docusaurus 3.9.2との互換性のため）
        print('  Installing React 18 (compatible with Docusaurus 3.9.2)...')
        subprocess.run(
            ['npm', 'install', 'react@^18.0.0', 'react-dom@^18.0.0'],
            cwd=site_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print('  ✓ React 18 installed successfully')

        # swagger-ui-react をインストール
        print('  Installing swagger-ui-react...')
        subprocess.run(
            ['npm', 'install', 'swagger-ui-react'],
            cwd=site_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print('  ✓ swagger-ui-react installed successfully')

        # @docusaurus/theme-mermaid をインストール
        print('  Installing @docusaurus/theme-mermaid...')
        subprocess.run(
            ['npm', 'install', '@docusaurus/theme-mermaid'],
            cwd=site_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print('  ✓ @docusaurus/theme-mermaid installed successfully')

        # buffer をインストール（swagger-ui-react用ポリフィル）
        print('  Installing buffer polyfill...')
        subprocess.run(
            ['npm', 'install', 'buffer'],
            cwd=site_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print('  ✓ buffer polyfill installed successfully')

    except subprocess.CalledProcessError as error:
        print(f'  ✗ Error installing dependencies: {error}', file=sys.stderr)
        if error.stderr:
            print(f'    {error.stderr}', file=sys.stderr)
        sys.exit(1)

    print('')


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description='Setup Docusaurus site structure')
    parser.add_argument('--site-dir', help='Site directory path')
    parser.add_argument('--docs-dir', help='Docs directory path')
    parser.add_argument('--specs-dir', help='Specs directory path')
    args = parser.parse_args()

    # パスの設定
    SITE_DIR = Path(args.site_dir or PROJECT_ROOT / 'docs/contract/site')
    DOCS_DIR = Path(args.docs_dir or PROJECT_ROOT / 'docs/contract/docs')
    SPECS_DIR = Path(args.specs_dir or PROJECT_ROOT / 'docs/contract/specs')
    DOC_CONFIG_PATH = PROJECT_ROOT / 'docs/contract/doc-config.json'

    print('=' * 60)
    print('Docusaurus Site Structure Setup')
    print('=' * 60)
    print('')
    print(f'Site directory:  {SITE_DIR}')
    print(f'Docs directory:  {DOCS_DIR}')
    print(f'Specs directory: {SPECS_DIR}')
    print('')

    # 1. 事前チェック
    if not pre_check(DOCS_DIR, SPECS_DIR, SITE_DIR, DOC_CONFIG_PATH):
        sys.exit(1)

    # 2. デフォルトファイルの削除
    remove_default_files(SITE_DIR)

    # 3. シンボリックリンクの作成
    create_symlinks(SITE_DIR, DOCS_DIR, SPECS_DIR)

    # 4. package.json の修正
    fix_package_json(SITE_DIR)

    # 5. SwaggerUIコンポーネントのコピー
    copy_swagger_ui_component(SITE_DIR, PROJECT_ROOT)

    # 6. 依存関係のインストール
    install_dependencies(SITE_DIR)

    # 完了
    print('=' * 60)
    print('✅ Site structure setup complete!')
    print('=' * 60)
    print('')
    print('Next steps:')
    print('  1. Run generate-custom-css.py to create custom.css')
    print('  2. Run generate-docusaurus-config.py to create docusaurus.config.js')
    print('  3. Run generate-index-page.py to create index.tsx')
    print('  4. Run generate-api-pages.py to create API documentation pages')
    print('')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
