---
allowed-tools: Skill(contract-site-builder)
description: "ドキュメントと仕様書からDocusaurusサイトを構築します。"
---

Build Docusaurus site from documentation and specs.

⚠️ **重要**: ユーザーとのやり取りは必ず日本語で行ってください。

## コマンドの役割

**前提**: `/generate-contract-docs`でドキュメントが既に生成されていること
**入力**: Markdownドキュメント (← `docs/contract/docs/`) + OpenAPI仕様書 (← `docs/contract/specs/`)
**出力**: Docusaurusサイト (→ `docs/contract/site/`)
**最終ステップ**: サイトを起動して確認

---

## 実行フロー

このコマンドは `contract-site-builder` スキルを呼び出します。

```javascript
Skill({
  skill: "contract-site-builder"
})
```

スキル内部で以下の処理が自動実行されます：

### フェーズ1: サイト構造セットアップ
1. Docusaurus初期化
2. デフォルトファイル削除
3. シンボリックリンク作成
4. package.json修正（ブラウザ自動起動無効化）
5. 依存関係インストール

### フェーズ2: 設定ファイル生成
6. Docusaurus設定生成
7. トップページ生成
8. CSSファイルコピー

### フェーズ3: ドキュメントコピーとビルド
9. Sidebarコピー
10. サイトビルド（オプション）
11. サイト起動（開発モード）

---

## 完了後

サイトが起動したら、ブラウザで `http://localhost:3000` を開いて確認してください。

本番ビルド：
```bash
cd docs/contract/site
npm run build
```
