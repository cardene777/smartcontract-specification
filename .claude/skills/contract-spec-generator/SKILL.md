---
name: contract-spec-generator
description: Solidityスマートコントラクトから5フェーズパイプラインでOpenAPI 3.0（YAML）仕様書を生成します。コントラクト分析、中間表現生成、AI強化、品質検証、OpenAPI公開を経て、クライアント納品可能なAPI仕様書を作成します。
---

# Contract Spec Generator

5フェーズパイプライン（コントラクト分析、中間表現生成、AI強化、品質検証、OpenAPI公開）を通じて、SolidityスマートコントラクトからOpenAPI 3.0（YAML）仕様書を生成します。このスキルは、包括的な日本語ドキュメントを含むクライアント納品可能なAPI仕様書を作成します。

**出力**: 完全な関数説明、エラーケース、型マッピングを含むOpenAPI 3.0 YAMLファイル

## 📋 全体フロー概要

```
Phase 0: 言語設定
└─ 0.1 ドキュメント生成言語の選択 [AskUserQuestion]

Phase 1: コントラクト分析と選択
├─ 1.1 利用可能なコントラクトのリスト化 (list-contracts.js)
├─ 1.2 対象コントラクトのフィルタリング (filter-contracts.py)
└─ 1.3 仕様書の差分検出 [オプション] (detect-contract-diff.py)

Phase 2: 中間表現の生成
└─ 2.1 Contract Spec JSONの生成 (generate-contract-spec-json.py)

Phase 3: AI強化（必須）
├─ 3.1 NatSpecコメントの抽出 (enhance-spec-from-source.py)
├─ 3.2 エラー解析（関数呼び出しチェーン追跡） (analyze-errors.py)
├─ 3.3 spec-reviewerエージェント呼び出し [バックグラウンド実行]
├─ 3.4 品質要件の確認
└─ 3.5 言語翻訳 [英語以外の場合のみ、language-translatorエージェント]

Phase 4: 品質検証
├─ 4.1 検証スクリプトの実行 (validate-spec.py)
├─ 4.2 検証レポートの確認
└─ 4.3 検証失敗の修正（spec-reviewerエージェント再呼び出し）

Phase 5: OpenAPI仕様書の生成
├─ 5.1 OpenAPI YAMLの生成 (generate-openapi-from-json.py)
├─ 5.2 ドキュメント設定ファイルの生成 (generate-doc-config.py)
├─ 5.3 サンプルの追加 [オプション] (enhance-openapi-examples.py)
└─ 5.4 出力の検証
```

### パラメータ

**必須パラメータ**（ユーザーから受け取る）:
- **ABIディレクトリ**: SolidityのABIファイルが格納されているディレクトリへのパス（例: `packages/contract/out`）
- **コントラクトソースディレクトリ**: Solidityソースファイルディレクトリへのパス（例: `packages/contract/src`）

**オプションパラメータ**（デフォルト値あり、環境変数で上書き可能）:
- **中間表現ディレクトリ**: `docs/contract/ir` (環境変数: `IR_DIR`)
- **出力ディレクトリ**: `docs/contract/specs` (環境変数: `OUTPUT_DIR`)
- **フィルタリング済みコントラクトリスト**: `docs/contract/filtered.json` (環境変数: `FILTERED_JSON`)

### ドキュメント内での変数表記

本ドキュメントでは、パスを示す際に以下の変数表記を使用します：

| 変数表記 | 説明 | デフォルト値 / 例 |
|---------|------|------------------|
| `{ABI_DIR}` | ABIディレクトリ（必須パラメータ） | 例: `packages/contract/out` |
| `{CONTRACT_DIR}` | コントラクトソースディレクトリ（必須パラメータ） | 例: `packages/contract/src` |
| `{IR_DIR}` | 中間表現ディレクトリ | デフォルト: `docs/contract/ir` |
| `{OUTPUT_DIR}` | 出力ディレクトリ | デフォルト: `docs/contract/specs` |
| `{FILTERED_JSON}` | フィルタリング済みコントラクトリスト | デフォルト: `docs/contract/filtered.json` |

**注意**: 実際のコマンド実行時には、これらの変数を実際のパスに置き換えてください。

### 環境変数の設定

