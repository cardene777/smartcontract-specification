---
sidebar_position: 11
---

# BankScopedRoles

> **[📋 API仕様書を見る](/api/BankScopedRoles)**

## 概要

Bank単位でのロール管理を実現します。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `Initializable`

## 主要機能

### Bank固有ロール

各BankにISSUER、BURNER、PAUSER、ALLOWLIST等のロールを個別に割り当て。

### ロール提案・承認

Bankロールの変更は提案→承認のフローで実行。複数の承認者による確認を必要とします。

## 関数一覧

<details>
<summary><strong>定数 (5)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`BANK`](#bank) | BANK_ROLE_PROPOSAL_EXPIRY 定数の値を取得します。 |
| [`BANK`](#bank) | BANK_ROLE_REQUIRED_APPROVALS 定数の値を取得します。 |
| [`DEVELOPER`](#developer) | DEVELOPER_ROLE ロールの識別子を取得します。 |
| [`PROPOSAL`](#proposal) | PROPOSAL_EXPIRY 定数の値を取得します。 |
| [`TRUST`](#trust) | TRUST_BANK_ROLE ロールの識別子を取得します。 |

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

### DEVELOPER

DEVELOPER_ROLE ロールの識別子を取得します。

このロールは developer に関連する操作の権限を管理します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | DEVELOPERロールのバイト列を返します。 |

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

</details>

<details>
<summary><strong>Mapping (8)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getBankRole`](#getbankrole) | bank role を取得します。 |
| [`getBankRoleProposal`](#getbankroleproposal) | bank role proposal を取得します。 |
| [`getDualKey`](#getdualkey) | dual key を取得します。 |
| [`getKeyRotationProposal`](#getkeyrotationproposal) | key rotation proposal を取得します。 |
| [`getRoleAdmin`](#getroleadmin) | 指定されたロールの管理者ロールを取得します。 |
| [`hasBankRole`](#hasbankrole) | bank role を持っているかどうかを確認します。 |
| [`hasRole`](#hasrole) | 指定されたアカウントが指定されたロールを持っているかどうかを確認します。 |
| [`supportsInterface`](#supportsinterface) | 指定されたインターフェースをサポートしているかどうかを確認します。 |

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
<summary><strong>読み取り関数 (13)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`canGrantRole`](#cangrantrole) | grant role が可能かどうかを確認します。 |
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
<summary><strong>書き込み関数 (15)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`approveBankRoleProposal`](#approvebankroleproposal) | bank role proposal の提案を承認します。 |
| [`approveKeyRotation`](#approvekeyrotation) | key rotation の提案を承認します。 |
| [`cancelBankRoleProposal`](#cancelbankroleproposal) | cel bank role proposal が可能かどうかを確認します。 |
| [`cancelKeyRotation`](#cancelkeyrotation) | cel key rotation が可能かどうかを確認します。 |
| [`executeBankRoleProposal`](#executebankroleproposal) | bank role proposal の提案を実行します。 |
| [`executeKeyRotation`](#executekeyrotation) | key rotation の提案を実行します。 |
| [`grantRole`](#grantrole) | 指定されたアカウントにロールを付与します。 |
| [`initializeDeveloperDualKey`](#initializedeveloperdualkey) | コントラクトを初期化します。 |
| [`initializeTrustBankDualKey`](#initializetrustbankdualkey) | コントラクトを初期化します。 |
| [`proposeBankRoleGrant`](#proposebankrolegrant) | bank role grant の提案を作成します。 |
| [`proposeBankRoleRevoke`](#proposebankrolerevoke) | bank role revoke の提案を作成します。 |
| [`proposeKeyRotation`](#proposekeyrotation) | key rotation の提案を作成します。 |
| [`renounceRole`](#renouncerole) | 呼び出し元が持つロールを放棄します。 |
| [`revokeRole`](#revokerole) | 指定されたアカウントからロールを取り消します。 |
| [`setMultiSigRequired`](#setmultisigrequired) | setMultiSigRequired |

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

</details>

<details>
<summary><strong>イベント (19)</strong></summary>

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
<summary><strong>エラー (25)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/AccessControlBadConfirmation` | アクセス制御の確認が失敗した時に返されるエラーです。 |
| `errors/AccessControlMultiSig_RequiresMultiSigAdmin` | マルチシグ管理者権限が必要な操作で権限がない時に返されるエラーです。 |
| `errors/AccessControlUnauthorizedAccount` | 権限のないアカウントが操作を試みた時に返されるエラーです。必要なロールを持っていません。 |
| `errors/BankScopedRoles_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/BankScopedRoles_InvalidBankId` | 無効な銀行IDが指定された時に返されるエラーです。 |
| `errors/BankScopedRoles_UnauthorizedRoleAdmin` | ロール管理者権限がない時に返されるエラーです。 |
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
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/MultiAdminAccessControl_AdminRoleAlreadyExists` | 既に存在する管理者ロールを追加しようとした時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_AdminRoleNotFound` | 管理者ロールが見つからない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_MissingRole` | 必要なロールを持っていない時に返されるエラーです。 |
| `errors/MultiAdminAccessControl_NoAdminRole` | 管理者ロールが存在しない時に返されるエラーです。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |
| `errors/ReentrancyGuardReentrantCall` | 再入呼び出しが検出された時に返されるエラーです。同一関数への再帰呼び出しは禁止されています。 |

</details>

