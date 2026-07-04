import os
import json
import re

# Consonant matcher helper
def get_consonants(text):
    return [c for c in text if '\u0915' <= c <= '\u0939']

def clean_sanskrit(text):
    for char in ['॑', '॒', '᳚', '।', '॥', ' ']:
        text = text.replace(char, '')
    return text

def align_words_to_chunks(chunks, words_list):
    tokens = []
    word_idx = 0
    n_words = len(words_list)
    
    for chunk in chunks:
        if chunk.strip() in ['', '।', '॥']:
            tokens.append({"text": chunk, "word_ids": []})
            continue
            
        # Clean इति from chunk to prevent matching errors
        chunk_clean = chunk
        for iti_pat in ["इति", "इती"]:
            chunk_clean = re.sub(iti_pat + r"[\u0951\u0952\u1cd0-\u1cff]*", "", chunk_clean)
            
        chunk_cons = get_consonants(chunk_clean)
        if not chunk_cons:
            tokens.append({"text": chunk, "word_ids": []})
            continue
            
        matched_ids = []
        while word_idx < n_words:
            word = words_list[word_idx]
            word_cons = get_consonants(word["pada_form"])
            if not word_cons:
                matched_ids.append(word["id"])
                word_idx += 1
                continue
                
            first_c = word_cons[0]
            if first_c in chunk_cons:
                idx_c = chunk_cons.index(first_c)
                chunk_cons = chunk_cons[idx_c + 1:]
                matched_ids.append(word["id"])
                word_idx += 1
            else:
                break
                
        tokens.append({"text": chunk, "word_ids": matched_ids})
    return tokens

def align_krama_chunks(chunks, words_list):
    tokens = []
    word_idx = 0
    n_words = len(words_list)
    
    for chunk in chunks:
        if chunk.strip() in ['', '।', '॥']:
            tokens.append({"text": chunk, "word_ids": []})
            continue
            
        chunk_clean = chunk
        for iti_pat in ["इति", "इती"]:
            chunk_clean = re.sub(iti_pat + r"[\u0951\u0952\u1cd0-\u1cff]*", "", chunk_clean)
            
        chunk_cons = get_consonants(chunk_clean)
        if not chunk_cons:
            tokens.append({"text": chunk, "word_ids": []})
            continue
            
        search_start = max(0, word_idx - 1)
        search_end = min(n_words, word_idx + 4)
        
        temp_chunk_cons = list(chunk_cons)
        matched_indices = []
        
        for w_i in range(search_start, search_end):
            word = words_list[w_i]
            word_cons = get_consonants(word["pada_form"])
            if not word_cons:
                continue
            first_c = word_cons[0]
            if first_c in temp_chunk_cons:
                idx_c = temp_chunk_cons.index(first_c)
                matched_indices.append(w_i)
                temp_chunk_cons = temp_chunk_cons[idx_c + 1:]
                
        if matched_indices:
            matched_ids = [words_list[i]["id"] for i in matched_indices]
            word_idx = max(matched_indices)
        else:
            matched_ids = []
            
        tokens.append({"text": chunk, "word_ids": matched_ids})
    return tokens

