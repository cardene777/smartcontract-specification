#!/usr/bin/env python3

"""
generate-docusaurus-config.py

sidebars.jsとdoc-config.jsonからdocusaurus.config.jsを自動生成するスクリプト

特徴:
  - sidebars.jsを読み込んでカテゴリとコントラクトリストを抽出
  - doc-config.jsonからプロジェクト設定を読み込み
  - カテゴリ別ナビゲーションドロップダウンを生成（Markdownドキュメントへリンク）
  - シンプルなDocusaurus設定を生成（プラグイン不要）

使用方法:
  python generate-docusaurus-config.py \
    --sidebars-path <sidebars-path> \
    --config <config-path> \
    --output-path <output-path>

例:
  python generate-docusaurus-config.py \
    --sidebars-path docs/contract/docs/sidebars.js \
    --config docs/contract/doc-config.json \
    --output-path docs/contract/site/docusaurus.config.js

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


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


def load_config(config_path: Path) -> Dict[str, Any]:
    """doc-config.jsonを読み込み"""
    if not config_path.exists():
        print(f'Error: Config file not found: {config_path}', file=sys.stderr)
        sys.exit(1)

    try:
        with config_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as error:
        print(f'Error parsing config file: {error}', file=sys.stderr)
        sys.exit(1)


def extract_contracts_from_sidebars(sidebars_path: Path) -> Dict[str, Any]:
    """sidebars.jsを読み込んでカテゴリとコントラクトリストを抽出"""
    if not sidebars_path.exists():
        print(f'Error: sidebars.js not found: {sidebars_path}', file=sys.stderr)
        sys.exit(1)

    content = sidebars_path.read_text(encoding='utf-8')

    contracts = []
    categories = []

    # カテゴリパターンを抽出（正規表現で）
    # 例:
    # {
    #   "type": "category",
    #   "label": "Core Contracts",
    #   "items": [
    #     "contracts/StablecoinCore",
    #     "contracts/StablecoinProxy"
    #   ]
    # }
    category_pattern = r'\{\s*["\']?type["\']?\s*:\s*["\']category["\']\s*,\s*["\']?label["\']?\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']?items["\']?\s*:\s*\[(.*?)\]'

    for match in re.finditer(category_pattern, content, re.DOTALL):
        label = match.group(1)
        items_str = match.group(2)

        # アイテムを抽出
        item_pattern = r'["\']contracts/([^"\']+)["\']'
        category_contracts = []

        for item_match in re.finditer(item_pattern, items_str):
            contract_name = item_match.group(1)
            category_contracts.append({
                'name': contract_name,
                'path': f'contracts/{contract_name}'
            })

        if category_contracts:
            categories.append({
                'label': label,
                'contracts': category_contracts
            })
            contracts.extend(category_contracts)

    return {'contracts': contracts, 'categories': categories}


def generate_overview_navbar() -> str:
    """ナビゲーションバーの概要ドロップダウンを生成"""
    lines = [
        '          {',
        "            type: 'dropdown',",
        "            label: '概要',",
        "            position: 'left',",
        '            items: [',
        "              { to: '/docs/overview', label: 'システム概要' },",
        "              { to: '/docs/architecture', label: 'アーキテクチャ' },",
        "              { to: '/docs/roles', label: 'ロール管理' },",
        "              { to: '/docs/security', label: 'セキュリティ' },",
        "              { to: '/docs/testing', label: 'テスト' },",
        "              { to: '/docs/upgrade', label: 'アップグレード' },",
        "              { to: '/docs/audit', label: '監査' },",
        '            ],',
        '          },',
    ]
    return '\n'.join(lines)


def generate_contracts_navbar(categories: List[Dict[str, Any]]) -> str:
    """ナビゲーションバーのコントラクトドロップダウンを生成（カテゴリ別）"""
    lines = []

    for category in categories:
        lines.append('          {')
        lines.append("            type: 'dropdown',")
        lines.append(f"            label: '{category['label']}',")
        lines.append("            position: 'left',")
        lines.append('            items: [')

        for contract in category['contracts']:
            lines.append('              {')
            lines.append(f"                to: '/docs/{contract['path']}',")
            lines.append(f"                label: '{contract['name']}',")
            lines.append('              },')

        lines.append('            ],')
        lines.append('          },')

    return '\n'.join(lines)


def generate_footer_links(contracts: List[Dict[str, Any]]) -> str:
    """フッターリンクを生成"""
    lines = []

    # 1. 概要セクション
    lines.extend([
        '          {',
        "            title: '概要',",
        '            items: [',
        "              { label: 'システム概要', to: '/docs/overview' },",
        "              { label: 'アーキテクチャ', to: '/docs/architecture' },",
        "              { label: 'ロール管理', to: '/docs/roles' },",
        "              { label: 'セキュリティ', to: '/docs/security' },",
        "              { label: 'テスト', to: '/docs/testing' },",
        "              { label: 'アップグレード', to: '/docs/upgrade' },",
        "              { label: '監査', to: '/docs/audit' },",
        '            ],',
        '          },',
    ])

    # 2. コントラクトセクション
    lines.append('          {')
    lines.append("            title: 'コントラクト',")
    lines.append('            items: [')

    # 最初の5つのコントラクトをフッターに追加
    top_contracts = contracts[:5]
    for contract in top_contracts:
        lines.append('              {')
        lines.append(f"                label: '{contract['name']}',")
        lines.append(f"                to: '/docs/{contract['path']}',")
        lines.append('              },')

    lines.append('            ],')
    lines.append('          },')

    return '\n'.join(lines)


def generate_docusaurus_config(config: Dict[str, Any], contracts: List[Dict[str, Any]],
                               categories: List[Dict[str, Any]]) -> str:
    """docusaurus.config.jsを生成"""
    # siteディレクトリにシンボリックリンクを作成している前提
    docs_relative_path = 'docs'
    specs_relative_path = 'specs'

    project_title = config.get('projectTitle', 'Smart Contract Specifications')
    project_name = config.get('projectName', 'Contracts')
    tagline = config.get('tagline', 'スマートコントラクト仕様書')
    github_org = config.get('githubOrg', 'organization')
    repo_name = config.get('repoName', 'repository')
    primary_color = config.get('primaryColor', '#1890ff')
    base_url = config.get('baseUrl', '/')

    return f"""// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {{themes as prismThemes}} from 'prism-react-renderer';

