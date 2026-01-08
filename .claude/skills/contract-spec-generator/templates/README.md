# Templates Directory

このディレクトリには、contract-spec-generatorスキルで使用するテンプレートファイルが格納されています。

## ディレクトリ構成

### spec-generation/
**Phase 1: OpenAPI/Swagger仕様書生成**

- `spec-prompt.md` - 仕様書生成プロンプト（AIに渡すプロンプトテンプレート）
- `batch-generation-guide.md` - バッチ生成ガイド（複数コントラクトの一括生成手順）

**使用タイミング**: コントラクトABIから仕様書を生成する際

---

### doc-generation/
**Phase 3: Markdownドキュメント生成**

- `doc-config.template.json` - ドキュメント設定ファイル（カテゴリ、説明、サイドバー構成）
- `contracts/` - 各コントラクト用テンプレート
  - `contract-doc.template.md` - コントラクトドキュメントのテンプレート
  - `element-list.template.md` - 要素一覧のテンプレート
- `overview/` - Overview系ページ用テンプレート
  - `overview-architecture.template.md` - アーキテクチャページ
  - `overview-audit.template.md` - 監査ページ
  - `overview-glossary.template.md` - 用語集ページ
  - `overview-roles.template.md` - 権限・ロールページ
  - `overview-state-transitions.template.md` - 状態管理ページ
  - `overview-testing.template.md` - テストページ
  - `overview-upgrade.template.md` - Upgradeページ

**使用タイミング**: 仕様書からMarkdownドキュメントを生成する際

---

### site-setup/
**Phase 2: Docusaurusサイト構築**

#### config/
- `docusaurus.config.template.js` - Docusaurus設定ファイル（navbar/footer/plugins）
- `package.template.json` - package.json（依存関係とスクリプト）
- `sidebars.template.js` - サイドバー構成
- `.gitignore.template` - gitignore

#### pages/
- `index.template.tsx` - トップページコンポーネント（カード形式のコントラクト一覧）
- `index.module.template.css` - トップページのスタイル定義

#### css/
- `custom.template.css` - グローバルカスタムCSS（カラーパレット、フォント、ダークモード）

**使用タイミング**: Docusaurus init実行後、設定ファイルを上書きする際

**重要**: `static/` ディレクトリはDocusaurus initコマンドが自動生成するため、テンプレートには含まれていません。

---

## プレースホルダー一覧

テンプレートファイルで使用されるプレースホルダー：

| プレースホルダー | 説明 | 例 |
|----------------|------|-----|
| `{{PROJECT_TITLE}}` | プロジェクトタイトル | "Avalanche Stablecoin Contract Specifications" |
| `{{PROJECT_NAME}}` | プロジェクト名 | "Avalanche Stablecoin" |
| `{{PROJECT_TAGLINE}}` | プロジェクトサブタイトル | "スマートコントラクト仕様書" |
| `{{PROJECT_DESCRIPTION}}` | プロジェクト説明 | "Avalanche Stablecoin スマートコントラクト仕様書" |
| `{{PROJECT_REPO_NAME}}` | リポジトリ名 | "avalanche-stablecoin" |
| `{{GITHUB_ORG}}` | GitHub組織名 | "cardene777" |
| `{{PRIMARY_COLOR}}` | プライマリカラー | "#1890ff" |
| `{{PRIMARY_COLOR_DARK}}` | プライマリカラー（暗） | "#177ddc" |
| `{{PRIMARY_COLOR_DARKER}}` | プライマリカラー（さらに暗） | "#1765ad" |
| `{{PRIMARY_COLOR_DARKEST}}` | プライマリカラー（最も暗） | "#135089" |
| `{{PRIMARY_COLOR_LIGHT}}` | プライマリカラー（明） | "#3aa0ff" |
| `{{PRIMARY_COLOR_LIGHTER}}` | プライマリカラー（さらに明） | "#4dabff" |
| `{{PRIMARY_COLOR_LIGHTEST}}` | プライマリカラー（最も明） | "#7cc4ff" |
| `{{TOTAL_CONTRACTS}}` | コントラクト総数 | "18" |
| `{{CONTRACTS_ARRAY}}` | コントラクト配列（JSON） | `['StablecoinCore', 'StablecoinProxy', ...]` |
| `{{CONTRACTS_DATA}}` | コントラクトデータ（カテゴリ別JSON） | カテゴリ・説明を含むJSON |
| `{{NAVBAR_ITEMS}}` | navbarアイテム（JSON） | ドロップダウンメニュー構成 |
| `{{FOOTER_LINKS}}` | footerリンク（JSON） | フッターリンク構成 |

## 使用方法

### セットアップフロー

**重要**: Docusaurusの公式initコマンドを先に実行してから、テンプレートで上書きします。

```bash
# Step 1: Docusaurus公式コマンドでプロジェクト初期化
npx create-docusaurus@latest docs-site classic --typescript

# Step 2: テンプレートファイルで必要部分を上書き
# (手動 or 自動化スクリプト使用)
```

### 1. 手動展開
```bash
# Docusaurus init後、テンプレートをコピー
cp templates/site-setup/config/docusaurus.config.template.js ./docs-site/docusaurus.config.js
cp templates/site-setup/css/custom.template.css ./docs-site/src/css/custom.css
cp templates/site-setup/pages/index.template.tsx ./docs-site/src/pages/index.tsx
cp templates/site-setup/pages/index.module.template.css ./docs-site/src/pages/index.module.css

# プレースホルダーを置換
sed -i '' 's/{{PROJECT_NAME}}/My Project/g' ./docs-site/docusaurus.config.js
sed -i '' 's/{{PRIMARY_COLOR}}/#1890ff/g' ./docs-site/src/css/custom.css
# (他のプレースホルダーも同様に置換)
```

### 2. 自動化スクリプト（推奨・未実装）
```bash
# setup-docusaurus-site.pyを使用（将来実装予定）
python3 .claude/skills/contract-spec-generator/scripts/setup-docusaurus-site.py \
  --output ./docs-site \
  --project "My Project" \
  --primary-color "#1890ff" \
  --config ./doc-config.json
```

## 関連ドキュメント

詳細な使用方法は親ディレクトリの `SKILL.md` を参照してください。

- Phase 1: OpenAPI仕様書生成 → `spec-generation/`
- Phase 2: Docusaurusサイト構築 → `site-setup/`
- Phase 3: Markdownドキュメント生成 → `doc-generation/`
