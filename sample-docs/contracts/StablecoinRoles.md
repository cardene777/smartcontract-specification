---
sidebar_position: 9
---

# StablecoinRoles

> **[📋 API仕様書を見る](/api/StablecoinRoles)**

## 概要

システム全体で使用するロールの定義と管理を行います。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `StablecoinHelpers`

## 主要機能

### ロール定義

ISSUER_ROLE、BURNER_ROLE、PAUSER_ROLE、FREEZER_ROLE、ALLOWLIST_ROLE等の標準ロールを定義。

### ロール階層

各ロールには管理者ロールが設定され、階層的な権限管理を実現。

### Bank固有ロール

Bank単位のロール（BANK_ISSUER_ROLE等）も定義。グローバルロールとBank固有ロールを使い分けます。

## 関数一覧

<details>
<summary><strong>定数 (13)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`ALLOWLIST`](#allowlist) | ALLOWLIST_ROLE ロールの識別子を取得します。 |
| [`BANK`](#bank) | BANK_PAUSER_ROLE ロールの識別子を取得します。 |
| [`BANK`](#bank) | BANK_ROLE_PROPOSAL_EXPIRY 定数の値を取得します。 |
| [`BANK`](#bank) | BANK_ROLE_REQUIRED_APPROVALS 定数の値を取得します。 |
| [`BURNER`](#burner) | BURNER_ROLE ロールの識別子を取得します。 |
| [`DEVELOPER`](#developer) | DEVELOPER_ROLE ロールの識別子を取得します。 |
| [`FORCE`](#force) | FORCE_TRANSFER_ROLE ロールの識別子を取得します。 |
| [`ISSUER`](#issuer) | ISSUER_ROLE ロールの識別子を取得します。 |
| [`PAUSER`](#pauser) | PAUSER_ROLE ロールの識別子を取得します。 |
| [`PAYMENT`](#payment) | PAYMENT_PROVIDER_ROLE ロールの識別子を取得します。 |
| [`PROPOSAL`](#proposal) | PROPOSAL_EXPIRY 定数の値を取得します。 |
| [`TRUST`](#trust) | TRUST_BANK_ROLE ロールの識別子を取得します。 |
| [`UPGRADER`](#upgrader) | UPGRADER_ROLE ロールの識別子を取得します。 |

### ALLOWLIST

ALLOWLIST_ROLE ロールの識別子を取得します。

このロールは allowlist に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | ALLOWLISTロールのバイト列を返します。 |

---

### BANK

BANK_PAUSER_ROLE ロールの識別子を取得します。

このロールは bank pauser に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BANK_PAUSERロールのバイト列を返します。 |

---

### BANK

BANK_ROLE_PROPOSAL_EXPIRY 定数の値を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BANK_ROLE_PROPOSAL_EXPIRYの値を返します。 |

---

### BANK

BANK_ROLE_REQUIRED_APPROVALS 定数の値を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BANK_ROLE_REQUIRED_APPROVALSの値を返します。 |

---

### BURNER

BURNER_ROLE ロールの識別子を取得します。

このロールは burner に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BURNERロールのバイト列を返します。 |

---

### DEVELOPER

DEVELOPER_ROLE ロールの識別子を取得します。

このロールは developer に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | DEVELOPERロールのバイト列を返します。 |

---

### FORCE

FORCE_TRANSFER_ROLE ロールの識別子を取得します。

このロールは force transfer に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | FORCE_TRANSFERロールのバイト列を返します。 |

---

### ISSUER

ISSUER_ROLE ロールの識別子を取得します。

このロールは issuer に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | ISSUERロールのバイト列を返します。 |

---

### PAUSER

PAUSER_ROLE ロールの識別子を取得します。

このロールは pauser に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | PAUSERロールのバイト列を返します。 |

---

### PAYMENT

PAYMENT_PROVIDER_ROLE ロールの識別子を取得します。

このロールは payment provider に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | PAYMENT_PROVIDERロールのバイト列を返します。 |

---

### PROPOSAL

PROPOSAL_EXPIRY 定数の値を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | PROPOSAL_EXPIRYの値を返します。 |

---

### TRUST

TRUST_BANK_ROLE ロールの識別子を取得します。

このロールは trust bank に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | TRUST_BANKロールのバイト列を返します。 |

---

### UPGRADER

UPGRADER_ROLE ロールの識別子を取得します。

このロールは upgrader に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | UPGRADERロールのバイト列を返します。 |

---

</details>

<details>
<summary><strong>変数 (5)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`decimals`](#decimals) | トークンの小数点以下の桁数を取得します。 |
| [`name`](#name) | トークンの名前を取得します。 |
| [`paused`](#paused) | コントラクトが一時停止状態かどうかを確認します。 |
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

### paused

コントラクトが一時停止状態かどうかを確認します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 一時停止中の場合trueを返します。 |

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
<summary><strong>Mapping (11)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`allowance`](#allowance) | spenderがownerから使用を許可されているトークン量を取得します。 |
| [`balanceOf`](#balanceof) | 指定されたアカウントのトークン残高を取得します。 |
| [`getBankRole`](#getbankrole) | bank role を取得します。 |
| [`getBankRoleProposal`](#getbankroleproposal) | bank role proposal を取得します。 |
| [`getDualKey`](#getdualkey) | dual key を取得します。 |
| [`getKeyRotationProposal`](#getkeyrotationproposal) | key rotation proposal を取得します。 |
| [`getRoleAdmin`](#getroleadmin) | 指定されたロールの管理者ロールを取得します。 |
| [`hasBankRole`](#hasbankrole) | bank role を持っているかどうかを確認します。 |
| [`hasRole`](#hasrole) | 指定されたアカウントが指定されたロールを持っているかどうかを確認します。 |
| [`isBankPaused`](#isbankpaused) | 指定されたBankが一時停止状態かどうかを確認します。 |
| [`supportsInterface`](#supportsinterface) | 指定されたインターフェースをサポートしているかどうかを確認します。 |

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

### getBankRole

bank role を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `roleType` | `any` | ✓ | roleTypeを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 銀行ロールを返します。 |

---

### getBankRoleProposal

bank role proposal を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalType` | `string` | proposalTypeを返します。 |
| `targetAccount` | `string` | targetAccountを返します。 |
| `bankId` | `string` | bankIdを返します。 |
| `proposer` | `string` | proposerを返します。 |
| `approvalCount` | `string` | approvalCountを返します。 |
| `executed` | `string` | executedを返します。 |
| `createdAt` | `string` | createdAtを返します。 |
| `expiresAt` | `string` | expiresAtを返します。 |

---

### getDualKey

dual key を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `primaryKey` | `string` | primaryKeyを返します。 |
| `backupKey` | `string` | backupKeyを返します。 |

---

### getKeyRotationProposal

key rotation proposal を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `role` | `string` | roleを返します。 |
| `oldKey` | `string` | oldKeyを返します。 |
| `newKey` | `string` | newKeyを返します。 |
| `proposer` | `string` | proposerを返します。 |
| `approvalCount` | `string` | approvalCountを返します。 |
| `executed` | `string` | executedを返します。 |
| `createdAt` | `string` | createdAtを返します。 |

---

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

### hasBankRole

bank role を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |
| `roleType` | `any` | ✓ | roleTypeを指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankRoleを持っている場合trueを返します。 |

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
<summary><strong>読み取り関数 (14)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`canGrantRole`](#cangrantrole) | grant role が可能かどうかを確認します。 |
| [`canPauseBank`](#canpausebank) | pause bank が可能かどうかを確認します。 |
| [`getBankAllowlistRole`](#getbankallowlistrole) | bank allowlist role を取得します。 |
| [`getBankBurnerRole`](#getbankburnerrole) | bank burner role を取得します。 |
| [`getBankIssuerRole`](#getbankissuerrole) | bank issuer role を取得します。 |
| [`getBankPauserRole`](#getbankpauserrole) | bank pauser role を取得します。 |
| [`getRoleAdmins`](#getroleadmins) | role admins を取得します。 |
| [`hasApprovedBankRoleProposal`](#hasapprovedbankroleproposal) | approved bank role proposal を持っているかどうかを確認します。 |
| [`hasApprovedKeyRotation`](#hasapprovedkeyrotation) | approved key rotation を持っているかどうかを確認します。 |
| [`hasBankRoleApprovalByRole`](#hasbankroleapprovalbyrole) | bank role approval by role を持っているかどうかを確認します。 |
| [`isBankRole`](#isbankrole) | bank role かどうかを確認します。 |
| [`isDeveloper`](#isdeveloper) | developer かどうかを確認します。 |
| [`isTrustBank`](#istrustbank) | trust bank かどうかを確認します。 |
| [`requiresMultiSig`](#requiresmultisig) | requiresMultiSig |

### canGrantRole

grant role が可能かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | GrantRoleが可能な場合trueを返します。 |

---

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

### getBankAllowlistRole

bank allowlist role を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankAllowlistRoleを返します。 |

---

### getBankBurnerRole

bank burner role を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankBurnerRoleを返します。 |

---

### getBankIssuerRole

bank issuer role を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankIssuerRoleを返します。 |

---

### getBankPauserRole

bank pauser role を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankPauserRoleを返します。 |

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

### hasApprovedBankRoleProposal

approved bank role proposal を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |
| `approver` | `any` | ✓ | approverを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | ApprovedBankRoleProposalを持っている場合trueを返します。 |

---

### hasApprovedKeyRotation

approved key rotation を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |
| `approver` | `any` | ✓ | approverを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | ApprovedKeyRotationを持っている場合trueを返します。 |

---

### hasBankRoleApprovalByRole

bank role approval by role を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |
| `role` | `any` | ✓ | ロールの識別子を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankRoleApprovalByRoleを持っている場合trueを返します。 |

---

### isBankRole

bank role かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | BankRoleの場合trueを返します。 |

---

### isDeveloper

developer かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | Developerの場合trueを返します。 |

---

### isTrustBank

trust bank かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | TrustBankの場合trueを返します。 |

---

### requiresMultiSig

requiresMultiSig

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | requiresMultiSigの結果を返します。 |

---

</details>

<details>
<summary><strong>書き込み関数 (25)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`approve`](#approve) | spenderが指定された量のトークンを使用することを承認します。 |
| [`approveBankRoleProposal`](#approvebankroleproposal) | bank role proposal の提案を承認します。 |
| [`approveKeyRotation`](#approvekeyrotation) | key rotation の提案を承認します。 |
| [`cancelBankRoleProposal`](#cancelbankroleproposal) | cel bank role proposal が可能かどうかを確認します。 |
| [`cancelKeyRotation`](#cancelkeyrotation) | cel key rotation が可能かどうかを確認します。 |
| [`executeBankRoleProposal`](#executebankroleproposal) | bank role proposal の提案を実行します。 |
| [`executeKeyRotation`](#executekeyrotation) | key rotation の提案を実行します。 |
| [`grantBankPauserRole`](#grantbankpauserrole) | grantBankPauserRole |
| [`grantBankRole`](#grantbankrole) | grantBankRole |
| [`grantRole`](#grantrole) | 指定されたアカウントにロールを付与します。 |
| [`initializeDeveloperDualKey`](#initializedeveloperdualkey) | コントラクトを初期化します。 |
| [`initializeTrustBank`](#initializetrustbank) | コントラクトを初期化します。 |
| [`initializeTrustBankDualKey`](#initializetrustbankdualkey) | コントラクトを初期化します。 |
| [`pauseBank`](#pausebank) | 指定されたBankを一時停止します。 |
| [`proposeBankRoleGrant`](#proposebankrolegrant) | bank role grant の提案を作成します。 |
| [`proposeBankRoleRevoke`](#proposebankrolerevoke) | bank role revoke の提案を作成します。 |
| [`proposeKeyRotation`](#proposekeyrotation) | key rotation の提案を作成します。 |
| [`renounceRole`](#renouncerole) | 呼び出し元が持つロールを放棄します。 |
| [`revokeBankPauserRole`](#revokebankpauserrole) | revokeBankPauserRole |
| [`revokeBankRole`](#revokebankrole) | revokeBankRole |
| [`revokeRole`](#revokerole) | 指定されたアカウントからロールを取り消します。 |
| [`setMultiSigRequired`](#setmultisigrequired) | setMultiSigRequired |
| [`transfer`](#transfer) | 指定されたアドレスにトークンを転送します。 |
| [`transferFrom`](#transferfrom) | fromからtoへトークンを転送します。事前にallowanceが設定されている必要があります。 |
| [`unpauseBank`](#unpausebank) | 指定されたBankの一時停止を解除します。 |

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

### approveBankRoleProposal

bank role proposal の提案を承認します。

承認者の一人として提案を承認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.approveBankRoleProposal(proposalId);
```

---

### approveKeyRotation

key rotation の提案を承認します。

承認者の一人として提案を承認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.approveKeyRotation(proposalId);
```

---

### cancelBankRoleProposal

cel bank role proposal が可能かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.cancelBankRoleProposal(proposalId);
```

---

### cancelKeyRotation

cel key rotation が可能かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.cancelKeyRotation(proposalId);
```

---

### executeBankRoleProposal

bank role proposal の提案を実行します。

必要な承認数が揃った後に実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.executeBankRoleProposal(proposalId);
```

---

### executeKeyRotation

key rotation の提案を実行します。

必要な承認数が揃った後に実行可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.executeKeyRotation(proposalId);
```

---

### grantBankPauserRole

grantBankPauserRole

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.grantBankPauserRole(account, bankId);
```

---

### grantBankRole

grantBankRole

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.grantBankRole(account, bankId);
```

---

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

### initializeDeveloperDualKey

コントラクトを初期化します。

プロキシ経由で一度だけ呼び出し可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `primaryKey` | `any` | ✓ | primaryKeyを指定します。 |
| `backupKey` | `any` | ✓ | backupKeyを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.initializeDeveloperDualKey(primaryKey, backupKey);
```

---

### initializeTrustBank

コントラクトを初期化します。

プロキシ経由で一度だけ呼び出し可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `primaryKey` | `any` | ✓ | primaryKeyを指定します。 |
| `backupKey` | `any` | ✓ | backupKeyを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.initializeTrustBank(primaryKey, backupKey);
```

---

### initializeTrustBankDualKey

コントラクトを初期化します。

プロキシ経由で一度だけ呼び出し可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `primaryKey` | `any` | ✓ | primaryKeyを指定します。 |
| `backupKey` | `any` | ✓ | backupKeyを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.initializeTrustBankDualKey(primaryKey, backupKey);
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

### proposeBankRoleGrant

bank role grant の提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `targetAccount` | `any` | ✓ | targetAccountを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.proposeBankRoleGrant(targetAccount, bankId);
```

---

### proposeBankRoleRevoke

bank role revoke の提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `targetAccount` | `any` | ✓ | targetAccountを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.proposeBankRoleRevoke(targetAccount, bankId);
```

---

### proposeKeyRotation

key rotation の提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `oldKey` | `any` | ✓ | oldKeyを指定します。 |
| `newKey` | `any` | ✓ | 新しいKeyを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.proposeKeyRotation(role, oldKey, newKey);
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

### revokeBankPauserRole

revokeBankPauserRole

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.revokeBankPauserRole(account, bankId);
```

---

### revokeBankRole

revokeBankRole

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `bankId` | `any` | ✓ | 銀行のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.revokeBankRole(account, bankId);
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

### setMultiSigRequired

setMultiSigRequired

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `required` | `any` | ✓ | 必要な承認数を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.setMultiSigRequired(role, required);
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
<summary><strong>イベント (28)</strong></summary>

### events/AccountAllowed

アカウントが許可リストに追加された時に発行されるイベントです。許可されたアカウントが記録されます。

---

### events/AccountDisallowed

アカウントが許可リストから削除された時に発行されるイベントです。削除されたアカウントが記録されます。

---

### events/Approval

トークンの使用許可が設定された時に発行されるイベントです。所有者、承認された使用者、および許可量が記録されます。

---

### events/BankPaused

銀行が一時停止された時に発行されるイベントです。銀行IDと一時停止を実行したアカウントが記録されます。

---

### events/BankRoleAdminSet

銀行ロールの管理者が設定された時に発行されるイベントです。銀行ID、ロール、管理者ロールが記録されます。

---

### events/BankRoleGranted

銀行スコープのロールがアカウントに付与された時に発行されるイベントです。銀行ID、ロール、アカウントが記録されます。

---

### events/BankRoleProposalApproved

銀行ロールの提案が承認された時に発行されるイベントです。提案ID、承認者が記録されます。

---

### events/BankRoleProposalCancelled

銀行ロールの提案がキャンセルされた時に発行されるイベントです。提案IDが記録されます。

---

### events/BankRoleProposalCreated

銀行ロールの提案が作成された時に発行されるイベントです。提案ID、銀行ID、提案者が記録されます。

---

### events/BankRoleProposalExecuted

銀行ロールの提案が実行された時に発行されるイベントです。提案IDが記録されます。

---

### events/BankRoleRevoked

銀行スコープのロールがアカウントから取り消された時に発行されるイベントです。銀行ID、ロール、アカウントが記録されます。

---

### events/BankUnpaused

銀行の一時停止が解除された時に発行されるイベントです。銀行IDと解除を実行したアカウントが記録されます。

---

### events/DualKeyInitialized

デュアルキーが初期化された時に発行されるイベントです。アドレスと2つのキーが記録されます。

---

### events/Initialized

コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。

---

### events/KeyRotationApproved

キーローテーションが承認された時に発行されるイベントです。提案ID、承認者が記録されます。

---

### events/KeyRotationCancelled

キーローテーションがキャンセルされた時に発行されるイベントです。提案IDが記録されます。

---

### events/KeyRotationExecuted

キーローテーションが実行された時に発行されるイベントです。古いキーと新しいキーが記録されます。

---

### events/KeyRotationProposed

キーローテーションが提案された時に発行されるイベントです。提案ID、提案者、新しいキーが記録されます。

---

### events/MultiSigRequirementSet

マルチシグ要件が設定された時に発行されるイベントです。ロールと必要承認数が記録されます。

---

### events/Paused

コントラクトが一時停止された時に発行されるイベントです。一時停止を実行したアカウントが記録されます。

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

### events/Transfer

トークンが転送された時に発行されるイベントです。送金元、送金先、および転送量が記録されます。

---

### events/TransferRouted

銀行経由でトークンが転送された時に発行されるイベントです。送金元銀行、送金先銀行、金額が記録されます。

---

### events/Unpaused

コントラクトの一時停止が解除された時に発行されるイベントです。解除を実行したアカウントが記録されます。

---

</details>

<details>
<summary><strong>エラー (51)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/AccessControlBadConfirmation` | アクセス制御の確認が失敗した時に返されるエラーです。 |
| `errors/AccessControlMultiSig_RequiresMultiSigAdmin` | マルチシグ管理者権限が必要な操作で権限がない時に返されるエラーです。 |
| `errors/AccessControlUnauthorizedAccount` | 権限のないアカウントが操作を試みた時に返されるエラーです。必要なロールを持っていません。 |
| `errors/AllowanceOverflow` | 許可量がオーバーフローした時に返されるエラーです。許可量の上限を超えています。 |
| `errors/AllowanceUnderflow` | 許可量がアンダーフローした時に返されるエラーです。減算量が現在の許可量を超えています。 |
| `errors/AmountZero` | 金額にゼロが指定された時に返されるエラーです。正の金額を指定する必要があります。 |
| `errors/BankExists` | 既に存在する銀行を作成しようとした時に返されるエラーです。 |
| `errors/BankInactive` | 銀行が非アクティブ状態の時に返されるエラーです。銀行をアクティブ化してください。 |
| `errors/BankNotFound` | 指定された銀行が存在しない時に返されるエラーです。銀行IDを確認してください。 |
| `errors/BankPauser_BankAlreadyPaused` | 既に一時停止中の銀行を一時停止しようとした時に返されるエラーです。 |
| `errors/BankPauser_BankNotPaused` | 一時停止されていない銀行の一時停止を解除しようとした時に返されるエラーです。 |
| `errors/BankPauser_InvalidBankId` | 無効な銀行IDが指定された時に返されるエラーです。 |
| `errors/BankPauser_UnauthorizedBankPauser` | 銀行のポーズ権限がない時に返されるエラーです。 |
| `errors/BankScopedRoles_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/BankScopedRoles_InvalidBankId` | 無効な銀行IDが指定された時に返されるエラーです。 |
| `errors/BankScopedRoles_UnauthorizedRoleAdmin` | ロール管理者権限がない時に返されるエラーです。 |
| `errors/CapBelowOutstanding` | キャップが既存の発行量を下回った時に返されるエラーです。 |
| `errors/CapExceeded` | 銀行のキャップを超過した時に返されるエラーです。キャップ内での操作が必要です。 |
| `errors/CapZero` | キャップがゼロに設定されようとした時に返されるエラーです。正のキャップを指定してください。 |
| `errors/DualKeyMultiSig_AlreadyApproved` | キーローテーション提案が既に承認されている時に返されるエラーです。 |
| `errors/DualKeyMultiSig_AlreadyInitialized` | デュアルキーが既に初期化されている時に返されるエラーです。 |
| `errors/DualKeyMultiSig_InsufficientApprovals` | キーローテーションの承認数が不足している時に返されるエラーです。 |
| `errors/DualKeyMultiSig_InvalidAddress` | 無効なアドレスがデュアルキーに指定された時に返されるエラーです。 |
| `errors/DualKeyMultiSig_InvalidKeyReplacement` | 無効なキー交換が試みられた時に返されるエラーです。 |
| `errors/DualKeyMultiSig_NotAuthorized` | デュアルキー操作の権限がない時に返されるエラーです。 |
| `errors/DualKeyMultiSig_NotInitialized` | デュアルキーが初期化されていない時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposalAlreadyExecuted` | キーローテーション提案が既に実行されている時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposalExpired` | キーローテーション提案の有効期限が切れた時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposalNotFound` | キーローテーション提案が存在しない時に返されるエラーです。 |
| `errors/DualKeyMultiSig_ProposerCannotApprove` | 提案者が自身の提案を承認しようとした時に返されるエラーです。 |
| `errors/EnforcedPause` | コントラクトが一時停止中に操作を試みた時に返されるエラーです。 |
| `errors/ExpectedPause` | コントラクトが一時停止状態であることが期待される操作で、一時停止されていない時に返されるエラーです。 |
| `errors/InsufficientAllowance` | 許可量が不足している時に返されるエラーです。事前にapproveで十分な許可量を設定してください。 |
| `errors/InsufficientBalance` | 残高が不足している時に返されるエラーです。操作に必要な残高を確保してください。 |
| `errors/InsufficientBucket` | バケット残高が不足している時に返されるエラーです。 |
| `errors/InvalidAddress` | 無効なアドレス（ゼロアドレスや不正なアドレス形式）が指定された時に返されるエラーです。 |
| `errors/InvalidBucket` | 無効なバケットが指定された時に返されるエラーです。 |
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/InvalidName` | 無効な名前が指定された時に返されるエラーです。 |
| `errors/InvalidReassignment` | 無効なバケット再割り当てが試みられた時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_AdminRoleAlreadyExists` | 既に存在する管理者ロールを追加しようとした時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_AdminRoleNotFound` | 管理者ロールが見つからない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_MissingRole` | 必要なロールを持っていない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_NoAdminRole` | 管理者ロールが存在しない時に返されるエラーです。 |
| `errors/NotAllowed` | アカウントが許可リストに含まれていない時に返されるエラーです。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |
| `errors/ReentrancyGuardReentrantCall` | 再入呼び出しが検出された時に返されるエラーです。同一関数への再帰呼び出しは禁止されています。 |
| `errors/Stablecoin_InvalidAddress` | ステーブルコインで無効なアドレスが指定された時に返されるエラーです。 |
| `errors/TotalSupplyOverflow` | 総供給量がオーバーフローした時に返されるエラーです。 |
| `errors/UnauthorizedIssuer` | 銀行の発行者権限がない時に返されるエラーです。 |

</details>

