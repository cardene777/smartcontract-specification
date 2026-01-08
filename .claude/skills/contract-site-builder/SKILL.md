---
name: contract-site-builder
description: MarkdownドキュメントとOpenAPI仕様書からDocusaurusドキュメントサイトを構築します。サイト初期化、設定生成、ビルドデプロイの4フェーズパイプラインで、ナビゲーション、スタイリング、swagger-ui-reactコンポーネント経由のAPI仕様統合を備えた完全な静的ドキュメントサイトをセットアップします。
---

# Contract Site Builder

## 概要

4フェーズパイプライン（サイト構造セットアップ、設定生成、ビルドとデプロイ、検証）を通じて、MarkdownドキュメントとOpenAPI仕様書から完全なDocusaurus静的ドキュメントサイトを構築します。このスキルは、カテゴリベースのナビゲーション、コントラクトドキュメント、React Swagger UIコンポーネントによるインタラクティブなAPI仕様ビューアを備えた本番環境対応の静的サイトを作成します。

**出力**: 完全なナビゲーション、ドキュメントページ、Swagger UI Reactコンポーネントで構築されたAPI仕様ビューアを備えたDocusaurus静的サイト

---

## パラメータ

### 必須パラメータ（ユーザーから受け取る）

- **入力ドキュメントディレクトリ**: Markdownドキュメントが格納されているディレクトリへのパス（例: `docs/contract/docs`）
- **入力仕様書ディレクトリ**: OpenAPI仕様書が格納されているディレクトリへのパス（例: `docs/contract/specs`）
- **設定ファイルパス**: ドキュメント設定ファイル（doc-config.json）への絶対パス（例: `docs/contract/doc-config.json`）

### オプションパラメータ（デフォルト値あり、環境変数で上書き可能）

- **出力サイトディレクトリ**: `docs/contract/site` (環境変数: `SITE_DIR`)
- **ビルド出力ディレクトリ**: `docs/contract/site/build` (環境変数: `BUILD_DIR`)
- **テンプレートディレクトリ**: `.claude/skills/contract-site-builder/templates/site-setup`

### ドキュメント内での変数表記

本ドキュメントでは、パスを示す際に以下の変数表記を使用します：

| 変数表記 | 説明 | デフォルト値 / 例 |
|---------|------|------------------|
| `{DOCS_DIR}` | 入力ドキュメントディレクトリ（必須パラメータ） | 例: `docs/contract/docs` |
| `{SPECS_DIR}` | 入力仕様書ディレクトリ（必須パラメータ） | 例: `docs/contract/specs` |
| `{DOC_CONFIG}` | 設定ファイルパス（必須パラメータ） | 例: `docs/contract/doc-config.json` |
| `{SITE_DIR}` | 出力サイトディレクトリ | デフォルト: `docs/contract/site` |
| `{BUILD_DIR}` | ビルド出力ディレクトリ | デフォルト: `docs/contract/site/build` |

### 環境変数の設定

以下の環境変数を設定してから、各コマンドを実行してください：

```bash
# ========================================
# 必須パラメータ（ユーザー環境に合わせて設定）
# ========================================
export DOCS_DIR="docs/contract/docs"
export SPECS_DIR="docs/contract/specs"
export DOC_CONFIG="docs/contract/doc-config.json"

# ========================================
# オプションパラメータ（デフォルト値、必要に応じて変更）
# ========================================
export SITE_DIR="docs/contract/site"
export BUILD_DIR="docs/contract/site/build"
export TEMPLATE_DIR=".claude/skills/contract-site-builder/templates/site-setup"
```

---

# 処理フロー

## 🚀 全体ワークフロー

完全なドキュメントサイトの作成は5つのフェーズで構成されます：

### Phase 0: 言語設定

#### 0.1 言語設定の確認と選択

**ステップ1: 言語設定ファイルの確認**

`docs/contract/language.json` の存在を確認：

