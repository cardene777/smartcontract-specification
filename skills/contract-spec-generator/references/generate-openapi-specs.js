#!/usr/bin/env node

/**
 * generate-openapi-specs.js
 *
 * Solidityコントラクトから OpenAPI 3.0 YAML と Swagger 2.0 JSON の高精度骨格を自動生成するスクリプト
 *
 * Stage 1: このスクリプトで基本的な説明、型マッピング、共通エラーを含む骨格を生成
 * Stage 2: contract-spec-generator スキルを使用して Claude Code が詳細を追加
 *   - 内部関数のエラー追跡
 *   - コントラクト固有のロジック説明
 *   - modifier情報
 *
 * 使用方法:
 *   node generate-openapi-specs.js
 *
 * 必要な環境:
 *   - Foundry (forge コマンド)
 *   - Node.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 対象コントラクトの定義
const CONTRACTS = [
  // アクセス制御層
  { path: 'src/access/AccessControlMultiSig.sol', name: 'AccessControlMultiSig' },
  { path: 'src/access/MultiSigWallet.sol', name: 'MultiSigWallet' },
  { path: 'src/access/MultiAdminAccessControl.sol', name: 'MultiAdminAccessControl' },
  { path: 'src/access/RoleMultiSigManager.sol', name: 'RoleMultiSigManager' },
  { path: 'src/access/DualKeyMultiSig.sol', name: 'DualKeyMultiSig' },
  { path: 'src/access/BankScopedRoles.sol', name: 'BankScopedRoles' },

  // 実装層
  { path: 'src/implementations/StablecoinCore.sol', name: 'StablecoinCore' },
  { path: 'src/implementations/StablecoinAdmin.sol', name: 'StablecoinAdmin' },
  { path: 'src/implementations/StablecoinTransfer.sol', name: 'StablecoinTransfer' },
  { path: 'src/implementations/StablecoinRoles.sol', name: 'StablecoinRoles' },
  { path: 'src/implementations/StablecoinView.sol', name: 'StablecoinView' },
  { path: 'src/implementations/StablecoinIssuance.sol', name: 'StablecoinIssuance' },
  { path: 'src/implementations/StablecoinBank.sol', name: 'StablecoinBank' },

  // その他
  { path: 'src/extensions/BankPausable.sol', name: 'BankPausable' },
  { path: 'src/storage/StablecoinStorage.sol', name: 'StablecoinStorage' },
  { path: 'src/tokens/ERC20SoladyUpgradeable.sol', name: 'ERC20SoladyUpgradeable' },
  { path: 'src/proxy/StablecoinProxy.sol', name: 'StablecoinProxy' },
  { path: 'src/proxy/Dictionary.sol', name: 'Dictionary' },
];

// 出力ディレクトリ
const SCRIPT_DIR = __dirname;
const PROJECT_ROOT = path.join(SCRIPT_DIR, '..');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'docs', 'contract');

console.log('📄 OpenAPI Enhanced Skeleton Generator');
console.log('========================================');
console.log(`Output: ${OUTPUT_DIR}\n`);

/**
 * forge inspect コマンドでABIを取得
 */
function getABI(contractPath, contractName) {
  try {
    const cmd = `forge inspect ${contractPath}:${contractName} abi`;
    const output = execSync(cmd, { encoding: 'utf-8', cwd: SCRIPT_DIR });
    return JSON.parse(output);
  } catch (error) {
    console.error(`  ❌ Error getting ABI: ${error.message}`);
    return null;
  }
}

/**
 * Solidityソースコードを読み込み
 */
function getSource(contractPath) {
  try {
    const fullPath = path.join(SCRIPT_DIR, contractPath);
    return fs.readFileSync(fullPath, 'utf-8');
  } catch (error) {
    console.error(`  ❌ Error reading source: ${error.message}`);
    return null;
  }
}

/**
 * 継承関係を抽出
 */
function extractInheritance(source) {
  const match = source.match(/contract\s+\w+\s+is\s+([\w\s,]+)/);
  if (match) {
    return match[1].split(',').map(s => s.trim());
  }
  return [];
}

/**
 * 構造体を抽出
 */
function extractStructs(source) {
  const structs = [];
  // struct Name { ... } パターンを検索
  const structRegex = /struct\s+(\w+)\s*\{([^}]+)\}/g;
  let match;

  while ((match = structRegex.exec(source)) !== null) {
    const name = match[1];
    const body = match[2];

    // フィールドを解析
    const fields = [];
    const fieldLines = body.split(';').filter(line => line.trim());

    for (const line of fieldLines) {
      const trimmed = line.trim();
      if (!trimmed) continue;

      // "type name" または "type[] name" パターン
      const fieldMatch = trimmed.match(/^(\w+(?:\[\])?)\s+(\w+)$/);
      if (fieldMatch) {
        fields.push({
          type: fieldMatch[1],
          name: fieldMatch[2]
        });
      }
    }

    structs.push({ name, fields });
  }

  return structs;
}

/**
 * modifierを抽出
 */
function extractModifiers(source) {
  const modifiers = [];
  // modifier Name(...) { ... } または modifier Name { ... } パターンを検索
  const modifierRegex = /modifier\s+(\w+)\s*(?:\(([^)]*)\))?\s*\{/g;
  let match;

  while ((match = modifierRegex.exec(source)) !== null) {
    const name = match[1];
    const paramsStr = match[2] || '';

    // パラメータを解析
    const params = [];
    if (paramsStr.trim()) {
      const paramParts = paramsStr.split(',');
      for (const part of paramParts) {
        const trimmed = part.trim();
        const paramMatch = trimmed.match(/(\w+(?:\[\])?)\s+(\w+)/);
        if (paramMatch) {
          params.push({
            type: paramMatch[1],
            name: paramMatch[2]
          });
        }
      }
    }

    modifiers.push({ name, params });
  }

  return modifiers;
}

/**
 * public状態変数を抽出（getter関数が自動生成されるもの）
 */
function extractStateVariables(source) {
  const variables = [];

  // パターン1: type public variableName; または type public variableName = value;
  // パターン2: type public immutable variableName;
  const varRegex = /^\s*(uint\d*|int\d*|address|bool|bytes\d*|string)\s+(?:public\s+(?:immutable\s+)?|(?:immutable\s+)?public\s+)(\w+)(?:\s*=\s*[^;]+)?;/gm;
  let match;

  while ((match = varRegex.exec(source)) !== null) {
    const typeName = match[1];
    const varName = match[2];
    variables.push({
      name: varName,
      type: typeName,
      isImmutable: match[0].includes('immutable')
    });
  }

  return variables;
}

/**
 * public定数を抽出（getter関数が自動生成されるもの）
 */
function extractConstants(source) {
  const constants = [];

  // パターン: type public constant NAME = value; または type constant public NAME = value;
  const constRegex = /^\s*(uint\d*|int\d*|address|bool|bytes\d*|string)\s+(?:public\s+constant|constant\s+public)\s+(\w+)\s*=/gm;
  let match;

  while ((match = constRegex.exec(source)) !== null) {
    const typeName = match[1];
    const constName = match[2];
    constants.push({
      name: constName,
      type: typeName
    });
  }

  return constants;
}

/**
 * public mappingを抽出（getter関数が自動生成されるもの）
 */
