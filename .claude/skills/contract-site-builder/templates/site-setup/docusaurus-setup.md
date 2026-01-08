# Docusaurusサイトのセットアップガイド

このガイドでは、生成したコントラクト仕様書（OpenAPI YAML）を表示するDocusaurusサイトの作成手順を説明します。

## 前提条件

- Node.js 18以上がインストールされていること
- npm, yarn, pnpm, bunのいずれかがインストールされていること
- コントラクト仕様書（OpenAPI YAML）が既に生成されていること

## セットアップ手順

### 1. Docusaurusプロジェクトの初期化

プロジェクトルートで以下のコマンドを実行：

```bash
npx create-docusaurus@latest docs-site classic --typescript
cd docs-site
```

### 2. 必要な依存関係のインストール

Swagger UIプラグインとその他の依存関係をインストール：

```bash
npm install docusaurus-plugin-openapi-docs docusaurus-theme-openapi-docs
```

または

```bash
yarn add docusaurus-plugin-openapi-docs docusaurus-theme-openapi-docs
```

### 3. package.jsonの更新

`docs-site/package.json`に以下の依存関係が含まれていることを確認：

```json
{
  "dependencies": {
    "@docusaurus/core": "^3.9.2",
    "@docusaurus/preset-classic": "^3.9.2",
    "@mdx-js/react": "^3.0.0",
    "clsx": "^1.1.1",
    "prism-react-renderer": "^1.2.1",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "docusaurus-plugin-openapi-docs": "^4.4.3",
    "docusaurus-theme-openapi-docs": "^4.4.3"
  }
}
```

### 4. docusaurus.config.jsの設定

`docs-site/docusaurus.config.js`を以下のように設定：

```javascript
const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').DocusaurusConfig} */
(module.exports = {
  title: 'Avalanche Stablecoin Contract Specifications',
  tagline: 'OpenAPI specifications for Solidity smart contracts',
  url: 'https://your-site-url.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-org',
  projectName: 'avalanche-stablecoin',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false, // ブログ機能を無効化
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api',
        docsPluginId: 'default',
        config: {
          // ここにコントラクトの仕様書を追加
          // 'ContractName': {
          //   specPath: '../docs/contract/specs/ContractName/ContractName.openapi.yaml',
          //   outputDir: 'docs/api/ContractName',
          // },
        },
      },
    ],
  ],

  themes: ['docusaurus-theme-openapi-docs'],

  themeConfig: {
    navbar: {
      title: 'Avalanche Stablecoin',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        // Overviewドロップダウン
        {
          type: 'dropdown',
          label: 'Overview',
          position: 'left',
          items: [
            { to: '/docs/overview', label: 'システム概要' },
            { to: '/docs/architecture', label: 'アーキテクチャ' },
            { to: '/docs/roles', label: '権限・ロール' },
            { to: '/docs/state', label: '状態管理' },
            { to: '/docs/security', label: 'セキュリティ' },
            { to: '/docs/upgrade', label: 'Upgrade' },
            { to: '/docs/testing', label: 'テスト' },
            { to: '/docs/audit', label: '監査' },
          ],
        },
        // Core Contractsドロップダウン
        {
          type: 'dropdown',
          label: 'Core Contracts',
          position: 'left',
          items: [
            { to: '/docs/contracts/StablecoinCore', label: 'StablecoinCore' },
            { to: '/docs/contracts/StablecoinProxy', label: 'StablecoinProxy' },
            { to: '/docs/contracts/StablecoinStorage', label: 'StablecoinStorage' },
            { to: '/docs/contracts/StablecoinView', label: 'StablecoinView' },
          ],
        },
        // Featuresドロップダウン
        {
          type: 'dropdown',
          label: 'Features',
          position: 'left',
          items: [
            { to: '/docs/contracts/StablecoinIssuance', label: 'StablecoinIssuance' },
            { to: '/docs/contracts/StablecoinTransfer', label: 'StablecoinTransfer' },
            { to: '/docs/contracts/StablecoinBank', label: 'StablecoinBank' },
            { to: '/docs/contracts/BankPausable', label: 'BankPausable' },
          ],
        },
        // Access Controlドロップダウン
        {
          type: 'dropdown',
          label: 'Access Control',
          position: 'left',
          items: [
            { to: '/docs/contracts/StablecoinRoles', label: 'StablecoinRoles' },
            { to: '/docs/contracts/StablecoinAdmin', label: 'StablecoinAdmin' },
            { to: '/docs/contracts/BankScopedRoles', label: 'BankScopedRoles' },
            { to: '/docs/contracts/MultiAdminAccessControl', label: 'MultiAdminAccessControl' },
          ],
        },
        // MultiSig & Othersドロップダウン
        {
          type: 'dropdown',
          label: 'MultiSig & Others',
          position: 'left',
          items: [
            { to: '/docs/contracts/DualKeyMultiSig', label: 'DualKeyMultiSig' },
            { to: '/docs/contracts/MultiSigWallet', label: 'MultiSigWallet' },
            { to: '/docs/contracts/AccessControlMultiSig', label: 'AccessControlMultiSig' },
            { to: '/docs/contracts/RoleMultiSigManager', label: 'RoleMultiSigManager' },
            { to: '/docs/contracts/ERC20SoladyUpgradeable', label: 'ERC20SoladyUpgradeable' },
            { to: '/docs/contracts/Dictionary', label: 'Dictionary' },
          ],
        },
        // GitHubリンク
        {
          href: 'https://github.com/your-org/avalanche-stablecoin',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
    },
  },
});
```