以降のコマンドをそのままコピペで実行できるよう、最初に環境変数を設定します：

```bash
# ========================================
# 必須パラメータ（ユーザー環境に合わせて設定）
# ========================================
export ABI_DIR="packages/contract/out"
export CONTRACT_DIR="packages/contract/src"

# ========================================
# オプションパラメータ（デフォルト値、必要に応じて変更）
# ========================================
export IR_DIR="docs/contract/ir"
export OUTPUT_DIR="docs/contract/specs"
export FILTERED_JSON="docs/contract/filtered.json"
```

**重要**: 上記の環境変数を設定した後、以降のコマンド例はそのままコピペで実行できます。

## 処理フロー

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

### フェーズ1: コントラクト分析と選択

#### 1.1 利用可能なコントラクトのリスト化

ABIディレクトリから全コントラクトを検出：

```bash
python3 .claude/skills/contract-spec-generator/scripts/list-contracts.py \
  --abi-dir $ABI_DIR \
  --output docs/contract/contracts.json
```

**処理**: ABIディレクトリからコントラクト名を抽出してJSONリストを生成

#### 1.2 対象コントラクトのフィルタリング

処理対象のコントラクトを選択：

```bash
python3 .claude/skills/contract-spec-generator/scripts/filter-contracts.py \
  --input docs/contract/contracts.json \
  --output $FILTERED_JSON
```

**処理**: テストコントラクト、抽象コントラクト、インターフェースを除外（対話的な選択も可能）

#### 1.2.1 フィルタリング結果の確認（必須）

フィルタリング後、対象コントラクトの一覧を表示し、ユーザー承認を得る：

**処理手順**:
1. `docs/contract/filtered.json` の内容を読み込む
2. 対象コントラクトのリストをユーザーに表示:
   ```
   📋 仕様書を生成する対象コントラクト（18個）:
   - StablecoinCore
   - StablecoinBank
   - StablecoinIssuance
   ...
   ```
3. `AskUserQuestion` ツールを使用してユーザーに確認:
   - 質問: "これらのコントラクトで仕様書を生成しますか？"
   - オプション:
     - "はい、全て生成する"
     - "いいえ、キャンセル"
     - "一部のみ生成したい（手動でfiltered.jsonを編集）"

4. ユーザーが承認した場合のみ、次のフェーズ（Phase 1.3またはPhase 2）に進む

**重要**: この確認ステップをスキップしないようにしてください。

#### 1.3 仕様書の差分検出（オプション）

既存の仕様書が存在する場合、変更を検出：

```bash
python3 .claude/skills/contract-spec-generator/scripts/detect-contract-diff.py \
  --filtered-json $FILTERED_JSON \
  --specs-dir $OUTPUT_DIR \
  --output docs/contract/diff-report.json
```

**処理**: 仕様書の更新が必要なコントラクトを特定

**環境変数**（隔離テスト用オプション）:
```bash
export ABI_DIR="temp/test-abi"
export CONTRACT_DIR="temp/test-contract/src"
export FILTERED_JSON="temp/output/filtered.json"
```

---

### フェーズ2: 中間表現の生成

#### 2.1 Contract Spec JSONの生成

ABIとソースコードから構造化された中間表現を作成：

```bash
python3 .claude/skills/contract-spec-generator/scripts/generate-contract-spec-json.py \
  --abi-dir $ABI_DIR \
  --filtered-json $FILTERED_JSON \
  --output-dir $IR_DIR
```

**処理**:
- ABI JSON構造を解析
- 関数、イベント、エラー、構造体を抽出
- Contract Spec JSON形式に変換（descriptionフィールドは空）

**生成される構造**:
```json
{
  "contractName": "StablecoinCore",
  "version": "1.0.0",
  "metadata": {
    "title": "StablecoinCore",
    "description": "",
    "category": ""
  },
  "readFunctions": [...],
  "writeFunctions": [...],
  "events": [...],
  "customErrors": {...}
}
```

---

### フェーズ3: AI強化（必須）

#### 3.1 NatSpecコメントの抽出

Solidity `///` コメントを解析してContract Spec JSONに注入：

```bash
python3 .claude/skills/contract-spec-generator/scripts/enhance-spec-from-source.py \
  --contract-dir $CONTRACT_DIR \
  --ir-dir $IR_DIR \
  --filtered-json $FILTERED_JSON
```

