---
name: overview-reviewer
description: overview-reviewerエージェントを起動してシステム概要ページ（全7ページ）を強化
---

# overview-reviewer コマンド

## 使用法

スキル内から呼び出し：
```
Skill({
  skill: "overview-reviewer",
  args: "ja"
})
```

**引数**:
- `$1`: 言語コード (例: `ja`, `en`, `ko`, `zh-CN`)

**重要**: エージェント起動前に`docs/contract/language.json`の存在を確認し、ない場合は以下の内容で作成してください：
```json
{
  "code": "$1",
  "name": "言語名"
}
```

エージェントは`docs/contract/language.json`から言語設定を読み込み、その言語で出力します。

## 目的

システム概要ページ（全7ページ）を詳細化し、Mermaid図と包括的な説明を追加します。

## 処理対象

以下の7つのMarkdownファイルを強化：
- `docs/contract/docs/overview.md` - システム全体の概要
- `docs/contract/docs/architecture.md` - アーキテクチャ設計
- `docs/contract/docs/roles.md` - ロール管理
- `docs/contract/docs/security.md` - セキュリティ設計
- `docs/contract/docs/testing.md` - テスト戦略
- `docs/contract/docs/upgrade.md` - アップグレード手順
- `docs/contract/docs/audit.md` - 監査準備

## 実行フロー

**ステップ1: overview-reviewerエージェントを起動**

Taskツールを使用してoverview-reviewerエージェントを起動：

```
Task({
  subagent_type: "overview-reviewer",
  run_in_background: false,
  description: "Enhance overview pages",
  prompt: `システム概要ページ（全7ページ）を $1 言語で詳細化してください。全ての内容を $1 で生成してください。

処理対象ファイル:
- docs/contract/docs/overview.md
- docs/contract/docs/architecture.md
- docs/contract/docs/roles.md
- docs/contract/docs/security.md
- docs/contract/docs/testing.md
- docs/contract/docs/upgrade.md
- docs/contract/docs/audit.md

入力ファイル:
- 全コントラクトのSpec JSON: docs/contract/ir/*.json
- 全Solidityソース: packages/contract/src/**/*.sol
- 全OpenAPI仕様書: docs/contract/specs/*/*.openapi.yaml
- フィルタ済みコントラクトリスト: docs/contract/filtered.json

タスク:
1. 全コントラクトを分析してシステム全体のアーキテクチャを理解
2. 各概要ページのテンプレートを読み込み
3. 詳細な説明とMermaid図を追加
4. Python inline scriptsで保存

重要:
- 各ページに最低1つのMermaid図を追加
- 実際のコントラクト実装に基づいた正確な内容
- frontmatter（YAML）は変更しない
- WriteツールとEditツールは使用禁止（Python inline scriptsのみ）`
})
```

**ステップ2: 完了メッセージの表示**

エージェント完了後、以下を表示：

```
✅ overview-reviewerエージェントが完了しました。
📄 全7つのシステム概要ページが強化されました：
   - overview.md
   - architecture.md
   - roles.md
   - security.md
   - testing.md
   - upgrade.md
   - audit.md
```

## 使用例

contract-doc-generatorスキル内から：
```
Skill({
  skill: "overview-reviewer",
  args: "ja"
})
```

または英語で：
```
Skill({
  skill: "overview-reviewer",
  args: "en"
})
```

## docs-reviewerとの違い

| 項目 | docs-reviewer | overview-reviewer |
|------|---------------|-------------------|
| 対象 | コントラクトドキュメント（18個） | システム概要ページ（7個） |
| 実行方式 | 並列（バックグラウンド） | 単一（フォアグラウンド） |
| 進捗管理 | 必要（progress-docs.json） | 不要 |
| 完了待機 | 必要（各subagent完了を待つ） | 不要（即座に完了） |

## 注意事項

- このコマンドは**docs-reviewerと並行して実行可能**
- フォアグラウンド実行のため、完了まで待機が必要（通常2-3分）
- 完了後は自動的に次のステップに進める