function extractMappings(source) {
  const mappings = [];

  // パターン: mapping(keyType => valueType) public mappingName;
  // ネストしたmappingも対応: mapping(keyType => mapping(keyType2 => valueType)) public mappingName;
  const mappingRegex = /^\s*(mapping\s*\([^)]+(?:\)\s*mapping\s*\([^)]+)*\s*\))\s+public\s+(\w+)\s*;/gm;
  let match;

  while ((match = mappingRegex.exec(source)) !== null) {
    const mappingType = match[1];
    const mappingName = match[2];

    // キータイプを抽出
    const keyTypes = [];
    const keyMatches = mappingType.match(/mapping\s*\(\s*(\w+)\s*=>/g);
    if (keyMatches) {
      for (const keyMatch of keyMatches) {
        const typeMatch = keyMatch.match(/mapping\s*\(\s*(\w+)/);
        if (typeMatch) {
          keyTypes.push(typeMatch[1]);
        }
      }
    }

    mappings.push({
      name: mappingName,
      type: mappingType,
      keyTypes: keyTypes
    });
  }

  return mappings;
}

/**
 * 関数が変数/定数/mappingのgetterかどうかを判定
 * @param {string} funcName - 関数名
 * @param {Array} funcInputs - 関数の入力パラメータ
 * @param {string} stateMutability - 関数のstateMutability (view/pure/etc)
 * @param {Array} variables - 抽出された変数リスト
 * @param {Array} constants - 抽出された定数リスト
 * @param {Array} mappings - 抽出されたmappingリスト
 */
function getFunctionCategory(funcName, funcInputs, stateMutability, variables, constants, mappings) {
  // view/pure関数のみ対象
  if (stateMutability !== 'view' && stateMutability !== 'pure') {
    return null;
  }

  // ソースから抽出した定数にマッチ
  const matchedConstant = constants.find(c => c.name === funcName);
  if (matchedConstant) {
    return '定数';
  }

  // 命名規則で定数を検出: 全て大文字+アンダースコア、入力なし
  // 例: ALLOWLIST_ROLE, PAUSER_ROLE, DEFAULT_ADMIN_ROLE, PROPOSAL_EXPIRY
  const isConstantNaming = /^[A-Z][A-Z0-9_]*$/.test(funcName);
  if (isConstantNaming && (!funcInputs || funcInputs.length === 0)) {
    return '定数';
  }

  // ソースから抽出したmappingにマッチ
  const matchedMapping = mappings.find(m => m.name === funcName);
  if (matchedMapping) {
    return 'Mapping';
  }

  // mapping検出: 入力パラメータがあるview関数でgetter風の名前
  // 例: balanceOf(address), allowance(address, address), isAllowed(address)
  const knownMappingGetters = [
    'balanceOf', 'allowance', 'nonces', 'isAllowed', 'getBankRole',
    'hasBankRole', 'getBankRoleAdmin', 'isBankPaused', 'getBankCap',
    'getBankOutstanding', 'getBankInfo', 'getRoleAdmin', 'hasRole',
    'supportsInterface', 'getDualKey', 'getKeyRotationProposal',
    'getProposal', 'isSigner', 'getSigners', 'getBankRoleProposal'
  ];
  if (funcInputs && funcInputs.length > 0 && knownMappingGetters.includes(funcName)) {
    return 'Mapping';
  }

  // ソースから抽出した変数にマッチ
  const matchedVariable = variables.find(v => v.name === funcName);
  if (matchedVariable) {
    return '変数';
  }

  // 変数検出: 入力なし、小文字始まりの単純なgetter
  // 例: name, symbol, decimals, totalSupply, owner, paused
  const knownVariableGetters = [
    'name', 'symbol', 'decimals', 'totalSupply', 'owner', 'paused',
    'requiredApprovals', 'proposalCount', 'nextProposalId'
  ];
  if ((!funcInputs || funcInputs.length === 0) && knownVariableGetters.includes(funcName)) {
    return '変数';
  }

  return null;
}

/**
 * 変数の説明を生成
 */
function getVariableDescription(varName, varType, isImmutable) {
  const immutableNote = isImmutable ? '（immutable）' : '';

  const VAR_DESC = {
    'totalSupply': `トークンの総供給量を保持する${immutableNote}変数です。`,
    'name': `トークンの名前を保持する${immutableNote}変数です。`,
    'symbol': `トークンのシンボルを保持する${immutableNote}変数です。`,
    'decimals': `トークンの小数点以下桁数を保持する${immutableNote}変数です。`,
    'owner': `コントラクトの所有者アドレスを保持する${immutableNote}変数です。`,
    'paused': `コントラクトの一時停止状態を保持する${immutableNote}変数です。`,
  };

  if (VAR_DESC[varName]) {
    return VAR_DESC[varName];
  }

  return `${varName}の値を保持する${immutableNote}変数です。`;
}

/**
 * 定数の説明を生成
 */
function getConstantDescription(constName) {
  const CONST_DESC = {
    'DEFAULT_ADMIN_ROLE': 'デフォルト管理者ロールのバイト列を返す定数です。',
    'MINTER_ROLE': 'ミンターロールのバイト列を返す定数です。',
    'PAUSER_ROLE': 'ポーザーロールのバイト列を返す定数です。',
    'BURNER_ROLE': 'バーナーロールのバイト列を返す定数です。',
    'UPGRADER_ROLE': 'アップグレーダーロールのバイト列を返す定数です。',
    'BANK_ADMIN_ROLE': '銀行管理者ロールのバイト列を返す定数です。',
    'BANK_ISSUER_ROLE': '銀行発行者ロールのバイト列を返す定数です。',
    'BANK_PAUSER_ROLE': '銀行ポーザーロールのバイト列を返す定数です。',
  };

  if (CONST_DESC[constName]) {
    return CONST_DESC[constName];
  }

  // ロール関連の定数
  if (constName.endsWith('_ROLE')) {
    return `${constName}のバイト列を返す定数です。`;
  }

  return `${constName}の値を返す定数です。`;
}

/**
 * Mappingの説明を生成
 */
function getMappingDescription(mappingName, keyTypes) {
  const MAPPING_DESC = {
    'balanceOf': 'アカウントアドレスから残高を取得するmapping配列です。',
    'allowance': '所有者と使用者のアドレスから許可量を取得するmapping配列です。',
    'nonces': 'アカウントアドレスからnonce値を取得するmapping配列です。',
    'isAllowed': 'アカウントアドレスが許可リストに含まれているかを取得するmapping配列です。',
  };

  if (MAPPING_DESC[mappingName]) {
    return MAPPING_DESC[mappingName];
  }

  const keyTypeStr = keyTypes.join(' → ');
  return `${keyTypeStr}をキーとして値を取得するmapping配列です。`;
}

/**
 * Solidity型からOpenAPI型マッピング情報を取得
 */
function getSolidityTypeMapping(solidityType) {
  const mapping = {
    type: 'string',
    pattern: null,
    example: null
  };

  if (solidityType === 'address') {
    mapping.pattern = '^0x[0-9a-fA-F]{40}$';
    mapping.example = '0x1234567890123456789012345678901234567890';
  } else if (solidityType === 'bytes4') {
    mapping.pattern = '^0x[0-9a-fA-F]{8}$';
    mapping.example = '0x12345678';
  } else if (solidityType === 'bytes32') {
    mapping.pattern = '^0x[0-9a-fA-F]{64}$';
    mapping.example = '0x1234567890123456789012345678901234567890123456789012345678901234';
  } else if (solidityType.startsWith('bytes') && solidityType !== 'bytes32' && solidityType !== 'bytes4') {
    mapping.pattern = '^0x[0-9a-fA-F]*$';
    mapping.example = '0x123456';
  } else if (solidityType.startsWith('uint') || solidityType.startsWith('int')) {
    mapping.example = '1000000000000000000';
  } else if (solidityType === 'bool') {
    mapping.example = 'true';
  } else if (solidityType === 'string') {
    mapping.example = 'Example String';
  }

  return mapping;
}

/**
 * パラメータ名から意味のある説明を生成
 */
function getParamDescription(paramName) {
  const PARAM_DESC = {
    // Address parameters
    'owner': '所有者のアドレスを指定します。',
    'newOwner': '新しい所有者となるアドレスを指定します。',
    'spender': 'トークンの使用を許可するアドレスを指定します。',
    'from': '送金元のアドレスを指定します。',
    'to': '送金先のアドレスを指定します。',
    'recipient': '受取人のアドレスを指定します。',
    'account': '対象アカウントのアドレスを指定します。',
    'sender': '送信者のアドレスを指定します。',
    'operator': 'オペレーターのアドレスを指定します。',
    'target': '対象コントラクトのアドレスを指定します。',
    'admin': '管理者のアドレスを指定します。',
    'newAdmin': '新しい管理者のアドレスを指定します。',
    'signer': '署名者のアドレスを指定します。',
    'newSigner': '新しい署名者のアドレスを指定します。',
    'key1': '第1キーのアドレスを指定します。',
    'key2': '第2キーのアドレスを指定します。',
    'newKey1': '新しい第1キーのアドレスを指定します。',
    'newKey2': '新しい第2キーのアドレスを指定します。',
    'initialOwner': '初期所有者のアドレスを指定します。',
    'pendingOwner': '保留中の所有者のアドレスを指定します。',
    'implementation': '実装コントラクトのアドレスを指定します。',
    'newImplementation': '新しい実装コントラクトのアドレスを指定します。',
    'minter': 'ミンターのアドレスを指定します。',
    'burner': 'バーナーのアドレスを指定します。',
    'pauser': 'ポーザーのアドレスを指定します。',
    'user': 'ユーザーのアドレスを指定します。',

    // Amount/Value parameters
    'amount': 'トークン量を指定します（wei単位）。',
    'value': '値を指定します。',
    'subtractedValue': '減算する許可量を指定します（wei単位）。',
    'addedValue': '追加する許可量を指定します（wei単位）。',
    'shares': 'シェア数を指定します。',
    'assets': 'アセット量を指定します。',

    // ID parameters
    'proposalId': '提案のIDを指定します。',
    'bankId': '銀行のIDを指定します。',
    'txIndex': 'トランザクションのインデックスを指定します。',
    'nonce': 'ナンス値を指定します。',
    'index': 'インデックスを指定します。',
    'id': 'IDを指定します。',

    // Role parameters
    'role': 'ロールの識別子を指定します。',
    'roleId': 'ロールのIDを指定します。',
    'newRole': '新しいロールの識別子を指定します。',
    'adminRole': '管理者ロールの識別子を指定します。',

    // Boolean parameters
    'approved': '承認状態を指定します。',
    'status': 'ステータスを指定します。',
    'active': 'アクティブ状態を指定します。',
    'paused': '一時停止状態を指定します。',

    // String parameters
    'name_': 'トークン名を指定します。',
    'symbol_': 'トークンシンボルを指定します。',
    'name': '名前を指定します。',
    'symbol': 'シンボルを指定します。',
    'reason': '理由を指定します。',
    'description': '説明を指定します。',

    // Data parameters
    'data': 'コールデータを指定します。',
    '_data': 'コールデータを指定します。',
    'callData': 'コールデータを指定します。',
    'signature': '署名データを指定します。',
    'selector': '関数セレクタを指定します。',
    'functionSelector': '関数セレクタを指定します。',
    'interfaceId': 'インターフェースIDを指定します。',

    // Deadline/Time parameters
    'deadline': '有効期限のタイムスタンプを指定します。',
    'expiry': '有効期限を指定します。',
    'timestamp': 'タイムスタンプを指定します。',

    // Other common parameters
    'required': '必要な承認数を指定します。',
    'threshold': 'しきい値を指定します。',
    'owners': '所有者アドレスの配列を指定します。',
    'admins': '管理者アドレスの配列を指定します。',
    'signers': '署名者アドレスの配列を指定します。',
    'decimals_': '小数点以下の桁数を指定します。',
    'v': '署名のv値を指定します。',
    'r': '署名のr値を指定します。',
    's': '署名のs値を指定します。',
    'requiredApprovals': '必要な承認数を指定します。',
    'requiredApprovals_': '必要な承認数を指定します。',
  };

  if (PARAM_DESC[paramName]) {
    return PARAM_DESC[paramName];
  }

  // Pattern-based descriptions
  if (paramName.endsWith('Id')) {
    return `${paramName}を指定します。`;
  }
  if (paramName.endsWith('Address')) {
    return `${paramName}のアドレスを指定します。`;
  }
  if (paramName.startsWith('new')) {
    return `新しい${paramName.substring(3)}を指定します。`;
  }
  if (paramName.startsWith('is') || paramName.startsWith('has') || paramName.startsWith('can')) {
    return `${paramName}の状態を指定します。`;
  }

  // Default
  return `${paramName}を指定します。`;
}

/**
 * 関数名から戻り値の説明を生成
 */
function getReturnDescription(funcName, outputName) {
  // If output has a meaningful name (not result0, result1, etc.), use it
  if (outputName && !outputName.match(/^result\d+$/)) {
    return `${outputName}を返します。`;
  }

  const RETURN_DESC = {
    // ERC20 standard functions
    'name': 'トークン名を返します。',
    'symbol': 'トークンシンボルを返します。',
    'decimals': '小数点以下の桁数を返します。',
    'totalSupply': 'トークンの総供給量を返します。',
    'balanceOf': 'アカウントの残高を返します。',
    'transfer': '送金が成功した場合trueを返します。',
    'approve': '承認が成功した場合trueを返します。',
    'allowance': '許可された残高を返します。',
    'transferFrom': '送金が成功した場合trueを返します。',
    'increaseAllowance': '許可量の増加が成功した場合trueを返します。',
    'decreaseAllowance': '許可量の減少が成功した場合trueを返します。',

    // Ownable/Access control
    'owner': '所有者のアドレスを返します。',
    'pendingOwner': '保留中の所有者のアドレスを返します。',
    'hasRole': '指定されたロールを持っている場合trueを返します。',
    'getRoleAdmin': 'ロールの管理者ロールを返します。',
    'getRoleMember': '指定インデックスのロールメンバーを返します。',
    'getRoleMemberCount': 'ロールメンバーの数を返します。',
    'supportsInterface': 'インターフェースをサポートしている場合trueを返します。',

    // Pausable
    'paused': '一時停止中の場合trueを返します。',

    // Bank related
    'getBankId': '銀行IDを返します。',
    'getBankInfo': '銀行情報を返します。',
    'getBankCount': '銀行の数を返します。',
    'isBankActive': '銀行がアクティブな場合trueを返します。',
    'getBankRole': '銀行ロールを返します。',
    'isBankPaused': '銀行が一時停止中の場合trueを返します。',

    // Proposal related
    'getProposal': '提案情報を返します。',
    'getProposalCount': '提案の数を返します。',
    'isProposalApproved': '提案が承認されている場合trueを返します。',
    'isProposalExecuted': '提案が実行済みの場合trueを返します。',
    'getApprovalCount': '承認数を返します。',
    'hasApproved': '承認済みの場合trueを返します。',

    // MultiSig
    'getTransaction': 'トランザクション情報を返します。',
    'getTransactionCount': 'トランザクションの数を返します。',
    'isConfirmed': '確認済みの場合trueを返します。',
    'getConfirmationCount': '確認数を返します。',
    'getOwners': '所有者アドレスの配列を返します。',
    'required': '必要な承認数を返します。',
    'getSigners': '署名者アドレスの配列を返します。',

    // Proxy
    'implementation': '実装コントラクトのアドレスを返します。',
    'getImplementation': '実装コントラクトのアドレスを返します。',

    // Dictionary
    'getFunctionSelector': '関数セレクタを返します。',
    'getFunctionSelectorList': '関数セレクタの配列を返します。',
    'getDescription': '説明を返します。',

    // Allowlist
    'isAllowed': '許可されている場合trueを返します。',
    'isOnAllowlist': '許可リストに含まれている場合trueを返します。',
  };

  if (RETURN_DESC[funcName]) {
    return RETURN_DESC[funcName];
  }

  // Role constants
  if (funcName.endsWith('_ROLE') && funcName === funcName.toUpperCase()) {
    const roleName = funcName.replace(/_ROLE$/, '');
    return `${roleName}ロールのバイト列を返します。`;
  }

  // Constants (all uppercase)
  if (funcName === funcName.toUpperCase() && funcName.includes('_')) {
    return `${funcName}の値を返します。`;
  }

  // Pattern-based descriptions
  if (funcName.match(/^get(.+)Count$/)) {
    const target = funcName.replace(/^get/, '').replace(/Count$/, '');
    return `${target}の数を返します。`;
  }
  if (funcName.startsWith('get')) {
    const target = funcName.replace(/^get/, '');
    return `${target}を返します。`;
  }
  if (funcName.startsWith('is')) {
    const condition = funcName.replace(/^is/, '');
    return `${condition}の場合trueを返します。`;
  }
  if (funcName.startsWith('has')) {
    const condition = funcName.replace(/^has/, '');
    return `${condition}を持っている場合trueを返します。`;
  }
  if (funcName.startsWith('can')) {
    const condition = funcName.replace(/^can/, '');
    return `${condition}が可能な場合trueを返します。`;
  }

  // Default
  return `${funcName}の結果を返します。`;
}

/**
 * イベント名から意味のある説明を生成
 */
function getEventDescription(eventName) {
  const EVENT_DESC = {
    // ERC20 Events
    'Transfer': 'トークンが転送された時に発行されるイベントです。送金元、送金先、および転送量が記録されます。',
    'Approval': 'トークンの使用許可が設定された時に発行されるイベントです。所有者、承認された使用者、および許可量が記録されます。',

    // Pausable Events
    'Paused': 'コントラクトが一時停止された時に発行されるイベントです。一時停止を実行したアカウントが記録されます。',
    'Unpaused': 'コントラクトの一時停止が解除された時に発行されるイベントです。解除を実行したアカウントが記録されます。',

    // Ownership Events
    'OwnershipTransferred': '所有権が移転された時に発行されるイベントです。以前の所有者と新しい所有者が記録されます。',

    // Access Control Events
    'RoleGranted': 'アカウントにロールが付与された時に発行されるイベントです。ロール、付与されたアカウント、付与したアカウントが記録されます。',
    'RoleRevoked': 'アカウントからロールが取り消された時に発行されるイベントです。ロール、取り消されたアカウント、取り消したアカウントが記録されます。',
    'RoleAdminChanged': 'ロールの管理者ロールが変更された時に発行されるイベントです。対象ロール、以前の管理者ロール、新しい管理者ロールが記録されます。',

    // Allowlist Events
    'AccountAllowed': 'アカウントが許可リストに追加された時に発行されるイベントです。許可されたアカウントが記録されます。',
    'AccountDisallowed': 'アカウントが許可リストから削除された時に発行されるイベントです。削除されたアカウントが記録されます。',

    // Bank Events
    'BankRegistered': '新しい銀行が登録された時に発行されるイベントです。銀行ID、名前、キャップなどが記録されます。',
    'BankRemoved': '銀行が削除された時に発行されるイベントです。削除された銀行のIDが記録されます。',
    'BankDeactivated': '銀行が非アクティブ化された時に発行されるイベントです。対象の銀行IDが記録されます。',
    'BankCapSet': '銀行のキャップが設定または変更された時に発行されるイベントです。銀行IDと新しいキャップが記録されます。',
    'BankPaused': '銀行が一時停止された時に発行されるイベントです。銀行IDと一時停止を実行したアカウントが記録されます。',
    'BankUnpaused': '銀行の一時停止が解除された時に発行されるイベントです。銀行IDと解除を実行したアカウントが記録されます。',
    'BankTransfer': '銀行間でトークンが転送された時に発行されるイベントです。転送元銀行、転送先銀行、金額が記録されます。',
    'TransferWithinBank': '同一銀行内でトークンが転送された時に発行されるイベントです。銀行ID、送金元、送金先、金額が記録されます。',
    'TransferRouted': '銀行経由でトークンが転送された時に発行されるイベントです。送金元銀行、送金先銀行、金額が記録されます。',
    'BankIssuerGranted': '銀行に発行者権限が付与された時に発行されるイベントです。銀行IDと付与されたアドレスが記録されます。',
    'BankIssuerRevoked': '銀行から発行者権限が取り消された時に発行されるイベントです。銀行IDと取り消されたアドレスが記録されます。',

    // Bank Role Events
    'BankRoleGranted': '銀行スコープのロールがアカウントに付与された時に発行されるイベントです。銀行ID、ロール、アカウントが記録されます。',
    'BankRoleRevoked': '銀行スコープのロールがアカウントから取り消された時に発行されるイベントです。銀行ID、ロール、アカウントが記録されます。',
    'BankRoleAdminSet': '銀行ロールの管理者が設定された時に発行されるイベントです。銀行ID、ロール、管理者ロールが記録されます。',
    'BankRoleProposalCreated': '銀行ロールの提案が作成された時に発行されるイベントです。提案ID、銀行ID、提案者が記録されます。',
    'BankRoleProposalApproved': '銀行ロールの提案が承認された時に発行されるイベントです。提案ID、承認者が記録されます。',
    'BankRoleProposalExecuted': '銀行ロールの提案が実行された時に発行されるイベントです。提案IDが記録されます。',
    'BankRoleProposalCancelled': '銀行ロールの提案がキャンセルされた時に発行されるイベントです。提案IDが記録されます。',

    // Minting Events
    'Minted': 'トークンが新規発行された時に発行されるイベントです。発行先アカウントと発行量が記録されます。',
    'ForcedTransfer': '強制転送が実行された時に発行されるイベントです。送金元、送金先、金額が記録されます。',

    // Bucket Events
    'BucketReassigned': 'バケットが再割り当てされた時に発行されるイベントです。元の所有者、新しい所有者、金額が記録されます。',

    // MultiSig Events
    'ProposalCreated': 'マルチシグ提案が作成された時に発行されるイベントです。提案ID、作成者、対象、データが記録されます。',
    'ProposalApproved': 'マルチシグ提案が承認された時に発行されるイベントです。提案ID、承認者が記録されます。',
    'ProposalExecuted': 'マルチシグ提案が実行された時に発行されるイベントです。提案ID、実行者が記録されます。',
    'ProposalCancelled': 'マルチシグ提案がキャンセルされた時に発行されるイベントです。提案IDが記録されます。',
    'SignerAdded': 'マルチシグに署名者が追加された時に発行されるイベントです。追加された署名者が記録されます。',
    'SignerRemoved': 'マルチシグから署名者が削除された時に発行されるイベントです。削除された署名者が記録されます。',
    'RequiredApprovalsChanged': '必要承認数が変更された時に発行されるイベントです。新しい必要承認数が記録されます。',
    'MultiSigRequirementSet': 'マルチシグ要件が設定された時に発行されるイベントです。ロールと必要承認数が記録されます。',

    // DualKey Events
    'DualKeyInitialized': 'デュアルキーが初期化された時に発行されるイベントです。アドレスと2つのキーが記録されます。',
    'KeyRotationProposed': 'キーローテーションが提案された時に発行されるイベントです。提案ID、提案者、新しいキーが記録されます。',
    'KeyRotationApproved': 'キーローテーションが承認された時に発行されるイベントです。提案ID、承認者が記録されます。',
    'KeyRotationExecuted': 'キーローテーションが実行された時に発行されるイベントです。古いキーと新しいキーが記録されます。',
    'KeyRotationCancelled': 'キーローテーションがキャンセルされた時に発行されるイベントです。提案IDが記録されます。',

    // Role Manager Events
    'RoleGrantedMultiSig': 'マルチシグ経由でロールが付与された時に発行されるイベントです。ロールとアカウントが記録されます。',
    'RoleRevokedMultiSig': 'マルチシグ経由でロールが取り消された時に発行されるイベントです。ロールとアカウントが記録されます。',
    'RoleGrantProposed': 'ロール付与が提案された時に発行されるイベントです。ロールとアカウントが記録されます。',
    'RoleRevokeProposed': 'ロール取り消しが提案された時に発行されるイベントです。ロールとアカウントが記録されます。',

    // Admin Events
    'RoleAdminAdded': 'ロール管理者が追加された時に発行されるイベントです。ロールと管理者が記録されます。',
    'RoleAdminRemoved': 'ロール管理者が削除された時に発行されるイベントです。ロールと管理者が記録されます。',
    'ApprovalRevoked': '承認が取り消された時に発行されるイベントです。所有者、使用者が記録されます。',

    // Proxy/Upgrade Events
    'Upgraded': 'コントラクトがアップグレードされた時に発行されるイベントです。新しい実装アドレスが記録されます。',
    'Initialized': 'コントラクトが初期化された時に発行されるイベントです。初期化バージョンが記録されます。',
    'ImplementationUpgraded': '実装コントラクトがアップグレードされた時に発行されるイベントです。関数セレクタと新しい実装が記録されます。',
    'ImplementationRemoved': '実装コントラクトが削除された時に発行されるイベントです。関数セレクタが記録されます。',
    'DictionaryUpgraded': 'ディクショナリがアップグレードされた時に発行されるイベントです。新しいディクショナリアドレスが記録されます。',
  };

  if (EVENT_DESC[eventName]) {
    return EVENT_DESC[eventName];
  }

  // Pattern-based descriptions
  if (eventName.includes('Paused')) {
    return `一時停止関連の状態変更が発生した時に発行されるイベントです。`;
  }
  if (eventName.includes('Transfer')) {
    return `トークン転送が発生した時に発行されるイベントです。`;
  }
  if (eventName.includes('Role')) {
    return `ロール関連の変更が発生した時に発行されるイベントです。`;
  }
  if (eventName.includes('Proposal')) {
    return `提案関連の操作が発生した時に発行されるイベントです。`;
  }
  if (eventName.includes('Bank')) {
    return `銀行関連の操作が発生した時に発行されるイベントです。`;
  }

  // Default
  return `${eventName}が発生した時に発行されるイベントです。`;
}

/**
 * エラー名から意味のある説明を生成
 */
function getErrorDescription(errorName) {
  const ERROR_DESC = {
    // Common Validation Errors
    'InvalidAddress': '無効なアドレス（ゼロアドレスや不正なアドレス形式）が指定された時に返されるエラーです。',
    'AmountZero': '金額にゼロが指定された時に返されるエラーです。正の金額を指定する必要があります。',
    'InsufficientBalance': '残高が不足している時に返されるエラーです。操作に必要な残高を確保してください。',
    'InsufficientAllowance': '許可量が不足している時に返されるエラーです。事前にapproveで十分な許可量を設定してください。',

    // ERC20 Errors
    'AllowanceOverflow': '許可量がオーバーフローした時に返されるエラーです。許可量の上限を超えています。',
    'AllowanceUnderflow': '許可量がアンダーフローした時に返されるエラーです。減算量が現在の許可量を超えています。',
    'TotalSupplyOverflow': '総供給量がオーバーフローした時に返されるエラーです。',

    // Access Control Errors
    'AccessControlUnauthorizedAccount': '権限のないアカウントが操作を試みた時に返されるエラーです。必要なロールを持っていません。',
    'AccessControlBadConfirmation': 'アクセス制御の確認が失敗した時に返されるエラーです。',
    'AccessControlMultiSig_RequiresMultiSigAdmin': 'マルチシグ管理者権限が必要な操作で権限がない時に返されるエラーです。',

    // Pausable Errors
    'EnforcedPause': 'コントラクトが一時停止中に操作を試みた時に返されるエラーです。',
    'ExpectedPause': 'コントラクトが一時停止状態であることが期待される操作で、一時停止されていない時に返されるエラーです。',

    // Ownable Errors
    'OwnableInvalidOwner': '無効な所有者が指定された時に返されるエラーです。',
    'OwnableUnauthorizedAccount': '所有者ではないアカウントが所有者専用の操作を試みた時に返されるエラーです。',

    // Initializable Errors
    'InvalidInitialization': '初期化が無効な時に返されるエラーです。既に初期化済みか、初期化順序が不正です。',
    'NotInitializing': '初期化中でない時に返されるエラーです。initializer修飾子のコンテキスト外での呼び出しが原因です。',

    // Reentrancy Errors
    'ReentrancyGuardReentrantCall': '再入呼び出しが検出された時に返されるエラーです。同一関数への再帰呼び出しは禁止されています。',

    // Proxy/UUPS Errors
    'ERC1967InvalidImplementation': '無効な実装アドレスが指定された時に返されるエラーです。',
    'ERC1967NonPayable': 'ETHの受け取りが許可されていない時に返されるエラーです。',
    'UUPSUnauthorizedCallContext': 'UUPSアップグレードが不正なコンテキストから呼び出された時に返されるエラーです。',
    'UUPSUnsupportedProxiableUUID': 'プロキシが互換性のない実装をアップグレードしようとした時に返されるエラーです。',
    'AddressEmptyCode': '指定されたアドレスにコードが存在しない時に返されるエラーです。',
    'FailedCall': '外部呼び出しが失敗した時に返されるエラーです。',

    // Bank Errors
    'BankNotFound': '指定された銀行が存在しない時に返されるエラーです。銀行IDを確認してください。',
    'BankExists': '既に存在する銀行を作成しようとした時に返されるエラーです。',
    'BankInactive': '銀行が非アクティブ状態の時に返されるエラーです。銀行をアクティブ化してください。',
    'CapExceeded': '銀行のキャップを超過した時に返されるエラーです。キャップ内での操作が必要です。',
    'CapZero': 'キャップがゼロに設定されようとした時に返されるエラーです。正のキャップを指定してください。',
    'CapBelowOutstanding': 'キャップが既存の発行量を下回った時に返されるエラーです。',
    'UnauthorizedIssuer': '銀行の発行者権限がない時に返されるエラーです。',
    'NotAllowed': 'アカウントが許可リストに含まれていない時に返されるエラーです。',

    // Bank Pauser Errors
    'BankPauser_BankAlreadyPaused': '既に一時停止中の銀行を一時停止しようとした時に返されるエラーです。',
    'BankPauser_BankNotPaused': '一時停止されていない銀行の一時停止を解除しようとした時に返されるエラーです。',
    'BankPauser_InvalidBankId': '無効な銀行IDが指定された時に返されるエラーです。',
    'BankPauser_UnauthorizedBankPauser': '銀行のポーズ権限がない時に返されるエラーです。',

    // Bank Scoped Roles Errors
    'BankScopedRoles_InvalidAccount': '無効なアカウントが指定された時に返されるエラーです。',
    'BankScopedRoles_InvalidBankId': '無効な銀行IDが指定された時に返されるエラーです。',
    'BankScopedRoles_UnauthorizedRoleAdmin': 'ロール管理者権限がない時に返されるエラーです。',

    // Bucket Errors
    'InsufficientBucket': 'バケット残高が不足している時に返されるエラーです。',
    'InvalidBucket': '無効なバケットが指定された時に返されるエラーです。',
    'InvalidReassignment': '無効なバケット再割り当てが試みられた時に返されるエラーです。',

    // MultiSig Errors
    'MultiSig_NotSigner': '署名者ではないアカウントが操作を試みた時に返されるエラーです。',
    'MultiSig_InvalidSigner': '無効な署名者が指定された時に返されるエラーです。',
    'MultiSig_SignerAlreadyExists': '既に存在する署名者を追加しようとした時に返されるエラーです。',
    'MultiSig_CannotRemoveLastSigner': '最後の署名者を削除しようとした時に返されるエラーです。',
    'MultiSig_InvalidRequiredApprovals': '無効な必要承認数が指定された時に返されるエラーです。',
    'MultiSig_InvalidTarget': '無効なターゲットアドレスが指定された時に返されるエラーです。',
    'MultiSig_InvalidDuration': '無効な有効期限が指定された時に返されるエラーです。',
    'MultiSig_ProposalNotFound': '指定された提案が存在しない時に返されるエラーです。',
    'MultiSig_ProposalExpired': '提案の有効期限が切れた時に返されるエラーです。',
    'MultiSig_ProposalAlreadyExecuted': '既に実行された提案を再度実行しようとした時に返されるエラーです。',
    'MultiSig_ProposalAlreadyCancelled': '既にキャンセルされた提案を操作しようとした時に返されるエラーです。',
    'MultiSig_AlreadyApproved': '既に承認済みの提案を再度承認しようとした時に返されるエラーです。',
    'MultiSig_NotApproved': '承認されていない提案を実行しようとした時に返されるエラーです。',
    'MultiSig_InsufficientApprovals': '必要な承認数に達していない時に返されるエラーです。',
    'MultiSig_ExecutionFailed': '提案の実行が失敗した時に返されるエラーです。',

    // DualKey MultiSig Errors
    'DualKeyMultiSig_NotInitialized': 'デュアルキーが初期化されていない時に返されるエラーです。',
    'DualKeyMultiSig_AlreadyInitialized': 'デュアルキーが既に初期化されている時に返されるエラーです。',
    'DualKeyMultiSig_NotAuthorized': 'デュアルキー操作の権限がない時に返されるエラーです。',
    'DualKeyMultiSig_InvalidAddress': '無効なアドレスがデュアルキーに指定された時に返されるエラーです。',
    'DualKeyMultiSig_InvalidKeyReplacement': '無効なキー交換が試みられた時に返されるエラーです。',
    'DualKeyMultiSig_ProposalNotFound': 'キーローテーション提案が存在しない時に返されるエラーです。',
    'DualKeyMultiSig_ProposalExpired': 'キーローテーション提案の有効期限が切れた時に返されるエラーです。',
    'DualKeyMultiSig_ProposalAlreadyExecuted': 'キーローテーション提案が既に実行されている時に返されるエラーです。',
    'DualKeyMultiSig_AlreadyApproved': 'キーローテーション提案が既に承認されている時に返されるエラーです。',
    'DualKeyMultiSig_InsufficientApprovals': 'キーローテーションの承認数が不足している時に返されるエラーです。',
    'DualKeyMultiSig_ProposerCannotApprove': '提案者が自身の提案を承認しようとした時に返されるエラーです。',

    // Multi Admin Access Control Errors
    'MultiAdminAccessControl_InvalidAccount': '無効なアカウントが指定された時に返されるエラーです。',
    'MultiAdminAccessControl_MissingRole': '必要なロールを持っていない時に返されるエラーです。',
    'MultiAdminAccessControl_NoAdminRole': '管理者ロールが存在しない時に返されるエラーです。',
    'MultiAdminAccessControl_AdminRoleAlreadyExists': '既に存在する管理者ロールを追加しようとした時に返されるエラーです。',
    'MultiAdminAccessControl_AdminRoleNotFound': '管理者ロールが見つからない時に返されるエラーです。',

    // Role Manager Errors
    'RoleManager_InvalidAccount': '無効なアカウントが指定された時に返されるエラーです。',
    'RoleManager_InvalidRole': '無効なロールが指定された時に返されるエラーです。',
    'RoleManager_RequiresMultiSig': 'マルチシグ経由での操作が必要な時に返されるエラーです。',
    'RoleManager_UnauthorizedRoleAdmin': 'ロール管理者権限がない時に返されるエラーです。',

    // Dictionary/Implementation Errors
    'InvalidDictionary': '無効なディクショナリが指定された時に返されるエラーです。',
    'InvalidImplementation': '無効な実装が指定された時に返されるエラーです。',
    'ImplementationNotFound': '実装が見つからない時に返されるエラーです。',
    'FunctionSelectorNotFound': '関数セレクタが見つからない時に返されるエラーです。',

    // Other Errors
    'InvalidName': '無効な名前が指定された時に返されるエラーです。',
    'Stablecoin_InvalidAddress': 'ステーブルコインで無効なアドレスが指定された時に返されるエラーです。',
  };

  if (ERROR_DESC[errorName]) {
    return ERROR_DESC[errorName];
  }

  // Pattern-based descriptions
  if (errorName.includes('Invalid')) {
    return `無効な値が指定された時に返されるエラーです。`;
  }
  if (errorName.includes('Unauthorized') || errorName.includes('NotAuthorized')) {
    return `権限のない操作が試みられた時に返されるエラーです。`;
  }
  if (errorName.includes('NotFound')) {
    return `指定されたリソースが見つからない時に返されるエラーです。`;
  }
  if (errorName.includes('Already')) {
    return `既に存在するリソースを作成しようとした時に返されるエラーです。`;
  }
  if (errorName.includes('Insufficient')) {
    return `リソースが不足している時に返されるエラーです。`;
  }
  if (errorName.includes('Expired')) {
    return `有効期限が切れた時に返されるエラーです。`;
  }

  // Default
  return `${errorName}が発生した時に返されるエラーです。`;
}

/**
 * 構造体名から意味のある説明を生成
 */
function getStructDescription(structName) {
  const STRUCT_DESC = {
    'DualKey': 'プライマリキーとバックアップキーの2つのアドレスと初期化状態を保持するという構造体です。キーローテーション機能で使用されます。',
    'KeyRotationProposal': '提案者、新しいキーアドレス、承認状態、実行状態、有効期限などを保持するという構造体です。',
    'BankRoleProposal': '提案タイプ、対象銀行、ロール、アカウント、承認状態などを保持するという構造体です。',
    'ERC20Storage': '残高マッピング、許可量マッピング、総供給量などを保持するという構造体です。',
  };

  if (STRUCT_DESC[structName]) {
    return STRUCT_DESC[structName];
  }

  // Pattern-based descriptions
  if (structName.includes('Proposal')) {
    return `提案に関連するデータを保持するという構造体です。`;
  }
  if (structName.includes('Storage')) {
    return `ストレージに関連するデータを保持するという構造体です。`;
  }
  if (structName.includes('Config')) {
    return `設定に関連するデータを保持するという構造体です。`;
  }

  // Default
  return `関連するデータフィールドを保持するという構造体です。`;
}

/**
 * Modifier名から意味のある説明を生成
 */
function getModifierDescription(modifierName) {
  const MODIFIER_DESC = {
    'onlyRole': '指定されたロールを持つアカウントのみが関数を実行できます。AccessControlパターンで使用される標準的な修飾子です。ロールを持たないアカウントが呼び出すとAccessControlUnauthorizedAccountがスローされます。',
    'onlySigner': 'マルチシグの署名者のみが関数を実行できます。署名者として登録されていないアカウントが呼び出すとMultiSig_NotSignerがスローされます。',
    'whenBankNotPaused': '指定された銀行が一時停止されていない場合のみ関数を実行できます。銀行が一時停止中の場合はBankPauser_BankAlreadyPausedがスローされます。',
    'whenBankPaused': '指定された銀行が一時停止中の場合のみ関数を実行できます。銀行が一時停止されていない場合はBankPauser_BankNotPausedがスローされます。',
    'whenNotPaused': 'コントラクトが一時停止されていない場合のみ関数を実行できます。一時停止中の場合はEnforcedPauseがスローされます。',
    'whenPaused': 'コントラクトが一時停止中の場合のみ関数を実行できます。一時停止されていない場合はExpectedPauseがスローされます。',
    'onlyOwner': '所有者のみが関数を実行できます。所有者以外が呼び出すとOwnableUnauthorizedAccountがスローされます。',
    'nonReentrant': '再入攻撃を防止します。関数の実行中に同じ関数が再度呼び出されるとReentrancyGuardReentrantCallがスローされます。',
    'initializer': 'コントラクトの初期化時のみ実行可能です。既に初期化済みの場合はInvalidInitializationがスローされます。',
    'onlyProxy': 'プロキシ経由でのみ呼び出し可能です。直接呼び出しはUUPSUnauthorizedCallContextがスローされます。',
  };

  if (MODIFIER_DESC[modifierName]) {
    return MODIFIER_DESC[modifierName];
  }

  // Pattern-based descriptions
  if (modifierName.startsWith('only')) {
    const target = modifierName.replace(/^only/, '');
    return `${target}のみが関数を実行できるよう制限します。権限がない場合はエラーがスローされます。`;
  }
  if (modifierName.startsWith('when')) {
    const condition = modifierName.replace(/^when/, '');
    return `${condition}の条件が満たされた場合のみ関数を実行できます。条件が満たされない場合はエラーがスローされます。`;
  }

  // Default
  return `${modifierName}修飾子は関数の実行前後に特定の条件をチェックまたは処理を追加します。`;
}

/**
 * 関数の説明を自動生成
 */
function generateFunctionDescription(funcName, inputs, outputs, stateMutability) {
  // ロール定数
  if (funcName.endsWith('_ROLE') && funcName === funcName.toUpperCase()) {
    const roleName = funcName.replace(/_ROLE$/, '').toLowerCase().replace(/_/g, ' ');
    return `${funcName} ロールの識別子を取得します。\n\nこのロールは ${roleName} に関連する操作の権限を管理します。`;
  }

  // 定数 (すべて大文字)
  if (funcName === funcName.toUpperCase() && funcName.includes('_')) {
    return `${funcName} 定数の値を取得します。`;
  }

  // ERC20標準関数
  const erc20Descriptions = {
    'name': 'トークンの名前を取得します。\n\nERC20標準関数です。',
    'symbol': 'トークンのシンボルを取得します。\n\nERC20標準関数です。',
    'decimals': 'トークンの小数点以下の桁数を取得します。\n\nERC20標準関数です。通常は18です。',
    'totalSupply': 'トークンの総供給量を取得します。\n\nERC20標準関数です。',
    'balanceOf': '指定されたアカウントのトークン残高を取得します。\n\nERC20標準関数です。',
    'allowance': 'spenderがownerから使用を許可されているトークン量を取得します。\n\nERC20標準関数です。',
    'transfer': '指定されたアドレスにトークンを転送します。\n\nERC20標準関数です。',
    'transferFrom': 'fromからtoへトークンを転送します。事前にallowanceが設定されている必要があります。\n\nERC20標準関数です。',
    'approve': 'spenderが指定された量のトークンを使用することを承認します。\n\nERC20標準関数です。'
  };

  if (erc20Descriptions[funcName]) {
    return erc20Descriptions[funcName];
  }

  // Pausable関数
  const pausableDescriptions = {
    'paused': 'コントラクトが一時停止状態かどうかを確認します。',
    'pause': 'コントラクトを一時停止します。\n\nPAUSER_ROLEを持つアカウントのみが実行可能です。',
    'unpause': 'コントラクトの一時停止を解除します。\n\nPAUSER_ROLEを持つアカウントのみが実行可能です。'
  };

  if (pausableDescriptions[funcName]) {
    return pausableDescriptions[funcName];
  }

  // AccessControl関数
  const accessControlDescriptions = {
    'hasRole': '指定されたアカウントが指定されたロールを持っているかどうかを確認します。',
    'grantRole': '指定されたアカウントにロールを付与します。\n\nロールの管理者のみが実行可能です。',
    'revokeRole': '指定されたアカウントからロールを取り消します。\n\nロールの管理者のみが実行可能です。',
    'renounceRole': '呼び出し元が持つロールを放棄します。',
    'getRoleAdmin': '指定されたロールの管理者ロールを取得します。',
    'supportsInterface': '指定されたインターフェースをサポートしているかどうかを確認します。\n\nERC165標準関数です。'
  };

  if (accessControlDescriptions[funcName]) {
    return accessControlDescriptions[funcName];
  }

  // Bank関連関数
  if (funcName.startsWith('pauseBank')) {
    return '指定されたBankを一時停止します。\n\nBANK_PAUSER_ROLEまたは該当Bankの一時停止権限を持つアカウントのみが実行可能です。';
  }
  if (funcName.startsWith('unpauseBank')) {
    return '指定されたBankの一時停止を解除します。\n\nBANK_PAUSER_ROLEまたは該当Bankの一時停止権限を持つアカウントのみが実行可能です。';
  }
  if (funcName.startsWith('isBankPaused')) {
    return '指定されたBankが一時停止状態かどうかを確認します。';
  }

  // Getter関数
  if (funcName.startsWith('get')) {
    const target = funcName.replace(/^get/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${target} を取得します。`;
  }

  // Boolean関数
  if (funcName.startsWith('is')) {
    const condition = funcName.replace(/^is/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${condition} かどうかを確認します。`;
  }

  if (funcName.startsWith('has')) {
    const condition = funcName.replace(/^has/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${condition} を持っているかどうかを確認します。`;
  }

  if (funcName.startsWith('can')) {
    const condition = funcName.replace(/^can/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${condition} が可能かどうかを確認します。`;
  }

  // Proposal関連関数
  if (funcName === 'propose') {
    return '提案を作成します。\n\nマルチシグ承認が必要な操作です。';
  }
  if (funcName.startsWith('propose')) {
    const action = funcName.replace(/^propose/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${action} の提案を作成します。\n\nマルチシグ承認が必要な操作です。`;
  }

  if (funcName === 'approve') {
    return '提案を承認します。\n\n承認者の一人として提案を承認します。';
  }
  if (funcName.startsWith('approve')) {
    const action = funcName.replace(/^approve/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${action} の提案を承認します。\n\n承認者の一人として提案を承認します。`;
  }

  if (funcName === 'execute') {
    return '提案を実行します。\n\n必要な承認数が揃った後に実行可能です。';
  }
  if (funcName.startsWith('execute')) {
    const action = funcName.replace(/^execute/, '').replace(/([A-Z])/g, ' $1').trim().toLowerCase();
    return `${action} の提案を実行します。\n\n必要な承認数が揃った後に実行可能です。`;
  }

  // Initialize関数
  if (funcName === 'initialize' || funcName.startsWith('initialize')) {
    return 'コントラクトを初期化します。\n\nプロキシ経由で一度だけ呼び出し可能です。';
  }

  // Implementation関数
  if (funcName === 'implementation') {
    return '現在の実装コントラクトのアドレスを取得します。';
  }

  // デフォルト
  return `${funcName}`;
}

/**
 * 一般的なエラーのリストを取得（書き込み関数用）
 */
function getCommonErrors(funcName, inputs) {
  const errors = [];

  // アドレスパラメータがある場合
  if (inputs.some(input => input.type === 'address')) {
    errors.push('InvalidAddress');
  }

  // 金額パラメータがある場合
  if (inputs.some(input => input.name && (input.name.includes('amount') || input.name.includes('value')))) {
    errors.push('AmountZero');
  }

  // ロール関連関数
  if (funcName.includes('Role') || funcName.includes('grant') || funcName.includes('revoke')) {
    errors.push('AccessControlUnauthorizedAccount');
  }

  // 一時停止関連
  if (funcName.includes('pause') || funcName.includes('Pause')) {
    errors.push('EnforcedPause');
  }

  // Bank関連
  if (funcName.includes('Bank') || funcName.includes('bank')) {
    errors.push('BankNotFound');
    errors.push('BankInactive');
  }

  return errors;
}

/**
 * OpenAPI YAML骨格を生成
 */
function generateOpenAPIYAML(contractName, abi, source) {
  const inheritance = extractInheritance(source);
  const functions = abi.filter(item => item.type === 'function');
  const events = abi.filter(item => item.type === 'event');
  const errors = abi.filter(item => item.type === 'error');
  const structs = extractStructs(source);
  const modifiers = extractModifiers(source);
  const stateVariables = extractStateVariables(source);
  const constants = extractConstants(source);
  const mappings = extractMappings(source);

  const viewFunctions = functions.filter(f => f.stateMutability === 'view' || f.stateMutability === 'pure');
  const writeFunctions = functions.filter(f => f.stateMutability !== 'view' && f.stateMutability !== 'pure');

  let yaml = `# file: docs/contract/${contractName}/${contractName}.openapi.yaml
# Generated by: contract-spec-generator skill (enhanced from skeleton)

openapi: 3.0.3
info:
  title: "${contractName} Solidity Interface"
  version: "1.0.0"
  description: |
    ${contractName} コントラクトの Solidity インターフェイスを OpenAPI 形式で表現した仕様です。
`;

  // 継承情報
  if (inheritance.length > 0) {
    yaml += `\n    このコントラクトは以下のコントラクトを継承しています。\n\n`;
    inheritance.forEach(parent => {
      yaml += `    ${parent}。\n\n`;
    });
  }

  // 関数カテゴリの確認（変数、定数、Mappingに該当する関数があるか）
  const hasVariableGetters = functions.some(f => getFunctionCategory(f.name, f.inputs, f.stateMutability, stateVariables, constants, mappings) === '変数');
  const hasConstantGetters = functions.some(f => getFunctionCategory(f.name, f.inputs, f.stateMutability, stateVariables, constants, mappings) === '定数');
  const hasMappingGetters = functions.some(f => getFunctionCategory(f.name, f.inputs, f.stateMutability, stateVariables, constants, mappings) === 'Mapping');

  // タグ定義
  yaml += `
tags:
  - name: 読み取り関数
    description: ステートを変更せず、コントラクト内の情報を取得する関数。
  - name: 書き込み関数
    description: ステートを変更する関数。
`;

  if (hasVariableGetters) {
    yaml += `  - name: 変数
`;
  }

  if (hasConstantGetters) {
    yaml += `  - name: 定数
`;
  }

  if (hasMappingGetters) {
    yaml += `  - name: Mapping
`;
  }

  yaml += `  - name: イベント
  - name: エラー
`;

  if (structs.length > 0) {
    yaml += `  - name: 構造体
`;
  }

  if (modifiers.length > 0) {
    yaml += `  - name: Modifier
`;
  }

  // タググループ
  yaml += `
x-tagGroups:
  - name: 関数
    tags:
      - 読み取り関数
      - 書き込み関数
`;

  if (hasVariableGetters) {
    yaml += `  - name: 変数
    tags:
      - 変数
`;
  }

  if (hasConstantGetters) {
    yaml += `  - name: 定数
    tags:
      - 定数
`;
  }

  if (hasMappingGetters) {
    yaml += `  - name: Mapping
    tags:
      - Mapping
`;
  }

  yaml += `  - name: イベント
    tags:
      - イベント
  - name: エラー
    tags:
      - エラー
`;

  if (structs.length > 0) {
    yaml += `  - name: 構造体
    tags:
      - 構造体
`;
  }

  if (modifiers.length > 0) {
    yaml += `  - name: Modifier
    tags:
      - Modifier
`;
  }

  yaml += `\npaths:\n`;

  // 関数名の出現回数をカウント（オーバーロード検出）
  const functionNameCount = {};
  functions.forEach(func => {
    functionNameCount[func.name] = (functionNameCount[func.name] || 0) + 1;
  });

  const functionNameUsage = {};

  // 関数パスを生成
  for (const func of functions) {
    const isView = func.stateMutability === 'view' || func.stateMutability === 'pure';
    const method = isView ? 'get' : 'post';

    functionNameUsage[func.name] = (functionNameUsage[func.name] || 0) + 1;
    const overloadIndex = functionNameUsage[func.name];
    const hasOverload = functionNameCount[func.name] > 1;
    const pathSuffix = hasOverload && overloadIndex > 1 ? `_${overloadIndex - 1}` : '';

    const description = generateFunctionDescription(func.name, func.inputs, func.outputs, func.stateMutability);

    yaml += `  /${func.name}${pathSuffix}:\n`;
    yaml += `    ${method}:\n`;
    yaml += `      summary: "${func.name}${hasOverload ? ` (オーバーロード ${overloadIndex})` : ''}"\n`;
    yaml += `      description: |\n`;
    description.split('\n').forEach(line => {
      yaml += `        ${line}\n`;
    });
    yaml += `      operationId: ${func.name}${pathSuffix}\n`;
    yaml += `      tags:\n`;

    // 関数カテゴリを判定（変数、定数、Mappingのgetterかどうか）
    const funcCategory = getFunctionCategory(func.name, func.inputs, func.stateMutability, stateVariables, constants, mappings);
    if (funcCategory) {
      yaml += `        - ${funcCategory}\n`;
    } else {
      yaml += `        - ${isView ? '読み取り関数' : '書き込み関数'}\n`;
    }

    // パラメータ
    if (func.inputs && func.inputs.length > 0) {
      yaml += `      parameters:\n`;
      for (const input of func.inputs) {
        const paramName = input.name || 'param';
        const typeMapping = getSolidityTypeMapping(input.type);

        yaml += `        - name: ${paramName}\n`;
        yaml += `          in: query\n`;
        yaml += `          required: true\n`;
        yaml += `          schema:\n`;
        yaml += `            type: ${typeMapping.type}\n`;
        if (typeMapping.pattern) {
          yaml += `            pattern: "${typeMapping.pattern}"\n`;
        }
        yaml += `          description: "${getParamDescription(paramName)}"\n`;
        if (typeMapping.example) {
          yaml += `          example: "${typeMapping.example}"\n`;
        }
      }
    }

    // レスポンス
    yaml += `      responses:\n`;
    yaml += `        "200":\n`;
    yaml += `          description: "正常終了時のレスポンスです。"\n`;
    yaml += `          content:\n`;
    yaml += `            application/json:\n`;
    yaml += `              schema:\n`;
    yaml += `                type: object\n`;

    if (func.outputs && func.outputs.length > 0) {
      yaml += `                properties:\n`;
      for (let i = 0; i < func.outputs.length; i++) {
        const output = func.outputs[i];
        const propName = output.name || `result${i}`;
        const typeMapping = getSolidityTypeMapping(output.type);

        yaml += `                  ${propName}:\n`;
        yaml += `                    type: ${typeMapping.type}\n`;
        if (typeMapping.pattern) {
          yaml += `                    pattern: "${typeMapping.pattern}"\n`;
        }
        yaml += `                    description: "${getReturnDescription(func.name, output.name)}"\n`;
        if (typeMapping.example) {
          yaml += `                    example: "${typeMapping.example}"\n`;
        }
      }
    }

    // 500エラーレスポンス（書き込み関数のみ）
    if (!isView) {
      const commonErrors = getCommonErrors(func.name, func.inputs);
      if (commonErrors.length > 0) {
        yaml += `        "500":\n`;
        yaml += `          description: "この関数で発生しうるエラーの一覧です。\\n\\n`;
        commonErrors.forEach(err => {
          yaml += `・${err}\\n\\n`;
        });
        yaml += `"\n`;
        yaml += `          content:\n`;
        yaml += `            application/json:\n`;
        yaml += `              schema:\n`;
        yaml += `                $ref: '#/components/schemas/ErrorResponse'\n`;
      }
    }

    yaml += `\n`;
  }

  // イベントパス
  const eventNameCount = {};
  events.forEach(event => {
    eventNameCount[event.name] = (eventNameCount[event.name] || 0) + 1;
  });

  const eventNameUsage = {};
  for (const event of events) {
    eventNameUsage[event.name] = (eventNameUsage[event.name] || 0) + 1;
    const overloadIndex = eventNameUsage[event.name];
    const hasOverload = eventNameCount[event.name] > 1;
    const eventSuffix = hasOverload && overloadIndex > 1 ? `_${overloadIndex - 1}` : '';

    const eventDesc = getEventDescription(event.name);
    yaml += `  /events/${event.name}${eventSuffix}:\n`;
    yaml += `    get:\n`;
    yaml += `      summary: "${event.name}${hasOverload ? ` (オーバーロード ${overloadIndex})` : ''}"\n`;
    yaml += `      description: |\n`;
    yaml += `        ${eventDesc}\n`;

    if (event.inputs && event.inputs.length > 0) {
      yaml += `        \n`;
      yaml += `        **パラメータ:**\n`;
      for (const input of event.inputs) {
        yaml += `        - \`${input.name}\` (${input.type})${input.indexed ? ' - indexed' : ''}\n`;
      }
    }

    yaml += `      operationId: event_${event.name}${eventSuffix}\n`;
    yaml += `      tags:\n`;
    yaml += `        - イベント\n`;
    yaml += `      responses:\n`;
    yaml += `        "200":\n`;
    yaml += `          description: "${eventDesc}"\n`;
    yaml += `          content:\n`;
    yaml += `            application/json:\n`;
    yaml += `              schema:\n`;
    yaml += `                $ref: '#/components/schemas/${event.name}Event${eventSuffix}'\n`;
    yaml += `\n`;
  }

  // エラーパス
  for (const error of errors) {
    const errorDesc = getErrorDescription(error.name);
    yaml += `  /errors/${error.name}:\n`;
    yaml += `    get:\n`;
    yaml += `      summary: "${error.name}"\n`;
    yaml += `      description: |\n`;
    yaml += `        ${errorDesc}\n`;

    if (error.inputs && error.inputs.length > 0) {
      yaml += `        \n`;
      yaml += `        **パラメータ:**\n`;
      for (const input of error.inputs) {
        yaml += `        - \`${input.name}\` (${input.type})\n`;
      }
    }

    yaml += `      operationId: error_${error.name}\n`;
    yaml += `      tags:\n`;
    yaml += `        - エラー\n`;
    yaml += `      responses:\n`;
    yaml += `        "200":\n`;
    yaml += `          description: "${errorDesc}"\n`;
    yaml += `          content:\n`;
    yaml += `            application/json:\n`;
    yaml += `              schema:\n`;
    yaml += `                type: object\n`;
    yaml += `                properties:\n`;
    yaml += `                  name:\n`;
    yaml += `                    type: string\n`;
    yaml += `                    example: "${error.name}"\n`;

    if (error.inputs && error.inputs.length > 0) {
      yaml += `                  parameters:\n`;
      yaml += `                    type: object\n`;
      yaml += `                    properties:\n`;
      for (const input of error.inputs) {
        const typeMapping = getSolidityTypeMapping(input.type);
        yaml += `                      ${input.name}:\n`;
        yaml += `                        type: string\n`;
        if (typeMapping.pattern) {
          yaml += `                        pattern: "${typeMapping.pattern}"\n`;
        }
        yaml += `                        description: "${getParamDescription(input.name)}"\n`;
      }
    }
    yaml += `\n`;
  }

  // 構造体パス
  for (const struct of structs) {
    const structDesc = getStructDescription(struct.name);
    yaml += `  /structs/${struct.name}:\n`;
    yaml += `    get:\n`;
    yaml += `      summary: "${struct.name}"\n`;
    yaml += `      description: |\n`;
    yaml += `        ${structDesc}\n`;

    if (struct.fields && struct.fields.length > 0) {
      yaml += `        \n`;
      yaml += `        **フィールド:**\n`;
      for (const field of struct.fields) {
        yaml += `        - ${field.name} (${field.type})\n`;
      }
    }

    yaml += `      operationId: struct_${struct.name}\n`;
    yaml += `      tags:\n`;
    yaml += `        - 構造体\n`;
    yaml += `      responses:\n`;
    yaml += `        "200":\n`;
    yaml += `          description: "${structDesc}"\n`;
    yaml += `          content:\n`;
    yaml += `            application/json:\n`;
    yaml += `              schema:\n`;
    yaml += `                $ref: '#/components/schemas/${struct.name}Struct'\n`;
    yaml += `\n`;
  }

  // modifierパス
  for (const modifier of modifiers) {
    const modifierDesc = getModifierDescription(modifier.name);
    yaml += `  /modifiers/${modifier.name}:\n`;
    yaml += `    get:\n`;
    yaml += `      summary: "${modifier.name}"\n`;
    yaml += `      description: |\n`;
    yaml += `        ${modifierDesc}\n`;

    if (modifier.params && modifier.params.length > 0) {
      yaml += `        \n`;
      yaml += `        **パラメータ:**\n`;
      for (const param of modifier.params) {
        yaml += `        - ${param.name} (${param.type})\n`;
      }
    }

    yaml += `      operationId: modifier_${modifier.name}\n`;
    yaml += `      tags:\n`;
    yaml += `        - Modifier\n`;
    yaml += `      responses:\n`;
    yaml += `        "200":\n`;
    yaml += `          description: "${modifierDesc}"\n`;
    yaml += `          content:\n`;
    yaml += `            application/json:\n`;
    yaml += `              schema:\n`;
    yaml += `                type: object\n`;
    yaml += `                properties:\n`;
    yaml += `                  name:\n`;
    yaml += `                    type: string\n`;
    yaml += `                    example: "${modifier.name}"\n`;

    if (modifier.params && modifier.params.length > 0) {
      yaml += `                  parameters:\n`;
      yaml += `                    type: array\n`;
      yaml += `                    items:\n`;
      yaml += `                      type: object\n`;
      yaml += `                      properties:\n`;
      yaml += `                        name:\n`;
      yaml += `                          type: string\n`;
      yaml += `                        type:\n`;
      yaml += `                          type: string\n`;
    }
    yaml += `\n`;
  }

  // Componentsスキーマ
  yaml += `components:\n`;
  yaml += `  schemas:\n`;
  yaml += `    ErrorResponse:\n`;
  yaml += `      type: object\n`;
  yaml += `      description: "コントラクト呼び出し時のエラー情報を表現する共通スキーマです。"\n`;
  yaml += `      properties:\n`;
  yaml += `        message:\n`;
  yaml += `          type: string\n`;
  yaml += `          description: "カスタムエラー名または \`revert\` / \`require\` のメッセージ文字列をそのまま格納します。"\n`;
  yaml += `        data:\n`;
  yaml += `          type: object\n`;
  yaml += `          description: "追加情報（任意）です。"\n`;

  // イベントスキーマ
  for (const key in eventNameUsage) {
    eventNameUsage[key] = 0;
  }

  for (const event of events) {
    eventNameUsage[event.name] = (eventNameUsage[event.name] || 0) + 1;
    const overloadIndex = eventNameUsage[event.name];
    const hasOverload = eventNameCount[event.name] > 1;
    const eventSuffix = hasOverload && overloadIndex > 1 ? `_${overloadIndex - 1}` : '';
    const eventSchemaName = `${event.name}Event${eventSuffix}`;

    yaml += `\n    ${eventSchemaName}:\n`;
    yaml += `      type: object\n`;
    yaml += `      description: "${event.name}${hasOverload ? ` (オーバーロード ${overloadIndex})` : ''}"\n`;

    if (event.inputs && event.inputs.length > 0) {
      yaml += `      properties:\n`;
      for (const input of event.inputs) {
        const typeMapping = getSolidityTypeMapping(input.type);
        yaml += `        ${input.name}:\n`;
        yaml += `          type: string\n`;
        if (typeMapping.pattern) {
          yaml += `          pattern: "${typeMapping.pattern}"\n`;
        }
        yaml += `          description: "${input.indexed ? 'インデックス付き。' : ''}${getParamDescription(input.name)}"\n`;
        if (typeMapping.example) {
          yaml += `          example: "${typeMapping.example}"\n`;
        }
      }
    }
  }

  // 構造体スキーマ
  for (const struct of structs) {
    yaml += `\n    ${struct.name}Struct:\n`;
    yaml += `      type: object\n`;
    yaml += `      description: "${struct.name} 構造体"\n`;

    if (struct.fields && struct.fields.length > 0) {
      yaml += `      properties:\n`;
      for (const field of struct.fields) {
        const typeMapping = getSolidityTypeMapping(field.type);
        yaml += `        ${field.name}:\n`;
        yaml += `          type: ${typeMapping.type}\n`;
        if (typeMapping.pattern) {
          yaml += `          pattern: "${typeMapping.pattern}"\n`;
        }
        yaml += `          description: "${getParamDescription(field.name)}"\n`;
        if (typeMapping.example) {
          yaml += `          example: "${typeMapping.example}"\n`;
        }
      }
    }
  }

  return yaml;
}

/**
 * Swagger JSON骨格を生成
 */
function generateSwaggerJSON(contractName, abi, source) {
  const inheritance = extractInheritance(source);
  const functions = abi.filter(item => item.type === 'function');
  const events = abi.filter(item => item.type === 'event');
  const errors = abi.filter(item => item.type === 'error');
  const structs = extractStructs(source);
  const modifiers = extractModifiers(source);
  const stateVariables = extractStateVariables(source);
  const constants = extractConstants(source);
  const mappings = extractMappings(source);

  const viewFunctions = functions.filter(f => f.stateMutability === 'view' || f.stateMutability === 'pure');
  const writeFunctions = functions.filter(f => f.stateMutability !== 'view' && f.stateMutability !== 'pure');

  // 関数カテゴリの確認（変数、定数、Mappingに該当する関数があるか）
  const hasVariableGetters = functions.some(f => getFunctionCategory(f.name, f.inputs, f.stateMutability, stateVariables, constants, mappings) === '変数');
  const hasConstantGetters = functions.some(f => getFunctionCategory(f.name, f.inputs, f.stateMutability, stateVariables, constants, mappings) === '定数');
  const hasMappingGetters = functions.some(f => getFunctionCategory(f.name, f.inputs, f.stateMutability, stateVariables, constants, mappings) === 'Mapping');

  let description = `${contractName} コントラクトの Solidity インターフェイスを Swagger 2.0 形式で表現した仕様です。`;

  if (inheritance.length > 0) {
    description += `\n\nこのコントラクトは以下のコントラクトを継承しています。\n\n`;
    description += inheritance.map(p => `${p}。`).join('\n\n');
  }


  // タグ定義
  const tags = [
    { name: '読み取り関数', description: 'ステートを変更せず、コントラクト内の情報を取得する関数。' },
    { name: '書き込み関数', description: 'ステートを変更する関数。' }
  ];

  if (hasVariableGetters) {
    tags.push({ name: '変数' });
  }

  if (hasConstantGetters) {
    tags.push({ name: '定数' });
  }

  if (hasMappingGetters) {
    tags.push({ name: 'Mapping' });
  }

  tags.push({ name: 'イベント' });
  tags.push({ name: 'エラー' });

  if (structs.length > 0) {
    tags.push({ name: '構造体' });
  }

  if (modifiers.length > 0) {
    tags.push({ name: 'Modifier' });
  }

  // x-tagGroups構築
  const tagGroups = [
    { name: '関数', tags: ['読み取り関数', '書き込み関数'] }
  ];

  if (hasVariableGetters) {
    tagGroups.push({ name: '変数', tags: ['変数'] });
  }

  if (hasConstantGetters) {
    tagGroups.push({ name: '定数', tags: ['定数'] });
  }

  if (hasMappingGetters) {
    tagGroups.push({ name: 'Mapping', tags: ['Mapping'] });
  }

  tagGroups.push({ name: 'イベント', tags: ['イベント'] });
  tagGroups.push({ name: 'エラー', tags: ['エラー'] });

  if (structs.length > 0) {
    tagGroups.push({ name: '構造体', tags: ['構造体'] });
  }

  if (modifiers.length > 0) {
    tagGroups.push({ name: 'Modifier', tags: ['Modifier'] });
  }

  const swagger = {
    swagger: '2.0',
    info: {
      title: `${contractName} Solidity Interface`,
      version: '1.0.0',
      description: description
    },
    host: 'example.com',
    basePath: '/',
    schemes: ['https'],
    tags: tags,
    'x-tagGroups': tagGroups,
    paths: {},
    definitions: {
      ErrorResponse: {
        type: 'object',
        description: 'コントラクト呼び出し時のエラー情報を表現する共通スキーマです。',
        properties: {
          message: {
            type: 'string',
            description: 'カスタムエラー名または `revert` / `require` のメッセージ文字列をそのまま格納します。'
          },
          data: {
            type: 'object',
            description: '追加情報（任意）です。'
          }
        }
      }
    }
  };

  // 関数名カウント
  const functionNameCount = {};
  functions.forEach(func => {
    functionNameCount[func.name] = (functionNameCount[func.name] || 0) + 1;
  });

  const functionNameUsage = {};

  // 関数パス
  for (const func of functions) {
    const isView = func.stateMutability === 'view' || func.stateMutability === 'pure';
    const method = isView ? 'get' : 'post';

    functionNameUsage[func.name] = (functionNameUsage[func.name] || 0) + 1;
    const overloadIndex = functionNameUsage[func.name];
    const hasOverload = functionNameCount[func.name] > 1;
    const pathSuffix = hasOverload && overloadIndex > 1 ? `_${overloadIndex - 1}` : '';
    const path = `/${func.name}${pathSuffix}`;

    const description = generateFunctionDescription(func.name, func.inputs, func.outputs, func.stateMutability);

    // 関数カテゴリを判定（変数、定数、Mappingのgetterかどうか）
    const funcCategory = getFunctionCategory(func.name, func.inputs, func.stateMutability, stateVariables, constants, mappings);
    const funcTag = funcCategory || (isView ? '読み取り関数' : '書き込み関数');

    if (!swagger.paths[path]) {
      swagger.paths[path] = {};
    }

    swagger.paths[path][method] = {
      summary: `${func.name}${hasOverload ? ` (オーバーロード ${overloadIndex})` : ''}`,
      description: description,
      operationId: `${func.name}${pathSuffix}`,
      tags: [funcTag],
      produces: ['application/json'],
      responses: {
        '200': {
          description: '正常終了時のレスポンスです。',
          schema: {
            type: 'object',
            properties: {}
          }
        }
      }
    };

    // パラメータ
    if (func.inputs && func.inputs.length > 0) {
      swagger.paths[path][method].parameters = [];
      for (const input of func.inputs) {
        const paramName = input.name || 'param';
        swagger.paths[path][method].parameters.push({
          name: paramName,
          in: 'query',
          required: true,
          type: 'string',
          description: getParamDescription(paramName)
        });
      }
    }

    // 出力プロパティ
    if (func.outputs && func.outputs.length > 0) {
      for (let i = 0; i < func.outputs.length; i++) {
        const output = func.outputs[i];
        const propName = output.name || `result${i}`;
        swagger.paths[path][method].responses['200'].schema.properties[propName] = {
          type: 'string',
          description: getReturnDescription(func.name, output.name)
        };
      }
    }

    // 500エラーレスポンス（書き込み関数のみ）
    if (!isView) {
      const commonErrors = getCommonErrors(func.name, func.inputs);
      if (commonErrors.length > 0) {
        let errorDescription = 'この関数で発生しうるエラーの一覧です。\n\n';
        commonErrors.forEach(err => {
          errorDescription += `・${err}\n\n`;
        });

        swagger.paths[path][method].responses['500'] = {
          description: errorDescription,
          schema: {
            $ref: '#/definitions/ErrorResponse'
          },
          examples: {
            'application/json': {
              message: commonErrors[0],
              data: {}
            }
          }
        };
      }
    }
  }

  // イベントパス
  const eventNameCount = {};
  events.forEach(event => {
    eventNameCount[event.name] = (eventNameCount[event.name] || 0) + 1;
  });

  const eventNameUsage = {};
  for (const event of events) {
    eventNameUsage[event.name] = (eventNameUsage[event.name] || 0) + 1;
    const overloadIndex = eventNameUsage[event.name];
    const hasOverload = eventNameCount[event.name] > 1;
    const eventSuffix = hasOverload && overloadIndex > 1 ? `_${overloadIndex - 1}` : '';

    const eventDesc = getEventDescription(event.name);
    swagger.paths[`/events/${event.name}${eventSuffix}`] = {
      get: {
        summary: `${event.name}${hasOverload ? ` (オーバーロード ${overloadIndex})` : ''}`,
        description: eventDesc,
        operationId: `event_${event.name}${eventSuffix}`,
        tags: ['イベント'],
        produces: ['application/json'],
        responses: {
          '200': {
            description: eventDesc,
            schema: {
              $ref: `#/definitions/${event.name}Event${eventSuffix}`
            }
          }
        }
      }
    };
  }

  // エラーパス
  for (const error of errors) {
    const errorSchema = {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          example: error.name
        }
      }
    };

    if (error.inputs && error.inputs.length > 0) {
      errorSchema.properties.parameters = {
        type: 'object',
        properties: {}
      };
      for (const input of error.inputs) {
        errorSchema.properties.parameters.properties[input.name] = {
          type: 'string',
          description: getParamDescription(input.name)
        };
      }
    }

    const errorDesc = getErrorDescription(error.name);
    swagger.paths[`/errors/${error.name}`] = {
      get: {
        summary: error.name,
        description: errorDesc,
        operationId: `error_${error.name}`,
        tags: ['エラー'],
        produces: ['application/json'],
        responses: {
          '200': {
            description: errorDesc,
            schema: errorSchema
          }
        }
      }
    };
  }

  // 構造体パス
  for (const struct of structs) {
    const structSchema = {
      type: 'object',
      properties: {}
    };

    if (struct.fields && struct.fields.length > 0) {
      for (const field of struct.fields) {
        structSchema.properties[field.name] = {
          type: 'string',
          description: getParamDescription(field.name)
        };
      }
    }

    const structDesc = getStructDescription(struct.name);
    swagger.paths[`/structs/${struct.name}`] = {
      get: {
        summary: struct.name,
        description: structDesc,
        operationId: `struct_${struct.name}`,
        tags: ['構造体'],
        produces: ['application/json'],
        responses: {
          '200': {
            description: structDesc,
            schema: {
              $ref: `#/definitions/${struct.name}Struct`
            }
          }
        }
      }
    };
  }

  // modifierパス
  for (const modifier of modifiers) {
    const modifierSchema = {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          example: modifier.name
        }
      }
    };

    if (modifier.params && modifier.params.length > 0) {
      modifierSchema.properties.parameters = {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            type: { type: 'string' }
          }
        }
      };
    }

    const modifierDesc = getModifierDescription(modifier.name);
    swagger.paths[`/modifiers/${modifier.name}`] = {
      get: {
        summary: modifier.name,
        description: modifierDesc,
        operationId: `modifier_${modifier.name}`,
        tags: ['Modifier'],
        produces: ['application/json'],
        responses: {
          '200': {
            description: modifierDesc,
            schema: modifierSchema
          }
        }
      }
    };
  }

  // イベントスキーマ
  for (const key in eventNameUsage) {
    eventNameUsage[key] = 0;
  }

  for (const event of events) {
    eventNameUsage[event.name] = (eventNameUsage[event.name] || 0) + 1;
    const overloadIndex = eventNameUsage[event.name];
    const hasOverload = eventNameCount[event.name] > 1;
    const eventSuffix = hasOverload && overloadIndex > 1 ? `_${overloadIndex - 1}` : '';
    const eventSchemaName = `${event.name}Event${eventSuffix}`;

    swagger.definitions[eventSchemaName] = {
      type: 'object',
      description: `${event.name}${hasOverload ? ` (オーバーロード ${overloadIndex})` : ''}`,
      properties: {}
    };

    if (event.inputs && event.inputs.length > 0) {
      for (const input of event.inputs) {
        swagger.definitions[eventSchemaName].properties[input.name] = {
          type: 'string',
          description: `${input.indexed ? 'インデックス付き。' : ''}${getParamDescription(input.name)}`
        };
      }
    }
  }

  // 構造体スキーマ
  for (const struct of structs) {
    swagger.definitions[`${struct.name}Struct`] = {
      type: 'object',
      description: `${struct.name} 構造体`,
      properties: {}
    };

    if (struct.fields && struct.fields.length > 0) {
      for (const field of struct.fields) {
        swagger.definitions[`${struct.name}Struct`].properties[field.name] = {
          type: 'string',
          description: getParamDescription(field.name)
        };
      }
    }
  }

  return JSON.stringify(swagger, null, 2);
}