**処理**:
- Solidityソースから `@notice`, `@dev`, `@param`, `@return` を抽出
- Contract Spec JSONの `documentation` フィールドに注入

#### 3.2 エラー解析（関数呼び出しチェーン追跡）

関数が発生させる可能性のある全エラーを再帰的に収集：

```bash
python3 .claude/skills/contract-spec-generator/scripts/analyze-errors.py \
  --contract-dir $CONTRACT_DIR \
  --ir-dir $IR_DIR \
  --filtered-json $FILTERED_JSON
```

**処理**:
- 各関数が直接発生させるエラーを抽出
- 関数呼び出しチェーンを追跡し、内部関数のエラーも収集
- 継承チェーンを辿って関数定義を解決
- 無限再帰を防止（visitedセットで管理）
- modifier内のエラーも検出

**技術詳細**:
- `extract_function_calls()`: 関数本体から関数呼び出しを抽出
- `find_function_in_sources()`: 継承チェーン全体から関数定義を検索
- `collect_errors_recursively()`: 再帰的にエラーを収集

**例**:
```solidity
function proposeKeyRotation(...) external returns (uint256 proposalId) {
    // 直接的なエラー
    if (!_isValidKey(...)) {
        revert BankScopedRoles_UnauthorizedRoleAdmin();
    }

    // 内部関数呼び出し（この関数のエラーも追跡される）
    return _proposeKeyRotation(role, oldKey, newKey);
}
```

#### 3.3 spec-reviewerエージェントの呼び出し（並列実行）

包括的なドキュメントを追加するため、spec-reviewerエージェントを並列でバックグラウンド実行する。

**ステップ1: 進捗管理の初期化**

```bash
python3 .claude/skills/contract-spec-generator/scripts/init-progress.py \
  --filtered-json $FILTERED_JSON \
  --output docs/contract/progress.json
```

**処理**: 総コントラクト数と各コントラクトの初期状態（pending）を記録

**ステップ2: spec-reviewerエージェント並列起動**

全コントラクトに対して、spec-reviewerエージェントを起動（`language.json`から読み取った言語コードを使用）：

```bash
/spec-reviewer {language.json の code}
```

例: `/spec-reviewer ja` または `/spec-reviewer en`

**ステップ3: subagent完了時の自動処理（終了コード方式）**

各subagentは完了時に以下を自動実行します：

**3.1 チェックリスト更新**

```bash
python3 .claude/skills/contract-spec-generator/scripts/update-progress.py --contract {ContractName}
```

**処理内容**:
1. 自分の担当のチェックリストにチェックを入れる（`progress.json`で`"completed"`に更新）
2. 他のチェックリストが全て埋まっているか確認
3. 進捗状況を表示（例: `📊 進捗: 15/18 (残り3個)`）
4. **終了コードで情報を渡す**:
   - `remaining === 0`（全完了） → **終了コード 0**
   - `remaining > 0`（未完了） → **終了コード 1**

**ステップ4: メインエージェント再起動時の判定**

各subagent完了時、メインエージェントが自動的に呼び起こされます（Claude Codeの仕様）。
メインエージェントが再起動したら、**subagentの出力を確認**：

**subagent出力に「🎉 全完了！」が含まれる場合**:
1. `/tasks`コマンドでダブルチェック
2. 全タスクが`completed`であることを確認
3. **Phase 4（品質検証）へ進む**

**それ以外の場合**:
- まだ実行中のsubagentがある
- **何もせず即停止**（次のsubagent完了時に再起動される）

**重要**: スクリプトは実行しない。subagentのupdate-progress.pyが出力する「🎉 全完了！」メッセージで判定する。

**エージェントが追加する内容**:
- `metadata.description` (3行以上の包括的な概要)
- `metadata.category` (コントラクトの分類)
- 全関数の `documentation.summary`
- 全関数の `documentation.details`
- 全パラメータと戻り値の `description`
- 全カスタムエラーの `description`（パターンマッチングでは対応できない複雑な説明も生成）
- 全イベントの `documentation.summary`
- 書き込み関数の完全なエラーケースリスト

#### 3.4 品質要件

