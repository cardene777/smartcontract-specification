---
sidebar_position: 2
---

# StablecoinProxy

> **[📋 API仕様書を見る](/api/StablecoinProxy)**

## 概要

UUPS（Universal Upgradeable Proxy Standard）パターンを採用したプロキシコントラクトです。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Proxy`

## 主要機能

### アップグレード機能

UPGRADER_ROLEを持つアカウントがコントラクトの実装を更新可能。ストレージは保持されたまま、ロジックのみを差し替えられます。

### delegatecall転送

全ての呼び出しを実装コントラクトに転送。ユーザーはプロキシアドレスのみを意識すれば良く、アップグレード後も同じアドレスで利用できます。

## 関数一覧

<details>
<summary><strong>読み取り関数 (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getDictionary`](#getdictionary) | dictionary を取得します。 |
| [`getImplementation`](#getimplementation) | implementation を取得します。 |

### getDictionary

dictionary を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | Dictionaryを返します。 |

---

### getImplementation

implementation を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `functionSelector` | `any` | ✓ | 関数セレクタを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 実装コントラクトのアドレスを返します。 |

---

</details>

<details>
<summary><strong>書き込み関数 (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`upgradeDictionary`](#upgradedictionary) | upgradeDictionary |
| [`upgradeDictionaryAndCall`](#upgradedictionaryandcall) | upgradeDictionaryAndCall |

### upgradeDictionary

upgradeDictionary

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `newDictionary` | `any` | ✓ | 新しいDictionaryを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.upgradeDictionary(newDictionary);
```

---

### upgradeDictionaryAndCall

upgradeDictionaryAndCall

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `newDictionary` | `any` | ✓ | 新しいDictionaryを指定します。 |
| `data` | `any` | ✓ | コールデータを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.upgradeDictionaryAndCall(newDictionary, data);
```

---

</details>

<details>
<summary><strong>イベント (1)</strong></summary>

### events/DictionaryUpgraded

ディクショナリがアップグレードされた時に発行されるイベントです。新しいディクショナリアドレスが記録されます。

---

</details>

<details>
<summary><strong>エラー (4)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/AddressEmptyCode` | 指定されたアドレスにコードが存在しない時に返されるエラーです。 |
| `errors/FailedCall` | 外部呼び出しが失敗した時に返されるエラーです。 |
| `errors/ImplementationNotFound` | 実装が見つからない時に返されるエラーです。 |
| `errors/InvalidDictionary` | 無効なディクショナリが指定された時に返されるエラーです。 |

</details>

