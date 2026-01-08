# Contract Spec Generator Scripts

Solidity コントラクトから OpenAPI 仕様書を生成するためのスクリプト集

## スクリプト一覧

### 1. コントラクト分析・フィルタリング

#### `list-contracts.js`
Solidityソースディレクトリからコントラクト一覧を取得

**機能:**
- メインコントラクト（直接定義されたコントラクト）を抽出
- 継承元コントラクトを解析
- 継承関係のマップを生成
- JSON形式で出力

**使用例:**
```bash
node list-contracts.js \
  --contract-dir packages/contract/src \
  --output tmp/contracts.json
```

**出力形式:**
```json
{
  "mainContracts": ["StablecoinCore", "StablecoinBank", ...],
  "inheritedContracts": ["ERC20", "Pausable", ...],
  "allContracts": [...],
  "inheritanceMap": {
    "StablecoinCore": ["ERC20", "Pausable"]
  },
  "summary": {
    "totalSolidityFiles": 50,
    "mainContractsCount": 20,
    "inheritedContractsCount": 15,
    "allContractsCount": 35
  }
}
```

---

#### `filter-contracts.js`
コントラクトリストから不要なコントラクトを除外

**機能:**
- スコープ選択（main/related/all）に応じてフィルタ
- テスト、モック、インターフェース等を自動除外
- 除外されたコントラクトをカテゴリ別に記録
- JSON形式で出力

**使用例:**
```bash
node filter-contracts.js \
  --input tmp/contracts.json \
  --scope main \
  --output tmp/filtered.json
```

**スコープ:**
- `main`: メインコントラクトのみ
- `related`: メインコントラクト + 直接継承されているコントラクト
- `all`: すべてのコントラクト

**除外カテゴリ:**
- `test`: `*Test`, `*TestBase`, `*TestImpl`
- `mock`: `Mock*`
- `interface`: `I*`
- `library`: `*Lib`
- `helper`: `*Helper*`, `*Utils*`
- `script`: `*Script`, `Deploy*`, `Upgrade*`
- `forge`: `Vm*`, `console*`, `std*`, `Common*`

**出力形式:**
```json
{
  "scope": "main",
  "selected": ["StablecoinCore", "StablecoinBank", ...],
  "excluded": {
    "test": ["StablecoinTest"],
    "mock": ["MockERC20"],
    "interface": ["IERC20"],
    ...
  },
  "summary": {
    "totalInput": 35,
    "selectedCount": 18,
    "excludedCount": 17
  }
}
```

---

### 2. 差分検出

#### `detect-contract-diff.js`
ABIファイルと既存仕様書の差分を検出

**機能:**
- 既存ファイルがない場合は早期リターン（初回生成）
- ABIファイルから関数・イベント・エラーを正確に抽出
- コントラクトレベル: 新規/削除/更新/未変更を検出
- 関数レベル: 新規/削除/変更を検出
- JSON差分レポートを生成

**使用例:**
```bash
node detect-contract-diff.js \
  --abi-dir packages/contract/out \
  --contract-dir packages/contract/src \
  --specs-dir docs/contract/specs
```

**出力:**
- コンソール: 人間が読みやすい形式で差分を表示
- ファイル: `contract-diff-report.json`

---

### 3. 仕様書生成

#### `generate-contract-spec-json.js`
Contract Spec JSON（中間表現）を生成

**機能:**
- ABIとソースコードから関数、イベント、エラー情報を抽出
- NatSpecコメントを解析
- `docs/contract/ir/{ContractName}.json` に保存

**使用例:**
```bash
node generate-contract-spec-json.js
```

---

#### `generate-openapi-from-json.js`
Contract Spec JSON から OpenAPI 3.0/Swagger 2.0 を生成

**機能:**
- Contract Spec JSON を読み込み
- OpenAPI 3.0 YAML を生成
- Swagger 2.0 JSON を生成
- `docs/contract/specs/{ContractName}/` に保存

**使用例:**
```bash
node generate-openapi-from-json.js
```

---

#### `generate-doc-config.js`
Contract Spec JSON と OpenAPI仕様書から doc-config.json を生成

**機能:**
- `docs/contract/tmp/filtered.json` から選択されたコントラクトリストを読み込み
- OpenAPI仕様書から説明を抽出
- コントラクト名のプレフィックスでカテゴリを自動分類
- プロジェクト情報はデフォルト値を設定
- `docs/contract/doc-config.json` に保存

**使用例:**
```bash
node generate-doc-config.js
```

**カテゴリ分類ルール:**
- `Stablecoin*` → "Stablecoin Contracts"
- `Bank*` → "Bank Management"
- `MultiSig*`, `DualKey*`, `AccessControl*`, `RoleMultiSig*` → "Access Control & MultiSig"
- その他 → "Other Contracts"

**出力形式:**
```json
{
  "projectTitle": "Contract Documentation",
  "projectName": "Avalanche Stablecoin",
  "tagline": "Smart Contract Documentation",
  "projectDescription": "...",
  "githubOrg": "your-org",
  "repoName": "your-repo",
  "baseUrl": "/",
  "primaryColor": "#1890ff",
  "categories": {
    "Stablecoin Contracts": ["StablecoinCore", ...],
    "Bank Management": ["BankPausable", ...],
    "Access Control & MultiSig": ["AccessControlMultiSig", ...],
    "Other Contracts": ["Dictionary", ...]
  },
  "descriptions": {
    "StablecoinCore": {
      "overview": "...",
      "detail": "..."
    }
  }
}
```

---

## 一時ファイル

スクリプト間で受け渡される中間ファイルは `docs/contract/tmp/` ディレクトリに保存されます:

- `docs/contract/tmp/contracts.json`: コントラクト一覧
- `docs/contract/tmp/filtered.json`: フィルタリング済みコントラクト
- `contract-diff-report.json`: 差分検出レポート（プロジェクトルート）

---

## ワークフロー

### 1. コントラクト一覧取得
**スクリプト**: `list-contracts.js`
**入力**: packages/contract/src/ (Solidityソースコード)
**出力**: tmp/contracts.json

### 2. フィルタリング
**スクリプト**: `filter-contracts.js`
**入力**: tmp/contracts.json
**出力**: tmp/filtered.json

### 3. Contract Spec JSON生成
**スクリプト**: `generate-contract-spec-json.js`
**入力**: packages/contract/out/ (ABI), packages/contract/src/ (ソースコード), tmp/filtered.json
**出力**: docs/contract/ir/*.json (英語)

### 4. 日本語化
**処理**: spec-reviewerエージェント
**入力**: docs/contract/ir/*.json (英語)
**出力**: docs/contract/ir/*.json (日本語化済み)

### 5. OpenAPI仕様書生成
**スクリプト**: `generate-openapi-from-json.js`
**入力**: docs/contract/ir/*.json (日本語化済み)
**出力**: docs/contract/specs/*/*.openapi.yaml

### 6. doc-config.json生成
**スクリプト**: `generate-doc-config.js`
**入力**: tmp/filtered.json, docs/contract/specs/*/*.openapi.yaml
**出力**: docs/contract/doc-config.json

---

## エラーハンドリング

- 成功時: `exit 0`
- 失敗時: `exit 1`
- エラーメッセージ: 日本語で `stderr` に出力

---

## テスト

各スクリプトは独立して実行・テストできます:

```bash
# コントラクト一覧取得のテスト
node list-contracts.js --contract-dir test/fixtures/contracts

# フィルタリングのテスト
echo '{"mainContracts":["Test","StablecoinCore"]}' > tmp/test.json
node filter-contracts.js --input tmp/test.json --scope main
```