AI強化は以下を生成する必要があります:
- ✅ 完全なメタデータdescription（3行以上）
- ✅ カテゴリ割り当て
- ✅ 全関数に `summary` と `details` がある
- ✅ 全パラメータに `description` がある
- ✅ 全エラーに `description` がある
- ✅ 書き込み関数に全ての可能なエラーケースがリストされている
- ✅ クライアント納品可能な品質レベル

#### 3.5 言語翻訳（英語以外の場合のみ）

英語以外の言語が選択された場合、全Contract Spec JSONを翻訳します。

**ステップ1: 翻訳進捗管理の初期化**

```bash
# 英語の場合はスキップ
if [ "$TARGET_LANGUAGE" = "en" ]; then
  echo "✅ 英語モード: 翻訳をスキップ"
  # Phase 4へ直接進む
fi

# 翻訳進捗管理を初期化
python3 .claude/skills/contract-spec-generator/scripts/init-progress-translation.py
```

**入力**: `{FILTERED_JSON}` (対象コントラクトリスト)

**出力**: `docs/contract/progress-translation.json` (翻訳進捗管理ファイル)

**処理**: 総コントラクト数と各コントラクトの初期状態（pending）を記録

**ステップ2: language-translatorエージェント並列起動**

全コントラクトに対して、language-translatorエージェントをバックグラウンドで並列起動：

```bash
# filtered.jsonからコントラクトリストを取得
CONTRACTS=$(node -e "console.log(require('./docs/contract/filtered.json').selected.join(' '))")

# 全コントラクトに対してlanguage-translatorを並列起動
for CONTRACT in $CONTRACTS; do
  # language-translatorエージェントを起動（バックグラウンド）
  claude-code agent language-translator \
    --input "CONTRACT_SPEC_JSON=docs/contract/ir/${CONTRACT}.json" \
    --input "TARGET_LANGUAGE=$TARGET_LANGUAGE" \
    --background
done

echo "✅ ${#CONTRACTS[@]}個の翻訳エージェントを起動"
```

**起動完了後、メインエージェントは停止**

全エージェント起動後、メインエージェントは**停止**します。各翻訳subagent完了時に自動的に再起動されます。

**ステップ3: subagent完了時の自動処理（終了コード方式）**

各翻訳subagentは完了時に以下を自動実行します：

```bash
python3 .claude/skills/contract-spec-generator/scripts/update-progress-translation.py --contract {ContractName}
```

**処理内容**:
1. 自分の担当のチェックリストにチェックを入れる（`progress-translation.json`で`"completed"`に更新）
2. 他のチェックリストが全て埋まっているか確認
3. 進捗状況を表示（例: `📊 翻訳進捗: 15/18 (残り3個)`）
4. **終了コードで情報を渡す**:
   - `remaining === 0`（全完了） → **終了コード 0**
   - `remaining > 0`（未完了） → **終了コード 1**

**ステップ4: メインエージェント再起動時の判定**

各翻訳subagent完了時、メインエージェントが自動的に呼び起こされます。
メインエージェントが再起動したら、**subagentの出力を確認**：

**subagent出力に「🎉 全翻訳完了！」が含まれる場合**:
1. `/tasks`コマンドでダブルチェック
2. 全タスクが`completed`であることを確認
3. **Phase 4（品質検証）へ進む**

**それ以外の場合**:
- まだ実行中の翻訳subagentがある
- **何もせず即停止**（次の翻訳subagent完了時に再起動される）

**重要**: スクリプトは実行しない。subagentのupdate-progress-translation.pyが出力する「🎉 全翻訳完了！」メッセージで判定する。

---

### フェーズ4: 品質検証

#### 4.1 検証スクリプトの実行

Contract Spec JSONの完全性を検証：

```bash
python3 .claude/skills/contract-spec-generator/scripts/validate-spec.py
```

```bash
python3 .claude/skills/contract-spec-generator/scripts/validate-spec.py \
  --ir-dir $IR_DIR \
  --output docs/contract/validation-report.json
```

**処理**:
- メタデータの完全性チェック（description、category）
- 読み取り関数の品質チェック（summary、パラメータ説明）
- 書き込み関数の品質チェック（summary、パラメータ、エラーケース）
- カスタムエラーの説明チェック
- イベントの説明チェック

#### 4.2 検証レポートの確認