**ファイルが存在する場合**:
1. JSONを読み込み、`code`と`name`フィールドを取得
2. 「✅ 選択された言語: {name} ({code})」と表示
3. この言語コードを使用して処理を続行

**ファイルが存在しない場合**:
1. AskUserQuestionツールで言語を選択：
   - **Question**: "Select documentation language / ドキュメント生成言語を選択してください"
   - **Options**:
     - English (en) - Default
     - 日本語 (ja)
     - 한국어 (ko)
     - 简体中文 (zh-CN)

2. 選択結果を`docs/contract/language.json`に保存：
   ```json
   {
     "code": "ja",
     "name": "日本語"
   }
   ```

**重要**: 選択された言語で以降のすべての出力（画面表示、ファイル生成、ドキュメント、仕様書）を行います。

---

### フェーズ1: サイト構造のセットアップ

#### 1.1 Docusaurusプロジェクトの初期化

TypeScriptテンプレートで新しいDocusaurusプロジェクトを作成：

**処理**:
1. TypeScriptでDocusaurus classicテンプレートを初期化
2. サイト構造のセットアップ（setup-site-structure.py）
   - 事前チェック: 前提条件の確認（docs/, specs/, doc-config.json）
   - デフォルトファイルを削除（docs/, blog/, docusaurus.config.ts）
   - シンボリックリンクを作成（docs → ../docs, specs → ../specs、sidebars.js → ../docs/sidebars.js）
   - package.jsonを修正（ブラウザ自動起動を無効化）
   - 依存関係をインストール（**React 18**、swagger-ui-react）
   - SwaggerUIコンポーネントをコピー（src/components/SwaggerUI.tsx）

**前提条件（重要）**:
- ✅ contract-spec-generator スキル完了（specs/, doc-config.json）
- ✅ contract-doc-generator スキル完了（docs/, sidebars.js）
- ✅ Node.js 18以上

**実行手順**:

```bash
# 1. Docusaurusを初期化（プロジェクトルートから実行）
npx create-docusaurus@latest $SITE_DIR classic --typescript

# 2. サイト構造をセットアップ（全自動）
python3 .claude/skills/contract-site-builder/scripts/setup-site-structure.py \
  --site-dir $SITE_DIR \
  --docs-dir $DOCS_DIR \
  --specs-dir $SPECS_DIR
```

**重要**: 全てのBashコマンドを**フォアグラウンドで実行**してください（`run_in_background=false`）

**setup-site-structure.pyの処理内容**:
- Step 0: 事前チェック（前提条件確認、エラーなら詳細メッセージ表示）
- Step 1: デフォルトファイル削除
- Step 2: シンボリックリンク作成（docs, specs, sidebars.js）
- Step 3: package.json修正（ブラウザ自動起動無効化）
- Step 4: npm依存関係インストール
  - **React 18.x** をインストール（Docusaurus 3.9.2との互換性のため）
  - **swagger-ui-react** をインストール
- Step 5: SwaggerUIコンポーネントコピー（React TypeScriptコンポーネント）

**⚠️ 重要な互換性情報**:
- Docusaurus 3.9.2は**React 18**を使用する必要があります
- `create-docusaurus`はReact 19をインストールする場合がありますが、setup-site-structure.pyが自動的にReact 18にダウングレードします
- React 19を使用すると`Cannot read properties of undefined (reading 'id')`エラーが発生します

**シンボリックリンクを使う理由:**
- ファイルの重複を避ける
- ドキュメントの単一の真実のソースを保つ
- 更新を簡素化（ファイルの再コピーが不要）

---

### フェーズ2: 設定の生成

#### 2.1 Docusaurus設定の生成

ナビゲーションとプラグイン設定を含む `docusaurus.config.js` を作成：

```bash
python3 .claude/skills/contract-site-builder/scripts/generate-docusaurus-config.py \
  --sidebars-path $DOCS_DIR/sidebars.js \
  --config $DOC_CONFIG \
  --output-path $SITE_DIR/docusaurus.config.js
```

