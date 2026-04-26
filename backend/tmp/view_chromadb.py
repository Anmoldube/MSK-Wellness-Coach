"""Quick ChromaDB viewer — run this to see all indexed documents."""
import chromadb

client = chromadb.PersistentClient(path="./data/chromadb")
col = client.get_or_create_collection("msk_knowledge_base")

print(f"\n📊 Total documents in ChromaDB: {col.count()}\n")

results = col.get(include=["documents", "metadatas"])

for i in range(len(results["ids"])):
    doc_id = results["ids"][i]
    meta = results["metadatas"][i]
    doc = results["documents"][i]
    print("=" * 60)
    print(f"ID:   {doc_id}")
    print(f"Type: {meta.get('doc_type', '?')}")
    print(f"Name: {meta.get('name', '?')}")
    print(f"Doc:  {doc[:150]}...")
    print()
