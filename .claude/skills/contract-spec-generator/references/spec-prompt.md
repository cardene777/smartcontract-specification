You are an engineer proficient in Solidity and OpenAPI/Swagger.
From the ABI and Solidity code provided below,
express the "Solidity contract specification" in OpenAPI 3.0 (YAML) and Swagger 2.0 (JSON).

Important: This is NOT an HTTP API design.
It is for describing the Solidity contract interface definition in OpenAPI/Swagger format.
Prioritize accurately and compactly expressing Solidity behavior,
rather than conforming to HTTP best practices.

--------------------------------------------------
Input Information
--------------------------------------------------

1. Optional metadata (only if present)
   - Network name (optional): {{NETWORK_NAME if provided}}
   - chainId (optional): {{CHAIN_ID if provided}}
   - Contract address (optional): {{CONTRACT_ADDRESS if provided}}
   If this information is not included in the input, do not ask the user for it.
   Items not included should be treated as "none" or omitted from the specification entirely.

2. Contract ABI (JSON)
----------------- ABI START -----------------
{{ABI_JSON}}
------------------ ABI END ------------------

3. Contract Solidity code
------------- SOLIDITY SOURCE START -------------
{{CONTRACT_SOURCE}}
-------------- SOLIDITY SOURCE END --------------


--------------------------------------------------
Determining the Target Contract
--------------------------------------------------

- The contract name {{CONTRACT_NAME}} should be automatically determined from the Solidity code.
  - Consider the `contract` declaration that has the most public/external functions and events
    matching the ABI as the "target contract", and use that name as {{CONTRACT_NAME}}.
  - Priority when there are multiple candidates:
    1. The first contract defined in the file.
    2. The most derived contract in the inheritance hierarchy.

- Generate the following two files for this {{CONTRACT_NAME}}:
  - OpenAPI 3.0 YAML: `openapi/{{CONTRACT_NAME}}.openapi.yaml`
  - Swagger 2.0 JSON: `openapi/{{CONTRACT_NAME}}.swagger.json`


--------------------------------------------------
Overall Guidelines (Especially Important Constraints)
--------------------------------------------------

- The purpose is to "organize Solidity contract specifications in OpenAPI/Swagger format".
- It is NOT assumed to be called via HTTP.
- For both read and write operations, always define HTTP 200 as the "success response" in the specification.
- For errors, always use HTTP status code 500.
  Even if there are multiple errors in the same function, they should all be defined as HTTP status 500.
  Distinguish each error by the `message` field in the response body (`ErrorResponse.message`) and through the description and `examples` in the response definition.
- Do NOT use 4xx status codes or 5xx status codes other than 500 (such as 501, 502).
  **Do NOT add any responses other than 200 and 500.**

- Do NOT use `x-` prefixed extension fields (such as `x-errors`, `x-modifiers`, `x-state-variable`).
  Only use standard OpenAPI/Swagger fields.

- Descriptions (`description`) should be written **in the appropriate language for your context**.
- When adding line breaks after each sentence period in descriptions, use `\n\n` in the actual string.
  Example:
  "This is A.\n\nThis is B.\n\nThis is C."

- Do NOT write the Solidity function signature itself verbatim in descriptions.
  Do NOT include lines like "Solidity function signature: function ...".
  Simply describe the function's role concisely.

