---
sidebar_position: 18
---

# Dictionary

> **[📋 API仕様書を見る](/api/Dictionary)**

## 概要

キーバリュー形式のオンチェーンデータストアです。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Ownable`

## 主要機能

### データ保存

bytes32キーに対して任意のbytesデータを保存可能。

### アクセス制御

データの書き込みには適切な権限が必要。読み取りは誰でも可能。

## 関数一覧

<details>
<summary><strong>変数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`owner`](#owner) | owner |

### owner

owner

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 所有者のアドレスを返します。 |

---

</details>

<details>
<summary><strong>Mapping (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`implementations`](#implementations) | implementations |
| [`supportsInterface`](#supportsinterface) | 指定されたインターフェースをサポートしているかどうかを確認します。 |

### implementations

implementations

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `functionSelector` | `any` | ✓ | 関数セレクタを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `implementation` | `string` | implementationを返します。 |

---

### supportsInterface

指定されたインターフェースをサポートしているかどうかを確認します。

ERC165標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `interfaceId` | `any` | ✓ | インターフェースIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | インターフェースをサポートしている場合trueを返します。 |

---

</details>

<details>
<summary><strong>読み取り関数 (5)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`functionSelectorList`](#functionselectorlist) | functionSelectorList |
| [`getFunctionCount`](#getfunctioncount) | function count を取得します。 |
| [`getImplementation`](#getimplementation) | implementation を取得します。 |
| [`getImplementationByIndex`](#getimplementationbyindex) | implementation by index を取得します。 |
| [`supportsInterfaces`](#supportsinterfaces) | supportsInterfaces |

### functionSelectorList

functionSelectorList

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `param` | `any` | ✓ | paramを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | functionSelectorListの結果を返します。 |

---

### getFunctionCount

function count を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `count` | `string` | countを返します。 |

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
| `implementation` | `string` | implementationを返します。 |

---

### getImplementationByIndex

implementation by index を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `index` | `any` | ✓ | インデックスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `functionSelector` | `string` | functionSelectorを返します。 |
| `implementation` | `string` | implementationを返します。 |

---

### supportsInterfaces

supportsInterfaces

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | supportsInterfacesの結果を返します。 |

---

</details>

<details>
<summary><strong>書き込み関数 (6)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`cleanupFunctionList`](#cleanupfunctionlist) | cleanupFunctionList |
| [`removeImplementation`](#removeimplementation) | removeImplementation |
| [`renounceOwnership`](#renounceownership) | renounceOwnership |
| [`setImplementation`](#setimplementation) | setImplementation |
| [`setImplementations`](#setimplementations) | setImplementations |
| [`transferOwnership`](#transferownership) | transferOwnership |

### cleanupFunctionList

cleanupFunctionList

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.cleanupFunctionList();
```

---

### removeImplementation

removeImplementation

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `functionSelector` | `any` | ✓ | 関数セレクタを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.removeImplementation(functionSelector);
```

---

### renounceOwnership

renounceOwnership

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.renounceOwnership();
```

---

### setImplementation

setImplementation

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `functionSelector` | `any` | ✓ | 関数セレクタを指定します。 |
| `implementation` | `any` | ✓ | 実装コントラクトのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.setImplementation(functionSelector, implementation);
```

---

### setImplementations

setImplementations

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `functionSelectors` | `any` | ✓ | functionSelectorsを指定します。 |
| `implementationAddresses` | `any` | ✓ | implementationAddressesを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.setImplementations(functionSelectors, implementationAddresses);
```

---

### transferOwnership

transferOwnership

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `newOwner` | `any` | ✓ | 新しい所有者となるアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.transferOwnership(newOwner);
```

---

</details>

<details>
<summary><strong>イベント (3)</strong></summary>

### events/ImplementationRemoved

実装コントラクトが削除された時に発行されるイベントです。関数セレクタが記録されます。

---

### events/ImplementationUpgraded

実装コントラクトがアップグレードされた時に発行されるイベントです。関数セレクタと新しい実装が記録されます。

---

### events/OwnershipTransferred

所有権が移転された時に発行されるイベントです。以前の所有者と新しい所有者が記録されます。

---

</details>

<details>
<summary><strong>エラー (4)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/FunctionSelectorNotFound` | 関数セレクタが見つからない時に返されるエラーです。 |
| `errors/InvalidImplementation` | 無効な実装が指定された時に返されるエラーです。 |
| `errors/OwnableInvalidOwner` | 無効な所有者が指定された時に返されるエラーです。 |
| `errors/OwnableUnauthorizedAccount` | 所有者ではないアカウントが所有者専用の操作を試みた時に返されるエラーです。 |

</details>

