#!/usr/bin/env python3

"""
generate-custom-css.py

doc-config.jsonからカスタムCSSを自動生成するスクリプト

特徴:
  - doc-config.jsonからプライマリカラーを読み込み
  - HEX → RGB変換とカラーバリエーション生成
  - ライト/ダークモード対応のCSSを生成
  - Swagger UIダークモード対応スタイルを含む

使用方法:
  python generate-custom-css.py \
    --config <config-path> \
    --output-path <output-path>

例:
  python generate-custom-css.py \
    --config docs/contract/doc-config.json \
    --output-path docs/contract/site/src/css/custom.css

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


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


def load_config(config_path: Path) -> Dict:
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


def hex_to_rgb(hex_color: str) -> Optional[Tuple[int, int, int]]:
    """HEXカラーをRGBに変換"""
    hex_color = hex_color.lstrip('#')

    if len(hex_color) != 6:
        return None

    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
    except ValueError:
        return None


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGBをHEXカラーに変換"""
    return f'#{r:02x}{g:02x}{b:02x}'


def lighten_color(hex_color: str, percent: float) -> str:
    """カラーを明るくする"""
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return hex_color

    r, g, b = rgb

    # 白に近づける
    r = min(255, int(r + (255 - r) * percent))
    g = min(255, int(g + (255 - g) * percent))
    b = min(255, int(b + (255 - b) * percent))

    return rgb_to_hex(r, g, b)


def darken_color(hex_color: str, percent: float) -> str:
    """カラーを暗くする"""
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return hex_color

    r, g, b = rgb

    # 黒に近づける
    r = max(0, int(r * (1 - percent)))
    g = max(0, int(g * (1 - percent)))
    b = max(0, int(b * (1 - percent)))

    return rgb_to_hex(r, g, b)


def generate_color_variations(primary_color: str) -> Dict[str, str]:
    """プライマリカラーからバリエーションを生成"""
    return {
        'PRIMARY_COLOR': primary_color,
        'PRIMARY_COLOR_DARK': darken_color(primary_color, 0.1),
        'PRIMARY_COLOR_DARKER': darken_color(primary_color, 0.15),
        'PRIMARY_COLOR_DARKEST': darken_color(primary_color, 0.3),
        'PRIMARY_COLOR_LIGHT': lighten_color(primary_color, 0.1),
        'PRIMARY_COLOR_LIGHTER': lighten_color(primary_color, 0.15),
        'PRIMARY_COLOR_LIGHTEST': lighten_color(primary_color, 0.3),
    }


