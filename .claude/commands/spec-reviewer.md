---
name: spec-reviewer
description: spec-reviewerエージェントを全コントラクトに対して並列起動
---

# spec-reviewer コマンド

**引数**:
- `$1`: 言語コード (例: `ja`, `en`, `ko`, `zh-CN`)

**重要**: 各エージェント起動前に`docs/contract/language.json`の存在を確認し、ない場合は以下の内容で作成してください：
```json
{
  "code": "$1",
  "name": "言語名"
}
```

エージェントは`docs/contract/language.json`から言語設定を読み込み、その言語で出力します。

## 目的

filtered.jsonに記載された全コントラクトに対して、spec-reviewerエージェントをバックグラウンドで並列起動します。

## 処理内容

1. `docs/contract/filtered.json` を読み込む
2. 各コントラクトに対してspec-reviewerエージェントを起動（言語コード: `$1`）
3. 起動完了メッセージを表示

## 実行フロー

**ステップ1: filtered.jsonの読み込み**

`docs/contract/filtered.json` から対象コントラクトリストを取得。

**ステップ2: 全spec-reviewerエージェントを並列起動**

filtered.jsonの`selected`配列から全コントラクトを取得し、**各コントラクトに対して**以下のパラメータでTaskツールを使用してspec-reviewerエージェントをバックグラウンド起動してください：

**各コントラクトごとに実行**:
```
Task({
  subagent_type: "spec-reviewer",
  run_in_background: true,
  description: "Enhance {ContractName} spec",
  prompt: `docs/contract/ir/{ContractName}.json を $1 言語で強化してください。全ての説明フィールドを $1 で生成し、空の説明フィールドを埋めてください。

完了後、必ず以下のコマンドを実行して進捗を更新してください:

python3 .claude/skills/contract-spec-generator/scripts/update-progress.py --contract {ContractName}`
})
```

**重要**: filtered.jsonの全18コントラクトに対して上記を実行してください。

**ステップ3: 完了メッセージの表示**

全エージェント起動後、以下を表示：

```
✅ {N}個のspec-reviewerエージェントをバックグラウンドで起動しました。
⏳ 各エージェントが完了次第、自動的に進捗が更新されます。
💡 エージェント完了時に再度呼び出されるまで待機してください。
```

## 注意事項

- このコマンドを実行する前に、必ず `init-progress.py` を実行して進捗管理を初期化してください
- バックグラウンドエージェントは完了時に自動的にメインエージェントを呼び出します
- 全エージェントの完了確認は `/tasks` コマンドと `check-progress.py` で行います
