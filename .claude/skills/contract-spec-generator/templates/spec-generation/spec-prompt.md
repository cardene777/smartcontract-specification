あなたは Solidity と OpenAPI/Swagger に精通したエンジニアです。
これから与える ABI と Solidity コードから、
「Solidity コントラクトの仕様」を OpenAPI 3.0 (YAML) と Swagger 2.0 (JSON) で表現してください。

重要：これは HTTP API 設計ではなく、
Solidity コントラクトのインターフェイス定義を OpenAPI / Swagger 形式で記述するためのものです。
HTTP 的なベストプラクティスに合わせるのではなく、
Solidity の挙動を正確かつコンパクトに表現することを最優先にしてください。

--------------------------------------------------
入力として渡す情報
--------------------------------------------------

1. 任意のメタ情報（存在する場合のみ）
   - ネットワーク名（任意）: {{NETWORK_NAME があれば}}
   - chainId（任意）: {{CHAIN_ID があれば}}
   - コントラクトアドレス（任意）: {{CONTRACT_ADDRESS があれば}}
   これらの情報が入力に含まれていない場合でも、あなたからユーザーに質問してはいけません。
   含まれていない項目は「なし」とみなすか、仕様書中からその項目自体を省略してください。

2. このコントラクトの ABI（JSON）
----------------- ABI START -----------------
{{ABI_JSON}}
------------------ ABI END ------------------

3. このコントラクトの Solidity コード
------------- SOLIDITY SOURCE START -------------
{{CONTRACT_SOURCE}}
-------------- SOLIDITY SOURCE END --------------


--------------------------------------------------
対象コントラクトの決定
--------------------------------------------------

- コントラクト名 {{CONTRACT_NAME}} は Solidity コードから自動的に決定してください。
  - ABI と一致する public / external 関数・イベントをもっとも多く持つ `contract` 宣言を、
    「対象コントラクト」とみなし、その名前を {{CONTRACT_NAME}} とします。
  - 候補が複数ある場合の優先順位：
    1. ファイル内で最初に定義されたコントラクト。
    2. 継承階層の一番下（もっとも派生側）のコントラクト。

- この {{CONTRACT_NAME}} を対象として、
  以下 2 つを生成してください。
  - OpenAPI 3.0 YAML: `openapi/{{CONTRACT_NAME}}.openapi.yaml`
  - Swagger 2.0 JSON: `openapi/{{CONTRACT_NAME}}.swagger.json`


--------------------------------------------------
全体方針（とくに重要な制約）
--------------------------------------------------

- 目的は「Solidity コントラクトの仕様を OpenAPI / Swagger 形式で整理すること」です。
- 実際に HTTP で叩くことは前提にしません。
- 読み取り・書き込みともに、仕様上の「成功レスポンス」として HTTP 200 を必ず定義してください。
- エラーについては、HTTP のステータスコードとして常に 500 を使って表現してください。
  同じ関数内に複数のエラーがある場合でも、すべて HTTP ステータス 500 として定義して構いません。
  各エラーはレスポンスボディの `message` フィールド（`ErrorResponse.message`）と、レスポンス定義の説明・`examples` で区別してください。
- 4xx 系のステータスコードや 501, 502 など、500 以外の 5xx ステータスコードは使わないでください。
  **200 と 500 以外のレスポンスを追加しないこと。**

- `x-` で始まる extension フィールド（`x-errors`, `x-modifiers`, `x-state-variable` など）は一切使わないでください。
  OpenAPI / Swagger の標準フィールドのみを使って表現してください。

- 説明文（`description`）は **必ず日本語** で書いてください。
- 説明文の中で文末の「。」ごとに改行を入れる場合、実際の文字列には `\n\n` を使ってください。
  例：
  「A です。\n\nB です。\n\nC です。」

- 説明文に **Solidity の関数シグネチャそのもの（`function ...`）をベタ書きしないでください。**
  「Solidity 関数シグネチャ: function ...」のような一文は不要です。
  関数の役割を日本語で簡潔に説明するだけにしてください。