- In descriptions, wrap the following Solidity identifiers in backticks (`` ` ``):
  - Variable names, parameter names (e.g., `taker`, `tradeId`)
  - Solidity special identifiers or constant values (e.g., `msg.sender`, `address(0)`)
  - Mapping names (e.g., `trades[tradeId]`)

  Do NOT wrap the following in backticks:
  - Function names
  - Event names
  - Error names
  - Modifier names
  - Struct names

  Examples:
  "Returned when `taker` is `address(0)`."
  "Returned when `msg.sender` is not `executionEngine`."
  "This function may emit LegFundedEvent and TradeSettledEvent."

- If both OpenAPI YAML and Swagger JSON cannot fit in a single response, automatically split the output without asking the user.
  Output OpenAPI 3.0 YAML in the first response, and Swagger 2.0 JSON in the next response. The split order should always be "OpenAPI → Swagger".

- Do NOT ask the user additional questions about information not included in the input.
  If required information is missing, treat it as "none" or generate the specification omitting that information.


--------------------------------------------------
1. Path and Operation Design
--------------------------------------------------

This is not an HTTP API, but due to Swagger/OpenAPI constraints,
paths and HTTP methods are assigned for convenience.

For public/external functions of the target contract, map them 1:1 with the following rules:

■ Read Functions (`view` / `pure`)

- Path: `/{{functionName}}`
- Method: `get`
- Define all arguments in `parameters`.
- Use `in: "query"` as the default.
  - You may use `in: "path"` for some parameters if natural (e.g., `/trades/{tradeId}`).
- **Never use `requestBody`.**
- On the Swagger 2.0 side, never create `in: "body"` parameters.
  Use only `in: "query"` or `in: "path"`.

■ Write Functions (`nonpayable` / `payable`)

- Path: `/{{functionName}}`
- Method: `post`
- Define all arguments in `parameters`.
- Use `in: "query"` or `in: "path"` as needed.
- **Do NOT include information that is not a Solidity function argument (`from`, `gas`, `nonce`, etc.).**
  Do not add anything to `parameters` that is not in the function signature.
- Do NOT define `requestBody` on the OpenAPI 3 side.
- Do NOT use `in: "body"` on the Swagger 2 side.

■ Writing summaries

- Do NOT use expressions like "getter for ◯◯" in operation `summary`.
  Instead, use short patterns like:
  - Variable getters: "Get value of `nextTradeId`", "Get value of `executionEngine`"
  - Mapping getters: "Get value from `trades` mapping", "Get value from `positions` mapping"
- Summary should always be in the form "Get value of ◯◯" or "Get information of ◯◯", without the word "getter".

■ Name notation in summary and description

- Do NOT add suffixes like "function", "event", "error" to function names, event names, error names, modifier names, or struct names.
- Write these names without backticks, as-is.

Examples:
- NG: "`getTrade` function"
- OK: "getTrade"

- NG: "`AccountAllowed` event"
- OK: "AccountAllowed"

- NG: "`InvalidAddress` error"
- OK: "InvalidAddress"


--------------------------------------------------
2. Error Handling for Read Functions
--------------------------------------------------

- For read functions (`view` / `pure`),
  unless `require` / `revert` / custom error is explicitly written,
  define only "success (200)".
- For read functions without such errors,
  define only 200 in `responses` and do not define 500 or any other status codes.

- If a read function has `require` / `revert` / custom error,
  you may add a 500 response for that function only.
  - 200: Normal return value.
  - 500: Error response returning `ErrorResponse` schema.
    Even if there are multiple errors in one function, all use HTTP status 500, with separate examples for each error (see "6. Errors" section for details).

- For mapping getters with "non-existent keys":
  Solidity just returns the default value without `revert`.
  Therefore, do NOT define 500 for such cases.


--------------------------------------------------
3. Auto-getters for State Variables / Mappings / Constants
--------------------------------------------------

Solidity automatically generates getters for the following declarations:

- `public` state variables
- `public` `mapping`
- `public` `constant` / `immutable`

Detect these "auto-getter functions" from the ABI and code,
and define them as `get` operations like regular read functions.

**Always clarify in the description whether it's a variable / mapping / constant.**

■ Description for regular variable (public state variable) getter

- Include the following sentence (you may add more explanation after):

  "An auto-generated getter function that retrieves the value of `<declaration itself>`."

  The "`<declaration itself>`" part must be output exactly as-is, without abbreviation or rephrasing.

  Example:
  If the declaration is `uint256 public nextTradeId;`:

  "An auto-generated getter function that retrieves the value of `uint256 public nextTradeId;`."

- For `address` type variables that are clearly contract addresses,
  you may make the description more natural.
  Example: For `address public immutable executionEngine;`, always include the "definition itself":

  "An auto-generated getter function that retrieves the value of `address public immutable executionEngine;`.\n\nReturns the address of the `executionEngine` contract."

■ Description for mapping getter

- Use the following 2 sentences as the basic form:

  "An auto-generated getter function that retrieves information from the `<declaration itself>` mapping.\n\nReturns the value corresponding to the specified key."

  The description must include the mapping definition with backticks (like `mapping(uint256 => Trade) public trades;`) at least once.
  Do not abbreviate or rephrase.

- Example:
  For declaration `mapping(uint256 => Trade) public trades;`:

  "An auto-generated getter function that retrieves information from the `mapping(uint256 => Trade) public trades;` mapping.\n\nReturns the `Trade` information corresponding to the specified `tradeId`."

- For multi-key mappings,
  describe like "Returns the `Position` information corresponding to the specified `owner` and `id`.",
  explaining key names and meanings.

■ Getter for `constant` / `immutable`

- Treat as "variable" and use the same pattern as regular variables.


--------------------------------------------------
4. Description for Regular Functions
--------------------------------------------------

For regular functions (not auto-getters),
do NOT write the full signature verbosely in the description.

- NG example:
  "A read API corresponding to Solidity function `getTrade(uint256 tradeId) external view returns (Trade memory)`." etc.

- OK example: Concisely describe only the role.

  Example: If `getTrade(uint256 tradeId)` returns `trades[tradeId]`:

  "A function that returns the value of `trades[tradeId]`."

- You may add 1-2 supplementary sentences,
  but do not write the function signature itself.

  Example (for a function like `fundLeg(uint256 tradeId, uint8 legIndex)`):

  "Deposits funds for either the `taker` or `maker` leg for the specified trade.\n\n`legIndex` of `0` represents the `taker` leg, `1` represents the `maker` leg.\n\nIf both legs are funded, settlement processing occurs internally.\n\nThis function may emit `LegFundedEvent` and `TradeSettledEvent`."

- When splitting descriptions into multiple lines, use `\n\n` for line breaks after each sentence.


--------------------------------------------------
5. Struct / Type Mapping
--------------------------------------------------

Analyze all `struct` in the contract,
and express them 1:1 in `components.schemas` for OpenAPI,
and `definitions` for Swagger.

- Schema name should be `{{StructName}}` or `{{StructName}}Struct`.

Include the following information for each field:

- Map `type` / `format` appropriately.
- `description` must include "original Solidity type".
  Example: "taker address (Solidity: address)."

Basic type mapping guidelines:

- `uint256` / `int256` etc. large integers → `type: "number"`, `format: "uint256"` / `"int256"`
- `address` → `type: "string"`, `pattern: "^0x[0-9a-fA-F]{40}$"`
- `bool` → `type: "boolean"`
- `string` → `type: "string"`
- `bytes32` → `type: "string"`, `pattern: "^0x[0-9a-fA-F]{64}$"`
- `bytes` → `type: "string"` (explain it's a hex string if needed)
- Arrays → `type: "array"`, `items: {...}`


--------------------------------------------------
6. Error (revert / custom error) Handling
--------------------------------------------------

- Express errors using a 2-layer structure:
  1. `ErrorResponse` schema with `code` / `message` / `data`.
  2. List errors in `description` of each function's 500 response, and detail in `examples`.

■ Handling errors from internal functions

- If an external or public function calls internal/private functions,
  include custom errors / revert / require from those internal functions
  in the 500 response of the calling external function.

- Analyze the Solidity code, trace the function call tree,
  and list all indirectly possible errors.

- Internal function errors should be added to the error list in 500 response description
  (using the "・ErrorName" format) and included in examples.

■ ErrorResponse schema

On OpenAPI side (YAML), define in `components.schemas.ErrorResponse`,
On Swagger side (JSON), define in `definitions.ErrorResponse` as follows:

- `message`: string
  - **Custom error name or the `revert` / `require` message string itself**.
  - Description example: "Stores error strings like `StableFxSettlement: trade already settled` as-is."

- `data`: object
  - Allow arbitrary additional information.

■ Error definition per function

- Analyze custom errors / `revert` / `require` that can occur in the function,
  and define a single HTTP 500 in that function's `responses`.
- The 500 response `schema` / `content` should reference `ErrorResponse`.

- In the 500 `description`, list only error codes in bullet points.
  Detailed explanations go in `examples`.

  - First line should be fixed as (separated by `\n\n`):
    "List of errors that can occur in this function."

  - From the second line, one line per error with "・" prefix.
    Do not wrap error names in backticks.
    The HTTP status 500 `description` string should look like:

    "List of errors that can occur in this function.\n\n・StableFxSettlement: caller is not execution engine\n\n・StableFxSettlement: invalid taker address\n\n・StableFxSettlement: invalid maker address\n\n・StableFxSettlement: invalid base token address\n\n・StableFxSettlement: invalid quote token address\n\n・StableFxSettlement: base and quote tokens must differ\n\n・StableFxSettlement: base amount must be positive\n\n・StableFxSettlement: quote amount must be positive\n\n・StableFxSettlement: deadline must be in the future"

■ Writing 500 response examples

- For **all** errors listed, create detailed explanations in 500 response `examples`, one per error.
- On OpenAPI 3.0 side (YAML), put named examples per error in `content.application/json.examples`.

  Example:

  ```yaml
  "500":
    description: "List of errors that can occur in this function.\n\n・StableFxSettlement: caller is not execution engine\n\n・StableFxSettlement: invalid taker address"
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/ErrorResponse"
        examples:
          OnlyExecutionEngine:
            summary: "StableFxSettlement: caller is not execution engine"
            description: "Returned when `msg.sender` is not `executionEngine`."
            value:
              message: "StableFxSettlement: caller is not execution engine"
              data: {}
          InvalidTakerAddress:
            summary: "StableFxSettlement: invalid taker address"
            description: "Returned when `taker` is `address(0)`."
            value:
              message: "StableFxSettlement: invalid taker address"
              data: {}
  ```

* On Swagger 2.0 side (JSON), named examples are not available,
  so put only one representative error in `examples.application/json`.
  Include the remaining errors in the 500 `description` bullet list.

  Example:

  ```json
  {
    "responses": {
      "200": {
        "description": "Response on successful completion.",
        "schema": { "$ref": "#/definitions/Trade" }
      },
      "500": {
        "description": "List of errors that can occur in this function.\n\n・StableFxSettlement: trade does not exist\n\n・StableFxSettlement: trade already settled\n\n・StableFxSettlement: trade not yet expired",
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

* On OpenAPI 3.0 side, for **all** errors in the bullet list, create one example object each (`summary` / `description` / `value`).
  If there are 9 errors, define 9 named examples in `examples`.
  This is intended to display as "error-specific blocks" in the UI.

* On Swagger 2.0 side, due to specification limitations, `examples` can only hold one,
  so put one representative in `examples.application/json`, and include the rest in the 500 `description` bullet list.
  Always separate bullets with "`\n\n・`", and do not wrap error names in backticks (e.g., ・StableFxSettlement: trade does not exist).

* In any case, do NOT write the error list in the function body's `description`.
  Consolidate error information in the 500 response `description` and `examples`.

* For functions without 500 response (no explicit errors),
  200 only is fine.

---

7. Modifier Handling

---

* Analyze modifiers in the contract and understand which functions they're applied to.

* Modifier specifications may be summarized in separate schemas if needed,
  but **do NOT use extensions (`x-modifiers` etc.).**

* If a function has modifiers applied, add one sentence to that function's `description`.

  Example:
  "This function is restricted to `executionEngine` address only via the `onlyExecutionEngine` modifier."

* Errors that can occur within modifiers should also be included
  in the function's 500 response `description` error list (using "・`StableFxSettlement: ...`" format).

---

8. Event Handling

---

* For all `event` in the contract,
  define the structure as a schema similar to `struct`.

  * Schema name should be `{{EventName}}Event`.

* Add `description` to each field,
  including "whether indexed" in the description.
  Example:
  "indexed: true. New trade ID (Solidity: uint256)."

* If there are related functions, add to that function's `description`:
  "This function may emit `TradeOpenedEvent`." or similar.

---

9. Inherited Contract Handling

---

* If the target contract {{CONTRACT_NAME}} inherits from other contracts,
  always include that information in the specification.

* Extract the inheritance list from the Solidity code,
  and append the following sentence to `info.description` in both OpenAPI/Swagger:

  "This contract inherits from the following contracts.\n\n`Ownable`.\n\n`SomeBase`."

* If inherited contracts are defined in the same file,
  you may analyze their public/external functions and events
  and briefly summarize in separate schemas or descriptions.
  However, output only one set of files for the target contract {{CONTRACT_NAME}}.

---

10. Optional Metadata (Network/Address) Handling

---

* Only if network name / chainId / contract address are included in the input,
  append them to `info.description`.

  Example:
  "This specification targets Network: Polygon PoS, chainId: 137, Contract Address: 0x..."

* Do NOT use extensions like `x-contract` to express this information.

---

11. OpenAPI / Swagger File Output Format

---

* First, briefly explain the overall approach of the generated specification **in one paragraph**.
  You may add line breaks after sentences, but keep it short.

* Then output file contents only, in the following order:

1. OpenAPI 3.0 YAML

```yaml
# file: openapi/{{CONTRACT_NAME}}.openapi.yaml
openapi: 3.0.3
info:
  title: "{{CONTRACT_NAME}} Solidity Interface"
  version: "1.0.0"
  description: "A specification expressing the {{CONTRACT_NAME}} contract's Solidity interface in OpenAPI format.{{Add network name / chainId / contract address / inheritance here if available.}}"
paths:
  {{Paths following the rules in this prompt in YAML}}
components:
  schemas:
    ErrorResponse:
      type: object
      description: "Common schema for expressing error information during contract calls."
      properties:
        message:
          type: string
          description: "Stores custom error name or `revert` / `require` message string as-is."
        data:
          type: object
          description: "Additional information (optional)."
    {{Struct and event schemas here}}
```

2. Swagger 2.0 JSON

```json
{
  "swagger": "2.0",
  "info": {
    "title": "{{CONTRACT_NAME}} Solidity Interface",
    "version": "1.0.0",
    "description": "A specification expressing the {{CONTRACT_NAME}} contract's Solidity interface in Swagger 2.0 format.{{Add network name / chainId / contract address / inheritance here if available.}}"
  },
  "host": "example.com",
  "basePath": "/",
  "schemes": ["https"],
  "paths": {
    {{Paths following the rules in this prompt in JSON}}
  },
  "definitions": {
    "ErrorResponse": {
      "type": "object",
      "description": "Common schema for expressing error information during contract calls.",
      "properties": {
        "message": {
          "type": "string",
          "description": "Stores custom error name or `revert` / `require` message string as-is."
        },
        "data": {
          "type": "object",
          "description": "Additional information (optional)."
        }
      }
    }
    {{Struct and event schemas here}}
  }
}
```

* Each code block must be valid YAML / JSON that can be parsed without errors.
* Ensure that functions, parameters, return values, structs, events, inheritance, and error definitions
  have consistent meaning between OpenAPI 3.0 and Swagger 2.0.
* Do not include `{{...}}` placeholders or explanatory text used here in the actual output.

Following all the rules above,
from the given ABI and Solidity code,
generate the contents of
`openapi/{{CONTRACT_NAME}}.openapi.yaml` and
`openapi/{{CONTRACT_NAME}}.swagger.json`
for the target contract {{CONTRACT_NAME}}.