**処理**:
1. sidebars.jsからカテゴリとコントラクトを抽出
2. カテゴリベースのナビゲーションドロップダウンを生成
3. シンプルなDocusaurus設定を生成（プラグイン不要）
4. プロジェクト設定値を反映

**生成される設定に含まれるもの**:
- プロジェクトタイトルとタグライン
- ドロップダウンメニュー付きNavbar:
  - 概要ドロップダウン（7ページ）
  - コントラクトカテゴリドロップダウン（動的生成）
- Footer:
  - 概要ページへのリンク
  - コントラクトページへのリンク
  - GitHubリンク（コミュニティセクション）
- Docusaurus classicプリセット設定のみ
- テーマ設定（Prismテーマ、Solidityサポート）

#### 2.2 インデックスページの生成

コントラクト一覧付きホームページを作成：

```bash
python3 .claude/skills/contract-site-builder/scripts/generate-index-page.py \
  --sidebars-path $DOCS_DIR/sidebars.js \
  --docs-dir $DOCS_DIR \
  --config $DOC_CONFIG \
  --output-path $SITE_DIR/src/pages/index.tsx
```

**処理**:
1. sidebars.jsからコントラクトとカテゴリを抽出
2. Markdownファイルからコントラクトの説明を抽出
3. カテゴリベースのコントラクトデータ配列を生成
4. 総コントラクト数を計算
5. React TypeScriptコンポーネントを生成

**生成されるページの機能**:
- プロジェクトタイトルとタグライン付きヒーローセクション
- コントラクト数の表示（「全XX個のスマートコントラクト仕様書」）
- カテゴリベースのコントラクトカード
- API仕様書ページへの直接リンク（`/docs/api/{コントラクト名}`）

#### 2.3 API仕様書ページの生成

各コントラクトのSwagger UIページを自動生成：

```bash
python3 .claude/skills/contract-site-builder/scripts/generate-api-pages.py \
  --sidebars-path $DOCS_DIR/sidebars.js \
  --output-dir $SITE_DIR/docs/api
```

**処理**:
1. sidebars.jsからコントラクトリストを抽出
2. 各コントラクトに対してMDXファイルを生成
3. SwaggerUIコンポーネントをインポート
4. 対応するOpenAPI YAMLファイルのURLを指定

**生成されるMDXファイルの構造**:
```mdx
---
id: StablecoinCore
title: StablecoinCore API仕様書
sidebar_position: 1
---

import SwaggerUI from '@site/src/components/SwaggerUI';

# StablecoinCore API仕様書

<SwaggerUI specUrl="/specs/StablecoinCore/StablecoinCore.openapi.yaml" />
```

**特徴**:
- DocusaurusテーマとSwagger UIの完全統合
- ヘッダー、フッター、サイドバーが維持される
- Reactコンポーネントベースで柔軟なカスタマイズ可能
- プラグイン不要でシンプルな構成

#### 2.4 CSSスタイルのコピー

スタイリング用の固定CSSテンプレートをコピー：

```bash
# インデックスページのスタイル
cp $TEMPLATE_DIR/pages/index.module.css \
   $SITE_DIR/src/pages/index.module.css

# サイト全体のカスタムスタイル
cp $TEMPLATE_DIR/css/custom.css \
   $SITE_DIR/src/css/custom.css
```

**注意**: CSSファイルは現在固定テンプレートとして管理されており、動的生成されません。

#### 2.5 サイドバー設定へのAPI仕様書セクション追加

`sidebars.js` にAPI仕様書カテゴリを追加（自動またはフェーズ1のシンボリックリンクで対応）：

**入力**: `sidebars.js`（入力ドキュメントディレクトリ内、contract-doc-generatorで生成）

**出力**: API仕様書セクションを含む完全なサイドバー構成