- 説明文の中で登場する Solidity の識別子のうち、以下のもののみバッククォート（`` ` ``）で囲んでください：
  - 変数名、パラメータ名（例：`taker`、`tradeId`）
  - Solidity の特殊な識別子や定数値（例：`msg.sender`、`address(0)`）
  - mapping名（例：`trades[tradeId]`）

  以下のものはバッククォートで囲まないでください：
  - 関数名
  - イベント名
  - エラー名
  - modifier名
  - struct名

  例：
  「`taker` が `address(0)` の場合に返されます。」
  「`msg.sender` が `executionEngine` でない場合に返されます。」
  「この関数は LegFundedEvent および TradeSettledEvent を発火する可能性があります。」

- もし OpenAPI YAML と Swagger JSON の両方を 1 回の応答に収められない場合でも、ユーザーに確認せずに自動で分割して出力してください。
  最初の応答では OpenAPI 3.0 の YAML を、次の応答では Swagger 2.0 の JSON を出力するようにし、分割順序は常に「OpenAPI → Swagger」としてください。

- 入力に含まれていない情報について、ユーザーに追加で質問してはいけません。
  必要な情報が無い場合は「なし」とみなすか、その情報を省略した形で仕様書を生成してください。


--------------------------------------------------
1. パスと operation の設計
--------------------------------------------------

これは HTTP API ではありませんが、Swagger/OpenAPI の制約上、
便宜的にパスと HTTP メソッドを割り当てます。

対象コントラクトの public / external な関数について、次のルールで 1:1 で対応させてください。

■ 読み取り系（`view` / `pure`）関数

- パス: `/{{functionName}}`
- メソッド: `get`
- 引数はすべて `parameters` に定義してください。
- `in` は基本的に `"query"` を使ってください。
  - 自然であれば一部を `in: "path"` としても構いません（例: `/trades/{tradeId}`）。
- **`requestBody` を絶対に使わないでください。**
- Swagger 2.0 側でも `in: "body"` のパラメータを絶対に作らないでください。
  すべて `in: "query"` または `in: "path"` にしてください。

■ 書き込み系（`nonpayable` / `payable`）関数

- パス: `/{{functionName}}`
- メソッド: `post`
- 引数はすべて `parameters` に定義してください。
- `in: "query"` または必要に応じて `in: "path"` を使ってください。
- **Solidity 関数の引数ではない情報（`from`, `gas`, `nonce` など）は一切含めないでください。**
  関数シグネチャに含まれていないものは `parameters` に追加しないでください。
- OpenAPI 3 側でも `requestBody` を定義しないでください。
- Swagger 2 側でも `in: "body"` を使わないでください。

■ summary の書き方

- operation の `summary` には、「◯◯の getter」のような表現を使ってはいけません。
  代わりに、次のようなパターンで短く書いてください。
  - 変数系 getter: 「`nextTradeId` の値を取得」「`executionEngine` の値を取得」
  - mapping 系 getter: 「`trades` mapping の値を取得」「`positions` mapping の値を取得」
- summary では必ず「◯◯の値を取得」「◯◯の情報を取得」のような形にし、「getter」という単語を含めないでください。

■ summary と description での名前の表記

- 関数名、イベント名、エラー名、modifier名、struct名には「〇〇関数」「〇〇イベント」「〇〇エラー」のような接尾辞をつけないでください。
- これらの名前はバッククォートで囲まず、そのまま表記してください。

例：
- NG: "`getTrade` 関数"
- OK: "getTrade"

- NG: "`AccountAllowed` イベント"
- OK: "AccountAllowed"

- NG: "`InvalidAddress` エラー"
- OK: "InvalidAddress"


--------------------------------------------------
2. 読み取り関数のエラー扱い
--------------------------------------------------

- 読み取り関数（`view` / `pure`）は、
  明示的に `require` / `revert` / custom error が書かれていない限り、
  「成功（200）」のみを定義してください。
- そのようなエラーが記述されていない読み取り関数では、
  `responses` に 200 だけを定義し、500 も含めて他のステータスコードは一切定義しないでください。

- 読み取り関数に `require` / `revert` / custom error がある場合は、
  その関数に限り 500 レスポンスを追加して構いません。
  - 200: 正常系の戻り値。
  - 500: `ErrorResponse` スキーマを返すエラー系。
    このとき、1 つの関数内に複数のエラーがある場合でも HTTP ステータスはすべて 500 とし、各エラーごとに別の example を用意してください（詳細は「6. エラー」の章を参照）。

- mapping の getter など「存在しないキー」の場合：
  Solidity では default 値が返るだけで `revert` しません。
  したがってそのようなケースに対して 500 を定義しないでください。


--------------------------------------------------
3. state variable / mapping / constant の自動 getter
--------------------------------------------------

Solidity では以下の宣言に対して自動 getter が生成されます。

- `public` な state variable
- `public` な `mapping`
- `public` な `constant` / `immutable`

ABI とコードから、これらの「自動 getter 関数」を検出し、
通常の読み取り関数と同様に `get` operation として定義してください。

その際、**説明文で必ず、変数 / mapping / constant であることを明示**してください。

■ 普通の変数（public state variable）の getter の description

- 次の 1 文を含めてください（後ろに他の説明を追加しても構いません）。

  「`<宣言そのもの>` という変数の値を取得する、自動で生成される getter 関数です。」

  この文に含まれる「`<宣言そのもの>`」部分は必ずそのまま出力し、省略したり別の表現に置き換えたりしてはいけません。

  例：
  宣言が `uint256 public nextTradeId;` の場合：

  「`uint256 public nextTradeId;` という変数の値を取得する、自動で生成される getter 関数です。」

- `address` 型の変数で、明らかにコントラクトアドレスである場合は、
  より自然な日本語にして構いません。
  例：`address public immutable executionEngine;` の場合は、必ず次のように「定義そのもの」を含めてください。

  「`address public immutable executionEngine;` という変数の値を取得する、自動で生成される getter 関数です。\n\n`executionEngine` コントラクトのアドレスを返します。」

■ mapping の getter の description

- 次のような 2 文を基本形にしてください。

  「`<宣言そのもの>` という mapping の情報を取得する、自動で生成される getter 関数です。\n\n指定したキーに対応する値を返します。」

  説明文には必ず 1 回以上、「`mapping(uint256 => Trade) public trades;`」のようにバッククォート付きでコントラクト内の mapping 定義そのものを含めてください。
  省略したり別の表現に置き換えたりしてはいけません。

- 具体例：
  宣言が `mapping(uint256 => Trade) public trades;` の場合：

  「`mapping(uint256 => Trade) public trades;` という mapping の情報を取得する、自動で生成される getter 関数です。\n\n指定した `tradeId` に対応する `Trade` 情報を返します。」

- 複数キーの mapping であれば、
  「指定した `owner` と `id` に対応する `Position` 情報を返します。」のように、
  キー名や意味を日本語で説明してください。

■ `constant` / `immutable` の getter

- 「変数」として扱い、普通の変数と同じパターンを使ってください。


--------------------------------------------------
4. 通常の関数の説明文
--------------------------------------------------

通常の（自動 getter ではない）関数については、
説明文でフルシグネチャを長々と書かないでください。

- NG 例：
  「Solidity 関数 `getTrade(uint256 tradeId) external view returns (Trade memory)` に対応する読み取り API です。」など。

- OK 例：役割だけを簡潔に日本語で書く。

  例：`getTrade(uint256 tradeId)` が `trades[tradeId]` を返すなら：

  「`trades[tradeId]` の値を返す関数です。」

- 追加で 1～2 文ほど補足しても構いませんが、
  いずれにせよ関数シグネチャそのものは書かないでください。

  例（`fundLeg(uint256 tradeId, uint8 legIndex)` のような関数）：

  「指定したトレードについて、`taker` または `maker` のいずれかが自分のレッグを入金します。\n\n`legIndex` が `0` の場合は `taker` レッグ、`1` の場合は `maker` レッグを表します。\n\n両レッグが入金済みの場合は内部的に決済処理が行われます。\n\nこの関数は `LegFundedEvent` および `TradeSettledEvent` を発火する可能性があります。」

- 説明文を複数行に分ける場合は、「。」ごとに区切りつつ、実際の文字列には `\n\n` を使って改行してください。


--------------------------------------------------
5. struct / 型マッピング
--------------------------------------------------

Solidity の全ての `struct` を解析し、
OpenAPI 側では `components.schemas`、
Swagger 側では `definitions` に 1:1 で表現してください。

- スキーマ名は `{{StructName}}` もしくは `{{StructName}}Struct` としてください。

各フィールドには以下の情報を入れてください。

- `type` / `format` を適切にマッピングすること。
- `description` に「元の Solidity 型」を必ず含めること。
  例：「taker アドレス (Solidity: address)。」

型マッピングの基本方針：

- `uint256` / `int256` など大きな整数 → `type: "number"`, `format: "uint256"` / `"int256"`
- `address` → `type: "string"`, `pattern: "^0x[0-9a-fA-F]{40}$"`
- `bool` → `type: "boolean"`
- `string` → `type: "string"`
- `bytes32` → `type: "string"`, `pattern: "^0x[0-9a-fA-F]{64}$"`
- `bytes` → `type: "string"`（必要に応じて hex 文字列である旨を説明）
- 配列 → `type: "array"`, `items: {...}`


--------------------------------------------------
6. エラー（revert / custom error）の扱い
--------------------------------------------------

- エラーについては、以下の 2 層構造で表現してください。
  1. `ErrorResponse` スキーマに `code` / `message` / `data` を持たせる。
  2. 各関数の 500 レスポンスで、`description` にエラー一覧を列挙し、`examples` で詳細を表現する。

■ 内部関数で発生するエラーの扱い

- 外部関数（external）または公開関数（public）が内部関数（internal/private）を呼び出している場合、
  その内部関数内で発生しうる custom error / revert / require も、
  呼び出し元の外部関数の 500 レスポンスに含めてください。

- Solidity コードを解析し、関数の呼び出しツリーを追跡して、
  間接的に発生しうるエラーもすべて列挙してください。

- 内部関数のエラーも、外部関数のエラー一覧（500 レスポンスの description）に
  同じ形式（「・エラー名」）で追加し、examples にも含めてください。

■ ErrorResponse スキーマ

OpenAPI 側（YAML）では、`components.schemas.ErrorResponse` に、
Swagger 側（JSON）では、`definitions.ErrorResponse` に以下のような定義を置いてください。

- `message`: string
  - **カスタムエラー名または `revert` / `require` のメッセージ文字列そのもの** を入れるフィールドとして定義してください。
  - 説明例：「`StableFxSettlement: trade already settled` のようなエラー文字列をそのまま格納します。」

- `data`: object
  - 任意の追加情報を入れられるようにしてください。

■ 関数ごとのエラー定義

- その関数で発生しうる custom error / `revert` / `require` を解析し、
  該当する関数の `responses` に HTTP 500 を 1 つ定義してください。
- 500 レスポンスの `schema` / `content` は `ErrorResponse` を参照するようにしてください。

- 500 の `description` には、エラーコードの一覧だけを箇条書きで列挙してください。
  詳細な説明は `examples` 側に書きます。

  - 1 行目は固定で次の文にしてください（`\n\n` で改行）：
    「この関数で発生しうるエラーの一覧です。」

  - 2 行目以降は、各エラーごとに 1 行ずつ、先頭に「・」を付けてください。
    エラー名はバッククォートで囲まないでください。
    HTTP ステータス 500 の `description` 文字列は、次のような形になります。

    「この関数で発生しうるエラーの一覧です。\n\n・StableFxSettlement: caller is not execution engine\n\n・StableFxSettlement: invalid taker address\n\n・StableFxSettlement: invalid maker address\n\n・StableFxSettlement: invalid base token address\n\n・StableFxSettlement: invalid quote token address\n\n・StableFxSettlement: base and quote tokens must differ\n\n・StableFxSettlement: base amount must be positive\n\n・StableFxSettlement: quote amount must be positive\n\n・StableFxSettlement: deadline must be in the future」

■ 500 レスポンスの examples の書き方

- エラー一覧に含まれる **すべての** エラーについて、その詳細説明を 500 レスポンスの `examples` に 1 件ずつ必ず記載してください。
- OpenAPI 3.0 側（YAML）では、`content.application/json.examples` にエラーごとの named example を持たせてください。

  例：

  ```yaml
  "500":
    description: "この関数で発生しうるエラーの一覧です。\n\n・StableFxSettlement: caller is not execution engine\n\n・StableFxSettlement: invalid taker address"
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/ErrorResponse"
        examples:
          OnlyExecutionEngine:
            summary: "StableFxSettlement: caller is not execution engine"
            description: "`msg.sender` が `executionEngine` でない場合に返されます。"
            value:
						  message: "StableFxSettlement: caller is not execution engine"
						  data: {}
          InvalidTakerAddress:
            summary: "StableFxSettlement: invalid taker address"
            description: "`taker` が `address(0)` の場合に返されます。"
            value:
						  message: "StableFxSettlement: invalid taker address"
						  data: {}