/** @type {{import('@docusaurus/types').Config}} */
const config = {{
  title: '{project_title}',
  tagline: '{tagline}',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://{github_org}.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '{base_url}',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: '{github_org}', // Usually your GitHub org/user name.
  projectName: '{repo_name}', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Mermaid support
  markdown: {{
    mermaid: true,
  }},
  themes: ['@docusaurus/theme-mermaid'],

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {{
    defaultLocale: 'ja',
    locales: ['ja'],
  }},

  plugins: [
    function customWebpackPlugin() {{
      const webpack = require('webpack');
      return {{
        name: 'custom-webpack-plugin',
        configureWebpack() {{
          return {{
            resolve: {{
              fallback: {{
                stream: false,
                buffer: require.resolve('buffer/'),
              }},
            }},
            plugins: [
              new webpack.ProvidePlugin({{
                Buffer: ['buffer', 'Buffer'],
              }}),
            ],
          }};
        }},
      }};
    }},
  ],

  presets: [
    [
      'classic',
      /** @type {{import('@docusaurus/preset-classic').Options}} */
      ({{
        docs: {{
          path: '{docs_relative_path}',
          sidebarPath: './sidebars.js',
          routeBasePath: 'docs',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/{github_org}/{repo_name}/tree/main/',
        }},
        blog: false,
        theme: {{
          customCss: './src/css/custom.css',
        }},
      }}),
    ],
  ],

  themeConfig:
    /** @type {{import('@docusaurus/preset-classic').ThemeConfig}} */
    ({{
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {{
        title: '{project_title}',
        logo: {{
          alt: '{project_title} Logo',
          src: 'img/logo.svg',
        }},
        items: [
{generate_overview_navbar()}
{generate_contracts_navbar(categories)}
        ],
      }},
      footer: {{
        style: 'dark',
        links: [
{generate_footer_links(contracts)}
          {{
            title: 'コミュニティ',
            items: [
              {{
                label: 'GitHub',
                href: 'https://github.com/{github_org}/{repo_name}',
              }},
            ],
          }},
        ],
        copyright: `Copyright © ${{new Date().getFullYear()}} {project_title}. Built with Docusaurus.`,
      }},
      prism: {{
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['solidity'],
      }},
    }}),
}};

export default config;
"""


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description='Generate docusaurus.config.js from sidebars and config')
    parser.add_argument('--sidebars-path', help='sidebars.js path')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--output-path', help='Output docusaurus.config.js path')
    args = parser.parse_args()

    # パスの設定
    SIDEBARS_PATH = Path(args.sidebars_path or PROJECT_ROOT / 'docs/contract/docs/sidebars.js')
    CONFIG_PATH = Path(args.config or PROJECT_ROOT / 'docs/contract/doc-config.json')
    OUTPUT_PATH = Path(args.output_path or PROJECT_ROOT / 'docs/contract/site/docusaurus.config.js')

    print('📝 Generating docusaurus.config.js...\n')
    print(f'Sidebars path: {SIDEBARS_PATH}')
    print(f'Config path: {CONFIG_PATH}')
    print(f'Output path: {OUTPUT_PATH}\n')

    # Config読み込み
    config = load_config(CONFIG_PATH)

    # sidebars.jsから抽出
    result = extract_contracts_from_sidebars(SIDEBARS_PATH)
    contracts = result['contracts']
    categories = result['categories']

    print(f'Found {len(contracts)} contracts in {len(categories)} categories:\n')
    for category in categories:
        print(f"  - {category['label']}: {len(category['contracts'])} contracts")
    print('')

    # docusaurus.config.js生成
    config_content = generate_docusaurus_config(config, contracts, categories)

    # 出力ディレクトリ作成
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ファイル出力
    OUTPUT_PATH.write_text(config_content, encoding='utf-8')

    print(f'✅ docusaurus.config.js generated: {OUTPUT_PATH}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