/**
 * メイン処理
 */
function main() {
  console.log('Starting enhanced skeleton generation...\n');

  let successCount = 0;
  let skipCount = 0;

  for (const contract of CONTRACTS) {
    console.log(`📝 ${contract.name}`);

    // ABIを取得
    const abi = getABI(contract.path, contract.name);
    if (!abi) {
      console.log(`  ⏭️  Skipped (ABI not available)\n`);
      skipCount++;
      continue;
    }

    // ソースコードを取得
    const source = getSource(contract.path);
    if (!source) {
      console.log(`  ⏭️  Skipped (source not available)\n`);
      skipCount++;
      continue;
    }

    // 出力ディレクトリを作成
    const contractDir = path.join(OUTPUT_DIR, contract.name);
    if (!fs.existsSync(contractDir)) {
      fs.mkdirSync(contractDir, { recursive: true });
    }

    // OpenAPI YAML を生成
    const yamlPath = path.join(contractDir, `${contract.name}.openapi.yaml`);
    const yaml = generateOpenAPIYAML(contract.name, abi, source);
    fs.writeFileSync(yamlPath, yaml, 'utf-8');
    console.log(`  ✅ ${contract.name}.openapi.yaml`);

    // Swagger JSON を生成
    const jsonPath = path.join(contractDir, `${contract.name}.swagger.json`);
    const json = generateSwaggerJSON(contract.name, abi, source);
    fs.writeFileSync(jsonPath, json, 'utf-8');
    console.log(`  ✅ ${contract.name}.swagger.json`);

    successCount++;
    console.log('');
  }

  console.log('========================================');
  console.log(`✅ Generated: ${successCount} contracts`);
  if (skipCount > 0) {
    console.log(`⏭️  Skipped: ${skipCount} contracts`);
  }
  console.log('\n📌 Generation complete!');
  console.log('Optional enhancements with contract-spec-generator skill:');
  console.log('  - Internal function error tracking');
  console.log('  - 500 error examples');
  console.log('  - Modifier information\n');
}

// 実行
main();