```

* Swagger 2.0 側（JSON）では named examples が使えないため、
  `examples.application/json` には代表的な 1 つのエラーだけを入れて構いません。
  残りのエラーは、上記のルールどおり 500 の `description` の箇条書きに含まれていれば十分です。

  例：

  ```json
  {
    "responses": {
      "200": {
        "description": "正常終了時のレスポンスです。",
        "schema": { "$ref": "#/definitions/Trade" }
      },
      "500": {
        "description": "この関数で発生しうるエラーの一覧です。\n\n・StableFxSettlement: trade does not exist\n\n・StableFxSettlement: trade already settled\n\n・StableFxSettlement: trade not yet expired",
        "schema": { "$ref": "#/definitions/ErrorResponse" },
        "examples": {
				  "application/json": {
				    "message": "StableFxSettlement: trade does not exist",
				    "data": {}
				  }
				}
      }
    }
  }
  ```

* OpenAPI 3.0 側では、500 レスポンスの `description` に箇条書きで列挙した **すべてのエラー** について、それぞれ 1 つの example オブジェクト（`summary` / `description` / `value`）を作成してください。
  エラーが 9 個あれば、`examples` にも 9 個の named example を定義してください。
  これが UI 上で「エラーごとのブロック」として表示されることを想定しています。

* Swagger 2.0 側では仕様の都合上 `examples` は 1 つしか持てないため、
  代表的な 1 件を `examples.application/json` に入れ、残りは 500 の `description` 内の箇条書きに含めてください。
  箇条書きは必ず「`\n\n・`」で区切り、エラー名はバッククォートで囲まないでください（例：・StableFxSettlement: trade does not exist）。

* いずれの場合も、関数本体の `description` にはエラー一覧を書かないでください。
  エラーに関する情報は 500 レスポンスの `description` と `examples` に集約してください。

* 500 レスポンスを定義しない関数（エラーが特に明示されていないもの）では、
  200 のみで構いません。

---

7. modifier の扱い

---

* コントラクト内の modifier を解析し、どの関数に適用されているかを把握してください。

* 各 modifier の仕様は、必要に応じて別の schema などにまとめても構いませんが、
  **extension（`x-modifiers` 等）は使わないでください。**

* 関数に modifier が適用されている場合は、その関数の `description` に 1 文追加してください。

  例：
  「この関数は `onlyExecutionEngine` modifier により、`executionEngine` アドレスのみが呼び出せます。」

* modifier 内で発生しうるエラーも、
  該当関数の 500 レスポンスの `description` 内のエラー一覧（「・`StableFxSettlement: ...`」形式）に含めてください。

---

8. event の扱い

---

* コントラクト内の全ての `event` について、
  構造を `struct` と同様にスキーマとして定義してください。

  * スキーマ名は `{{EventName}}Event` としてください。

* 各フィールドに `description` を付け、
  「indexed かどうか」も説明文の中に含めてください。
  例：
  「indexed: true。新規トレード ID (Solidity: uint256)。」

* 関連する関数がある場合、その関数の `description` に、
  「この関数は `TradeOpenedEvent` を発火する可能性があります。」のような 1 文を追加してください。

---

9. 継承コントラクトの扱い

---

* 対象コントラクト {{CONTRACT_NAME}} が他のコントラクトを継承している場合、
  その情報を仕様書に必ず含めてください。

* Solidity コードから、対象コントラクトの継承リストを抽出し、
  OpenAPI / Swagger それぞれの `info.description` に、日本語で次のような文を追記してください。

  「このコントラクトは以下のコントラクトを継承しています。\n\n`Ownable`。\n\n`SomeBase`。」

* 継承元コントラクトが同じファイル内に定義されている場合、
  可能な範囲でその public / external 関数やイベントも解析し、
  別の schema や説明文として簡単にまとめても構いません。
  ただしこのプロンプトでは、出力ファイルは対象コントラクト {{CONTRACT_NAME}} 用の 1 組だけにしてください。

---

10. 任意メタ情報（ネットワーク・アドレス）の扱い

---

* ネットワーク名 / chainId / コントラクトアドレスが入力に含まれている場合のみ、
  それらを `info.description` に日本語で追記してください。

  例：
  「この仕様はネットワーク: Polygon PoS、chainId: 137、コントラクトアドレス: 0x... を対象としています。」

* これらの情報を表現するために、`x-contract` のような extension は使わないでください。

---

11. OpenAPI / Swagger ファイルの出力形式

---

* 最初に、生成した仕様の全体方針を **日本語で 1 段落だけ** 簡潔に説明してください。
  ここでも文末ごとに改行して構いませんが、短くまとめてください。

* その後、以下の順番でファイル内容のみを出力してください。

1. OpenAPI 3.0 YAML

```yaml
# file: openapi/{{CONTRACT_NAME}}.openapi.yaml
openapi: 3.0.3
info:
  title: "{{CONTRACT_NAME}} Solidity Interface"
  version: "1.0.0"
  description: "{{CONTRACT_NAME}} コントラクトの Solidity インターフェイスを OpenAPI 形式で表現した仕様です。{{ここにネットワーク名 / chainId / コントラクトアドレス / 継承関係があれば日本語で追記してください。}}"