JSONレポートを確認：

```json
{
  "passed": ["StablecoinCore", "StablecoinBank"],
  "failed": [
    {
      "contract": "AccessControlMultiSig",
      "errors": [
        "メタデータの説明が空です",
        "読み取り関数 getRoleAdmin: サマリーが空です"
      ],
      "warnings": ["イベント RoleGranted: サマリーが空です"]
    }
  ],
  "warnings": [...]
}
```

**終了コード**:
- `0`: 全ての検証が合格
- `1`: 1つ以上の検証が失敗

#### 4.3 検証失敗の修正

検証が失敗した場合:
1. レポート内のエラーメッセージを確認
2. 失敗したコントラクトに対してspec-reviewerエージェントを再呼び出し
3. 全て合格するまで検証を再実行

**全ての検証が合格するまでフェーズ5に進まないでください。**

---

### フェーズ5: OpenAPI仕様書の生成

#### 5.1 OpenAPI YAMLの生成

Contract Spec JSONをOpenAPI 3.0 YAMLに変換：

```bash
python3 .claude/skills/contract-spec-generator/scripts/generate-openapi-from-json.py
```

**入力**: `{IR_DIR}/*.json` (検証済み)

**出力**: `docs/contract/specs/[ContractName]/[ContractName].openapi.yaml`

**処理**:
- Contract Spec JSONをOpenAPI 3.0形式に変換
- タグ分類を適用（読み取り関数、書き込み関数、イベント等）
- HTTPエンドポイントマッピングを定義
- レスポンススキーマを生成
- エラーレスポンスの例を追加

#### 5.2 ドキュメント設定ファイルの生成

ドキュメントサイト用の設定ファイルを作成：

```bash
python3 .claude/skills/contract-spec-generator/scripts/generate-doc-config.py
```

**入力**:
- `{FILTERED_JSON}`
- `{IR_DIR}/*.json`

**出力**: `docs/contract/doc-config.json`

**処理**:
- カテゴリ分類を生成
- コントラクト概要を集約
- Docusaurusサイト構築用の設定を出力

#### 5.3 サンプルの追加（オプション）

OpenAPI仕様書にリクエスト/レスポンスサンプルを追加：

```bash
python3 .claude/skills/contract-spec-generator/scripts/enhance-openapi-examples.py
```

**入力**: `docs/contract/specs/*/*.openapi.yaml`

**出力**: `docs/contract/specs/*/*.openapi.yaml` (サンプル付き)

**処理**: 各エンドポイントにサンプルリクエストとレスポンスを追加

#### 5.4 出力の検証

生成された仕様書を確認：
- ファイルサイズと行数
- 完全な関数ドキュメント
- エラーレスポンスの例
- 型マッピング

**期待される品質**:
- 全関数に日本語の説明がある
- 全パラメータが文書化されている
- 例付きのエラーケース
- クライアント納品可能な形式

---

# リファレンス

## 📚 スクリプトリファレンス

### list-contracts.js
**パス**: `.claude/skills/contract-spec-generator/scripts/list-contracts.js`

**目的**: ABIディレクトリから全コントラクトを検出

**出力**: `docs/contract/contracts.json`

**使用法**: `node scripts/list-contracts.js`

---

### filter-contracts.py
**パス**: `.claude/skills/contract-spec-generator/scripts/filter-contracts.py`

**目的**: 対話的なコントラクト選択またはバッチフィルタリング

**入力**: `docs/contract/contracts.json`

**出力**: `{FILTERED_JSON}`

**使用法**: `node scripts/filter-contracts.py`

**機能**:
- テストコントラクト（*.t.sol）の除外
- 抽象コントラクトの除外
- インターフェースの除外
- 対話的な複数選択または環境変数による指定

---

### detect-contract-diff.py
**パス**: `.claude/skills/contract-spec-generator/scripts/detect-contract-diff.py`

**目的**: ABIと既存仕様書の間の変更を検出

**入力**:
- `{FILTERED_JSON}`
- `{OUTPUT_DIR}` (既存の仕様書)

**出力**: `docs/contract/diff-report.json`

**使用法**: `node scripts/detect-contract-diff.py`

---

### generate-contract-spec-json.py
**パス**: `.claude/skills/contract-spec-generator/scripts/generate-contract-spec-json.py`

