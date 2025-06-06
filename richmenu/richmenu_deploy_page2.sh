#!/bin/bash

# ======= 使用者設定 =======
ACCESS_TOKEN=$LINE_ACCESS_TOKEN
ALIAS_ID="richmenu-alias-page2"
IMAGE_PATH="images/page2.png"
CHATBAR_TEXT="喜歡的話，請追蹤我們的粉專🫶"
RICHMENU_NAME="page2"
# ==========================

echo "[1] 從 list 找出 name 為 ${RICHMENU_NAME} 的 rich menu..."
MENU_IDS=$(curl -s -X GET "https://api.line.me/v2/bot/richmenu/list" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq -r '.richmenus[] | select(.name=="'"$RICHMENU_NAME"'") | .richMenuId')

TOTAL_COUNT=$(echo "$MENU_IDS" | wc -l | tr -d ' ')
echo "[2] 找到 $TOTAL_COUNT 個 rich menu 名稱為 '$RICHMENU_NAME'"

if [[ "$TOTAL_COUNT" -gt 0 ]]; then
  echo "[3] 開始刪除..."
  echo "$MENU_IDS" | while read OLD_ID; do
    echo "🗑️ 刪除 richMenuId: $OLD_ID"
    curl -s -X DELETE "https://api.line.me/v2/bot/richmenu/$OLD_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json"
  done
else
  echo "[3] 沒有找到要刪除的 rich menu"
fi

# === 刪除 alias ===
echo "[4] 嘗試刪除 alias $ALIAS_ID..."
ALIAS_EXISTS=$(curl -s -X GET "https://api.line.me/v2/bot/richmenu/alias/${ALIAS_ID}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq -r '.richMenuId')

if [[ "$ALIAS_EXISTS" != "null" ]]; then
  echo "🗑️ 刪除 alias $ALIAS_ID"
  curl -s -X DELETE "https://api.line.me/v2/bot/richmenu/alias/${ALIAS_ID}" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json"
else
  echo "✅ 無對應 alias，略過"
fi

# 建立新 rich menu，並取得新 richMenuId
echo "[5] 建立新的 rich menu..."
CREATE_RES=$(curl -s -X POST "https://api.line.me/v2/bot/richmenu" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "page2new",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 87,
        "y": 478,
        "width": 656,
        "height": 463
      },
      "action": {
        "type": "postback",
        "data": "example_question_law"
      }
    },
    {
      "bounds": {
        "x": 961,
        "y": 483,
        "width": 611,
        "height": 470
      },
      "action": {
        "type": "postback",
        "data": "example_question_housing"
      }
    },
    {
      "bounds": {
        "x": 1790,
        "y": 462,
        "width": 635,
        "height": 483
      },
      "action": {
        "type": "postback",
        "data": "example_question_activity"
      }
    },
    {
      "bounds": {
        "x": 103,
        "y": 1052,
        "width": 619,
        "height": 467
      },
      "action": {
        "type": "postback",
        "data": "example_question_admin_procedure"
      }
    },
    {
      "bounds": {
        "x": 949,
        "y": 1048,
        "width": 632,
        "height": 470
      },
      "action": {
        "type": "postback",
        "data": "example_question_course"
      }
    },
    {
      "bounds": {
        "x": 1778,
        "y": 1052,
        "width": 631,
        "height": 463
      },
      "action": {
        "type": "postback",
        "data": "example_question_club"
      }
    },
    {
      "bounds": {
        "x": 8,
        "y": 17,
        "width": 994,
        "height": 276
      },
      "action": {
        "type": "richmenuswitch",
        "richMenuAliasId": "richmenu-alias-page1",
        "data": "richmenu-changed-to-page1"
      }
    },
    {
      "bounds": {
        "x": 2067,
        "y": 21,
        "width": 429,
        "height": 276
      },
      "action": {
        "type": "richmenuswitch",
	"richMenuAliasId": "richmenu-alias-page3",
	"data": "richmenu-changed-to-page3"
      }
    }
  ]
}')

NEW_ID=$(echo "$CREATE_RES" | jq -r '.richMenuId')
echo "[5] 新的 richMenuId: $NEW_ID"

# 上傳圖片
echo "[6] 上傳圖片..."
curl -s -X POST "https://api-data.line.me/v2/bot/richmenu/$NEW_ID/content" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: image/png" \
  -T "$IMAGE_PATH"

# 設定 alias
echo "[7] 綁定 alias: $ALIAS_ID → $NEW_ID"
curl -s -X POST "https://api.line.me/v2/bot/richmenu/alias" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "richMenuAliasId": "'$ALIAS_ID'",
    "richMenuId": "'$NEW_ID'"
  }'

# 設定預設 rich menu
echo "[8] 設定預設 rich menu..."
curl -s -X POST "https://api.line.me/v2/bot/user/all/richmenu/$NEW_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d ''

echo "✅ 部署完成！"

