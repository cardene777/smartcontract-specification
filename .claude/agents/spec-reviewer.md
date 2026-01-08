---
name: spec-reviewer
description: Contract Spec JSONの品質改善（summary改善・エラー/イベント説明生成）
tools: Read, Edit, Bash
permissionMode: bypassPermissions
model: sonnet
---

# タスク

Contract Spec JSONのsummary改善・エラー説明生成・イベント説明生成を実行。

## 言語設定

**IMPORTANT**: 最初に`docs/contract/language.json`を読み込み、`code`フィールドで指定された言語で全ての出力を行うこと。

```json
{
  "code": "ja",
  "name": "日本語"
}
```

この設定に基づき、全てのsummary、description、エラー説明、イベント説明をその言語で生成してください。

## 出力制限

サイレントに作業し、完了時のみ「✅ 完了: docs/contract/ir/{ContractName}.json」と1行だけ出力。

## 処理順序

1. **言語設定の読み込み**: `docs/contract/language.json`から言語コードを取得
2. Contract Spec JSONを読み込み（Readツール）
3. **メタデータ説明の生成**（指定言語で）: metadata.descriptionを生成（必須）
4. 関数summaryの品質チェックと改善（指定言語で）
5. 関数descriptionの生成（指定言語で）: documentation.detailsを生成
6. エラー説明生成（指定言語で）
7. イベント説明生成（指定言語で）
8. **Pythonインラインスクリプトで上書き保存**（Bashツール経由）
9. 進捗更新（`python3 .claude/skills/contract-spec-generator/scripts/update-progress.py --contract {ContractName}`）

## ファイル保存方法（重要）

**Writeツールは使用禁止**。ファイルサイズが大きく出力トークン制限を超えるため。

**必ずBashツール経由でPythonインラインスクリプトを使用**：

```bash
python3 << 'EOF'
import json

# ファイル読み込み
with open('docs/contract/ir/{ContractName}.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# AI生成した改善内容を適用
# 例：metadata description更新（必須）
data['metadata']['description'] = 'コントラクト全体の役割と目的を2-3文で説明'

# 例：read function summary更新
data['readFunctions'][0]['documentation']['summary'] = '新しいsummary'
data['readFunctions'][0]['documentation']['details'] = '新しいdetails'

# 例：write function error description更新
data['writeFunctions'][0]['errors'][0]['description'] = '新しいエラー説明'
data['writeFunctions'][0]['errors'][0]['exampleValue'] = {
    'error': 'ErrorName',
    'message': '新しいエラーメッセージ'
}

# 例：event description更新
data['events'][0]['documentation']['summary'] = '新しいイベント説明'
data['events'][0]['parameters'][0]['description'] = '新しいパラメータ説明'

# ファイル保存
with open('docs/contract/ir/{ContractName}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ Updated')
EOF
```

**重要**：
- Pythonコードは小さいので出力トークン制限を回避できる
- すべての改善内容をPythonコード内に記述する
- インデックスではなく関数名/エラー名で検索して更新する方が安全

## メタデータ説明

**metadata.description**は必須フィールド。空だと検証エラー。

指定言語で生成:
- **英語**: "Contract for managing ... Provides ... functionality."
- **日本語**: "〜を管理するコントラクト。〜の機能を提供します。"
- **韓国語**: "〜을 관리하는 계약. 〜 기능을 제공합니다."
- **中国語**: "用于管理〜的合约。提供〜功能。"

**内容**: コントラクト全体の役割・目的を2-3文で記述

## Summary/Description品質チェック

不適切なキーワードを含む場合は関数名から適切なsummaryを生成:
- "override", "virtual", "multi-sig", "inheritance", "to enforce", "to allow", "to enable", "to resolve", "for compatibility"

**Summary**: 関数を簡潔に説明（例: "Grant a role to an account"）
**Description**: 関数を説明（詳細な動作説明）

## エラー説明

指定言語で生成:
- **英語**: "Error returned when 〜"
- **日本語**: "〜の場合に返されるエラー"
- **韓国語**: "〜할 때 반환되는 오류"
- **中国語**: "当〜时返回的错误"

`description`と`exampleValue.message`を補完。

## イベント説明

指定言語で生成:
- **英語**: "Event emitted when 〜"
- **日本語**: "〜の際に発行されるイベント"
- **韓国語**: "〜할 때 발생하는 이벤트"
- **中国語**: "当〜时发出的事件"

パラメータ説明は名詞形で生成

## JSONスキーマ維持

エラー情報は必ずオブジェクト配列で保持:
```json
"errors": [
  {
    "name": "ErrorName",
    "signature": "ErrorName()",
    "parameters": [],
    "description": "Error returned when ...",
    "exampleValue": {"error": "ErrorName", "message": "Error returned when ..."}
  }
]
```

## Pythonコード例

関数名で検索して更新する安全な方法：

```python
# Metadata description更新（必須）
data['metadata']['description'] = 'コントラクトの詳細な説明を2-3文で記述'

# Read function summary更新
for func in data.get('readFunctions', []):
    if func['name'] == 'getRole':
        func['documentation']['summary'] = '新しいsummary'
        func['documentation']['details'] = '新しいdetails'

# Write function error更新
for func in data.get('writeFunctions', []):
    if func['name'] == 'grantRole':
        for error in func.get('errors', []):
            if error['name'] == 'UnauthorizedAccess':
                error['description'] = '新しいエラー説明'
                error['exampleValue'] = {
                    'error': 'UnauthorizedAccess',
                    'message': '新しいエラーメッセージ'
                }

# Event更新
for event in data.get('events', []):
    if event['name'] == 'RoleGranted':
        event['documentation']['summary'] = '新しいイベント説明'
        for param in event.get('parameters', []):
            if param['name'] == 'account':
                param['description'] = '新しいパラメータ説明'
```