**目的**: ABIからContract Spec JSONスケルトンを生成

**入力**:
- `{FILTERED_JSON}`
- `{ABI_DIR}` (ABIファイル)

**出力**: `{IR_DIR}/*.json`

**使用法**:
```bash
python3 .claude/skills/contract-spec-generator/scripts/generate-contract-spec-json.py \
  --abi-dir $ABI_DIR \
  --filtered-json $FILTERED_JSON \
  --output-dir $IR_DIR
```

---

### enhance-spec-from-source.py
**パス**: `.claude/skills/contract-spec-generator/scripts/enhance-spec-from-source.py`

**目的**: NatSpecコメントを抽出してContract Spec JSONに注入

**入力**:
- `{IR_DIR}/*.json`
- `{CONTRACT_DIR}` (Solidityソース)
- `{FILTERED_JSON}`

**出力**: `{IR_DIR}/*.json` (NatSpec付き)

**使用法**:
```bash
python3 .claude/skills/contract-spec-generator/scripts/enhance-spec-from-source.py \
  --contract-dir $CONTRACT_DIR \
  --ir-dir $IR_DIR \
  --filtered-json $FILTERED_JSON
```

---

### analyze-errors.py
**パス**: `.claude/skills/contract-spec-generator/scripts/analyze-errors.py`

**目的**: 関数呼び出しチェーンを追跡してエラーを収集

**入力**:
- `{IR_DIR}/*.json` (NatSpec付き)
- `{CONTRACT_DIR}` (Solidityソース)
- `{FILTERED_JSON}`

**出力**: `{IR_DIR}/*.json` (エラー情報付き)

**使用法**:
```bash
python3 .claude/skills/contract-spec-generator/scripts/analyze-errors.py \
  --contract-dir $CONTRACT_DIR \
  --ir-dir $IR_DIR \
  --filtered-json $FILTERED_JSON
```

**処理内容**:
- 各書き込み関数からエラーを抽出
- 関数呼び出しチェーンを再帰的に追跡
- 継承チェーンを辿って関数定義を検索
- modifier内のエラーも検出
- 無限再帰防止

**主要関数**:
- `extract_function_calls(func_body)`: 関数本体から関数呼び出しを抽出
- `find_function_in_sources(func_name, all_sources, contract_name, inheritance_chain)`: 継承チェーン全体から関数定義を検索
- `collect_errors_recursively(func_name, source, all_sources, contract_name, custom_errors, modifiers_map, visited)`: 再帰的にエラーを収集

---

### validate-spec.py
**パス**: `.claude/skills/contract-spec-generator/scripts/validate-spec.py`

**目的**: AI強化後のContract Spec JSON品質を検証

**入力**: `{IR_DIR}/*.json` (AI強化版)

**出力**: `docs/contract/validation-report.json`

**使用法**:
```bash
python3 .claude/skills/contract-spec-generator/scripts/validate-spec.py \
  --ir-dir $IR_DIR \
  --output docs/contract/validation-report.json
```

**終了コード**:
- `0`: 全検証が合格
- `1`: 1つ以上の検証が失敗

**検証チェック項目**:
- メタデータの完全性（description、category）
- 読み取り関数の品質（summary、パラメータ説明）
- 書き込み関数の品質（summary、パラメータ、エラーケース）
- カスタムエラーの説明
- イベントの説明

---

### generate-openapi-from-json.py
**パス**: `.claude/skills/contract-spec-generator/scripts/generate-openapi-from-json.py`

**目的**: Contract Spec JSONからOpenAPI 3.0 YAMLを生成

**入力**: `{IR_DIR}/*.json` (検証済み)

**出力**: `docs/contract/specs/*/*.openapi.yaml`

**使用法**:
```bash
python3 .claude/skills/contract-spec-generator/scripts/generate-openapi-from-json.py \
  --ir-dir $IR_DIR \
  --output-dir $OUTPUT_DIR
```

---

### generate-doc-config.py
**パス**: `.claude/skills/contract-spec-generator/scripts/generate-doc-config.py`

**目的**: ドキュメント設定ファイルを生成

**入力**:
- `{FILTERED_JSON}`
- `{IR_DIR}/*.json`

**出力**: `docs/contract/doc-config.json`