# Clean page helper
def clean_page(p, text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if "Jangamwadi Math Collection" in stripped:
            continue
        if "Digitized by eGangotri" in stripped:
            continue
        if "सायणाचार्य" in stripped and "भाष्य" in stripped:
            continue
        if "[न०" in stripped and "रुद्राध्याय" in stripped:
            continue
        if re.match(r'^\(\s*\d+\s*\)$', stripped):
            continue
        if re.match(r'^\[न०.*\]\s*रुद्राध्यायः', stripped):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# Extraction of Sanskrit commentaries from page files
def extract_commentaries(mantra_id, current_page_num, next_page_num):
    pages_text = []
    for p in range(current_page_num, next_page_num + 1):
        filepath = f"/Users/Rkanadam/personal/namakam/src/assets/rudradhyaya/page-{p:03d}.txt"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                pages_text.append(clean_page(p, f.read()))
    
    full_text = "\n".join(pages_text)
    
    sayana_match = re.search(r"सा०\s*भा०", full_text)
    bb_match = re.search(r"[भम]०\s*भा०\s*[भामा]०|[भम]०\s*भा०\s*मा०|भ०\s*भा०\s*मा०", full_text)
    
    sayana_sanskrit = ""
    bb_sanskrit = ""
    
    if sayana_match and bb_match:
        sayana_sanskrit = full_text[sayana_match.start():bb_match.start()].strip()
        bb_text_rem = full_text[bb_match.start():]
        next_heading_match = re.search(r"॥[^॥]+माह\s*॥", bb_text_rem[100:])
        if next_heading_match:
            bb_sanskrit = bb_text_rem[:100 + next_heading_match.start()].strip()
        else:
            bb_sanskrit = bb_text_rem.strip()
    elif sayana_match:
        sayana_sanskrit = full_text[sayana_match.start():].strip()
    elif bb_match:
        bb_sanskrit = full_text[bb_match.start():].strip()
        
    sayana_sanskrit = re.sub(r"^सा०\s*भा०\s*", "", sayana_sanskrit).strip()
    bb_sanskrit = re.sub(r"^[भम]०\s*भा०\s*[भामा]०\s*|^[भम]०\s*भा०\s*मा०\s*|^भ०\s*भा०\s*मा०\s*", "", bb_sanskrit).strip()
    
    return sayana_sanskrit, bb_sanskrit

def split_english_commentaries(sayana_field):
    sayana_eng = ""
    bb_eng = ""
    if "Sayana's Commentary:" in sayana_field:
        parts = sayana_field.split("Sayana's Commentary:")
        rem = parts[1]
        if "Bhatta Bhaskara's Commentary:" in rem:
            subparts = rem.split("Bhatta Bhaskara's Commentary:")
            sayana_eng = subparts[0].strip()
            bb_eng = subparts[1].strip()
        else:
            sayana_eng = rem.strip()
    elif "Bhatta Bhaskara's Commentary:" in sayana_field:
        parts = sayana_field.split("Bhatta Bhaskara's Commentary:")
        sayana_eng = parts[0].strip()
        bb_eng = parts[1].strip()
    else:
        sayana_eng = sayana_field.strip()
    return sayana_eng, bb_eng

# Anuvakam 2 unique words dictionary
ANUVAKAM2_DICT = {
    "namaḥ": {
        "word": "नमः",
        "transliteration": "namaḥ",
        "root": "√nam (to bow, to bend, to submit)",
        "grammar": {
            "base": "नमस् (namas)",
            "form": "nominative/accusative singular, neuter (treated as indeclinable avyaya)",
            "type": "action noun (bhāvavācaka)",
            "panini": [
                "√नम् + असुन् (Uṇādi 4.188) → नमस्",
                "P 8.3.34 — visarjanīya (ḥ) at pada-end before pause (avasāna)",
                "Governs dative case (caturthī vibhakti) by Aṣṭādhyāyī 2.3.16: 'Namaḥ-svasti-svāhā-svadhā-alaṃ-vaṣaḍ-yogāc-ca'"
            ]
        },
        "meanings": {
            "english": "Salutations; reverential bowing; surrender; homage",
            "nighantu": "Nighaṇṭu 3.18 — listed among karmavācaka words (action-denoting terms). Naighaṇṭuka-kāṇḍa groups it with acts of reverence.",
            "nirukta": "Yāska (Nirukta 3.16) derives from √nam — 'namati praṇamati' (one bows down). Also parsed as 'na + maḥ' (not mine), indicating surrender of ego.",
            "amara_kosha": "Amarakośa 3.4.19 — listed as an avyaya indicating praṇāma (prostration) or reverence.",
            "abhidhana_ratnamala": "Anekārtha-kāṇḍa 5.26 lists it under Avyayas meaning bowing or salutation (namaskāra).",
            "vedantic": "In Advaita, 'namaḥ' is parsed as 'na mama' (not mine) — a surrender of kartṛtva and bhoktṛtva (doership and enjoyership). It represents complete effacement of ahaṅkāra before the Supreme."
        }
    },
    "pati": {
        "word": "पतिः",
        "transliteration": "patiḥ",
        "root": "√pā (to protect)",
        "grammar": {
            "base": "पति (pati)",
            "form": "dative singular: pataye (पतये)",
            "type": "noun, masculine",
            "panini": [
                "√पा + अति (Uṇādi 4.58) → पति — protector/lord",
                "P 1.4.8 — pati-śabda when not compounded has the 'ghi' designation only optionally in case endings, but in compounds it behaves like regular i-stems."
            ]
        },
        "meanings": {
            "english": "Lord; master; husband; protector",
            "nighantu": "Associated with master or protector in Nighaṇṭu.",
            "nirukta": "Derived from √pā: 'pāti iti patiḥ' — He who protects and preserves.",
            "amara_kosha": "Amarakośa 2.6.30 lists pati under master/husband.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.112 lists pati.",
            "vedantic": "Rudra as Pati represents the Supreme Lord (Īśvara) of all creation. He is the master who rules over all individual souls (paśu) and bondages (pāśa)."
        }
    },
    "ca": {
        "word": "च",
        "transliteration": "ca",
        "root": "च (ca)",
        "grammar": {
            "base": "च (ca)",
            "form": "indeclinable particle (avyaya)",
            "type": "nipāta",
            "panini": [
                "P 1.4.57 — classified as nipāta (avyaya)"
            ]
        },
        "meanings": {
            "english": "And; also; moreover",
            "nighantu": "Structural word.",
            "nirukta": "Nirukta 1.4 discusses 'ca' as a nipāta representing aggregation (samuccaya).",
            "amara_kosha": "Amarakośa 3.4.2 lists 'ca' under indeclinables denoting aggregation.",
            "abhidhana_ratnamala": "Listed under avyayas.",
            "vedantic": "The particle 'ca' (and) is used to link the diverse aspects of the universe, reinforcing the Vedantic truth that everything is interconnected and ultimately one with Rudra."
        }
    },
    "hiraṇyabāhu": {
        "word": "हिरण्यबाहुः",
        "transliteration": "hiraṇyabāhuḥ",
        "root": "hiraṇya (gold) + bāhu (arm)",
        "grammar": {
            "base": "हिरण्यबाहु (hiraṇyabāhu)",
            "form": "dative singular: hiraṇyabāhave (हिरण्यबाहवे)",
            "type": "compound, masculine",
            "panini": [
                "Bahuvrīhi compound: hiraṇyamiva bāhū yasya saḥ. Dative singular: hiraṇyabāhave (P 2.3.16)."
            ]
        },
        "meanings": {
            "english": "One who has golden arms; golden-armed",
            "nighantu": "hiraṇya is listed under gold synonyms (Nighaṇṭu 1.2).",
            "nirukta": "'hiraṇya-sadṛśau bāhū yasya saḥ' — He whose arms are beautiful and valuable like gold.",
            "amara_kosha": "Amarakośa 2.9.91 lists hiraṇya as synonym of gold, and 2.6.76 lists bāhu under arm.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.4 lists hiraṇya under gold.",
            "vedantic": "Refers to the manifestation of the Supreme Brahman as the Purusha within the Sun (antar-āditya puruṣa) described in the Chāndogya Upaniṣad (1.6.6): 'ya eṣo'ntarāditye hiraṇmayaḥ puruṣo dṛśyate... hiraṇyabāhuḥ'."
        }
    },
    "senānī": {
        "word": "सेनानीः",
        "transliteration": "senānīḥ",
        "root": "senā (army) + √nī (to lead)",
        "grammar": {
            "base": "सेनानी (senānī)",
            "form": "dative singular: senānye (सेनान्ये)",
            "type": "compound, masculine",
            "panini": [
                "Upapada-samāsa: senā-śabda + √nī + kvip-pratyaya (P 3.2.61). Dative singular: senānye."
            ]
        },
        "meanings": {
            "english": "The commander of armies; general; leader of the hosts",
            "nighantu": "senā is listed in Nighaṇṭu 2.17 among army/battle names.",
            "nirukta": "'senāṃ nayati iti senānīḥ' — He who leads the armies/hosts.",
            "amara_kosha": "Amarakośa Kṣatriyavarga (2.8.84) lists senānī as a synonym of commander (senāpati).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.66 lists senānī as leader of the army.",
            "vedantic": "Rudra is the commander of all divine forces (deva-senā) that combat the forces of ignorance, suffering, and adharma."
        }
    },
    "diś": {
        "word": "दिश्",
        "transliteration": "diś",
        "root": "√diś (to point out, direct)",
        "grammar": {
            "base": "दिश् (diś)",
            "form": "genitive plural: diśām (दिशाम्)",
            "type": "noun, feminine",
            "panini": [
                "Root noun from √diś + kvip. Genitive plural: diśām."
            ]
        },
        "meanings": {
            "english": "Directions; quarters of space",
            "nighantu": "Nighaṇṭu 1.6 under space/sky synonyms (antarīkṣa-nāmāni).",
            "nirukta": "'diśaty avakāśaṃ yā sā diś' — That which points out or provides space/directions.",
            "amara_kosha": "Amarakośa Svargavarga (1.1.58) lists diś as synonym of kakubha, āśā, and harit.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 1.24 lists diś among spatial synonyms.",
            "vedantic": "The directions are the spatial coordinates of the manifest universe. Rudra as 'diśāṃ patiḥ' (Lord of the directions) represents the omnipresent consciousness that pervades and rules all quarters of space."
        }
    },
    "vṛkṣa": {
        "word": "वृक्षः",
        "transliteration": "vṛkṣaḥ",
        "root": "√vraśc (to cut) or √vṛ (to cover/envelop)",
        "grammar": {
            "base": "वृक्ष (vṛkṣa)",
            "form": "dative plural: vṛkṣebhyaḥ (वृक्षेभ्यः) / genitive plural: vṛkṣāṇām (वृक्षाणाम्)",
            "type": "noun, masculine",
            "panini": [
                "Derived from √vrasc + sa-pratyaya (Uṇādi 3.125) with samprasāraṇa."
            ]
        },
        "meanings": {
            "english": "Trees",
            "nighantu": "Listed under vanaspati (plants/trees).",
            "nirukta": "'vraścata iti vṛkṣaḥ' — That which is cut down; or 'vṛṇoti iti vṛkṣaḥ' — That which covers or provides shade.",
            "amara_kosha": "Amarakośa Vanausadhivarga (2.4.1) lists vṛkṣa: 'taruḥ śākhī palāśī ca dru vṛkṣo mahīruhaḥ'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.1 lists vṛkṣa, taru, and mahīruha.",
            "vedantic": "Trees represent the vegetative life of the cosmos. By saluting Rudra as trees, the Upanishadic seer recognizes the divine presence in all plant life."
        }
    },
    "harikeśa": {
        "word": "हरिकेशः",
        "transliteration": "harikeśaḥ",
        "root": "hari (green/tawny) + keśa (hair/foliage)",
        "grammar": {
            "base": "हरिकेश (harikeśa)",
            "form": "dative plural: harikeśebhyaḥ (हरिकेशेभ्यः) / dative singular: harikeśāya (हरिकेशाय)",
            "type": "compound, masculine",
            "panini": [
                "Bahuvrīhi compound: harita-varṇāḥ keśāḥ (parṇāni) yasya saḥ."
            ]
        },
        "meanings": {
            "english": "Having green/tawny hair or foliage",
            "nighantu": "hari is listed under yellow/green synonyms (Nighaṇṭu 1.15).",
            "nirukta": "'harita-varṇāḥ keśāḥ (parṇāni) yasya saḥ' — He whose hair consists of green leaves.",
            "amara_kosha": "Amarakośa lists hari under green/tawny (3.5.34) and keśa under hair (2.6.94).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 5.12 lists hari and keśa.",
            "vedantic": "Rudra is visualized as the cosmic tree of life. His 'hair' is the green foliage of the trees, symbolizing the life-sustaining force of nature."
        }
    },
    "paśu": {
        "word": "पशुः",
        "transliteration": "paśuḥ",
        "root": "√paś (to bind) or √paś (to see)",
        "grammar": {
            "base": "पशु (paśu)",
            "form": "genitive plural: paśūnām (पशूनाम्)",
            "type": "noun, masculine",
            "panini": [
                "Derived from √paś (to see/bind) + ku-pratyaya (Uṇādi 1.29)."
            ]
        },
        "meanings": {
            "english": "Cattle; beasts; animals; individual souls bound by worldly bonds",
            "nighantu": "Listed in Nighaṇṭu 2.11 under cattle/animal names.",
            "nirukta": "'paśyati iti paśuḥ' — That which sees; or 'pāśair baddhavyam iti paśuḥ' — That which is bound by a rope/bond.",
            "amara_kosha": "Amarakośa Siṃhādivarga (2.5.2) lists paśu as synonym of tiryañc and catuṣpad.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.111 lists paśu.",
            "vedantic": "In Śaiva Siddhānta, 'paśu' represents the individual soul (jīva) which is bound by the bonds (pāśa) of ego, karma, and māyā. Rudra is Paśupati — the Lord who liberates these bound souls."
        }
    },
    "saspinjara": {
        "word": "सस्पिञ्जरः",
        "transliteration": "saspinjaraḥ",
        "root": "saspa (young grass) + piñjara (tawny/reddish-yellow)",
        "grammar": {
            "base": "सस्पिञ्जर (saspinjara)",
            "form": "dative singular: saspinjarāya (सस्पिञ्जराय)",
            "type": "compound, masculine",
            "panini": [
                "Karmadhāraya compound: saspa-sadṛśaḥ piñjaraḥ. Dative singular: saspinjarāya."
            ]
        },
        "meanings": {
            "english": "Reddish-yellow; of the color of young, tender grass",
            "nighantu": "piñjara is listed under yellow synonyms (Nighaṇṭu 1.15).",
            "nirukta": "Compound: saspa (young grass) + piñjara (tawny/reddish-yellow). Represents the vibrant, golden-red hue of the rising sun.",
            "amara_kosha": "Amarakośa lists saspa under young grass (2.4.155) and piñjara under reddish-yellow (3.5.31).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 5.24 lists piñjara.",
            "vedantic": "Rudra's form is compared to the beautiful, refreshing color of tender grass or the golden-red dawn, showing his nurturing and life-giving aspect."
        }
    },
    "tviṣīmat": {
        "word": "त्विषीमान्",
        "transliteration": "tviṣīmān",
        "root": "tviṣ (light/glow/splendor) + matup",
        "grammar": {
            "base": "त्विषीमत् (tviṣīmat)",
            "form": "dative singular: tviṣīmate (त्विषीमते) / dative singular: tviṣīmate (Vedic form: त्विषीमते)",
            "type": "noun, masculine",
            "panini": [
                "Noun base tviṣīmat. Dative singular: tviṣīmate (with vowel lengthening in Vedic)."
            ]
        },
        "meanings": {
            "english": "Glowingly bright; brilliant; resplendent",
            "nighantu": "tviṣ is listed in Nighaṇṭu 1.16 among light/glow synonyms (jvalato nāmāni).",
            "nirukta": "Derived from tviṣ + matup-pratyaya: 'tviṣiḥ asya asti iti tviṣīmān' — He who possesses brilliant light.",
            "amara_kosha": "Amarakośa Svargavarga (1.1.55) lists tviṣ as synonym of prabhā, bhā, and dyuti.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 1.30 lists tviṣ.",
            "vedantic": "Represents the self-luminous consciousness (svayaṃ-jyoti) of Brahman that illumines the entire universe."
        }
    },
    "pathin": {
        "word": "पथिन्",
        "transliteration": "pathin",
        "root": "√path (to go)",
        "grammar": {
            "base": "पथिन् (pathin)",
            "form": "genitive plural: pathīnām (पथीनाम्)",
            "type": "noun, masculine",
            "panini": [
                "Declined nominal stem pathin. Genitive plural: pathīnām (with Vedic vowel lengthening)."
            ]
        },
        "meanings": {
            "english": "Paths; ways",
            "nighantu": "Listed in Nighaṇṭu 2.14 under path/way synonyms.",
            "nirukta": "'panthānaḥ pathyante gamyante ebhiḥ iti' — Those that are walked upon.",
            "amara_kosha": "Amarakośa Bhūvarga (2.1.15) lists pathin: 'panthāḥ prathipathaḥ padavī sṛtiḥ'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.158 lists pathin.",
            "vedantic": "Paths represent both the physical roads and the spiritual paths (mārgas) like Devayāna and Pitṛyāna. Rudra as the Lord of paths guides the seekers along the right spiritual paths."
        }
    },
    "babhlusa": {
        "word": "बभ्लुशः",
        "transliteration": "babhlusaḥ",
        "root": "babhru (tawny/golden-brown) + śa",
        "grammar": {
            "base": "बभ्लुश (babhlusa)",
            "form": "dative singular: babhlusāya (बभ्लुशाय) / dative singular: babhlusāya (बभ्लुशाय)",
            "type": "compound, masculine",
            "panini": [
                "Derived from babhru + sa-pratyaya. Dative singular: babhlusāya."
            ]
        },
        "meanings": {
            "english": "One who is seated on the bull; tawny-colored; golden-brown",
            "nighantu": "babhru is listed under gold/yellow synonyms (Nighaṇṭu 1.15).",
            "nirukta": "From babhru (tawny) + śa (possession/agent). Or derived from √bhṛ (to nourish/support): 'bharta-mūrtiḥ' — He who nourishes the worlds.",
            "amara_kosha": "Amarakośa lists babhru under tawny/brown (3.5.33).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 5.15 lists babhru.",
            "vedantic": "Represents Rudra's form as the golden-brown or tawny sustainer of the universe, who supports all beings through his infinite grace."
        }
    },
    "vivyādhin": {
        "word": "विव्याधी",
        "transliteration": "vivyādhī",
        "root": "vi + √vyadh (to pierce/strike) + in",
        "grammar": {
            "base": "विव्याधिन् (vivyādhin)",
            "form": "dative singular: vivyādhine (विव्याधिने)",
            "type": "compound, masculine",
            "panini": [
                "Upapada-samāsa: vi-vyadh + nini-pratyaya (P 3.2.78). Dative singular: vivyādhine."
            ]
        },
        "meanings": {
            "english": "One who pierces through; he who strikes effectively",
            "nighantu": "√vyadh is listed in Nighaṇṭu among violence/injury roots.",
            "nirukta": "'vi-vividhaṃ vyadhyati iti vivyādhī' — He who pierces the darkness of ignorance or strikes down the wicked.",
            "amara_kosha": "Not separately listed, but vyādhi is under disease (2.6.48).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.221 lists vyadh in the sense of striking.",
            "vedantic": "Rudra's arrow is the ultimate force of transformation. He pierces the individual ego and the veil of māyā to reveal the inner Self."
        }
    },
    "anna": {
        "word": "अन्नम्",
        "transliteration": "annam",
        "root": "√ad (to eat)",
        "grammar": {
            "base": "अन्न (anna)",
            "form": "genitive plural: annānām (अन्नानाम्)",
            "type": "noun, neuter",
            "panini": [
                "Root √ad + kta-pratyaya (with ad -> an and t -> n by P 8.2.42). Genitive plural: annānām."
            ]
        },
        "meanings": {
            "english": "Food; nourishment; matter; object of consumption",
            "nighantu": "Listed in Nighaṇṭu 2.7 under food synonyms.",
            "nirukta": "'adyate bhujyate iti annam' — That which is eaten by living beings.",
            "amara_kosha": "Amarakośa Manuṣyavarga (2.7.26) lists anna: 'annaṃ bhaktaṃ surādhīnaṃ bhojanaṃ'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.148 lists anna.",
            "vedantic": "In the Taittirīya Upaniṣad, Anna is Brahman: 'annaṃ brahmeti vyajānāt'. Rudra as the Lord of foods is both the food (consumed object) and the consumer."
        }
    },
    "upavītin": {
        "word": "उपवीती",
        "transliteration": "upavītī",
        "root": "upa + √vye (to cover) + in",
        "grammar": {
            "base": "उपवीतिन् (upavītin)",
            "form": "dative singular: upavītine (उपवीतिने)",
            "type": "compound, masculine",
            "panini": [
                "Derived from upa-√vye + kta → upavīta, then + ini-pratyaya (P 5.2.115). Dative singular: upavītine."
            ]
        },
        "meanings": {
            "english": "One who wears the sacred thread (yajñopavīta) over the left shoulder",
            "nighantu": "upavīta is associated with sacrifice (yajña) in Nighaṇṭu 3.17.",
            "nirukta": "'upavītam asya asti iti' — He who is invested with the sacred thread.",
            "amara_kosha": "Amarakośa Brāhmaṇavarga (2.7.41) lists yajñopavīta and upavīta.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.152 lists yajñopavīta.",
            "vedantic": "Rudra is the supreme performer of the cosmic sacrifice (yajña). Wearing the yajñopavīta shows his commitment to cosmic order (ṛta) and dharma."
        }
    },
    "puṣṭa": {
        "word": "पुष्टः",
        "transliteration": "puṣṭaḥ",
        "root": "√puṣ (to nourish/prosper)",
        "grammar": {
            "base": "पुष्ट (puṣṭa)",
            "form": "genitive plural: puṣṭānaḥ (पुष्टानाम्) / genitive plural: puṣṭānām (पुष्टानाम्)",
            "type": "noun, masculine (also adjective)",
            "panini": [
                "Root √puṣ + kta-pratyaya. Genitive plural: puṣṭānām."
            ]
        },
        "meanings": {
            "english": "Nourished; prosperous; full; complete",
            "nighantu": "√puṣ is listed among growth and nourishment roots in Nighaṇṭu.",
            "nirukta": "'puṣṭam asya saṃjātam' — That which is well-nourished or complete.",
            "amara_kosha": "Amarakośa lists puṣṭi under growth/nourishment (3.3.62).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 3.44 lists puṣṭi.",
            "vedantic": "Prosperity and strength are manifestations of the divine energy (vibhūti). Rudra as the Lord of the prosperous governs the distribution of abundance."
        }
    },
    "bhava": {
        "word": "भवः",
        "transliteration": "bhavaḥ",
        "root": "√bhū (to be/become)",
        "grammar": {
            "base": "भव (bhava)",
            "form": "genitive singular: bhavasya (भवस्य)",
            "type": "noun, masculine",
            "panini": [
                "Derived from √bhū + ghañ/ac-pratyaya (P 3.3.56). Genitive singular: bhavasya."
            ]
        },
        "meanings": {
            "english": "Existence; source of all being; Lord of creation",
            "nighantu": "bhū is listed among existence roots.",
            "nirukta": "'bhavaty asmāt jagat iti bhavaḥ' — He from whom the universe comes into existence.",
            "amara_kosha": "Amarakośa Svargavarga (1.1.30) lists bhava as a primary name of Śiva.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 1.15 lists bhava under names of Śiva.",
            "vedantic": "Bhava represents the eternal source of existence. In Advaita, he is the substrate (adhiṣṭhāna) of all creation."
        }
    },
    "heti": {
        "word": "हेतिः",
        "transliteration": "hetiḥ",
        "root": "√hi (to send/throw/cast)",
        "grammar": {
            "base": "हेति (heti)",
            "form": "dative singular: hetyai (हेत्यै)",
            "type": "noun, feminine",
            "panini": [
                "Root √hi + ktin-pratyaya (P 3.3.94). Dative singular: hetyai."
            ]
        },
        "meanings": {
            "english": "Weapon; missile; stroke of energy",
            "nighantu": "Listed in Nighaṇṭu 2.20 under weapon/missile synonyms (āyudha-nāmāni).",
            "nirukta": "'hinoti hinasti vā iti hetiḥ' — That which is sent forth to strike or destroy.",
            "amara_kosha": "Amarakośa Kṣatriyavarga (2.8.91) lists heti as a synonym of weapon.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.82 lists heti.",
            "vedantic": "Represent the divine instrument of destruction of adharma. The weapon is the power of discrimination (viveka) that destroys ignorance."
        }
    },
    "jagat": {
        "word": "जगत्",
        "transliteration": "jagat",
        "root": "√gam (to go)",
        "grammar": {
            "base": "जगत् (jagat)",
            "form": "genitive plural: jagatām (जगताम्)",
            "type": "noun, neuter",
            "panini": [
                "Intensive participle form from √gam (jagamīti)."
            ]
        },
        "meanings": {
            "english": "The moving world; the universe of changing objects",
            "nighantu": "Listed in Nighaṇṭu 1.6 among world/earth synonyms.",
            "nirukta": "'gacchati iti jagat' — That which constantly moves and changes.",
            "amara_kosha": "Amarakośa Svargavarga (1.1.6) lists jagat: 'loko'yaṃ bharataṃ varṣaṃ jagat'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 1.5 lists jagat.",
            "vedantic": "The world is characterized by constant change (saṃsāra). Rudra as 'jagataṃ patiḥ' is the Lord and controller of this changing universe."
        }
    },
    "rudra": {
        "word": "रुद्रः",
        "transliteration": "rudraḥ",
        "root": "√rud (to cry, howl) or √ru (to break, dissolve)",
        "grammar": {
            "base": "रुद्र (rudra)",
            "form": "dative singular: rudrāya (रुद्राय)",
            "type": "proper noun, masculine",
            "panini": [
                "√रुद् + रक् (Uṇādi 2.22) → रुद्र."
            ]
        },
        "meanings": {
            "english": "The Howler; remover of sorrow; driver away of suffering",
            "nighantu": "Nighaṇṭu 5.3 listed among the names of deities of the middle region.",
            "nirukta": "Yāska (Nirukta 10.3) gives: (1) 'rodayati iti rudraḥ' (makes enemies weep); (2) 'rut dravayati' (drives away suffering).",
            "amara_kosha": "Amarakośa 1.1.29 lists रुद्रः among primary names of Śiva.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 1.15 lists rudra.",
            "vedantic": "In Advaita, Rudra is Brahman in the aspect of cosmic dissolution (saṃhāra-mūrti), resolving all diversity back into primal unity."
        }
    },
    "ātatāvin": {
        "word": "आततावी",
        "transliteration": "ātatāvī",
        "root": "ā + √tan + √av + in",
        "grammar": {
            "base": "आतताविन् (ātatāvin)",
            "form": "dative singular: ātatāvine (आतताविने)",
            "type": "compound, masculine",
            "panini": [
                "Upapada-samāsa: ātata (drawn) + √av (to protect) + nini-pratyaya. Dative singular: ātatāvine."
            ]
        },
        "meanings": {
            "english": "One whose bow is drawn/stretched for protection; defender",
            "nighantu": "√av is listed in Nighaṇṭu among protection roots.",
            "nirukta": "'ātatena dhanuṣā avati rakṣati iti ātatāvī' — He who protects with a drawn bow.",
            "amara_kosha": "Standard lexicons list 'ātatāyī' (assailant), but the Vedic 'ātatāvin' specifically means protector.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.115 lists av as protection.",
            "vedantic": "Rudra's readiness with his bow is to provide constant, immediate protection to those who surrender to him."
        }
    },
    "kṣetra": {
        "word": "क्षेत्रम्",
        "transliteration": "kṣetram",
        "root": "√kṣi (to dwell) or √kṣad (to protect)",
        "grammar": {
            "base": "क्षेत्र (kṣetra)",
            "form": "genitive plural: kṣetrāṇām (क्षेत्राणाम्)",
            "type": "noun, neuter",
            "panini": [
                "Derived from √kṣi + tra-pratyaya (P 3.2.164). Genitive plural: kṣetrāṇām."
            ]
        },
        "meanings": {
            "english": "Fields; sacred places; bodies (as fields of experience)",
            "nighantu": "kṣetra is listed in Nighaṇṭu 2.1 among dwelling/abode synonyms.",
            "nirukta": "'kṣiyate nivāsyate asmin iti kṣetram' — That in which one dwells; or 'kṣatāt trāyate' (protects from decay).",
            "amara_kosha": "Amarakośa Bhūvarga (2.1.6) lists kṣetra as synonym of kedāra.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.12 lists kṣetra.",
            "vedantic": "In Bhagavad Gītā (13.1), the body is called the field (kṣetra) and the soul is the knower of the field (kṣetrajña). Rudra is the Lord of both."
        }
    },
    "sūta": {
        "word": "सूतः",
        "transliteration": "sūtaḥ",
        "root": "√sū (to impel) or √siv (to sew)",
        "grammar": {
            "base": "सूत (sūta)",
            "form": "dative singular: sūtāya (सूताय)",
            "type": "noun, masculine",
            "panini": [
                "Derived from √sū + kta-pratyaya. Dative singular: sūtāya."
            ]
        },
        "meanings": {
            "english": "Charioteer; driver of the cosmic chariot; chronicler",
            "nighantu": "sūta is listed under helper/charioteer synonyms.",
            "nirukta": "'sūte prerayati aśvān iti sūtaḥ' — He who impels the horses.",
            "amara_kosha": "Amarakośa Kṣatriyavarga (2.8.58) lists sūta as synonym of sārathi.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.76 lists sūta.",
            "vedantic": "In the Upanishadic metaphor, the body is a chariot, the intellect is the charioteer (sūta). Rudra is the Supreme Charioteer guiding the soul."
        }
    },
    "ahantya": {
        "word": "अहन्त्यः",
        "transliteration": "ahantyaḥ",
        "root": "a + √han (to kill) + yat",
        "grammar": {
            "base": "अहन्त्य (ahantya)",
            "form": "dative singular: ahantyāya (अहन्त्याय) / dative singular: ahantyaire (Vedic spelling)",
            "type": "compound, masculine",
            "panini": [
                "Negative Tatpuruṣa: na hantyaḥ. Dative singular: ahantyāya."
            ]
        },
        "meanings": {
            "english": "One who cannot be harmed/killed; inviolable; indestructible",
            "nighantu": "√han is listed under violence/killing roots.",
            "nirukta": "'hantuṃ na yogyaḥ iti ahantyaḥ' — He who cannot be destroyed.",
            "amara_kosha": "Synonyms of imperishable are listed under Akṣaravarga.",
            "abhidhana_ratnamala": "Listed under Anekārtha.",
            "vedantic": "Represents the eternal, imperishable nature (akṣara) of Brahman. The Self is never born and never dies."
        }
    },
    "vana": {
        "word": "वनम्",
        "transliteration": "vanam",
        "root": "√van (to love/desire/worship)",
        "grammar": {
            "base": "वन (vana)",
            "form": "genitive plural: vanānām (वनानाम्)",
            "type": "noun, neuter",
            "panini": [
                "Derived from √van + ac-pratyaya. Genitive plural: vanānām."
            ]
        },
        "meanings": {
            "english": "Forests",
            "nighantu": "Listed in Nighaṇṭu 1.12 under water/abundance synonyms and 2.1 under dwelling.",
            "nirukta": "'vanyate sevyate iti vanam' — That which is sought after or worshipped for peace.",
            "amara_kosha": "Amarakośa Vanausadhivarga (2.4.1) lists vana: 'araṇyaṃ gahanaṃ kāntāraṃ vipinaṃ vanam'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.3 lists vana.",
            "vedantic": "Forests are the abodes of silence and contemplation. Rudra as 'vanānāṃ patiḥ' dwells in these silent spaces."
        }
    },
    "rohita": {
        "word": "रोहितः",
        "transliteration": "rohitaḥ",
        "root": "√ruh (to grow/rise/shine)",
        "grammar": {
            "base": "रोहित (rohita)",
            "form": "dative singular: rohitāya (रोहिताय)",
            "type": "noun, masculine (also adjective)",
            "panini": [
                "Derived from √ruh + itan-pratyaya (with h -> t). Dative singular: rohitāya."
            ]
        },
        "meanings": {
            "english": "The red/shining one; of ruby-red color",
            "nighantu": "Listed in Nighaṇṭu 1.15 under red synonyms.",
            "nirukta": "'rohate vardhate iti rohitaḥ' — That which shines with a brilliant red color.",
            "amara_kosha": "Amarakośa lists rohita under red (3.5.30).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 5.22 lists rohita.",
            "vedantic": "The red color represents the active, creative force (rajas) or the fiery splendor of the sun."
        }
    },
    "sthapati": {
        "word": "स्थपतिः",
        "transliteration": "sthapatiḥ",
        "root": "stha (abiding) + pati (lord)",
        "grammar": {
            "base": "स्थपति (sthapati)",
            "form": "dative singular: sthapataye (स्थपतये)",
            "type": "compound, masculine",
            "panini": [
                "Genitive Tatpuruṣa or Upapada: sthātṛṇāṃ patiḥ. Dative singular: sthapataye."
            ]
        },
        "meanings": {
            "english": "The master builder; architect; chief; lord",
            "nighantu": "sthapati is associated with chief or builder.",
            "nirukta": "'sthāyaḥ patiḥ' — The master of the household or building.",
            "amara_kosha": "Amarakośa lists sthapati as chief architect or sovereign (2.8.5).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.112 lists sthapati.",
            "vedantic": "Rudra is the supreme architect (Viśvakarman) of the cosmos, who designs and builds the structure of the universe."
        }
    },
    "mantrin": {
        "word": "मन्त्रिी",
        "transliteration": "mantrī",
        "root": "mantra (counsel) + in",
        "grammar": {
            "base": "मन्त्रिन् (mantrin)",
            "form": "dative singular: mantriṇe (मन्त्रिणे)",
            "type": "noun, masculine",
            "panini": [
                "Derived from mantra + ini-pratyaya. Dative singular: mantriṇe."
            ]
        },
        "meanings": {
            "english": "The counselor; adviser; possessor of sacred mantras",
            "nighantu": "mantra is listed in Nighaṇṭu under speech/counsel synonyms.",
            "nirukta": "Derived from mantra: 'mantrayate iti mantrī' — He who counsels or gives advice.",
            "amara_kosha": "Amarakośa Kṣatriyavarga (2.8.4) lists mantrī as synonym of dhīsaciva.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.55 lists mantrin.",
            "vedantic": "Rudra is the source of all mantras (Mantra-draṣṭā) and the inner guide (Guru) who counsels the seeker."
        }
    },
    "vāṇija": {
        "word": "वाणिजः",
        "transliteration": "vāṇijaḥ",
        "root": "vaṇij (merchant) + a",
        "grammar": {
            "base": "वाणिज (vāṇija)",
            "form": "dative singular: vāṇijāya (वाणिजाय)",
            "type": "noun, masculine",
            "panini": [
                "Derived from vaṇij + a-pratyaya. Dative singular: vāṇijāya."
            ]
        },
        "meanings": {
            "english": "The merchant; trader",
            "nighantu": "vaṇij is listed in Nighaṇṭu under trade/exchange synonyms.",
            "nirukta": "'vaṇijyate anena iti vāṇijaḥ' — He who is engaged in trade.",
            "amara_kosha": "Amarakośa Vaiśyavarga (2.9.78) lists vaṇij and vāṇija.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.14 lists vāṇija.",
            "vedantic": "Commerce represents the transaction of life, karma, and experience. Rudra as the merchant governs the cosmic law of karma-phala."
        }
    },
    "kakṣa": {
        "word": "कक्षः",
        "transliteration": "kakṣaḥ",
        "root": "√kaṣ (to injure/rub) or √kāṅkṣ (to desire)",
        "grammar": {
            "base": "कक्ष (kakṣa)",
            "form": "genitive plural: kakṣāṇām (कक्षाणाम्)",
            "type": "noun, masculine",
            "panini": [
                "Derived from √kaṣ + sa-pratyaya. Genitive plural: kakṣāṇām."
            ]
        },
        "meanings": {
            "english": "Glades; thickets; hidden places; dry grasses",
            "nighantu": "Listed in Nighaṇṭu under forest/grass synonyms.",
            "nirukta": "'kaṣati iti kakṣaḥ' — That which rubs against; or refers to hidden valleys.",
            "amara_kosha": "Amarakośa lists kakṣa under dry grass (2.4.156) and armpit/secret place (3.3.4).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.6 lists kakṣa.",
            "vedantic": "Represent the hidden or inaccessible parts of nature and the mind. Rudra is present even in the deepest thickets of the heart."
        }
    },
    "bhuvanti": {
        "word": "bhuvanti",
        "transliteration": "bhuvantiḥ",
        "root": "√bhū (to be/expand)",
        "grammar": {
            "base": "bhuvanti (bhuvanti)",
            "form": "dative singular: bhuvantaye (भुवन्तये)",
            "type": "noun, masculine",
            "panini": [
                "Vedic derivative. Dative singular: bhuvantaye."
            ]
        },
        "meanings": {
            "english": "One who spreads out or expands the earth/worlds",
            "nighantu": "√bhū is listed among growth and existence roots.",
            "nirukta": "'bhuvaṃ bhūmiṃ tanoti vistārayati iti bhuvantiḥ' — He who causes expansion.",
            "amara_kosha": "bhuva is listed under earth/world synonyms.",
            "abhidhana_ratnamala": "Listed under earth synonyms.",
            "vedantic": "Rudra as the cosmic expanding force ensures that space and matter expand to accommodate life."
        }
    },
    "varivaskṛta": {
        "word": "वारिवस्कृत्",
        "transliteration": "varivaskṛt",
        "root": "varivas (room/wealth) + √kṛ",
        "grammar": {
            "base": "वारिवस्कृत (varivaskṛt)",
            "form": "dative singular: varivaskṛtāya (वारिवस्कृताय)",
            "type": "compound, masculine",
            "panini": [
                "Upapada-samāsa: varivas + √kṛ + kvip. Dative singular: varivaskṛtāya."
            ]
        },
        "meanings": {
            "english": "One who creates wealth, space, or welfare",
            "nighantu": "varivas is listed in Nighaṇṭu 2.10 among wealth synonyms.",
            "nirukta": "'varivaḥ (wealth/room) sukhaṃ karoti iti varivaskṛt'.",
            "amara_kosha": "Amarakośa lists varivas under wealth or room.",
            "abhidhana_ratnamala": "Lists varivas under wealth.",
            "vedantic": "Representing the divine grace that removes congestion (spatial or mental) and provides the 'room' (freedom) of liberation."
        }
    },
    "oṣadhi": {
        "word": "ओषधिः",
        "transliteration": "oṣadhiḥ",
        "root": "oṣa (heat) + dhi (holding)",
        "grammar": {
            "base": "ओषधि (oṣadhi)",
            "form": "genitive plural: oṣadhīnām (ओषधीनाम्)",
            "type": "noun, feminine",
            "panini": [
                "Compound: oṣa + √dhā + ki-pratyaya. Genitive plural: oṣadhīnām."
            ]
        },
        "meanings": {
            "english": "Herbs; medicinal plants",
            "nighantu": "Listed in Nighaṇṭu 2.8 among plant names.",
            "nirukta": "'oṣaṃ duḥkhaṃ dahati yacchanti ca iti oṣadhiḥ' — That which burns away pain/disease.",
            "amara_kosha": "Amarakośa Vanausadhivarga (2.4.1) lists oṣadhi: 'oṣadhyaḥ phala-pākāntāḥ'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.2 lists oṣadhi.",
            "vedantic": "Herbs are the source of healing. Rudra as the Lord of herbs is the Ultimate Healer (Vaidyanātha) who cures all physical and spiritual diseases."
        }
    },
    "uccaiṣghoṣa": {
        "word": "उच्चैर्घोषः",
        "transliteration": "uccaiṣghoṣaḥ",
        "root": "uccais (loudly) + ghoṣa (roar)",
        "grammar": {
            "base": "उच्चैर्घोष (uccaiṣghoṣa)",
            "form": "dative singular: uccaiṣghoṣāya (उच्चैर्घोषाय)",
            "type": "compound, masculine",
            "panini": [
                "Bahuvrīhi compound. Dative singular: uccaiṣghoṣāya."
            ]
        },
        "meanings": {
            "english": "Loud-sounding; shouting aloud; roaring",
            "nighantu": "ghoṣa is listed in Nighaṇṭu 1.11 under sound synonyms.",
            "nirukta": "'uccaiḥ ghoṣo yasya saḥ' — He whose roar is thunderous.",
            "amara_kosha": "Amarakośa lists uccais under high/loud (3.4.13) and ghoṣa under sound (1.5.15).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 1.40 lists ghoṣa.",
            "vedantic": "The loud sound is the voice of the storm-cloud or the primal vibration (Praṇava/Aum) that echoes through the universe."
        }
    },
    "ākrandayanta": {
        "word": "आक्रन्दयन्",
        "transliteration": "ākrandayan",
        "root": "ā + √krand + causal + śatṛ",
        "grammar": {
            "base": "आक्रन्दयत् (ākrandayanta)",
            "form": "dative singular: ākrandayate (आक्रन्दयते)",
            "type": "noun/participle, masculine",
            "panini": [
                "Causal present participle from ā-√krand + śatṛ-pratyaya. Dative singular: ākrandayate."
            ]
        },
        "meanings": {
            "english": "Making [enemies] wail; calling out aloud; summoning",
            "nighantu": "√krand is listed under sound/shouting roots.",
            "nirukta": "'ākrandayati śatrūn iti' — He who makes his enemies weep in fear.",
            "amara_kosha": "Amarakośa lists krandana under wailing (1.5.18).",
            "abhidhana_ratnamala": "Lists krand in the sense of crying out.",
            "vedantic": "Rudra as the destroyer of evil forces causes the lower animal nature to weep and dissolve."
        }
    },
    "pattin": {
        "word": "पत्ती",
        "transliteration": "pattī",
        "root": "pad (foot) + tini",
        "grammar": {
            "base": "पत्ति (pattin)",
            "form": "genitive plural: pattīnām (पत्तीनाम्)",
            "type": "noun, masculine",
            "panini": [
                "Derived from pad + tini-pratyaya. Genitive plural: pattīnām."
            ]
        },
        "meanings": {
            "english": "Foot-soldiers; infantry",
            "nighantu": "pattin is listed under army synonyms.",
            "nirukta": "'padbhyāṃ gacchatīti pattī' — One who travels on foot.",
            "amara_kosha": "Amarakośa Kṣatriyavarga (2.8.80) lists pattī: 'pattis tu padātir padagaḥ'.",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 2.70 lists pattī.",
            "vedantic": "Foot-soldiers represent the common, working classes. By saluting them, Rudra's presence is recognized in the humblest."
        }
    },
    "kṛtsnavīta": {
        "word": "कृत्स्नवीतः",
        "transliteration": "kṛtsnavītaḥ",
        "root": "kṛtsna (complete) + vīta (enveloped)",
        "grammar": {
            "base": "कृत्स्नवीत (kṛtsnavīta)",
            "form": "dative singular: kṛtsnavītāya (कृत्स्नवीताय)",
            "type": "compound, masculine",
            "panini": [
                "Bahuvrīhi compound. Dative singular: kṛtsnavītāya."
            ]
        },
        "meanings": {
            "english": "Completely enveloped; all-pervading; wearing armor",
            "nighantu": "kṛtsna is listed under synonyms of all/whole (Nighaṇṭu 3.2).",
            "nirukta": "'kṛtsnaṃ vītaṃ vyāptaṃ yena saḥ' — He who completely envelops everything.",
            "amara_kosha": "Amarakośa lists kṛtsna under whole/all (3.1.53).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 3.2 lists kṛtsna.",
            "vedantic": "Rudra as the all-pervading consciousness (Īśāvāsyam) covers and envelops everything in the universe, protecting and sustaining all."
        }
    },
    "dhāvat": {
        "word": "धावन्",
        "transliteration": "dhāvan",
        "root": "√dhāv (to run) + śatṛ",
        "grammar": {
            "base": "धावत् (dhāvat)",
            "form": "dative singular: dhāvate (धावते)",
            "type": "participle, masculine",
            "panini": [
                "Present participle from √dhāv + śatṛ-pratyaya. Dative singular: dhāvate."
            ]
        },
        "meanings": {
            "english": "Running; chasing",
            "nighantu": "√dhāv is listed in Nighaṇṭu under movement roots.",
            "nirukta": "'dhāvati iti dhāvan' — He who runs swiftly to protect or destroy.",
            "amara_kosha": "Amarakośa lists dhāvana under running (3.3.111).",
            "abhidhana_ratnamala": "Lists dhāv in the sense of running.",
            "vedantic": "Rudra is dynamic, always moving and running to aid his devotees."
        }
    },
    "sattva": {
        "word": "सत्त्वम्",
        "transliteration": "sattvam",
        "root": "sat + tva",
        "grammar": {
            "base": "सत्त्व (sattva)",
            "form": "genitive plural: sattvanām (सत्त्वनाम्)",
            "type": "noun, neuter (also masculine)",
            "panini": [
                "Derived from sat + tva-pratyaya. Genitive plural: sattvānām (Vedic: sattvanām)."
            ]
        },
        "meanings": {
            "english": "Living beings; devotees; strength/courage",
            "nighantu": "sattva is associated with being or strength.",
            "nirukta": "Derived from sat (existence): 'sato bhāvaḥ sattvam' — The state of being, or that which exists.",
            "amara_kosha": "Amarakośa lists sattva under creature/strength/essence (3.3.82).",
            "abhidhana_ratnamala": "Abhidhānaratnamālā 3.32 lists sattva.",
            "vedantic": "Sattva represents the quality of purity and light. In the plural, it represents all living creatures that share the divine essence of Sat (Existence)."
        }
    }
}

# Resolve dictionary details for Anuvakam 2
def get_anuvakam2_word_details(word_text, word_id):
    clean_word = clean_sanskrit(word_text)
    ref_key = None
    if "नमो" in clean_word or "नमः" in clean_word or "नमस्" in clean_word:
        ref_key = "namaḥ"
    elif "हिरण्यबाहवे" in clean_word:
        ref_key = "hiraṇyabāhu"
    elif "सेनान्ये" in clean_word:
        ref_key = "senānī"
    elif "दिशाम्" in clean_word:
        ref_key = "diś"
    elif "च" in clean_word:
        ref_key = "ca"
    elif "पतये" in clean_word:
        ref_key = "pati"
    elif "वृक्षेभ्य" in clean_word:
        ref_key = "vṛkṣa"
    elif "हरिकेशेभ्य" in clean_word:
        ref_key = "harikeśa"
    elif "पशूनाम्" in clean_word:
        ref_key = "paśu"
    elif "सस्पिञ्जराय" in clean_word:
        ref_key = "saspinjara"
    elif "त्विषीमते" in clean_word or "त्वीषीमते" in clean_word:
        ref_key = "tviṣīmat"
    elif "पथीनाम्" in clean_word:
        ref_key = "pathin"
    elif "बभ्लुशाय" in clean_word:
        ref_key = "babhlusa"
    elif "विव्याधिने" in clean_word:
        ref_key = "vivyādhin"
    elif "अन्नानाम्" in clean_word:
        ref_key = "anna"
    elif "हरिकेशाय" in clean_word:
        ref_key = "harikeśa"
    elif "उपवीतिने" in clean_word:
        ref_key = "upavītin"
    elif "पुष्टानाम्" in clean_word:
        ref_key = "puṣṭa"
    elif "भवस्य" in clean_word:
        ref_key = "bhava"
    elif "हेत्यै" in clean_word:
        ref_key = "heti"
    elif "जगताम्" in clean_word:
        ref_key = "jagat"
    elif "रुद्राय" in clean_word:
        ref_key = "rudra"
    elif "आतताविने" in clean_word:
        ref_key = "ātatāvin"
    elif "क्षेत्राणाम" in clean_word:
        ref_key = "kṣetra"
    elif "सूताय" in clean_word:
        ref_key = "sūta"
    elif "अहन्त्याय" in clean_word:
        ref_key = "ahantya"
    elif "वनाणाम" in clean_word or "वनानाम्" in clean_word:
        ref_key = "vana"
    elif "रोहिताय" in clean_word:
        ref_key = "rohita"
    elif "स्थपतये" in clean_word:
        ref_key = "sthapati"
    elif "वृक्षाणाम" in clean_word:
        ref_key = "vṛkṣa"
    elif "मन्त्रिणे" in clean_word:
        ref_key = "mantrin"
    elif "वाणिजाय" in clean_word:
        ref_key = "vāṇija"
    elif "कक्षाणाम" in clean_word:
        ref_key = "kakṣa"
    elif "भुवन्तये" in clean_word:
        ref_key = "bhuvanti"
    elif "वारिवस्कृताय" in clean_word:
        ref_key = "varivaskṛta"
    elif "ओषधीनाम्" in clean_word:
        ref_key = "oṣadhi"
    elif "उच्चैर्घोषाय" in clean_word:
        ref_key = "uccaiṣghoṣa"
    elif "आक्रन्दयते" in clean_word:
        ref_key = "ākrandayanta"
    elif "पत्तीनाम्" in clean_word:
        ref_key = "pattin"
    elif "कृत्स्नवीताय" in clean_word:
        ref_key = "kṛtsnavīta"
    elif "धावते" in clean_word:
        ref_key = "dhāvat"
    elif "सत्त्वनाम्" in clean_word or "सत्त्वानम्" in clean_word:
        ref_key = "sattva"
        
    details = ANUVAKAM2_DICT.get(ref_key, {})
    if not details:
        return {
            "id": word_id,
            "pada_form": word_text,
            "meanings": {"english": "", "nirukta": "", "vedantic": ""},
            "grammatical_references": {"panini": "", "case_ending": ""},
            "lexicographical_references": {"nighantu": "", "amara_kosha": "", "abhidhana_ratnamala": ""}
        }
        
    return {
        "id": word_id,
        "pada_form": word_text,
        "meanings": {
            "english": details["meanings"]["english"],
            "nirukta": details["meanings"]["nirukta"],
            "vedantic": details["meanings"]["vedantic"]
        },
        "grammatical_references": {
            "panini": details["grammar"]["panini"],
            "case_ending": details["grammar"]["form"]
        },
        "lexicographical_references": {
            "nighantu": details["meanings"].get("nighantu", ""),
            "amara_kosha": details["meanings"].get("amara_kosha", ""),
            "abhidhana_ratnamala": details["meanings"].get("abhidhana_ratnamala", "")
        }
    }

# Process Anuvakam 1
def process_anuvakam1():
    print("Processing Anuvakam 1...")
    
    with open("/Users/Rkanadam/personal/namakam/src/claude_anuvakam1_word_dictionary.json", "r", encoding="utf-8") as f:
        dict_data = json.load(f)
        
    with open("/Users/Rkanadam/personal/namakam/src/correlated_namakam.json", "r", encoding="utf-8") as f:
        correlated_data = json.load(f)
        
    anuvaka1_corr = correlated_data["anuvakas"][0]
    
    os.makedirs("/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam1/", exist_ok=True)
    
    for idx, m_corr in enumerate(anuvaka1_corr["mantras"]):
        m_id = m_corr["id"]
        samhita = m_corr["sanskrit"]["samhita"]
        pada = m_corr["sanskrit"]["pada"]
        krama = m_corr["sanskrit"]["krama"]
        
        m_dict = dict_data["mantras"][idx]
        word_sequence = m_dict["word_sequence"]
        
        current_page_file = m_corr["sources"].get("rudradhyaya_page")
        if not current_page_file:
            for fallback_idx in range(idx - 1, -1, -1):
                fallback_page = anuvaka1_corr["mantras"][fallback_idx]["sources"].get("rudradhyaya_page")
                if fallback_page:
                    current_page_file = fallback_page
                    break
        
        current_page_num = int(re.search(r"page-(\d+)\.txt", current_page_file).group(1)) if current_page_file else 18
        
        next_page_num = None
        for fallback_idx in range(idx + 1, len(anuvaka1_corr["mantras"])):
            fallback_page = anuvaka1_corr["mantras"][fallback_idx]["sources"].get("rudradhyaya_page")
            if fallback_page:
                next_page_num = int(re.search(r"page-(\d+)\.txt", fallback_page).group(1))
                break
        
        if next_page_num is None:
            next_page_num = 38
        
        sayana_sanskrit, bb_sanskrit = extract_commentaries(m_id, current_page_num, next_page_num)
        sayana_eng, bb_eng = split_english_commentaries(m_corr["translations"]["sayana"])
        
        commentaries = {
            "sayana": {
                "rishi": m_corr["translations"].get("rishi", "Kashyapa"),
                "chandas": m_corr["translations"].get("chandas", "Anushtup"),
                "devata": m_corr["translations"].get("devata", "Rudra"),
                "text": sayana_eng,
                "sanskrit": sayana_sanskrit
            },
            "bhatta_bhaskara": {
                "rishi": m_corr["translations"].get("rishi", "Kashyapa"),
                "chandas": m_corr["translations"].get("chandas", "Anushtup"),
                "devata": m_corr["translations"].get("devata", "Rudra"),
                "dhyana": "Meditation on Shiva as detailed in standard commentaries.",
                "text": bb_eng,
                "sanskrit": bb_sanskrit
            },
            "abhinava_shankara": {
                "rishi": m_corr["translations"].get("rishi", "Atreya"),
                "chandas": m_corr["translations"].get("chandas", "Anushtup"),
                "devata": m_corr["translations"].get("devata", "Sri Rudra"),
                "dhyana": "Meditation on Lord Maheshvara with resplendent Goddess.",
                "text": m_corr["translations"].get("abhinava_shankara", ""),
                "sanskrit": m_corr["commentaries_sanskrit"].get("abhinava_shankara", "")
            }
        }
        
        words = []
        pada_parts = [p.replace(" ॥", "").strip() for p in pada.split(" । ")]
        
        for w_idx, item in enumerate(word_sequence):
            w_id = w_idx + 1
            ref = item["ref"]
            pada_form = pada_parts[w_idx] if w_idx < len(pada_parts) else item["form"]
            
            dict_item = dict_data["dictionary"].get(ref, {})
            
            start_idx = 0
            end_idx = 0
            text_span = ""
            
            clean_pada = clean_sanskrit(pada_form)
            clean_sam = clean_sanskrit(samhita)
            match_found = False
            for length in range(len(clean_pada), 1, -1):
                sub = clean_pada[:length]
                idx_in_sam = clean_sam.find(sub)
                if idx_in_sam != -1:
                    char_count = 0
                    for raw_idx, char in enumerate(samhita):
                        if char not in ['॑', '॒', '᳚', '।', '॥', ' ']:
                            if char_count == idx_in_sam:
                                start_idx = raw_idx
                                sub_len = len(sub)
                                raw_end_count = 0
                                for raw_end_idx in range(start_idx, len(samhita)):
                                    end_char = samhita[raw_end_idx]
                                    if end_char not in ['॑', '॒', '᳚', '।', '॥', ' ']:
                                        raw_end_count += 1
                                    if raw_end_count == sub_len:
                                        end_idx = raw_end_idx + 1
                                        text_span = samhita[start_idx:end_idx]
                                        match_found = True
                                        break
                                break
                            char_count += 1
                if match_found:
                    break
                    
            if not match_found:
                text_span = pada_form
                start_idx = 0
                end_idx = len(pada_form)
                
            words.append({
                "id": w_id,
                "pada_form": pada_form,
                "samhita_span": {
                    "start": start_idx,
                    "end": end_idx,
                    "text": text_span
                },
                "meanings": {
                    "english": dict_item.get("meanings", {}).get("english", ""),
                    "nirukta": dict_item.get("meanings", {}).get("nirukta", ""),
                    "vedantic": dict_item.get("meanings", {}).get("vedantic", "")
                },
                "grammatical_references": {
                    "panini": dict_item.get("grammar", {}).get("panini", []),
                    "case_ending": dict_item.get("grammar", {}).get("form", "")
                },
                "lexicographical_references": {
                    "nighantu": dict_item.get("meanings", {}).get("nighantu", ""),
                    "amara_kosha": dict_item.get("meanings", {}).get("amara_kosha", ""),
                    "abhidhana_ratnamala": dict_item.get("meanings", {}).get("abhidhana_ratnamala", "")
                }
            })
            
        sam_chunks = re.split(r'(\s+।\s+|\s+॥\s*|\s+)', samhita)
        sam_chunks = [c for c in sam_chunks if c]
        samhita_tokens = align_words_to_chunks(sam_chunks, words)
        
        pada_chunks = re.split(r'(\s+।\s+|\s+॥\s*|\s+)', pada)
        pada_chunks = [c for c in pada_chunks if c]
        pada_tokens = align_words_to_chunks(pada_chunks, words)
        
        krama_chunks = re.split(r'(\s+।\s+|\s+॥\s*|\s+)', krama)
        krama_chunks = [c for c in krama_chunks if c]
        krama_tokens = align_krama_chunks(krama_chunks, words)
        
        mantra_obj = {
            "anuvakam": 1,
            "title": "प्रथमोनुवाकः",
            "id": m_id,
            "samhita": samhita,
            "pada": pada,
            "krama": krama,
            "commentaries": commentaries,
            "samhita_tokens": samhita_tokens,
            "pada_tokens": pada_tokens,
            "krama_tokens": krama_tokens,
            "words": words
        }
        
        out_path = f"/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam1/mantra{m_id}.json"
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(mantra_obj, out_f, ensure_ascii=False, indent=2)
            
    print("Anuvakam 1 completed successfully.")

# Process Anuvakam 2
def process_anuvakam2():
    print("Processing Anuvakam 2...")
    
    with open("/Users/Rkanadam/personal/namakam/src/correlated_namakam.json", "r", encoding="utf-8") as f:
        correlated_data = json.load(f)
        
    anuvaka2_corr = correlated_data["anuvakas"][1]
    
    os.makedirs("/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam2/", exist_ok=True)
    
    for idx, m_corr in enumerate(anuvaka2_corr["mantras"]):
        m_id = m_corr["id"]
        samhita = m_corr["sanskrit"]["samhita"]
        pada = m_corr["sanskrit"]["pada"]
        krama = m_corr["sanskrit"]["krama"]
        
        sayana_eng, bb_eng = split_english_commentaries(m_corr["translations"]["sayana"])
        
        commentaries = {
            "sayana": {
                "rishi": "Manduka",
                "chandas": "Maha-Gayatri",
                "devata": "Rudra",
                "text": sayana_eng,
                "sanskrit": ""
            },
            "bhatta_bhaskara": {
                "rishi": "Manduka",
                "chandas": "Maha-Gayatri",
                "devata": "Rudra",
                "dhyana": "Meditation on Shiva's universal form (Vaishvarupya).",
                "text": bb_eng,
                "sanskrit": ""
            },
            "abhinava_shankara": {
                "rishi": "Manduka",
                "chandas": "Maha-Gayatri",
                "devata": "Rudra",
                "dhyana": "Meditation on the golden-armed Lord.",
                "text": m_corr["translations"].get("abhinava_shankara", ""),
                "sanskrit": m_corr["commentaries_sanskrit"].get("abhinava_shankara", "")
            }
        }
        
        words = []
        pada_parts = [p.replace(" ॥", "").strip() for p in pada.split(" । ")]
        
        for w_idx, part in enumerate(pada_parts):
            w_id = w_idx + 1
            word_details = get_anuvakam2_word_details(part, w_id)
            
            start_idx = 0
            end_idx = 0
            text_span = ""
            
            clean_pada = clean_sanskrit(part)
            clean_sam = clean_sanskrit(samhita)
            match_found = False
            for length in range(len(clean_pada), 1, -1):
                sub = clean_pada[:length]
                idx_in_sam = clean_sam.find(sub)
                if idx_in_sam != -1:
                    char_count = 0
                    for raw_idx, char in enumerate(samhita):
                        if char not in ['॑', '॒', '᳚', '।', '॥', ' ']:
                            if char_count == idx_in_sam:
                                start_idx = raw_idx
                                sub_len = len(sub)
                                raw_end_count = 0
                                for raw_end_idx in range(start_idx, len(samhita)):
                                    end_char = samhita[raw_end_idx]
                                    if end_char not in ['॑', '॒', '᳚', '।', '॥', ' ']:
                                        raw_end_count += 1
                                    if raw_end_count == sub_len:
                                        end_idx = raw_end_idx + 1
                                        text_span = samhita[start_idx:end_idx]
                                        match_found = True
                                        break
                                break
                            char_count += 1
                if match_found:
                    break
                    
            if not match_found:
                text_span = part
                start_idx = 0
                end_idx = len(part)
                
            word_details["samhita_span"] = {
                "start": start_idx,
                "end": end_idx,
                "text": text_span
            }
            words.append(word_details)
            
        sam_chunks = re.split(r'(\s+।\s+|\s+॥\s*|\s+)', samhita)
        sam_chunks = [c for c in sam_chunks if c]
        samhita_tokens = align_words_to_chunks(sam_chunks, words)
        
        pada_chunks = re.split(r'(\s+।\s+|\s+॥\s*|\s+)', pada)
        pada_chunks = [c for c in pada_chunks if c]
        pada_tokens = align_words_to_chunks(pada_chunks, words)
        
        krama_chunks = re.split(r'(\s+।\s+|\s+॥\s*|\s+)', krama)
        krama_chunks = [c for c in krama_chunks if c]
        krama_tokens = align_krama_chunks(krama_chunks, words)
        
        mantra_obj = {
            "anuvakam": 2,
            "title": "द्वितीयोनुवाकः",
            "id": m_id,
            "samhita": samhita,
            "pada": pada,
            "krama": krama,
            "commentaries": commentaries,
            "samhita_tokens": samhita_tokens,
            "pada_tokens": pada_tokens,
            "krama_tokens": krama_tokens,
            "words": words
        }
        
        out_path = f"/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam2/mantra{m_id}.json"
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(mantra_obj, out_f, ensure_ascii=False, indent=2)
            
    print("Anuvakam 2 completed successfully.")

if __name__ == "__main__":
    process_anuvakam1()
    process_anuvakam2()
    print("All tasks completed successfully!")
