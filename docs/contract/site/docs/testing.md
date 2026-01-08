---
id: testing
title: テストガイド
sidebar_label: テスト
---

# テストガイド

## テスト戦略

ERC20コントラクトのテストは、以下の観点で実施することを推奨します。

## 単体テスト

### 基本機能テスト

| テストケース | 説明 |
|-------------|------|
| 初期状態 | コンストラクタ後の状態が正しいか |
| `name()` | トークン名が正しく返されるか |
| `symbol()` | シンボルが正しく返されるか |
| `decimals()` | 小数点桁数が正しいか（デフォルト: 18） |
| `totalSupply()` | 総供給量が正しいか |

### 転送テスト

| テストケース | 説明 |
|-------------|------|
| 正常転送 | 残高十分な場合に転送成功 |
| 残高不足 | `ERC20InsufficientBalance`エラー |
| ゼロアドレス送付先 | `ERC20InvalidReceiver`エラー |
| ゼロ量転送 | 成功（イベント発行） |

### 許可テスト

| テストケース | 説明 |
|-------------|------|
| 許可設定 | 許可量が正しく設定されるか |
| 許可上書き | 許可量が上書きされるか |
| 無限許可 | `type(uint256).max`の動作 |
| ゼロアドレスspender | `ERC20InvalidSpender`エラー |

### transferFromテスト

| テストケース | 説明 |
|-------------|------|
| 正常転送 | 許可・残高十分な場合に成功 |
| 許可不足 | `ERC20InsufficientAllowance`エラー |
| 無限許可での転送 | 許可量が減少しないか |

## Foundryテスト例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/MyToken.sol";

contract ERC20Test is Test {
    MyToken token;
    address alice = address(0x1);
    address bob = address(0x2);

    function setUp() public {
        token = new MyToken();
        token.transfer(alice, 1000 ether);
    }

    function test_Transfer() public {
        vm.prank(alice);
        token.transfer(bob, 100 ether);

        assertEq(token.balanceOf(alice), 900 ether);
        assertEq(token.balanceOf(bob), 100 ether);
    }

    function test_TransferInsufficientBalance() public {
        vm.prank(alice);
        vm.expectRevert();
        token.transfer(bob, 2000 ether);
    }

    function test_Approve() public {
        vm.prank(alice);
        token.approve(bob, 500 ether);

        assertEq(token.allowance(alice, bob), 500 ether);
    }

    function test_TransferFrom() public {
        vm.prank(alice);
        token.approve(bob, 500 ether);

        vm.prank(bob);
        token.transferFrom(alice, bob, 200 ether);

        assertEq(token.balanceOf(bob), 200 ether);
        assertEq(token.allowance(alice, bob), 300 ether);
    }
}
```

## テストカバレッジ

推奨カバレッジ目標：

| 種類 | 目標 |
|------|------|
| 行カバレッジ | 100% |
| ブランチカバレッジ | 100% |
| 関数カバレッジ | 100% |

```bash
# Foundryでカバレッジを確認
forge coverage
```

## インテグレーションテスト

実際のDeFiプロトコルとの統合をテスト：

1. DEXでのスワップ
2. レンディングプロトコルでの担保
3. ブリッジでのクロスチェーン転送
