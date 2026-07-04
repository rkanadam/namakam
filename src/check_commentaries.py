import json

with open('/Users/Rkanadam/personal/namakam/src/correlated_namakam.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Root keys:", list(data.keys()))
anuvakas = data.get("anuvakas", [])
print("Number of anuvakas:", len(anuvakas))

for a in anuvakas:
    a_id = a.get("id")
    if a_id in [3, 4]:
        print(f"\nAnuvaka {a_id}: {a.get('title')}")
        mantras = a.get("mantras", [])
        print(f"Number of mantras: {len(mantras)}")
        for m in mantras[:3]:  # print first 3 mantras as sample
            m_id = m.get("id")
            print(f"  Mantra {m_id}:")
            print(f"    samhita: {m.get('sanskrit', {}).get('samhita')}")
            print(f"    pada: {m.get('sanskrit', {}).get('pada')}")
            print(f"    krama: {m.get('sanskrit', {}).get('krama')}")
            translations = m.get("translations", {})
            print(f"    translations keys: {list(translations.keys())}")
            for k, v in translations.items():
                print(f"      {k}: {v[:100]}... (length: {len(v)})" if v else f"      {k}: Empty")
            comm_sans = m.get("commentaries_sanskrit", {})
            print(f"    commentaries_sanskrit keys: {list(comm_sans.keys())}")
            for k, v in comm_sans.items():
                print(f"      {k}: {v[:100]}... (length: {len(v)})" if v else f"      {k}: Empty")