**サイドバー構造例**:
```javascript
module.exports = {
  docsSidebar: [
    { type: 'doc', id: 'overview', label: 'システム概要' },
    // ... 概要ページ
    { type: 'category', label: 'Core Contracts', items: [...] },
    // ... コントラクトドキュメント
    {
      type: 'category',
      label: 'API仕様書',
      items: [
        'api/AccessControlMultiSig',
        'api/StablecoinCore',
        // ... 全コントラクト
      ]
    }
  ]
};
```

**注意**: シンボリックリンク（`site/docs → ../docs`、`site/sidebars.js → ../docs/sidebars.js`）により、MarkdownドキュメントとOpenAPI仕様書とサイドバー設定はコピー不要で常に最新状態を参照します。

---

### フェーズ3: ビルドとデプロイ

#### 3.1 依存関係のインストール

全ての依存関係がインストールされていることを確認：

```bash
cd $SITE_DIR
npm install
```

**処理**: package.jsonにリストされた全パッケージをインストール

#### 3.2 本番サイトのビルド

本番用の静的ファイルを生成：

```bash
cd $SITE_DIR
npm run build
```

**処理**:
- 全てのMarkdownとMDXページをHTMLに変換
- Reactコンポーネント（SwaggerUI）をバンドル
- JavaScriptとCSSをバンドル・最適化
- アセットを最適化
- 静的ルートを生成
- Swagger UI Reactコンポーネントを含む対話型APIページを生成

#### 3.3 開発サーバーの起動（オプション）

サイトをローカルでプレビュー：

```bash
cd $SITE_DIR
npm start
```

**出力**: `http://localhost:3000` での開発サーバー

**用途**:
- ローカルテスト
- ビジュアル検証
- ナビゲーションテスト
- リンクチェック

#### 3.4 本番ビルドの配信（オプション）

本番ビルドをローカルでテスト：

```bash
cd $SITE_DIR
npm run serve
```

**出力**: `http://localhost:3000` での本番ビルドサーバー

**用途**:
- デプロイ前の最終検証
- パフォーマンステスト
- 本番ビルドの検証

---

### フェーズ4: 検証（オプション）

#### 4.1 ビジュアル検証チェックリスト

**ホームページ**:
- ✅ プロジェクトタイトルとタグラインが表示される
- ✅ 「全XX個のスマートコントラクト仕様書」が表示される
- ✅ カテゴリベースのカードが表示される
- ✅ 各カードにコントラクト名、説明、「仕様書を見る」ボタンがある
- ✅ 「Docusaurus Tutorial」ボタンがない

**Navbar**:
- ✅ 左側にロゴとプロジェクト名
- ✅ 7ページの「概要」ドロップダウン
- ✅ コントラクトカテゴリのドロップダウン（動的生成）

**Footer**:
- ✅ 概要ページへのリンク
- ✅ コントラクトページへのリンク
- ✅ GitHubリンク（コミュニティセクション）

**サイドバー**:
- ✅ 概要ページに `guidesSidebar` が表示される
- ✅ コントラクトページに `contractsSidebar` が表示される
- ✅ コントラクトがカテゴリ別にグループ化される

**ページ**:
- ✅ 全7つの概要ページが表示される
- ✅ 全てのコントラクトドキュメントページが表示される
- ✅ ホームページの「仕様書を見る」ボタンが `/docs/api/{コントラクト名}` にリンクされる
- ✅ API仕様書ページ（Swagger UI Reactコンポーネント）が正しく表示される
- ✅ Swagger UIがDocusaurusテーマ（ヘッダー・フッター・サイドバー）と統合されている

#### 4.2 エラーチェック

- ✅ 404エラーがない
- ✅ コンソールエラーがない
- ✅ ビルドエラーがない
- ✅ 全てのリンクが機能する
- ✅ 全ての画像が読み込まれる

---

# リファレンス

## 📚 スクリプトリファレンス

### setup-site-structure.py
**パス**: `.claude/skills/contract-site-builder/scripts/setup-site-structure.py`

**目的**: Docusaurusプロジェクトを初期化し、ディレクトリ構造をセットアップ

