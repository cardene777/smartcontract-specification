---
sidebar_position: 12
---

# MultiAdminAccessControl

> **[📋 API仕様書を見る](/api/MultiAdminAccessControl)**

## 概要

複数管理者による承認が必要なアクセス制御を実装します。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Initializable`

## 主要機能

### 複数管理者

単一のDEFAULT_ADMIN_ROLEではなく、複数のアドレスが管理者として登録可能。

### 承認フロー

重要な操作には複数の管理者からの承認が必要。単独での操作を防止します。

## 関数一覧

<details>
<summary><strong>Mapping (3)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getRoleAdmin`](#getroleadmin) | 指定されたロールの管理者ロールを取得します。 |
| [`hasRole`](#hasrole) | 指定されたアカウントが指定されたロールを持っているかどうかを確認します。 |
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
<summary><strong>読み取り関数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getRoleAdmins`](#getroleadmins) | role admins を取得します。 |

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
<summary><strong>書き込み関数 (3)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`grantRole`](#grantrole) | 指定されたアカウントにロールを付与します。 |
| [`renounceRole`](#renouncerole) | 呼び出し元が持つロールを放棄します。 |
| [`revokeRole`](#revokerole) | 指定されたアカウントからロールを取り消します。 |

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

</details>

<details>
<summary><strong>イベント (6)</strong></summary>

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
<summary><strong>エラー (9)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/AccessControlBadConfirmation` | アクセス制御の確認が失敗した時に返されるエラーです。 |
| `errors/AccessControlUnauthorizedAccount` | 権限のないアカウントが操作を試みた時に返されるエラーです。必要なロールを持っていません。 |
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/MultiAdminAccessControl_AdminRoleAlreadyExists` | 既に存在する管理者ロールを追加しようとした時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_AdminRoleNotFound` | 管理者ロールが見つからない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_MissingRole` | 必要なロールを持っていない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_NoAdminRole` | 管理者ロールが存在しない時に返されるエラーです。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |

</details>

