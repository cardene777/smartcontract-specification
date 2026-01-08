---
allowed-tools: Skill(contract-doc-generator)
description: "OpenAPI仕様書からMarkdownドキュメントを生成します。"
---

Generate Markdown documentation from OpenAPI specifications.

⚠️ **重要**: ユーザーとのやり取りは必ず日本語で行ってください。

## コマンドの役割

**前提**: `/generate-contract-specs`で仕様書が既に生成されていること
**入力**: OpenAPI仕様書 (← `docs/contract/specs/`)
**出力**: Markdownドキュメント (→ `docs/contract/docs/`)
**次のステップ**: `/build-contract-site` でサイト構築

---

## 実行フロー

このコマンドは `contract-doc-generator` スキルを呼び出します。

```javascript
Skill({
  skill: "contract-doc-generator"
})
```

スキル内部で以下の処理が自動実行されます：

### フェーズ1: ドキュメント生成
1. OpenAPI仕様書からMarkdownテンプレート生成
   - 各コントラクトごとに5つのMarkdownファイル生成
   - sidebars.js生成（Docusaurusナビゲーション設定）

### フェーズ2: ドキュメント詳細化
2. docs-reviewer エージェント（バックグラウンド実行）
   - コントラクト概要の充実
   - 主要機能の詳細解説（3-5個のコア機能）
   - Mermaid図の追加
   - セキュリティノート、制約の記述

### 概要ページ生成
3. 7つの概要ページ生成
   - システム概要、アーキテクチャ、ロール管理、セキュリティ、テスト、アップグレード、監査

---

## 完了後

ドキュメント生成が完了したら、次のコマンドでサイトを構築してください：

```
/build-contract-site
```