**使用法**:
```bash
python3 .claude/skills/contract-site-builder/scripts/setup-site-structure.py \
  --site-dir $SITE_DIR \
  --docs-dir $DOCS_DIR \
  --specs-dir $SPECS_DIR
```

**処理**:
1. 前提条件チェック（docs/, specs/, doc-config.json の存在確認）
2. デフォルトのディレクトリと設定を削除
3. docsとspecsとsidebars.jsへのシンボリックリンクを作成
4. package.jsonを修正（ブラウザ自動起動無効化）
5. swagger-ui-reactをインストール
6. SwaggerUIコンポーネント（React TypeScript）をコピー

---

### generate-docusaurus-config.py
**パス**: `.claude/skills/contract-site-builder/scripts/generate-docusaurus-config.py`

**目的**: ナビゲーション付きのシンプルなDocusaurus設定を生成（プラグイン不要）

**使用法**:
```bash
python3 .claude/skills/contract-site-builder/scripts/generate-docusaurus-config.py \
  --sidebars-path $DOCS_DIR/sidebars.js \
  --config $DOC_CONFIG \
  --output-path $SITE_DIR/docusaurus.config.js
```

**処理**:
- sidebars.jsからカテゴリを抽出
- navbarドロップダウンメニューを生成
- シンプルなDocusaurus設定を生成（preset-classicのみ）
- プロジェクト設定値を反映

**特徴**:
- プラグイン不要
- Docusaurus classicプリセットのみ使用
- swagger-ui-reactをReactコンポーネントとして利用

---

### generate-api-pages.py
**パス**: `.claude/skills/contract-site-builder/scripts/generate-api-pages.py`

**目的**: 各コントラクトのSwagger UI APIページ（MDX）を自動生成

**使用法**:
```bash
python3 .claude/skills/contract-site-builder/scripts/generate-api-pages.py \
  --sidebars-path $DOCS_DIR/sidebars.js \
  --output-dir $SITE_DIR/docs/api
```

**処理**:
1. sidebars.jsからコントラクトリストを抽出
2. 各コントラクトに対してMDXファイルを生成
3. SwaggerUIコンポーネントをインポート
4. 対応するOpenAPI YAMLへのURLを指定

**生成されるMDXファイル例**:
```mdx
---
id: StablecoinCore
title: StablecoinCore API仕様書
sidebar_position: 1
---

import SwaggerUI from '@site/src/components/SwaggerUI';

# StablecoinCore API仕様書

<SwaggerUI specUrl="/specs/StablecoinCore/StablecoinCore.openapi.yaml" />
```

**重要なフロントマターフィールド**:
- `id`: Docusaurusがドキュメントを識別するための必須フィールド（コントラクト名）
- `title`: ブラウザタブやメタデータで使用されるページタイトル
- `sidebar_position`: サイドバー内での表示順序

---

### generate-index-page.py
**パス**: `.claude/skills/contract-site-builder/scripts/generate-index-page.py`

**目的**: コントラクト一覧付きホームページを生成

**使用法**:
```bash
python3 .claude/skills/contract-site-builder/scripts/generate-index-page.py \
  --sidebars-path $DOCS_DIR/sidebars.js \
  --docs-dir $DOCS_DIR \
  --config $DOC_CONFIG \
  --output-path $SITE_DIR/src/pages/index.tsx
```

**処理**:
- コントラクトとカテゴリを抽出
- Markdownからコントラクトの説明を読み取り
- コントラクトデータ配列を生成
- React TypeScriptコンポーネントを作成

**テンプレートの場所**:
`.claude/skills/contract-site-builder/templates/site-setup/pages/index.template.tsx`

---

## 🔧 技術詳細

### Docusaurus設定構造