### 5. 仕様書の登録

生成されたOpenAPI YAMLファイルをSwagger UIプラグインに登録します。`docusaurus.config.js`の`plugins`セクション内の`config`オブジェクトに各コントラクトを追加：

```javascript
config: {
  'StablecoinCore': {
    specPath: 'specs/StablecoinCore/StablecoinCore.openapi.yaml',
    outputDir: 'docs/api/StablecoinCore',
  },
  'StablecoinBank': {
    specPath: 'specs/StablecoinBank/StablecoinBank.openapi.yaml',
    outputDir: 'docs/api/StablecoinBank',
  },
  // 他のコントラクトも同様に追加
}
```

## 仕様書の自動登録

複数のコントラクト仕様書を一括で登録する場合、以下のようなスクリプトを使用できます：

```javascript
// docusaurus.config.jsに追加
const fs = require('fs');
const path = require('path');

// specs/ ディレクトリからすべてのコントラクトを自動検出
function getContractConfigs() {
  const specsDir = path.join(__dirname, 'specs');
  const config = {};

  if (!fs.existsSync(specsDir)) {
    return config;
  }

  const contracts = fs.readdirSync(specsDir);

  for (const contract of contracts) {
    const yamlPath = path.join(specsDir, contract, `${contract}.openapi.yaml`);
    if (fs.existsSync(yamlPath)) {
      config[contract] = {
        specPath: `specs/${contract}/${contract}.openapi.yaml`,
        outputDir: `docs/api/${contract}`,
      };
    }
  }

  return config;
}

// plugins内で使用
plugins: [
  [
    'docusaurus-plugin-openapi-docs',
    {
      id: 'api',
      docsPluginId: 'default',
      config: getContractConfigs(),
    },
  ],
],

themes: ['docusaurus-theme-openapi-docs'],
```

## 開発サーバーの起動

```bash
npm run start
```

または

```bash
yarn start
```

サーバーが起動したら、ブラウザで `http://localhost:3000` を開きます。

## ビルド

本番用にビルドする場合：

```bash
npm run build
```

ビルドされたファイルは `build/` ディレクトリに出力されます。

## デプロイ

### GitHub Pagesへのデプロイ

```bash
npm run deploy
```

### Vercelへのデプロイ

1. Vercelアカウントを作成
2. プロジェクトをGitHubにプッシュ
3. Vercelダッシュボードで「New Project」をクリック
4. GitHubリポジトリを選択
5. Root Directoryを `docs-site` に設定
6. デプロイ

### Netlifyへのデプロイ

1. Netlifyアカウントを作成
2. プロジェクトをGitHubにプッシュ
3. Netlifyダッシュボードで「New site from Git」をクリック
4. GitHubリポジトリを選択
5. Build command: `npm run build`
6. Publish directory: `docs-site/build`
7. デプロイ

## トラブルシューティング

### ビルドエラー: "Cannot find module"

依存関係を再インストール：

```bash
rm -rf node_modules package-lock.json
npm install
```

### YAML解析エラー

YAMLファイルのインデントと構文を確認してください。特に以下の点に注意：

- インデントは2スペース
- 複数行の文字列は `|` または `>` を使用
- 特殊文字はクォートで囲む

### Swagger UIページが表示されない

1. `config`オブジェクトの`specPath`と`outputDir`が正しいか確認
2. OpenAPI YAMLファイルが存在するか確認
3. `docusaurus gen-api-docs all`コマンドでドキュメントを生成
4. 開発サーバーを再起動

## カスタマイズ

### テーマカラーの変更

`docusaurus.config.js`の`theme.primaryColor`を変更：

```javascript
theme: {
  primaryColor: '#1890ff', // 任意の色に変更
}
```

### サイドバーの幅を変更

```javascript
theme: {
  theme: {
    sidebar: {
      width: '300px', // 任意の幅に変更
    },
  },
}
```

### フッターのカスタマイズ

`docusaurus.config.js`の`themeConfig.footer`を編集：

```javascript
footer: {
  style: 'dark',
  links: [
    {
      title: 'Overview',
      items: [
        { label: 'システム概要', to: '/docs/overview' },
        { label: 'アーキテクチャ', to: '/docs/architecture' },
        { label: '権限・ロール', to: '/docs/roles' },
        { label: 'セキュリティ', to: '/docs/security' },
      ],
    },
    {
      title: 'Core Contracts',
      items: [
        { label: 'StablecoinCore', to: '/docs/contracts/StablecoinCore' },
        { label: 'StablecoinProxy', to: '/docs/contracts/StablecoinProxy' },
        { label: 'StablecoinStorage', to: '/docs/contracts/StablecoinStorage' },
        { label: 'StablecoinView', to: '/docs/contracts/StablecoinView' },
      ],
    },
    {
      title: 'API仕様書',
      items: [
        { label: 'StablecoinCore', to: '/api/StablecoinCore' },
        { label: 'StablecoinBank', to: '/api/StablecoinBank' },
        { label: 'StablecoinIssuance', to: '/api/StablecoinIssuance' },
        { label: 'StablecoinTransfer', to: '/api/StablecoinTransfer' },
      ],
    },
  ],
  copyright: `Copyright © ${new Date().getFullYear()} Your Project.`,
}
```

## 参考リンク

- [Docusaurus公式ドキュメント](https://docusaurus.io/)
- [Docusaurus OpenAPI Docs Plugin](https://github.com/PaloAltoNetworks/docusaurus-openapi-docs)
- [OpenAPI仕様](https://swagger.io/specification/)
