---
sidebar_position: 16
---

# RoleMultiSigManager

> **[📋 API仕様書を見る](/api/RoleMultiSigManager)**

## 概要

ロール変更の提案・承認フローを管理します。

### 継承関係

このコントラクトは以下のコントラクトを継承しています：

- `MultiSigWallet`

## 主要機能

### ロール変更提案

ロールの付与・剥奪を提案として作成。提案には有効期限があります。

### 承認管理

複数の承認者からの承認を収集。必要承認数に達すると実行可能になります。

### 提案のキャンセル

不要になった提案をキャンセル可能。有効期限切れの提案も自動的に無効化。

## 関数一覧

<details>
<summary><strong>定数 (1)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`DEFAULT`](#default) | DEFAULT_PROPOSAL_DURATION 定数の値を取得します。 |

### DEFAULT

DEFAULT_PROPOSAL_DURATION 定数の値を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | DEFAULT_PROPOSAL_DURATIONの値を返します。 |

---

</details>

<details>
<summary><strong>変数 (2)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`requiredApprovals`](#requiredapprovals) | requiredApprovals |
| [`targetContract`](#targetcontract) | targetContract |

### requiredApprovals

requiredApprovals

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | requiredApprovalsの結果を返します。 |

---

### targetContract

targetContract

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | targetContractの結果を返します。 |

---

</details>

<details>
<summary><strong>Mapping (3)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getProposal`](#getproposal) | proposal を取得します。 |
| [`getRoleAdmin`](#getroleadmin) | 指定されたロールの管理者ロールを取得します。 |
| [`isSigner`](#issigner) | signer かどうかを確認します。 |

### getProposal

proposal を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 提案情報を返します。 |

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

### isSigner

signer かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | Signerの場合trueを返します。 |

---

</details>

<details>
<summary><strong>読み取り関数 (4)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`getSignerCount`](#getsignercount) | signer count を取得します。 |
| [`getSigners`](#getsigners) | signers を取得します。 |
| [`hasApproved`](#hasapproved) | approved を持っているかどうかを確認します。 |
| [`requiresMultiSig`](#requiresmultisig) | requiresMultiSig |

### getSignerCount

signer count を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | Signerの数を返します。 |

---

### getSigners

signers を取得します。

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 署名者アドレスの配列を返します。 |

---

### hasApproved

approved を持っているかどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |
| `signer` | `any` | ✓ | 署名者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `result0` | `string` | 承認済みの場合trueを返します。 |

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
<summary><strong>書き込み関数 (16)</strong></summary>

| 関数名 | 説明 |
|--------|------|
| [`addSigner`](#addsigner) | addSigner |
| [`approve`](#approve) | spenderが指定された量のトークンを使用することを承認します。 |
| [`cancel`](#cancel) | cel が可能かどうかを確認します。 |
| [`changeRequiredApprovals`](#changerequiredapprovals) | changeRequiredApprovals |
| [`execute`](#execute) | 提案を実行します。 |
| [`grantRoleDirect`](#grantroledirect) | grantRoleDirect |
| [`initialize`](#initialize) | コントラクトを初期化します。 |
| [`initialize`](#initialize) | コントラクトを初期化します。 |
| [`propose`](#propose) | 提案を作成します。 |
| [`proposeGrantRole`](#proposegrantrole) | grant role の提案を作成します。 |
| [`proposeRevokeRole`](#proposerevokerole) | revoke role の提案を作成します。 |
| [`removeSigner`](#removesigner) | removeSigner |
| [`revokeApproval`](#revokeapproval) | revokeApproval |
| [`revokeRoleDirect`](#revokeroledirect) | revokeRoleDirect |
| [`setRequiresMultiSig`](#setrequiresmultisig) | setRequiresMultiSig |
| [`setTargetContract`](#settargetcontract) | setTargetContract |

### addSigner

addSigner

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signer` | `any` | ✓ | 署名者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.addSigner(signer);
```

---

### approve

spenderが指定された量のトークンを使用することを承認します。

ERC20標準関数です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.approve(proposalId);
```

---

### cancel

cel が可能かどうかを確認します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.cancel(proposalId);
```

---

### changeRequiredApprovals

changeRequiredApprovals

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `newRequired` | `any` | ✓ | 新しいRequiredを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.changeRequiredApprovals(newRequired);
```

---

### execute

提案を実行します。

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
contract.execute(proposalId);
```

---

### grantRoleDirect

grantRoleDirect

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
contract.grantRoleDirect(role, account);
```

---

### initialize

コントラクトを初期化します。

プロキシ経由で一度だけ呼び出し可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signers_` | `any` | ✓ | signers_を指定します。 |
| `requiredApprovals_` | `any` | ✓ | 必要な承認数を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.initialize(signers_, requiredApprovals_);
```

---

### initialize

コントラクトを初期化します。

プロキシ経由で一度だけ呼び出し可能です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signers_` | `any` | ✓ | signers_を指定します。 |
| `requiredApprovals_` | `any` | ✓ | 必要な承認数を指定します。 |
| `targetContract_` | `any` | ✓ | targetContract_を指定します。 |
| `sensitiveRoles_` | `any` | ✓ | sensitiveRoles_を指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.initialize(signers_, requiredApprovals_, targetContract_, sensitiveRoles_);
```

---

### propose

提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `target` | `any` | ✓ | 対象コントラクトのアドレスを指定します。 |
| `value` | `any` | ✓ | 値を指定します。 |
| `data` | `any` | ✓ | コールデータを指定します。 |
| `duration` | `any` | ✓ | durationを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.propose(target, value, data, duration);
```

---

### proposeGrantRole

grant role の提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `duration` | `any` | ✓ | durationを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.proposeGrantRole(role, account, duration);
```

---

### proposeRevokeRole

revoke role の提案を作成します。

マルチシグ承認が必要な操作です。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `role` | `any` | ✓ | ロールの識別子を指定します。 |
| `account` | `any` | ✓ | 対象アカウントのアドレスを指定します。 |
| `duration` | `any` | ✓ | durationを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|
| `proposalId` | `string` | proposalIdを返します。 |

**使用例:**

```solidity
contract.proposeRevokeRole(role, account, duration);
```

---

### removeSigner

removeSigner

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `signer` | `any` | ✓ | 署名者のアドレスを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.removeSigner(signer);
```

---

### revokeApproval

revokeApproval

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `proposalId` | `any` | ✓ | 提案のIDを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.revokeApproval(proposalId);
```

---

### revokeRoleDirect

revokeRoleDirect

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
contract.revokeRoleDirect(role, account);
```

---

### setRequiresMultiSig

setRequiresMultiSig

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
contract.setRequiresMultiSig(role, required);
```

---

### setTargetContract

setTargetContract

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `newTarget` | `any` | ✓ | 新しいTargetを指定します。 |

**戻り値:**

| 名前 | 型 | 説明 |
|------|-----|------|

**使用例:**

```solidity
contract.setTargetContract(newTarget);
```

---

</details>

<details>
<summary><strong>イベント (13)</strong></summary>

### events/ApprovalRevoked

承認が取り消された時に発行されるイベントです。所有者、使用者が記録されます。

---

### events/Initialized

コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。

---

### events/ProposalApproved

マルチシグ提案が承認された時に発行されるイベントです。提案ID、承認者が記録されます。

---

### events/ProposalCancelled

マルチシグ提案がキャンセルされた時に発行されるイベントです。提案IDが記録されます。

---

### events/ProposalCreated

マルチシグ提案が作成された時に発行されるイベントです。提案ID、作成者、対象、データが記録されます。

---

### events/ProposalExecuted

マルチシグ提案が実行された時に発行されるイベントです。提案ID、実行者が記録されます。

---

### events/RequiredApprovalsChanged

必要承認数が変更された時に発行されるイベントです。新しい必要承認数が記録されます。

---

### events/RoleGrantProposed

ロール付与が提案された時に発行されるイベントです。ロールとアカウントが記録されます。

---

### events/RoleGrantedMultiSig

マルチシグ経由でロールが付与された時に発行されるイベントです。ロールとアカウントが記録されます。

---

### events/RoleRevokeProposed

ロール取り消しが提案された時に発行されるイベントです。ロールとアカウントが記録されます。

---

### events/RoleRevokedMultiSig

マルチシグ経由でロールが取り消された時に発行されるイベントです。ロールとアカウントが記録されます。

---

### events/SignerAdded

マルチシグに署名者が追加された時に発行されるイベントです。追加された署名者が記録されます。

---

### events/SignerRemoved

マルチシグから署名者が削除された時に発行されるイベントです。削除された署名者が記録されます。

---

</details>

<details>
<summary><strong>エラー (22)</strong></summary>

| エラー名 | 説明 |
|----------|------|
| `errors/InvalidInitialization` | 初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。 |
| `errors/MultiSig_AlreadyApproved` | 既に承認済みの提案を再度承認しようとした時に返されるエラーです。 |
| `errors/MultiSig_CannotRemoveLastSigner` | 最後の署名者を削除しようとした時に返されるエラーです。 |
| `errors/MultiSig_ExecutionFailed` | 提案の実行が失敗した時に返されるエラーです。 |
| `errors/MultiSig_InsufficientApprovals` | 必要な承認数に達していない時に返されるエラーです。 |
| `errors/MultiSig_InvalidDuration` | 無効な有効期限が指定された時に返されるエラーです。 |
| `errors/MultiSig_InvalidRequiredApprovals` | 無効な必要承認数が指定された時に返されるエラーです。 |
| `errors/MultiSig_InvalidSigner` | 無効な署名者が指定された時に返されるエラーです。 |
| `errors/MultiSig_InvalidTarget` | 無効なターゲットアドレスが指定された時に返されるエラーです。 |
| `errors/MultiSig_NotApproved` | 承認されていない提案を実行しようとした時に返されるエラーです。 |
| `errors/MultiSig_NotSigner` | 署名者ではないアカウントが操作を試みた時に返されるエラーです。 |
| `errors/MultiSig_ProposalAlreadyCancelled` | 既にキャンセルされた提案を操作しようとした時に返されるエラーです。 |
| `errors/MultiSig_ProposalAlreadyExecuted` | 既に実行された提案を再度実行しようとした時に返されるエラーです。 |
| `errors/MultiSig_ProposalExpired` | 提案の有効期限が切れた時に返されるエラーです。 |
| `errors/MultiSig_ProposalNotFound` | 指定された提案が存在しない時に返されるエラーです。 |
| `errors/MultiSig_SignerAlreadyExists` | 既に存在する署名者を追加しようとした時に返されるエラーです。 |
| `errors/NotInitializing` | 初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。 |
| `errors/ReentrancyGuardReentrantCall` | 再入呼び出しが検出された時に返されるエラーです。同一関数への再帰呼び出しは禁止されています。 |
| `errors/RoleManager_InvalidAccount` | 無効なアカウントが指定された時に返されるエラーです。 |
| `errors/RoleManager_InvalidRole` | 無効なロールが指定された時に返されるエラーです。 |
| `errors/RoleManager_RequiresMultiSig` | マルチシグ経由での操作が必要な時に返されるエラーです。 |
| `errors/RoleManager_UnauthorizedRoleAdmin` | ロール管理者権限がない時に返されるエラーです。 |

</details>

