---
sidebar_position: 8
---

# BankPausable

> **[📋 API仕様書を見る](/api/BankPausable)**

## 概要

Bank単位での一時停止機能を提供します。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Initializable`

## 主要機能

### Bank別一時停止

BANK_PAUSER_ROLEを持つアカウントが特定のBankのみを一時停止。他のBankへの影響を最小限に抑えます。

### グローバル一時停止

PAUSER_ROLEによる全体の一時停止も可能。緊急時に全操作を停止できます。

## 関数一覧

<details>
<summary><strong>定数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`BANK`](#bank) | BANK_PAUSER_ROLE ロールの識別子を取得します。 |

### BANK

BANK_PAUSER_ROLE ロールの識別子を取得します。

このロールは bank pauser に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BANK_PAUSERロールのバイト列を返します。 |

---

</details>

<details>
<summary><strong>Mapping (4)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getRoleAdmin`](#getroleadmin) | 指定されたロールの管理者ロールを取得します。 |
| [`hasRole`](#hasrole) | 指定されたアカウントが指定されたロールを持っているかどうかを確認します。 |
| [`isBankPaused`](#isbankpaused) | 指定されたBankが一時停止状態かどうかを確認します。 |
| [`supportsInterface`](#supportsinterface) | 指定されたインターフェースをサポートしているかどうかを確認します。 |

### getRoleAdmin

指定されたロールの管理者ロールを取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | ロールの管理者ロールを返します。 |

---

### hasRole

指定されたアカウントが指定されたロールを持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 指定されたロールを持っている場合trueを返します。 |

---

### isBankPaused

指定されたBankが一時停止状態かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 銀行が一時停止中の場合trueを返します。 |

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
<summary><strong>読み取り関数 (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`canPauseBank`](#canpausebank) | pause bank が可能かどうかを確認します。 |
| [`getRoleAdmins`](#getroleadmins) | role admins を取得します。 |

### canPauseBank

pause bank が可能かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | PauseBankが可能な場合trueを返します。 |

---

### getRoleAdmins

role admins を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | RoleAdminsを返します。 |

---

</details>

<details>
<summary><strong>書き込み関数 (5)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`grantRole`](#grantrole) | 指定されたアカウントにロールを付与します。 |
| [`pauseBank`](#pausebank) | 指定されたBankを一時停止します。 |
| [`renounceRole`](#renouncerole) | 呼び出し元が持つロールを放棄します。 |
| [`revokeRole`](#revokerole) | 指定されたアカウントからロールを取り消します。 |
| [`unpauseBank`](#unpausebank) | 指定されたBankの一時停止を解除します。 |

### grantRole

指定されたアカウントにロールを付与します。

ロールの管理者のみが実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.grantRole(role, account);
```

---

### pauseBank

指定されたBankを一時停止します。

BANK_PAUSER_ROLEまたは該当Bankの一時停止権限を持つアカウントのみが実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.pauseBank(bankId);
```

---

### renounceRole

呼び出し元が持つロールを放棄します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `callerConfirmation` | `any` | ✓ | callerConfirmationを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.renounceRole(role, callerConfirmation);
```

---

### revokeRole

指定されたアカウントからロールを取り消します。

ロールの管理者のみが実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.revokeRole(role, account);
```

---

### unpauseBank

指定されたBankの一時停止を解除します。

BANK_PAUSER_ROLEまたは該当Bankの一時停止権限を持つアカウントのみが実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.unpauseBank(bankId);
```

---

</details>

<details>
<summary><strong>イベント (8)</strong></summary>

### events/BankPaused

銀行が一時停止された時に発行されるイベントです。銀行IDと一時停止を実行したアカウントが記録されます。

---

### events/BankUnpaused

銀行の一時停止が解除された時に発行されるイベントです。銀行IDと解除を実行したアカウントが記録されます。

---

### events/Initialized

コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。

---

### events/RoleAdminAdded

ロール管理者が追加された時に発行されるイベントです。ロールと管理者が記録されます。

---

### events/RoleAdminChanged

ロールの管理者ロールが変更された時に発行されるイベントです。対象ロール、以前の管理者ロール、新しい管理者ロールが記録されます。

---

### events/RoleAdminRemoved

ロール管理者が削除された時に発行されるイベントです。ロールと管理者が記録されます。

---

### events/RoleGranted

アカウントにロールが付与された時に発行されるイベントです。ロール、付与されたアカウント、付与したアカウントが記録されます。

---

### events/RoleRevoked

アカウントからロールが取り消された時に発行されるイベントです。ロール、取り消されたアカウント、取り消したアカウントが記録されます。

---

</details>

<details>
<summary><strong>エラー (13)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/AccessControlBadConfirmation` | アクセス制御の確認が失敗した時に返されるエラーです。 |
| `errors/AccessControlUnauthorizedAccount` | 権限のないアカウントが操作を試みた時に返されるエラーです。必要なロールを持っていません。 |
| `errors/BankPauser_BankAlreadyPaused` | 既に一時停止中の銀行を一時停止しようとした時に返されるエラーです。 |
| `errors/BankPauser_BankNotPaused` | 一時停止されていない銀行の一時停止を解除しようとした時に返されるエラーです。 |
| `errors/BankPauser_InvalidBankId` | 無効な銀行IDが指定された時に返されるエラーです。 |
| `errors/BankPauser_UnauthorizedBankPauser` | 銀行のポーズ権限がない時に返されるエラーです。 |
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/MultiAdminAccessControl_AdminRoleAlreadyExists` | 既に存在する管理者ロールを追加しようとした時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_AdminRoleNotFound` | 管理者ロールが見つからない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_MissingRole` | 必要なロールを持っていない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_NoAdminRole` | 管理者ロールが存在しない時に返されるエラーです。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |

</details>