```javascript
const config = {
  title: 'プロジェクトタイトル',
  tagline: 'プロジェクトのタグライン',
  url: 'https://example.com',
  baseUrl: '/',

  presets: [
    [
      'classic',
      {
        docs: {
          id: 'default',
          path: 'docs',  // シンボリックリンク → ../docs
          sidebarPath: './sidebars.js',  // シンボリックリンク → ../docs/sidebars.js
          routeBasePath: 'docs',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'プロジェクト名',
      logo: { ... },
      items: [
        // 概要ドロップダウン（7ページ）
        {
          type: 'dropdown',
          label: '概要',
          position: 'left',
          items: [
            { to: '/docs/overview', label: 'システム概要' },
            { to: '/docs/architecture', label: 'アーキテクチャ' },
            { to: '/docs/roles', label: 'ロール管理' },
            { to: '/docs/security', label: 'セキュリティ' },
            { to: '/docs/testing', label: 'テスト' },
            { to: '/docs/upgrade', label: 'アップグレード' },
            { to: '/docs/audit', label: '監査' }
          ]
        },
        // カテゴリドロップダウン（動的生成）
        ...categoryDropdowns
      ]
    },
    footer: {
      style: 'dark',
      links: [
        // 概要セクション
        { title: '概要', items: [...] },
        // コントラクトセクション
        { title: 'コントラクト', items: [...] },
        // コミュニティセクション（GitHubリンク）
        {
          title: 'コミュニティ',
          items: [
            { label: 'GitHub', href: 'https://github.com/...' }
          ]
        }
      ]
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['solidity'],
    },
  },
};

export default config;
```

**主な特徴**:
- プラグイン不要（`plugins` 配列なし）
- テーマ追加不要（`themes` 配列なし）
- preset-classicのみで完結
- シンボリックリンクでdocsとspecsにアクセス

### インデックスページのデータ構造

```typescript
const contractsData = [
  {
    category: 'Core Contracts',
    items: [
      {
        name: 'StablecoinCore',
        path: '/docs/api/StablecoinCore',  // API仕様書ページへのリンク
        description: 'ステーブルコインシステムの中核となるコントラクト...',
      },
      // ... その他のコントラクト
    ]
  },
  // ... その他のカテゴリ
];
```

**特徴**:
- ホームページから直接API仕様書ページにリンク
- `/docs/api/{コントラクト名}` 形式のURL
- 各カードに「仕様書を見る」ボタンを表示

### サイドバー設定

`contract-doc-generator` により生成され、API仕様書セクションを追加：

```javascript
module.exports = {
  docsSidebar: [
    // 概要ページ
    { type: 'doc', id: 'overview', label: 'システム概要' },
    { type: 'doc', id: 'architecture', label: 'アーキテクチャ' },
    { type: 'doc', id: 'roles', label: 'ロール管理' },
    { type: 'doc', id: 'security', label: 'セキュリティ' },
    { type: 'doc', id: 'testing', label: 'テスト' },
    { type: 'doc', id: 'upgrade', label: 'アップグレード' },
    { type: 'doc', id: 'audit', label: '監査' },

    // コントラクトドキュメント
    {
      type: 'category',
      label: 'Core Contracts',
      items: ['contracts/StablecoinCore', 'contracts/StablecoinProxy', ...]
    },

    // API仕様書（generate-api-pages.jsで生成されたMDXファイル）
    {
      type: 'category',
      label: 'API仕様書',
      items: [
        'api/AccessControlMultiSig',
        'api/BankPausable',
        'api/StablecoinCore',
        // ... 全18コントラクト
      ]
    }
  ]
};
```

**特徴**:
- 単一のサイドバー構成（`docsSidebar`）
- 概要、コントラクトドキュメント、API仕様書を統合
- API仕様書ページはMDXファイル（Swagger UIコンポーネント埋め込み）

### デプロイオプション

**1. GitHub Pages**
```bash
# docusaurus.config.jsで設定
organizationName: 'your-org',
projectName: 'your-project',
deploymentBranch: 'gh-pages',

# デプロイ
GIT_USER=<Your GitHub username> npm run deploy
```

**2. Vercel**
- GitHubリポジトリを接続
- ビルド設定を構成:
  - ビルドコマンド: `npm run build`
  - 出力ディレクトリ: `build`
