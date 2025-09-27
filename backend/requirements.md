# Requirements

## 功能需求
1. **支持任意結構化的 JSON 數據**：
   - API 必須能處理任意結構化的 JSON 數據。
   - 使用 JSON Schema 驗證數據結構。

2. **支持 CRUD 操作**：
   - `POST`：創建新資源。
   - `GET`：根據 ID 獲取資源，支持條件讀取。
   - `DELETE`：刪除資源。

3. **條件讀取**：
   - 使用 `ETag` 和 `If-None-Match` 標頭。
   - 如果資源未改變，返回 `304 Not Modified`。

4. **數據存儲**：
   - 使用 MongoDB 作為 key/value 存儲。
   - 每個文檔的 `_id` 作為唯一鍵。

5. **數據驗證**：
   - 使用 JSON Schema 驗證客戶端發送的數據。
   - 如果數據不符合 JSON Schema，返回 `400 Bad Request`。

## API 設計
1. **URI**：
   - `POST /api/v1/plans`：創建新計劃。
   - `GET /api/v1/plans/{id}`：根據 ID 獲取計劃。
   - `DELETE /api/v1/plans/{id}`：刪除計劃。

2. **狀態碼**：
   - `201 Created`：成功創建。
   - `200 OK`：成功獲取。
   - `204 No Content`：成功刪除。
   - `400 Bad Request`：數據驗證失敗。
   - `404 Not Found`：資源不存在。

3. **Headers**：
   - `ETag`：用於條件讀取。
   - `If-None-Match`：客戶端發送，用於條件讀取。

4. **版本**：
   - 使用 URI 前綴表示版本，例如 `/api/v1`。

## 實現邏輯
1. **JSON Schema 定義**：
   - 定義一個通用的 JSON Schema，允許任意結構化數據。

2. **條件讀取邏輯**：
   - 根據 JSON 數據的內容生成唯一的 `ETag`。
   - 如果 `If-None-Match` 與 `ETag` 匹配，返回 `304 Not Modified`。

3. **數據存儲邏輯**：
   - 使用 MongoDB 存儲 JSON 數據，並使用 `_id` 作為唯一鍵。

4. **數據驗證邏輯**：
   - 在 `POST` 請求中，使用 JSON Schema 驗證客戶端發送的數據。
   - 如果數據不符合 JSON Schema，返回 `400 Bad Request`。

## 測試需求
1. **測試 API 功能**：
   - 測試所有 REST API 操作是否正常工作。
   - 測試條件讀取是否正確返回 `304 Not Modified`。

2. **測試數據驗證**：
   - 測試 JSON Schema 是否正確驗證客戶端數據。
   - 測試不符合 JSON Schema 的數據是否返回 `400 Bad Request`。

3. **測試數據存儲**：
   - 測試 MongoDB 是否正確存儲和刪除數據。