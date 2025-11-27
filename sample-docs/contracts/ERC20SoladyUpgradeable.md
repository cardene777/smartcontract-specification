---
sidebar_position: 17
---

# ERC20SoladyUpgradeable

> **[📋 API仕様書を見る](/api/ERC20SoladyUpgradeable)**

## 概要

Soladyライブラリを使用した効率的なERC20実装です。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Initializable`

## 主要機能

### ガス効率

Soladyの最適化されたERC20実装を採用。標準的な実装より少ないガスで動作します。

### アップグレード対応

Initializableパターンを使用し、プロキシ経由でのアップグレードに対応。

## 関数一覧

<details>
<summary><strong>変数 (4)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`decimals`](#decimals) | トークンの小数点以下の桁数を取得します。 |
| [`name`](#name) | トークンの名前を取得します。 |
| [`symbol`](#symbol) | トークンのシンボルを取得します。 |
| [`totalSupply`](#totalsupply) | トークンの総供給量を取得します。 |

### decimals

トークンの小数点以下の桁数を取得します。

ERC20標準関数です。通常は18です。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 小数点以下の桁数を返します。 |

---

### name

トークンの名前を取得します。

ERC20標準関数です。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | トークン名を返します。 |

---

### symbol

トークンのシンボルを取得します。

ERC20標準関数です。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | トークンシンボルを返します。 |

---

### totalSupply

トークンの総供給量を取得します。

ERC20標準関数です。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result` | `string` | resultを返します。 |

---

</details>

<details>
<summary><strong>Mapping (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`allowance`](#allowance) | spenderがownerから使用を許可されているトークン量を取得します。 |
| [`balanceOf`](#balanceof) | 指定されたアカウントのトークン残高を取得します。 |

### allowance

spenderがownerから使用を許可されているトークン量を取得します。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `owner` | `any` | ✓ | 所有者のアドレスを指定します。 |
| `spender` | `any` | ✓ | トークンの使用を許可するアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result` | `string` | resultを返します。 |

---

### balanceOf

指定されたアカウントのトークン残高を取得します。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `owner` | `any` | ✓ | 所有者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result` | `string` | resultを返します。 |

---

</details>

<details>
<summary><strong>書き込み関数 (3)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`approve`](#approve) | spenderが指定された量のトークンを使用することを承認します。 |
| [`transfer`](#transfer) | 指定されたアドレスにトークンを転送します。 |
| [`transferFrom`](#transferfrom) | fromからtoへトークンを転送します。事前にallowanceが設定されている必要があります。 |

### approve

spenderが指定された量のトークンを使用することを承認します。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `spender` | `any` | ✓ | トークンの使用を許可するアドレスを指定します。 |
| `amount` | `any` | ✓ | トークン量を指定します（wei単位）。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 承認が成功した場合trueを返します。 |

**使用例:**

```solidity
contract.approve(spender, amount);
```

---

### transfer

指定されたアドレスにトークンを転送します。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `to` | `any` | ✓ | 送金先のアドレスを指定します。 |
| `amount` | `any` | ✓ | トークン量を指定します（wei単位）。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 送金が成功した場合trueを返します。 |

**使用例:**

```solidity
contract.transfer(to, amount);
```

---

### transferFrom

fromからtoへトークンを転送します。事前にallowanceが設定されている必要があります。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `from` | `any` | ✓ | 送金元のアドレスを指定します。 |
| `to` | `any` | ✓ | 送金先のアドレスを指定します。 |
| `amount` | `any` | ✓ | トークン量を指定します（wei単位）。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 送金が成功した場合trueを返します。 |

**使用例:**

```solidity
contract.transferFrom(from, to, amount);
```

---

</details>

<details>
<summary><strong>イベント (3)</strong></summary>

### events/Approval

トークンの使用許可が設定された時に発行されるイベントです。所有者、承認された使用者、および許可量が記録されます。

---

### events/Initialized

コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。

---

### events/Transfer

トークンが転送された時に発行されるイベントです。送金元、送金先、および転送量が記録されます。

---

</details>

<details>
<summary><strong>エラー (7)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/AllowanceOverflow` | 許可量がオーバーフローした時に返されるエラーです。許可量の上限を超えています。 |
| `errors/AllowanceUnderflow` | 許可量がアンダーフローした時に返されるエラーです。減算量が現在の許可量を超えています。 |
| `errors/InsufficientAllowance` | 許可量が不足している時に返されるエラーです。事前にapproveで十分な許可量を設定してください。 |
| `errors/InsufficientBalance` | 残高が不足している時に返されるエラーです。操作に必要な残高を確保してください。 |
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |
| `errors/TotalSupplyOverflow` | 総供給量がオーバーフローした時に返されるエラーです。 |

</details>