- プッシュ時に自動デプロイ

**3. Netlify**
- `build/` フォルダをドラッグ＆ドロップ
- またはビルド設定でGitHubリポジトリを接続:
  - ビルドコマンド: `npm run build`
  - 公開ディレクトリ: `build`

**4. AWS S3 + CloudFront**
```bash
# ビルドフォルダをS3にアップロード
aws s3 sync build/ s3://your-bucket-name

# CloudFrontキャッシュを無効化
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

**5. カスタムサーバー**
- 任意の静的ファイルサーバーで `build/` フォルダを配信
- 例: nginx、Apache、Python SimpleHTTPServer

---

## ✅ ベストプラクティス

1. **シンボリックリンクを検証** - docsとspecsのリンクが正しく作成されていることを確認
2. **サイドバー設定をチェック** - sidebars.jsがコピーされ有効であることを確認
3. **ローカルでビルドをテスト** - デプロイ前に `npm run build` を実行
4. **本番ビルドをプレビュー** - `npm run serve` を使用して本番出力をテスト
5. **全てのリンクを検証** - navbarとサイドバーのリンクが機能することを確認
6. **API仕様を検証** - Swagger UIページが正しく読み込まれることを確認
7. **レスポンシブデザインをチェック** - モバイルとデスクトップでテスト

---

## 🔗 次のステップ

このスキルでドキュメントサイトを構築した後：

1. **ホスティングへのデプロイ**: デプロイプラットフォームを選択（GitHub Pages、Vercel、Netlifyなど）
2. **カスタムドメインの設定**（オプション）: ドキュメント用のカスタムドメインをセットアップ
3. **HTTPSの有効化**: サイトがHTTPS経由で配信されることを確認
4. **CI/CDのセットアップ**: ドキュメント更新時のデプロイを自動化

**関連スキル**:
- `contract-spec-generator`: OpenAPI仕様書の生成（前提条件）
- `contract-doc-generator`: Markdownドキュメントの生成（前提条件）

**関連コマンド**:
- `/build-contract-site`: このスキルを実行してDocusaurusサイトを構築

---

## 📦 依存関係

必要なパッケージ（自動インストール）:

- `@docusaurus/core` - Docusaurusコア
- `@docusaurus/preset-classic` - クラシックテーマプリセット
- `@docusaurus/theme-mermaid` - Mermaid図表サポート
- `swagger-ui-react` - Swagger UI Reactコンポーネント
- `react` - Reactライブラリ
- `react-dom` - React DOMライブラリ

**Node.js要件**: Node.js 18+推奨

**重要**: 以下のパッケージは不要（使用しない）:
- ~~`docusaurus-plugin-openapi-docs`~~ - プラグインベース（使用せず）
- ~~`docusaurus-theme-openapi-docs`~~ - プラグインベース（使用せず）
- ~~`redocusaurus`~~ - Redoc統合（使用せず）

代わりに `swagger-ui-react` をReactコンポーネントとして直接利用します。

---

## 🚨 トラブルシューティング

**「Cannot find module 'swagger-ui-react'」でビルドが失敗**
- 解決策: 出力サイトディレクトリで `npm install` を実行
- `setup-site-structure.py` を再実行してswagger-ui-reactをインストール

**navbarリンクで404エラー**
- 解決策: 全7つの概要ページが入力ドキュメントディレクトリに存在することを確認
- シンボリックリンク `site/docs → ../docs` が正しく作成されていることを確認

**API仕様書ページが読み込まれない**
- 解決策: `/docs/api/{コントラクト名}.mdx` ファイルが存在することを確認
- `generate-api-pages.py` を実行してMDXファイルを生成
- `static/specs/` または `specs/` ディレクトリにOpenAPI YAMLファイルが存在することを確認
- ブラウザコンソールで404エラーを確認（specUrlのパスが正しいか）

**Swagger UIコンポーネントが見つからない**
- 解決策: `site/src/components/SwaggerUI.tsx` が存在することを確認
- `setup-site-structure.py` を再実行してコンポーネントをコピー

**シンボリックリンクが機能しない**
- 解決策: シンボリックリンクが正しく作成されていることを確認
  ```bash
  ls -la {SITE_DIR}/docs
  ls -la {SITE_DIR}/sidebars.js
  ```
- 必要に応じて `setup-site-structure.py` を再実行

**ビルドは成功するがページが空白・黒画面**
- 解決策: ブラウザコンソールでエラーを確認
- package.jsonに不要なプラグイン（docusaurus-plugin-openapi-docs等）が残っていないか確認
- `site/src/pages/` に複数のindex.*ファイル（index.js と index.tsx）が存在しないか確認
- docusaurus.config.jsに `plugins` 配列や `themes` 配列が残っていないか確認

**「Cannot read properties of undefined (reading 'id')」でビルド失敗**
- 症状: 全ページで `TypeError: Cannot read properties of undefined (reading 'id')` エラー
- 原因: MDXファイルのフロントマターに必須の`id`フィールドがない
- 解決策:
  - `generate-api-pages.py` を最新版で再実行してMDXファイルを再生成
  - 各MDXファイルのフロントマターに `id` と `title` フィールドがあることを確認
  ```bash
  head -n 5 {DOCS_DIR}/api/StablecoinCore.mdx
  # 以下が含まれているべき:
  # ---
  # id: StablecoinCore
  # title: StablecoinCore API仕様書
  # sidebar_position: 1
  # ---
  ```

**sidebars.jsのシンボリックリンクが作成されていない**
- 症状: サイドバーが正しく表示されない、または古いsidebars.tsが使用されている
- 原因: `setup-site-structure.py` が古いバージョンでsidebars.jsのリンクを作成していない
- 解決策:
  - 手動でシンボリックリンクを作成:
    ```bash
    cd {SITE_DIR}
    rm -f sidebars.ts sidebars.js
    ln -s ../docs/sidebars.js sidebars.js
    ```
  - または `setup-site-structure.py` を最新版で再実行

### エラー: "Cannot find module" (パス解決エラー)

**症状**: スクリプト実行時にモジュールが見つからない

**原因**: 相対パスの解決が実行ディレクトリに依存

**解決策**:
- スクリプトをプロジェクトルートから実行
- または環境変数で絶対パスを指定:
  ```bash
  SITE_DIR=/absolute/path/to/site node scripts/setup-site-structure.js
  ```

### エラー: "Unterminated string constant"

**症状**: index.tsx ビルド時にシンタックスエラー

**原因**: Markdown description に改行が含まれている

**解決策**:
- generate-index-page.py を再実行（自動で改行を削除）
- または手動で description を1行に修正

### エラー: "ReferenceError: STRUCTURE is not defined"

**症状**: SSG（静的サイト生成）時にプレースホルダーがエラー

**原因**: テンプレートファイルに `{{PLACEHOLDER}}` が残っている

**解決策**:
- テンプレートファイルのプレースホルダーを削除
- または generate-contract-docs.js を最新版で再実行

### エラー: "Cannot read properties of undefined (reading 'id')"

**症状**: ページレンダリング時にエラー

**原因**: sidebars.js の構造とフロントマターの不一致

**解決策**:
- sidebars.js を `docsSidebar` のみに統一
- フロントマターから `sidebar:` 行を削除

### エラー: "Brave BrowserにApple Eventsを送信する権限がありません"

**症状**: `npm start` 実行時にブラウザ起動エラー（サーバーは正常起動）

**原因**: Docusaurusがブラウザを自動起動しようとするが、macOSの権限がない

**解決策**:
- `setup-site-structure.py` を最新版で実行（自動的にブラウザ自動起動を無効化）
- または手動で package.json の start スクリプトに `--no-open` を追加
- サーバー起動後、手動でブラウザを開いて `http://localhost:3000` にアクセス