paths:
  {{ここに本プロンプトのルールに従った paths を YAML で記載}}
components:
  schemas:
    ErrorResponse:
      type: object
      description: "コントラクト呼び出し時のエラー情報を表現する共通スキーマです。"
      properties:
			  message:
			    type: string
			    description: "カスタムエラー名または `revert` / `require` のメッセージ文字列をそのまま格納します。"
			  data:
			    type: object
			    description: "追加情報（任意）です。"
    {{ここに struct や event のスキーマを記載}}
```

2. Swagger 2.0 JSON

```json
{
  "swagger": "2.0",
  "info": {
    "title": "{{CONTRACT_NAME}} Solidity Interface",
    "version": "1.0.0",
    "description": "{{CONTRACT_NAME}} コントラクトの Solidity インターフェイスを Swagger 2.0 形式で表現した仕様です。{{ここにネットワーク名 / chainId / コントラクトアドレス / 継承関係があれば日本語で追記してください。}}"
  },
  "host": "example.com",
  "basePath": "/",
  "schemes": ["https"],
  "paths": {
    {{ここに本プロンプトのルールに従った paths を JSON で記載}}
  },
  "definitions": {
    "ErrorResponse": {
		  "type": "object",
		  "description": "コントラクト呼び出し時のエラー情報を表現する共通スキーマです。",
		  "properties": {
		    "message": {
		      "type": "string",
		      "description": "カスタムエラー名または `revert` / `require` のメッセージ文字列をそのまま格納します。"
		    },
		    "data": {
		      "type": "object",
		      "description": "追加情報（任意）です。"
		    }
		  }
		}
    {{ここに struct や event のスキーマを記載}}
  }
}
```

* それぞれのコードブロックは有効な YAML / JSON としてパース可能である必要があります。
* OpenAPI 3.0 と Swagger 2.0 の間で、
  関数・パラメータ・戻り値・struct・event・継承関係・エラー定義の意味が一致するようにしてください。
* コメント用にここで使った `{{...}}` や説明文は、実際の出力には含めないでください。

以上すべてのルールに従って、
与えられた ABI と Solidity コードから、
対象コントラクト {{CONTRACT_NAME}} の
`openapi/{{CONTRACT_NAME}}.openapi.yaml` と
`openapi/{{CONTRACT_NAME}}.swagger.json` の内容を生成してください。