**使用法**: `node scripts/generate-doc-config.py`

---

### enhance-openapi-examples.py
**パス**: `.claude/skills/contract-spec-generator/scripts/enhance-openapi-examples.py`

**目的**: OpenAPI仕様書にリクエスト/レスポンス例を追加（オプション）

**入力**: `docs/contract/specs/*/*.openapi.yaml`

**出力**: `docs/contract/specs/*/*.openapi.yaml` (例付き)

**使用法**: `node scripts/enhance-openapi-examples.py`

---

## 🔧 技術詳細

### Solidity型マッピング

| Solidity型 | OpenAPI型 | フォーマット | 例 |
|-----------|----------|---------|-----|
| `address` | `string` | `address` | "0x742d35Cc6634C0532925a3b844Bc454e4438f44e" |
| `uint256`, `uint` | `string` | `uint256` | "1000000000000000000" |
| `int256`, `int` | `string` | `int256` | "-1000000000000000000" |
| `bool` | `boolean` | - | true |
| `string` | `string` | - | "Hello" |
| `bytes`, `bytes32` | `string` | `bytes` | "0x1234..." |
| 配列 (`[]`) | `array` | - | ["item1", "item2"] |
| 構造体 | `object` | - | {"field1": "value1"} |

### エラーレスポンス形式

全エンドポイントには標準化されたエラーレスポンスが含まれます：

```yaml
responses:
  '200':
    description: 正常な処理
    content:
      application/json:
        schema:
          type: object
          properties:
            return0:
              type: string
              description: 戻り値の説明
  '500':
    description: "この関数で発生する可能性のあるエラーの一覧です。<br>・**InvalidAddress**<br>アドレスがゼロアドレスの場合<br>・**InsufficientBalance**<br>残高が不足している場合<br>"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ErrorResponse'
        examples:
          InvalidAddress:
            summary: InvalidAddress
            value:
              error: "InvalidAddress"
              message: "アドレスがゼロアドレスの場合"
          InsufficientBalance:
            summary: InsufficientBalance
            value:
              error: "InsufficientBalance"
              message: "残高が不足している場合"
```

### タグカテゴリ

関数と要素はUI上でのグループ化のためにタグに分類されます：

- **読み取り関数**: 状態を変更しないview/pure関数
- **書き込み関数**: コントラクトの状態を変更する関数
- **変数**: パブリックな状態変数
- **定数**: 定数値
- **Mapping**: マッピング変数
- **イベント**: コントラクトイベント
- **エラー**: カスタムエラー
- **構造体**: 構造体定義
- **Modifier**: 関数修飾子

---

## ✅ ベストプラクティス

1. **全フェーズを順番に実行** - フェーズをスキップしない（特にPhase 3.3のspec-reviewerエージェント呼び出し）
2. **AI強化後は必ず検証を実行** - フェーズ4をスキップしない
3. **テストには環境変数を使用** - 隔離されたtemp/ディレクトリでテスト
4. **OpenAPI生成前に検証が合格していることを確認** - フェーズ5には検証済み入力が必要
5. **検証レポートを注意深く確認** - 全てのエラーを修正、警告は許容可能
6. **バッチ処理を使用** - 一貫性のため全コントラクトを1セッションで処理
7. **spec-reviewerエージェントを適切に呼び出す** - 全ての翻訳・説明生成を担当（必ずバックグラウンド実行）
8. **出力品質をチェック** - ファイルサイズ、行数、ドキュメント完全性を検証

---

## 🔗 次のステップ

このスキルでOpenAPI仕様書を生成した後：

1. **Markdownドキュメントの生成**: `contract-doc-generator` スキルを使用してOpenAPI仕様書からMarkdownドキュメントを作成
2. **ドキュメントサイトの構築**: `contract-site-builder` スキルを使用してDocusaurusドキュメントサイトを作成
3. **デプロイ**: 生成された静的サイトをホスティングプラットフォームにデプロイ

**関連スキル**:
- `contract-doc-generator`: OpenAPI仕様書からのMarkdownドキュメント生成
- `contract-site-builder`: Docusaurusサイトの構築とデプロイ

**関連コマンド**:
- `/generate-contract-specs`: このスキルを実行してOpenAPI仕様書を生成