def generate_custom_css(config: Dict) -> str:
    """カスタムCSSを生成"""
    primary_color = config.get('primaryColor', '#8c7851')
    colors = generate_color_variations(primary_color)

    return f"""/**
 * Any CSS included here will be global. The classic template
 * bundles Infima by default. Infima is a CSS framework designed to
 * work well for content-centric websites.
 */

/* You can override the default Infima variables here. */
/* Custom Color Scheme - Warm & Elegant */
:root {{
  /* ライトモード: 温かく優雅な配色 */
  --color-background: #f9f4ef;
  --color-headline: #020826;
  --color-paragraph: #716040;
  --color-button: {colors['PRIMARY_COLOR']};
  --color-button-text: #fffffe;
  --color-stroke: #020826;
  --color-main: #fffffe;
  --color-highlight: {colors['PRIMARY_COLOR']};
  --color-secondary: #eaddcf;
  --color-tertiary: #f25042;

  --ifm-color-primary: {colors['PRIMARY_COLOR']};
  --ifm-color-primary-dark: {colors['PRIMARY_COLOR_DARK']};
  --ifm-color-primary-darker: {colors['PRIMARY_COLOR_DARKER']};
  --ifm-color-primary-darkest: {colors['PRIMARY_COLOR_DARKEST']};
  --ifm-color-primary-light: {colors['PRIMARY_COLOR_LIGHT']};
  --ifm-color-primary-lighter: {colors['PRIMARY_COLOR_LIGHTER']};
  --ifm-color-primary-lightest: {colors['PRIMARY_COLOR_LIGHTEST']};
  --ifm-code-font-size: 95%;

  --ifm-background-color: #fdfcfa;
  --ifm-background-surface-color: #fffffe;
  --ifm-navbar-background-color: rgba(255, 255, 254, 0.98);
  --ifm-footer-background-color: #fdfcfa;
  --ifm-font-color-base: #716040;

  /* タイポグラフィ */
  --ifm-font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  --ifm-heading-font-weight: 600;
  --ifm-line-height-base: 1.7;
}}

/* Dark mode - 温かみのあるダークテーマ */
html[data-theme='dark'] {{
  /* ダークモード: リッチで温かい配色 */
  --color-background: #55423d;
  --color-headline: #fffffe;
  --color-paragraph: #fff3ec;
  --color-button: #ffc0ad;
  --color-button-text: #271c19;
  --color-stroke: #140d0b;
  --color-main: #fff3ec;
  --color-highlight: #e78fb3;
  --color-secondary: #ffc0ad;
  --color-tertiary: #9656a1;

  --ifm-color-primary: #ffc0ad;
  --ifm-color-primary-dark: #ffad94;
  --ifm-color-primary-darker: #ffa489;
  --ifm-color-primary-darkest: #ff8964;
  --ifm-color-primary-light: #ffd3c6;
  --ifm-color-primary-lighter: #ffdcd1;
  --ifm-color-primary-lightest: #fff3ef;

  --ifm-background-color: #55423d;
  --ifm-background-surface-color: #6b5650;
  --ifm-navbar-background-color: rgba(85, 66, 61, 0.98);
  --ifm-footer-background-color: #483632;
  --ifm-font-color-base: #fff3ec;

  --color-border: #7d6760;
}}

/* ナビゲーションバーのモダン化 */
.navbar {{
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}}

html[data-theme='dark'] .navbar {{
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid #7d6760;
}}

/* カードのエレガントなデザイン */
.card {{
  border: 1px solid #eaddcf;
  box-shadow: 0 2px 8px rgba(140, 120, 81, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fffffe;
  border-radius: 8px;
}}

.card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(140, 120, 81, 0.15);
  border-color: {colors['PRIMARY_COLOR']};
}}

html[data-theme='dark'] .card {{
  background: #6b5650;
  border: 1px solid #7d6760;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}}

html[data-theme='dark'] .card:hover {{
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
  border-color: #ffc0ad;
}}

/* ボタンのエレガントなデザイン */
.button--primary {{
  background: {colors['PRIMARY_COLOR']};
  border: none;
  font-weight: 500;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 6px;
  letter-spacing: 0.02em;
  color: #fffffe;
}}

.button--primary:hover {{
  background: {colors['PRIMARY_COLOR_DARK']};
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(140, 120, 81, 0.3);
  color: #fffffe;
}}

html[data-theme='dark'] .button--primary {{
  background: #ffc0ad;
  color: #271c19;
}}

html[data-theme='dark'] .button--primary:hover {{
  background: #ffad94;
  box-shadow: 0 4px 12px rgba(255, 192, 173, 0.4);
  color: #271c19;
}}

.docusaurus-highlight-code-line {{
  background-color: rgba(0, 0, 0, 0.1);
  display: block;
  margin: 0 calc(-1 * var(--ifm-pre-padding));
  padding: 0 var(--ifm-pre-padding);
}}

html[data-theme='dark'] .docusaurus-highlight-code-line {{
  background-color: rgba(0, 0, 0, 0.3);
}}

/* ========================================
   Swagger UI ダークモード対応
   ======================================== */

/* 全体の背景 - 白い部分を消す */
html[data-theme='dark'] .swagger-ui {{
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui .wrapper {{
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui .scheme-container {{
  background: #55423d !important;
  box-shadow: none !important;
}}

/* infoセクション全体の背景を透明に */
html[data-theme='dark'] .swagger-ui .information-container {{
  background: transparent !important;
}}

/* テキスト色 - 説明文など */
html[data-theme='dark'] .swagger-ui .info .title,
html[data-theme='dark'] .swagger-ui .info p,
html[data-theme='dark'] .swagger-ui .info .description,
html[data-theme='dark'] .swagger-ui .info .description p,
html[data-theme='dark'] .swagger-ui .info .description .markdown,
html[data-theme='dark'] .swagger-ui .info .description .markdown p,
html[data-theme='dark'] .swagger-ui .markdown p,
html[data-theme='dark'] .swagger-ui .renderedMarkdown p {{
  color: #fff3ec !important;
}}

/* タイトル */
html[data-theme='dark'] .swagger-ui .info .title {{
  color: #fffffe !important;
}}

/* セクションヘッダー（Read Functions等） */
html[data-theme='dark'] .swagger-ui .opblock-tag {{
  color: #fff3ec !important;
  border-bottom: 1px solid #7d6760 !important;
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui .opblock-tag:hover {{
  background: rgba(255, 192, 173, 0.1) !important;
}}

/* トグル矢印を白に */
html[data-theme='dark'] .swagger-ui .opblock-tag svg,
html[data-theme='dark'] .swagger-ui .opblock-tag .arrow,
html[data-theme='dark'] .swagger-ui .expand-operation svg,
html[data-theme='dark'] .swagger-ui svg.arrow {{
  fill: #fff3ec !important;
}}

html[data-theme='dark'] .swagger-ui .opblock-tag button {{
  background: transparent !important;
}}

/* Serversセクション - 背景を修正 */
html[data-theme='dark'] .swagger-ui .servers-title,
html[data-theme='dark'] .swagger-ui .servers label,
html[data-theme='dark'] .swagger-ui .servers > label {{
  color: #fff3ec !important;
}}

html[data-theme='dark'] .swagger-ui .servers {{
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui .servers select {{
  background: #6b5650 !important;
  color: #fff3ec !important;
  border: 1px solid #7d6760 !important;
}}

/* オペレーションブロック（トグル展開時） */
html[data-theme='dark'] .swagger-ui .opblock {{
  background: transparent !important;
  border-color: #7d6760 !important;
}}

html[data-theme='dark'] .swagger-ui .opblock .opblock-summary {{
  border-color: #7d6760 !important;
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui .opblock .opblock-summary-path,
html[data-theme='dark'] .swagger-ui .opblock .opblock-summary-description {{
  color: #fff3ec !important;
}}

/* 展開時のコンテンツエリア */
html[data-theme='dark'] .swagger-ui .opblock-body {{
  background: #55423d !important;
}}

html[data-theme='dark'] .swagger-ui .opblock-body pre {{
  background: #3d2d29 !important;
  color: #fff3ec !important;
}}

html[data-theme='dark'] .swagger-ui .opblock-section-header {{
  background: #4a3a36 !important;
  box-shadow: none !important;
}}

html[data-theme='dark'] .swagger-ui .opblock-section-header h4,
html[data-theme='dark'] .swagger-ui .opblock-section-header label {{
  color: #fff3ec !important;
}}

/* GET/POST等のメソッドラベル背景 */
html[data-theme='dark'] .swagger-ui .opblock.opblock-get {{
  background: rgba(97, 175, 254, 0.1) !important;
  border-color: #61affe !important;
}}

html[data-theme='dark'] .swagger-ui .opblock.opblock-get .opblock-summary {{
  background: rgba(97, 175, 254, 0.1) !important;
}}

html[data-theme='dark'] .swagger-ui .opblock.opblock-post {{
  background: rgba(73, 204, 144, 0.1) !important;
  border-color: #49cc90 !important;
}}

html[data-theme='dark'] .swagger-ui .opblock.opblock-put {{
  background: rgba(252, 161, 48, 0.1) !important;
  border-color: #fca130 !important;
}}

html[data-theme='dark'] .swagger-ui .opblock.opblock-delete {{
  background: rgba(249, 62, 62, 0.1) !important;
  border-color: #f93e3e !important;
}}

/* パラメータテーブル */
html[data-theme='dark'] .swagger-ui .parameters-col_name,
html[data-theme='dark'] .swagger-ui .parameters-col_description,
html[data-theme='dark'] .swagger-ui .parameter__name,
html[data-theme='dark'] .swagger-ui .parameter__type,
html[data-theme='dark'] .swagger-ui table thead tr th,
html[data-theme='dark'] .swagger-ui table tbody tr td {{
  color: #fff3ec !important;
}}

html[data-theme='dark'] .swagger-ui table {{
  border-color: #7d6760 !important;
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui table thead tr {{
  background: #4a3a36 !important;
}}

html[data-theme='dark'] .swagger-ui table tbody tr {{
  background: #55423d !important;
}}

html[data-theme='dark'] .swagger-ui table tbody tr:nth-child(even) {{
  background: #4a3a36 !important;
}}

/* モデル/スキーマ */
html[data-theme='dark'] .swagger-ui .model-title,
html[data-theme='dark'] .swagger-ui .model,
html[data-theme='dark'] .swagger-ui .model-box {{
  color: #fff3ec !important;
  background: transparent !important;
}}

/* 入力フィールド */
html[data-theme='dark'] .swagger-ui input[type="text"],
html[data-theme='dark'] .swagger-ui textarea {{
  background: #6b5650 !important;
  color: #fff3ec !important;
  border: 1px solid #7d6760 !important;
}}

/* レスポンスセクション */
html[data-theme='dark'] .swagger-ui .responses-wrapper,
html[data-theme='dark'] .swagger-ui .response {{
  background: transparent !important;
}}

html[data-theme='dark'] .swagger-ui .responses-header,
html[data-theme='dark'] .swagger-ui .response-col_status,
html[data-theme='dark'] .swagger-ui .response-col_description {{
  color: #fff3ec !important;
}}

/* コードブロック */
html[data-theme='dark'] .swagger-ui .highlight-code,
html[data-theme='dark'] .swagger-ui pre.microlight {{
  background: #3d2d29 !important;
  color: #fff3ec !important;
}}

/* ボタン */
html[data-theme='dark'] .swagger-ui .btn {{
  background: {colors['PRIMARY_COLOR']} !important;
  color: #fffffe !important;
  border: none !important;
}}

html[data-theme='dark'] .swagger-ui .btn:hover {{
  background: {colors['PRIMARY_COLOR_DARK']} !important;
}}

html[data-theme='dark'] .swagger-ui .btn.execute {{
  background: #49cc90 !important;
  color: #fff !important;
}}

html[data-theme='dark'] .swagger-ui .btn.cancel {{
  background: #f93e3e !important;
  color: #fff !important;
}}

/* リンク色 */
html[data-theme='dark'] .swagger-ui a {{
  color: #ffc0ad !important;
}}

/* URL/パスのスタイル */
html[data-theme='dark'] .swagger-ui .info .base-url {{
  color: #ffc0ad !important;
}}

/* JSONビュー */
html[data-theme='dark'] .swagger-ui .json-schema-form-item input {{
  background: #6b5650 !important;
  color: #fff3ec !important;
}}

/* 全ての白背景を消す */
html[data-theme='dark'] .swagger-ui .opblock-description-wrapper,
html[data-theme='dark'] .swagger-ui .opblock-external-docs-wrapper,
html[data-theme='dark'] .swagger-ui .opblock-title_normal {{
  background: transparent !important;
  color: #fff3ec !important;
}}

/* コピー・ダウンロードボタン */
html[data-theme='dark'] .swagger-ui .copy-to-clipboard,
html[data-theme='dark'] .swagger-ui .download-contents {{
  background: #6b5650 !important;
}}

html[data-theme='dark'] .swagger-ui .copy-to-clipboard button,
html[data-theme='dark'] .swagger-ui .download-contents button {{
  background: transparent !important;
}}

/* "No parameters" テキスト */
html[data-theme='dark'] .swagger-ui .opblock-description-wrapper p,
html[data-theme='dark'] .swagger-ui .opblock-body .opblock-section .opblock-section-header + div,
html[data-theme='dark'] .swagger-ui .parameters-container .parameters,
html[data-theme='dark'] .swagger-ui .opblock-body > div > div {{
  color: #fff3ec !important;
}}

/* "Example Value" / "Schema" タブ */
html[data-theme='dark'] .swagger-ui .tab li,
html[data-theme='dark'] .swagger-ui .tab li button,
html[data-theme='dark'] .swagger-ui .tablinks,
html[data-theme='dark'] .swagger-ui .response-control-media-type__title,
html[data-theme='dark'] .swagger-ui .response-control-media-type--select-label {{
  color: #fff3ec !important;
}}

html[data-theme='dark'] .swagger-ui .tab li.active,
html[data-theme='dark'] .swagger-ui .tab li button.active {{
  color: #ffc0ad !important;
}}

/* モデル内のテキスト全般 */
html[data-theme='dark'] .swagger-ui .model-container,
html[data-theme='dark'] .swagger-ui .model span,
html[data-theme='dark'] .swagger-ui .model .prop,
html[data-theme='dark'] .swagger-ui .model .prop-type,
html[data-theme='dark'] .swagger-ui .model .prop-format,
html[data-theme='dark'] .swagger-ui .model-toggle,
html[data-theme='dark'] .swagger-ui .model-box-control {{
  color: #fff3ec !important;
}}

/* Linksセクションを非表示（全て "No links" のため） */
.swagger-ui .responses-wrapper .response .response-col_links,
.swagger-ui .responses-wrapper thead .response-col_links {{
  display: none !important;
}}

/* ========================================
   Swagger UI 共通 - 背景色修正
   ======================================== */

/* 全体の背景を透明に（ライト・ダーク共通） */
.swagger-ui {{
  background: transparent !important;
}}

.swagger-ui .wrapper {{
  background: transparent !important;
}}

.swagger-ui .information-container {{
  background: transparent !important;
}}

.swagger-ui .info {{
  background: transparent !important;
}}

.swagger-ui .info hgroup.main {{
  background: transparent !important;
}}

.swagger-ui .scheme-container {{
  background: transparent !important;
  box-shadow: none !important;
}}

/* バッジ周りのコンテナ背景を透明に */
.swagger-ui .info .main,
.swagger-ui .info > div,
.swagger-ui .topbar {{
  background: transparent !important;
}}

/* バージョン・OASバッジの親要素の背景を完全に透明化 */
.swagger-ui .info hgroup,
.swagger-ui .info hgroup.main,
.swagger-ui .info hgroup.main > *,
.swagger-ui .info .title,
.swagger-ui .info .title small,
.swagger-ui .info .title small pre,
.swagger-ui .info .version-stamp,
.swagger-ui .info__title,
.swagger-ui .info__version,
.swagger-ui .info > hgroup,
.swagger-ui .info > hgroup > * {{
  background: transparent !important;
  background-color: transparent !important;
}}

/* バッジ自体のスタイルは維持（Swagger UIデフォルト色を使用） */
.swagger-ui .info .title small pre.version {{
  background-color: #89bf04 !important; /* Swagger UI default green */
}}

.swagger-ui .version-pragma {{
  background-color: #3b4151 !important; /* Swagger UI default dark */
}}
"""


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    parser = argparse.ArgumentParser(description='Generate custom CSS from doc-config.json')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--output-path', help='Output CSS file path')
    args = parser.parse_args()

    # パスの設定
    CONFIG_PATH = Path(args.config or PROJECT_ROOT / 'docs/contract/doc-config.json')
    OUTPUT_PATH = Path(args.output_path or PROJECT_ROOT / 'docs/contract/site/src/css/custom.css')

    print('📝 Generating custom CSS...\n')
    print(f'Config path: {CONFIG_PATH}')
    print(f'Output path: {OUTPUT_PATH}\n')

    # Config読み込み
    config = load_config(CONFIG_PATH)

    # プライマリカラー取得
    primary_color = config.get('primaryColor', '#8c7851')
    print(f'Primary color: {primary_color}')

    # カラーバリエーション生成
    colors = generate_color_variations(primary_color)
    print('\nColor variations:')
    for key, value in colors.items():
        print(f'  {key}: {value}')
    print('')

    # CSS生成
    css_content = generate_custom_css(config)

    # 出力ディレクトリ作成
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # ファイル出力
    OUTPUT_PATH.write_text(css_content, encoding='utf-8')

    print(f'✅ custom.css generated: {OUTPUT_PATH}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Fatal error: {error}', file=sys.stderr)
        sys.exit(1)
