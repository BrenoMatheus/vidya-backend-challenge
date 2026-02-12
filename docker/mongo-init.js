db = db.getSiblingDB("sales_texts")

db.sale_texts.createIndex(
  { text: "text" },
  {
    name: "sale_texts_text_index",
    default_language: "portuguese"
  }
)

print("✅ Mongo text index created successfully")
