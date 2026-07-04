import json
import os
import re

# Output directories
ANUVAKAM7_DIR = '/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam7'
ANUVAKAM8_DIR = '/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam8'

os.makedirs(ANUVAKAM7_DIR, exist_ok=True)
os.makedirs(ANUVAKAM8_DIR, exist_ok=True)

# Word Database containing grammatical, Nirukta, and lexicographical references for all unique words
WORD_DB = {
    "नमः": {
        "meanings": {
            "english": "Salutations / Bowing down / Reverence.",
            "nirukta": "Derived from the root 'nam' (नम्) meaning 'to bow, bend, or submit'. In Nirukta, 'namas' is defined in the sense of bowing or honoring (namanīya).",
            "vedantic": "Interpreted as 'Na' (not) + 'mama' (mine) — indicating the complete surrender of the individual ego and the realization that nothing belongs to the limited self, but all belongs to the Supreme consciousness."
        },
        "grammatical_references": {
            "panini": "Derived from the verbal root √nam (नमुँ प्रह्वत्वे शब्दे च, Bhvādi-gaṇa, 1.1030) with the suffix 'asun' (असुन्). Governs the dative case (caturthī vibhakti) by the Aṣṭadhyāyī sūtra: 'Namaḥ-svasti-svāhā-svadhā-alaṃ-vaṣaḍ-yogāc-ca' (2.3.16).",
            "case_ending": "Avyaya (indeclinable nominal form/noun)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms (udaka-nāmāni, Nighaṇṭu 1.12, item 17) and food synonyms (anna-nāmāni, Nighaṇṭu 2.7) due to its Vedic polysemous usage representing nourishment and flow.",
            "amara_kosha": "Listed in Amarakośa Avyayavarga (3.4.19) as a term indicating bowing, salutation, or reverence.",
            "abhidhana_ratnamala": "Classified in Anekārtha-kāṇḍa (5.26) under Avyayas, meaning bowing or salutation (namaskāra)."
        }
    },
    "नमो": {
        "meanings": {
            "english": "Salutations / Bowing down / Reverence.",
            "nirukta": "Same as 'नमः'.",
            "vedantic": "Same as 'नमः'."
        },
        "grammatical_references": {
            "panini": "Same as 'नमः' (form altered by Visarga Sandhi: 'namas' becomes 'namo' before voiced consonants by rule 'haśi ca' 6.1.114).",
            "case_ending": "Avyaya."
        },
        "lexicographical_references": {
            "nighantu": "Same as 'नमः'.",
            "amara_kosha": "Same as 'नमः'.",
            "abhidhana_ratnamala": "Same as 'नमः'."
        }
    },
    "दुन्दुभ्याय": {
        "meanings": {
            "english": "To the one in the form of the war-drum (dundubhi).",
            "nirukta": "Derived from 'dundubhi', which is onomatopoeic from the sound 'dhum-dhum' of the drum, or from √dubh (to strike/sound) with reduplication.",
            "vedantic": "Rudra is the cosmic sound (Nada-Brahman) that reverberates through the universe. The war-drum represents the call to action, awakening, and the roar of the cosmic dissolution."
        },
        "grammatical_references": {
            "panini": "Derived from 'dundubhi' + suffix 'ya' (signifying existence/relation, by 'tatra bhavaḥ') -> 'dundubhya' + dative singular 'ṅe' (caturthī-ekavacana) -> 'dundubhyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Śabdādivarga (1.5.8) as a synonym for drum: 'bherī dundubhir-ānakaḥ'.",
            "abhidhana_ratnamala": "Classified in Śabda-kāṇḍa under musical instruments."
        }
    },
    "आहनन्याय": {
        "meanings": {
            "english": "To the one in the form of the drum-stick, or the sound produced by striking.",
            "nirukta": "Derived from prefix 'ā' + root 'han' (to strike/kill) + suffix 'ya' (āhananya), meaning that which is used to strike, or the sound produced thereby.",
            "vedantic": "Rudra is not only the instrument of sounding (the drum-stick) but also the struck sound itself, representing both cause and effect in the cosmic display."
        },
        "grammatical_references": {
            "panini": "Derived from ā-√han (हनँ हिंसागत्योः, Adādi-gaṇa, 2.0002) with the kṛtya suffix 'nyat' or 'yat' (by 'āṅy-āhanaḥ' or general rules) + dative singular 'ṅe' -> 'āhananyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "धृष्णवे": {
        "meanings": {
            "english": "To the courageous, bold, or overpowering one.",
            "nirukta": "Derived from the root 'dhṛṣ' (धृष्) meaning 'to dare, be bold, or overpower'.",
            "vedantic": "Rudra is the supreme courage and power that remains untamed and victorious over all limitations, ignorance, and darkness."
        },
        "grammatical_references": {
            "panini": "Derived from root √dhṛṣ (धृषाँ प्रागल्भ्ये, Bhvādi-gaṇa, 1.0776) with the kiti-suffix 'knu' (क्नु) by rule 'glā-ji-stha-śca-gla-su-sū-dhṛ-bhaḥ' + dative singular 'ṅe' -> 'dhṛष्णवे'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for strength or courage (bala-nāmāni).",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8) under terms for bravery or heroism.",
            "abhidhana_ratnamala": "Listed in Anekārtha-kāṇḍa under names of strength and valor."
        }
    },
    "प्रमृशाय": {
        "meanings": {
            "english": "To the examiner, discerner, or the one who grasps/strikes the enemy.",
            "nirukta": "Derived from prefix 'pra' + root 'mṛś' (मृश् - to touch, consider, reflect, or grasp).",
            "vedantic": "Refers to the Lord as the inner witness (sākṣin) who examines and weighs the karma of all beings, or who penetrates the essence of all things."
        },
        "grammatical_references": {
            "panini": "Derived from pra-√mṛś (मृशँ आमर्शने, Tudādi-gaṇa, 6.0150) with the suffix 'ghañ' or 'ac' + dative singular 'ṅe' -> 'pramṛśāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "दूताय": {
        "meanings": {
            "english": "To the messenger or envoy (especially in the form of Agni/Fire).",
            "nirukta": "Derived from √dū (to go) or √du (to distress/burn) + 'tan' suffix; he who goes to convey messages.",
            "vedantic": "Rudra as Agni acts as the divine messenger carrying the offerings of human beings to the gods, linking the finite to the infinite."
        },
        "grammatical_references": {
            "panini": "Derived from root √dū (दू उपतापे, Divādi-gaṇa, 4.0042) or √du (दु गत्यर्थः) with Uṇādi suffix 'tan' (तन्) -> 'dūta' + dative singular 'ṅe' -> 'dūtāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under the deities of the middle region or messengers.",
            "amara_kosha": "Listed in Svargavarga (1.1.58) as 'dūtaḥ sandeśaharaḥ'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.19) under messengers."
        }
    },
    "प्रहिताय": {
        "meanings": {
            "english": "To the sent one, the special envoy, or the one who is highly beneficial.",
            "nirukta": "Derived from prefix 'pra' + root 'hi' (to send/promote) + past passive participle 'kta' -> 'prahita'.",
            "vedantic": "Refers to the Lord sent/manifested in the world for the welfare of devotees, or the promptings of the inner controller (Antaryāmin)."
        },
        "grammatical_references": {
            "panini": "Derived from pra-√hi (हिँ गतौ वृद्धौ च, Svādi-gaṇa, 5.0011) with the suffix 'kta' (क्त) + dative singular 'ṅe' -> 'prahitāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under terms for messengers or servants sent on a mission.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "निषङ्गिणे": {
        "meanings": {
            "english": "To the one possessing a sword (or arrow/quiver).",
            "nirukta": "Derived from 'niṣaṅga' (sword or attachment) + possessive suffix 'in' (ini).",
            "vedantic": "The sword represents the sharp power of discrimination (viveka) that cuts through the knot of ignorance (hṛdaya-granthi)."
        },
        "grammatical_references": {
            "panini": "Derived from 'niṣaṅga' + possessive suffix 'ini' (इनिँ) by rule 'atas-ini-ṭhanau' (5.2.115) -> 'niṣaṅgin' + dative singular 'ṅe' -> 'niṣaṅgiṇe' (with 'n' to 'ṇ' change by 'nude-śca-śo-vibhāṣā').",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.93) as sword-bearer: 'niṣaṅgī khaḍgadharaḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "इषुधिमते": {
        "meanings": {
            "english": "To the one possessing a quiver (iṣudhi) of arrows.",
            "nirukta": "Derived from 'iṣudhi' (arrow-holder: iṣu + √dhā) + possessive suffix 'matup'.",
            "vedantic": "The quiver represents the endless repository of divine laws, resources, and corrective forces available to the Lord."
        },
        "grammatical_references": {
            "panini": "Derived from compound 'iṣu-dhi' (iṣūṇāṃ dhānam/dhīyate 'smin) + possessive suffix 'matup' (मतुप्) -> 'iṣudhimat' + dative singular 'ṅe' -> 'iṣudhimate'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under weapons or quiver synonyms.",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.91) as 'tūṇī-pādāv-iṣudhiḥ'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.126) under quiver synonyms: 'tūṇa', 'iṣudhi'."
        }
    },
    "तीक्ष्णेषवे": {
        "meanings": {
            "english": "To the one possessing sharp (tīkṣṇa) arrows (iṣu).",
            "nirukta": "Bahuvrīhi compound: 'tīkṣṇāḥ iṣavaḥ yasya saḥ' (he whose arrows are sharp).",
            "vedantic": "Sharp arrows represent the penetrating, laser-focused power of truth that pierces the illusion of duality and destroys ego-constructs instantly."
        },
        "grammatical_references": {
            "panini": "Derived as a Bahuvrīhi compound of 'tīkṣṇa' + 'iṣu' + dative singular 'ṅe' -> 'tīkṣnedgeṣave'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "आयुधिने": {
        "meanings": {
            "english": "To the one bearing weapons (āyudha).",
            "nirukta": "Derived from 'āyudha' (weapon: ā-√yudh) + possessive suffix 'in' (ini).",
            "vedantic": "Rudra's weapons are the active forces of cosmic regulation and correction, always ready to protect Dharma and dissolve adharma."
        },
        "grammatical_references": {
            "panini": "Derived from 'āyudha' + possessive suffix 'ini' -> 'āyudhin' + dative singular 'ṅe' -> 'āyudhine'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Kṣatriyavarga under terms for armed warriors.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "स्वायुधाय": {
        "meanings": {
            "english": "To the one possessing excellent/beautiful (su) weapons (āyudha).",
            "nirukta": "Bahuvrīhi compound: 'śobhanāni āyudhāni yasya saḥ' (he whose weapons are excellent/beautiful).",
            "vedantic": "The 'beauty' or 'excellence' of the Lord's weapons lies in their non-violence toward devotees; they are instruments of absolute grace, peace, and liberation."
        },
        "grammatical_references": {
            "panini": "Derived as a Bahuvrīhi compound of 'su' + 'āyudha' + dative singular 'ṅe' -> 'svāyudhāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "सुधन्वने": {
        "meanings": {
            "english": "To the one possessing an excellent/beautiful (su) bow (dhanvan).",
            "nirukta": "Bahuvrīhi compound: 'śobhanaṃ dhanus yasya saḥ' (he whose bow is excellent/beautiful).",
            "vedantic": "The bow represents the sacred syllable OM (Pranava). A 'beautiful bow' means the chanting and meditation on OM is pure, clear, and leads straight to the target (Brahman)."
        },
        "grammatical_references": {
            "panini": "Derived as a Bahuvrīhi compound of 'su' + 'dhanvan' + dative singular 'ṅe' -> 'sudhanvane'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.84) as a synonym for bow: 'sudhanvā'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "स्रुत्याय": {
        "meanings": {
            "english": "To the one residing in the small pathways, lanes, or footpaths.",
            "nirukta": "Derived from 'srutyā' (footpath/lane, derived from √sru - to flow/run) + suffix 'yat' or 'ghañ' (existing in).",
            "vedantic": "Rudra is present not only in grand places but also in the narrowest, most remote, and humble pathways of life."
        },
        "grammatical_references": {
            "panini": "Derived from 'srutyā' + taddhita suffix 'yat' (in the sense of 'bhavaḥ' - existing there, by rule 'tatra bhavaḥ' 4.3.53) + dative singular 'ṅe' -> 'srutyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under path/way synonyms.",
            "amara_kosha": "Listed in Bhūmivarga (2.1.15) as a synonym for a footpath: 'srutyā'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.164) as a footpath."
        }
    },
    "पथ्याय": {
        "meanings": {
            "english": "To the one residing in the highways, main roads, or path of Dharma.",
            "nirukta": "Derived from 'pathin' (path) + suffix 'ya' (pathyā - fit for the path, or highway).",
            "vedantic": "The Lord is the protector of those who travel the main highway of spiritual life (the Devayāna and Pitṛyāna, or the path of right action/Dharma)."
        },
        "grammatical_references": {
            "panini": "Derived from 'pathin' + suffix 'yat' (by rule 'patho yuttarapadavyabahāre' or general 'tatra bhavaḥ' rules) -> 'pathya' + dative singular 'ṅe' -> 'pathyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under path synonyms.",
            "amara_kosha": "Listed in Bhūmivarga (2.1.15) as 'panthāḥ... pathyā'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.164) under paths."
        }
    },
    "काट्याय": {
        "meanings": {
            "english": "To the one residing in a well, pit, or dense/impenetrable forest (kāṭa).",
            "nirukta": "Derived from 'kaṭa' (a hole, well, or dense forest) + suffix 'ya'.",
            "vedantic": "Rudra is present in the hidden, deep, and difficult-to-reach recesses of the heart (the cavern of the heart, guhā), as well as in life's most challenging crises."
        },
        "grammatical_references": {
            "panini": "Derived from 'kaṭa' + suffix 'yat' (bhava-arthe) + dative singular 'ṅe' -> 'kāṭyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "नीप्याय": {
        "meanings": {
            "english": "To the one residing in valleys, low-lying lands, or water-channels (nīpa).",
            "nirukta": "Derived from 'nīpa' (low-land or foot of a mountain) + suffix 'ya'.",
            "vedantic": "Rudra resides in the lowest, humblest places, showing that the divine is equally present in high peaks and low valleys."
        },
        "grammatical_references": {
            "panini": "Derived from 'nīpa' + suffix 'yat' + dative singular 'ṅe' -> 'nīpyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Bhūmivarga under mountain-valleys or lowlands.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "सूद्याय": {
        "meanings": {
            "english": "To the one residing in slush, mud, or marshy waters (sūda).",
            "nirukta": "Derived from 'sūda' (marsh/mud/well) + suffix 'ya'.",
            "vedantic": "The Lord is present in the muddy, impure, and transitional elements of life, showing that nothing is outside the divine presence."
        },
        "grammatical_references": {
            "panini": "Derived from 'sūda' + suffix 'yat' + dative singular 'ṅe' -> 'sūdyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms.",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "सरस्याय": {
        "meanings": {
            "english": "To the one residing in large lakes, pools, or ponds (saras).",
            "nirukta": "Derived from 'saras' (lake, from √sṛ - to flow/glide) + suffix 'ya'.",
            "vedantic": "Rudra is the tranquil, deep consciousness resembled by a calm lake (saras), reflecting the light of truth clearly."
        },
        "grammatical_references": {
            "panini": "Derived from 'saras' + suffix 'yat' + dative singular 'ṅe' -> 'sarasyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms.",
            "amara_kosha": "Listed in Vārivarga (1.10) under lakes and pools.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under water bodies."
        }
    },
    "नाद्याय": {
        "meanings": {
            "english": "To the one residing in flowing rivers (nadī).",
            "nirukta": "Derived from 'nadī' (river, from √nad - to sound/roar) + suffix 'ya'.",
            "vedantic": "Rudra is the dynamic, flowing stream of life and time (saṃsāra-nadī), roaring with activity, yet ever pure."
        },
        "grammatical_references": {
            "panini": "Derived from 'nadī' + suffix 'yat' (or 'yaḥ') + dative singular 'ṅe' -> 'nādyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms.",
            "amara_kosha": "Listed in Vārivarga (1.10.31) under rivers: 'nadī'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under river names."
        }
    },
    "वैशन्ताय": {
        "meanings": {
            "english": "To the one residing in small ponds, tanks, or reservoirs (veśanta).",
            "nirukta": "Derived from 'veśanta' (a small pool, from √viś - to enter, where water settles) + suffix 'a' or 'ya'.",
            "vedantic": "Rudra resides in the small, localized bodies of water, representing the individual souls (jīvas) in whom the cosmic consciousness resides in miniature."
        },
        "grammatical_references": {
            "panini": "Derived from 'veśanta' + suffix 'aṇ' or 'ya' -> 'vaiśanta' + dative singular 'ṅe' -> 'vaiśantāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms.",
            "amara_kosha": "Listed in Vārivarga (1.10.15) under small ponds: 'veśantaḥ palvalam'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under small water bodies."
        }
    },
    "कूप्याय": {
        "meanings": {
            "english": "To the one residing in deep wells (kūpa).",
            "nirukta": "Derived from 'kūpa' (a well/hole, from √kup - to be agitated, or from kavi + √pā) + suffix 'ya'.",
            "vedantic": "Rudra is the deep, hidden water of self-knowledge inside the well of the body, which must be drawn out through the rope of devotion and bucket of effort."
        },
        "grammatical_references": {
            "panini": "Derived from 'kūpa' + suffix 'yat' (by rule 'kūpād-yañ') -> 'kūpya' + dative singular 'ṅe' -> 'kūpyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms.",
            "amara_kosha": "Listed in Vārivarga (1.10.28) under wells: 'kūpas-tu andhūḥ'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under wells."
        }
    },
    "अवट्याय": {
        "meanings": {
            "english": "To the one residing in ditches, pits, or holes in the ground (avaṭa).",
            "nirukta": "Derived from 'avaṭa' (a pit/hole) + suffix 'ya'.",
            "vedantic": "Shows that the divine is present in the uneven, broken, and dark pits of existence, protecting the traveller even in falls."
        },
        "grammatical_references": {
            "panini": "Derived from 'avaṭa' + suffix 'yat' + dative singular 'ṅe' -> 'avaṭyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Vārivarga under pits or ditches: 'avaṭo vā'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "वर्ष्याय": {
        "meanings": {
            "english": "To the one in the rain (varṣā).",
            "nirukta": "Derived from 'varṣā' (rain, from √vṛṣ - to pour/rain) + suffix 'ya' (existing in).",
            "vedantic": "Rudra is the refreshing, life-giving rain of grace that pours down from the heaven of consciousness to nourish the parched world."
        },
        "grammatical_references": {
            "panini": "Derived from 'varṣā' + suffix 'yat' -> 'varṣya' + dative singular 'ṅe' -> 'varṣyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under rain or water synonyms.",
            "amara_kosha": "Listed in Svargavarga under rain and clouds.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "अवर्ष्याय": {
        "meanings": {
            "english": "To the one residing in drought, no-rain, or clear weather.",
            "nirukta": "Negative compound: 'na varṣyaḥ' (not in the rain, or clear weather).",
            "vedantic": "Rudra is present during times of difficulty (drought/testing) as well as prosperity, representing the unshakeable peace that transcends all external conditions."
        },
        "grammatical_references": {
            "panini": "Derived from 'na' (nan) + 'varṣya' + dative singular 'ṅe' -> 'avarṣyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "मेघ्याय": {
        "meanings": {
            "english": "To the one residing in the clouds (megha).",
            "nirukta": "Derived from 'megha' (cloud, from √mih - to sprinkle/make wet) + suffix 'ya'.",
            "vedantic": "Rudra is the cloud of divine mercy that gathers in the sky of the mind, ready to shower the nectar of bliss."
        },
        "grammatical_references": {
            "panini": "Derived from 'megha' + suffix 'yat' + dative singular 'ṅe' -> 'meghyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under cloud synonyms.",
            "amara_kosha": "Listed in Svargavarga (1.1.41) under clouds: 'megha-dhārādhara-jaladhara'.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa under clouds."
        }
    },
    "विद्युत्याय": {
        "meanings": {
            "english": "To the one residing in the lightning (vidyut).",
            "nirukta": "Derived from 'vidyut' (lightning, from vi-√dyut - to shine/flash) + suffix 'ya'.",
            "vedantic": "Rudra is the lightning-flash of sudden illumination (sphoṭa/satori) that dispels the darkness of ignorance in a single instant."
        },
        "grammatical_references": {
            "panini": "Derived from 'vidyut' + suffix 'yat' + dative singular 'ṅe' -> 'vidyutyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under atmospheric phenomena (lightning).",
            "amara_kosha": "Listed in Svargavarga (1.1.47) as 'vidyut taḍit'.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa under lightning."
        }
    },
    "ईध्रियाय": {
        "meanings": {
            "english": "To the one residing in the clear, unclouded sky (īdhrā).",
            "nirukta": "Derived from 'īdhrā' (clear weather/pure light, from √indh - to kindle/shine) + suffix 'ya'.",
            "vedantic": "Rudra is the clear, untainted, and pure sky of pure consciousness (cidākāśa), free from the clouds of thought (vṛttis)."
        },
        "grammatical_references": {
            "panini": "Derived from 'īdhrā' + suffix 'ghas' or 'yat' -> 'īdhriya' + dative singular 'ṅe' -> 'īdhriyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "आतप्याय": {
        "meanings": {
            "english": "To the one residing in the hot sun, sunshine, or heat (ātapa).",
            "nirukta": "Derived from 'ātapa' (heat of the sun, from ā-√tap - to heat/shine) + suffix 'ya'.",
            "vedantic": "Rudra is the heat of spiritual austerity (tapas) that purifies the soul, and the light of truth that shines brightly."
        },
        "grammatical_references": {
            "panini": "Derived from 'ātapa' + suffix 'yat' + dative singular 'ṅe' -> 'ātapyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Svargavarga under sun-shine: 'ātapaḥ'.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa under light and heat."
        }
    },
    "वात्याय": {
        "meanings": {
            "english": "To the one residing in the wind, gale, or storm (vāta).",
            "nirukta": "Derived from 'vāta' (wind, from √vā - to blow) + suffix 'ya'.",
            "vedantic": "Rudra is the vital breath (prāṇa) that moves all living beings, and the powerful wind of change that sweeps away old constructs."
        },
        "grammatical_references": {
            "panini": "Derived from 'vāta' + suffix 'yat' + dative singular 'ṅe' -> 'vātyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under wind synonyms.",
            "amara_kosha": "Listed in Svargavarga (1.1.55) as 'vāto vāyuḥ'.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa under wind names."
        }
    },
    "रेष्मियाय": {
        "meanings": {
            "english": "To the one residing in the storm, hailstorm, or wind of dissolution (reṣma).",
            "nirukta": "Derived from 'reṣma' (a storm/destroying wind, from √riṣ - to injure/perish) + suffix 'ya'.",
            "vedantic": "Rudra is the force of dissolution (pralaya) that resolves the universe back into its unmanifest cause, clearing the path for new creation."
        },
        "grammatical_references": {
            "panini": "Derived from 'reṣma' + suffix 'yat' + dative singular 'ṅe' -> 'reष्मियाय'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "वास्तव्याय": {
        "meanings": {
            "english": "To the one residing in the building site, homestead, or wealth in the form of property (vāstu).",
            "nirukta": "Derived from 'vāstu' (house/site, from √vas - to dwell) + suffix 'tavya' or 'yat' (vāstavya).",
            "vedantic": "Rudra is the substrate and foundation of all structures, the ground of being on which the superstructure of the universe is built."
        },
        "grammatical_references": {
            "panini": "Derived from 'vāstu' + suffix 'yat' -> 'vāstavya' + dative singular 'ṅe' -> 'vāstavyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Bhūmivarga (2.2.4) under buildings: 'vāstu'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "वास्तुपाय": {
        "meanings": {
            "english": "To the guardian/protector (pā) of the homestead/site (vāstu).",
            "nirukta": "Upapada compound: 'vāstu pati' or 'vāstu pāti' (he who protects the site/house).",
            "vedantic": "Rudra as Vāstoṣpati is the guardian of the home, protecting the family, cattle, and peace of the household."
        },
        "grammatical_references": {
            "panini": "Derived as an Upapada compound: 'vāstu' + √pā (पा रक्षणे, Adādi-gaṇa, 2.0051) + suffix 'ka' or 'ḍa' -> 'vāstupa' + dative singular 'ṅe' -> 'vāstupāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Bhūmivarga under house guardians.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "सोमाय": {
        "meanings": {
            "english": "To Soma (the moon-god or beverage), or to the one who is accompanied by Umā (sa + umā).",
            "nirukta": "(1) 'Sa-umā' = accompanied by Umā (the Divine Mother/Sakti). (2) Derived from √su (to press/extract) + 'man' suffix, meaning the Soma juice or Moon-god.",
            "vedantic": "Rudra is always united with His supreme energy (Sakti/Umā), through whom He performs creation, preservation, and dissolution. Also, Soma represents the nectar of immortal bliss (ānanda)."
        },
        "grammatical_references": {
            "panini": "Derived from 'soma' + dative singular 'ṅe' -> 'somāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under atmospheric deities and plant synonyms.",
            "amara_kosha": "Listed in Svargavarga (1.1.59) as 'soma indur-niśāpatiḥ'.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa as moon-god."
        }
    },
    "रुद्राय": {
        "meanings": {
            "english": "To Rudra.",
            "nirukta": "Yāska's Nirukta gives multiple etymologies: (1) 'Rudra rautīti sataḥ' — He who roars/howls; (2) 'Rodayater vā' — He who makes others weep; (3) 'Rutam (sorrow/ignorance) dravayati (dissolves) iti Rudrah' — He who drives away suffering.",
            "vedantic": "The destroyer of primary ignorance (avidya) and worldly suffering (samsara-duhkha). He is the ultimate reality that dissolves the illusion of duality."
        },
        "grammatical_references": {
            "panini": "Derived from the verbal root √rud (रुदिँ अश्रुविमोचने, Adādi-gaṇa, 2.0002) with the Uṇādi suffix 'kran' (रक्) -> 'rudra' + dative singular 'ṅe' -> 'rudrāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under deities of the atmospheric region (Nighaṇṭu 5.5).",
            "amara_kosha": "Listed in Svargavarga (1.1.34) as a major synonym of Lord Śiva: 'rudraḥ sthāṇur umāpatiḥ'.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa (1.30-33) as a key name of Lord Shiva: 'rudras-tryambaka-īśānaḥ'."
        }
    },
    "ताम्राय": {
        "meanings": {
            "english": "To the copper-red one (at sunrise).",
            "nirukta": "Derived from √tam (to choke/darken) + suffix 'ran', meaning the color of copper.",
            "vedantic": "Represents the visible solar form of Rudra at sunrise, indicating the beginning of cosmic manifestation."
        },
        "grammatical_references": {
            "panini": "Derived from root √tam (तमुँ काङ्क्षायाम्, Divādi-gaṇa, 4.0099) with Uṇādi suffix 'ran' -> 'tāmra' + dative singular 'ṅe' -> 'tāmrāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed under colors and metals: 'tāmrakaḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "अरुणाय": {
        "meanings": {
            "english": "To the ruddy or pinkish-red one (after sunrise).",
            "nirukta": "Derived from √ṛ (to move/go) + Uṇādi suffix 'unan' -> 'aruṇa' (the dawn or ruddy color).",
            "vedantic": "Rudra as the morning sun (aruṇa) dispelling physical and mental darkness, bringing activity and life."
        },
        "grammatical_references": {
            "panini": "Derived from root √ṛ (ऋँ गतौ, Bhvādi-gaṇa, 1.1086) with Uṇādi suffix 'unan' -> 'aruṇa' + dative singular 'ṅe' -> 'aruṇāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under color synonyms.",
            "amara_kosha": "Listed in Svargavarga (1.1.46) as 'aruṇaḥ sūryasārathiḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "शङ्काय": {
        "meanings": {
            "english": "To the bringer of happiness/welfare (śam).",
            "nirukta": "Derived from 'śam' (peace/welfare) + root 'gam' (to go/lead) + suffix 'da' or 'a' -> 'śaṅga' (he who leads to peace/happiness).",
            "vedantic": "The Lord is the absolute source of spiritual peace and liberation (śam), which He bestows upon His devotees."
        },
        "grammatical_references": {
            "panini": "Derived from 'śam' + √gam (गम्ँ गत्यर्थकः) + suffix 'ac' or 'ḍa' -> 'śaṅga' + dative singular 'ṅe' -> 'śaṅgāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "पशुपतये": {
        "meanings": {
            "english": "To the Lord (pati) of all creatures or bound souls (paśu).",
            "nirukta": "Genitive compound: 'paśūnāṃ patiḥ' (the protector/master of the tethered ones).",
            "vedantic": "All individual souls are 'paśu' because they are bound by the ropes (pāśa) of ignorance and karma. Rudra is their Lord (Pati) who binds them for their evolution and ultimately liberates them."
        },
        "grammatical_references": {
            "panini": "Derived from compound of 'paśu' + 'pati' + dative singular 'ṅe' (which becomes 'pataye' by standard rules for i-stems).",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under atmospheric deities.",
            "amara_kosha": "Listed in Svargavarga as a major name of Śiva: 'paśupatiḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "उग्राय": {
        "meanings": {
            "english": "To the supreme, excellent, or fierce one.",
            "nirukta": "Derived from √uc (to be strong/gather) or √vac + Uṇādi suffix 'ran' -> 'ugra' (powerful/fierce).",
            "vedantic": "Rudra is the supreme sovereign (Ugra) who governs all cosmic forces, including Indra and Agni, who operate out of fear of Him."
        },
        "grammatical_references": {
            "panini": "Derived from root √uc (उचीँ समवाये, Bhvādi-gaṇa, 1.0253) with Uṇādi suffix 'ran' -> 'ugra' + dative singular 'ṅe' -> 'ugrāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "भीमाय": {
        "meanings": {
            "english": "To the terrifying or awe-inspiring one.",
            "nirukta": "Derived from √bhī (to fear) with suffix 'mak' -> 'bhīma' (he who causes fear).",
            "vedantic": "Rudra represents the fearsome aspect of reality (death, change, decay) that shakes the soul out of its complacency and worldly attachment."
        },
        "grammatical_references": {
            "panini": "Derived from root √bhī (भी᳚ भये, Juhotyādi-gaṇa, 3.0002) with Uṇādi suffix 'mak' -> 'bhīma' + dative singular 'ṅe' -> 'bhīmāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for fear or strength.",
            "amara_kosha": "Listed in Svargavarga under names of Śiva: 'bhīmaḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "अग्रेवधाय": {
        "meanings": {
            "english": "To the one who slays the enemies standing directly in front of His devotee.",
            "nirukta": "Compound: 'agre vadhaḥ yasya' (he whose killing/weapon operates in front).",
            "vedantic": "Shows the immediate, direct protection of the Lord in times of active combat or spiritual crisis."
        },
        "grammatical_references": {
            "panini": "Derived from 'agre' (locative of agra) + 'vadha' (from √vadh - to kill) + dative singular 'ṅe' -> 'agrevadhāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "दूरेवधाय": {
        "meanings": {
            "english": "To the one who slays the enemies from a distance.",
            "nirukta": "Compound: 'dūre vadhaḥ yasya' (he whose killing/weapon operates from afar).",
            "vedantic": "Represents the preventive grace of the Lord, neutralizing obstacles and negative karma before they manifest near the devotee."
        },
        "grammatical_references": {
            "panini": "Derived from 'dūre' (locative of dūra) + 'vadha' + dative singular 'ṅe' -> 'dūrevadhāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "हन्त्रे": {
        "meanings": {
            "english": "To the slayer/destroyer.",
            "nirukta": "Derived from √han (to kill) + agentive suffix 'tṛc'.",
            "vedantic": "Rudra as the ultimate agent of dissolution who slays all names and forms at the end of time, returning them to their unmanifest source."
        },
        "grammatical_references": {
            "panini": "Derived from root √han (हनँ हिंसागत्योः, Adādi-gaṇa, 2.0002) with agentive suffix 'tṛc' (तृच्) -> 'hantṛ' + dative singular 'ṅe' -> 'hantre'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "हनीयसे": {
        "meanings": {
            "english": "To the excessive or ultimate slayer.",
            "nirukta": "Derived from √han (to kill) + comparative suffix 'īyasun' (hanīyas).",
            "vedantic": "Rudra is the absolute destroyer of all, who destroys even the destroyers themselves (Yama, time) at the final dissolution (mahāpralaya)."
        },
        "grammatical_references": {
            "panini": "Derived from root √han + comparative suffix 'īyasun' -> 'hanīyas' + dative singular 'ṅe' -> 'hanīyase'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "वृक्षेभ्यः": {
        "meanings": {
            "english": "To the trees (which are forms of Rudra).",
            "nirukta": "Derived from √vrasc (to cut/fell) or √vṛch, meaning that which is cut or destroyed.",
            "vedantic": "Rudra is the tree of worldly existence (saṃsāra-vṛkṣa) whose branches are actions and leaves are the Vedas. By saluting the trees, we worship the Lord's manifestation in nature."
        },
        "grammatical_references": {
            "panini": "Derived from root √vrasc (ओव्रश्चू᳚ छेदने, Tudādi-gaṇa, 6.0017) with Uṇādi suffix 'sa' -> 'vṛkṣa' + dative plural 'bhyas' -> 'vṛkṣebhyaḥ'.",
            "case_ending": "Dative Plural (Caturthī Vibhakti, Bahuvacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under plant synonyms.",
            "amara_kosha": "Listed in Vanauṣadhivarga (2.4.1) as 'tarur-vṛkṣaḥ'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.1) under trees."
        }
    },
    "हरिकेशेभ्यः": {
        "meanings": {
            "english": "To the green-haired ones (i.e. having green leaves in place of hair).",
            "nirukta": "Bahuvrīhi compound: 'haritaḥ keśāḥ (parṇāni) yeṣāṃ te' (those whose hair/leaves are green).",
            "vedantic": "The green leaves represent the life-giving, protective rituals (karma-kāṇḍa) of the Vedas that keep the tree of saṃsāra alive."
        },
        "grammatical_references": {
            "panini": "Derived as a Bahuvrīhi compound of 'harita' (green) + 'keśa' (hair) + dative plural 'bhyas' -> 'harikeśebhyaḥ'.",
            "case_ending": "Dative Plural (Caturthī Vibhakti, Bahuvacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "ताराय": {
        "meanings": {
            "english": "To the deliverer who carries souls across the ocean of saṃsāra (or the Pranava OM).",
            "nirukta": "Derived from √tṛ (to cross/carry over) + suffix 'ghañ' -> 'tāra' (that which causes crossing).",
            "vedantic": "Rudra is the saving knowledge (Tāraka-Brahman) in the form of OM that carries the departing soul across the ocean of birth and death."
        },
        "grammatical_references": {
            "panini": "Derived from root √tṛ (तॄ प्लवनतरणयोः, Bhvādi-gaṇa, 1.1124) with suffix 'ghañ' -> 'tāra' + dative singular 'ṅe' -> 'tārāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Avyayavarga or Nānārthavarga under terms of deliverance or sound.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "शम्भवे": {
        "meanings": {
            "english": "To the source of peace, welfare, or happiness (śam).",
            "nirukta": "Derived from 'śam' (welfare/peace) + root 'bhū' (to exist/become) + suffix 'ḍu' -> 'śambhu' (he from whom welfare arises).",
            "vedantic": "Rudra is the primary cause and source of the highest spiritual peace (mukti) and bliss."
        },
        "grammatical_references": {
            "panini": "Derived from 'śam' + √bhū (भू सत्तायाम्, Bhvādi-gaṇa, 1.0001) + suffix 'ḍu' (by rule Uṇādi 1.138) -> 'śambhu' + dative singular 'ṅe' -> 'śambhave'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Svargavarga (1.1.30) as a major name of Śiva: 'śambhuryis-tryambakaḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "मयोभवे": {
        "meanings": {
            "english": "To the source of delight, worldly happiness, or pleasure (mayas).",
            "nirukta": "Derived from 'mayas' (delight/pleasure) + √bhū (to arise) + suffix 'kvip' or 'ḍu' -> 'mayobhū' (he from whom delight arises).",
            "vedantic": "Rudra is the source of all worldly joy (abhyudaya) as well as transcendental bliss (niḥśreyasa)."
        },
        "grammatical_references": {
            "panini": "Derived from compound of 'mayas' + √bhū + suffix 'kvip' or Uṇādi 'ḍu' -> 'mayobhū' + dative singular 'ṅe' -> 'mayobhave'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "शङ्कराय": {
        "meanings": {
            "english": "To the maker of peace, welfare, or happiness (śam).",
            "nirukta": "Upapada compound: 'śam (welfare) karoti iti Śaṅkaraḥ' (he who actively creates welfare).",
            "vedantic": "The active, dynamic aspect of Rudra that constantly works to purify, elevate, and bless all creation with peace and auspiciousness."
        },
        "grammatical_references": {
            "panini": "Derived as an Upapada compound: 'śam' + √kṛ (डुकृञ् करणे, Tanādi-gaṇa, 8.0010) + suffix 'aca' (by rule 3.2.44) -> 'śaṅkara' + dative singular 'ṅe' -> 'śaṅkarāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Svargavarga (1.1.30) as 'śaṅkaraḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "मयस्कराय": {
        "meanings": {
            "english": "To the maker of delight, worldly joy, or pleasure (mayas).",
            "nirukta": "Upapada compound: 'mayas (delight) karoti iti mayaskaraḥ' (he who actively creates joy).",
            "vedantic": "Rudra is the direct dispenser of the positive fruits of actions, bringing happiness and joy to the living beings."
        },
        "grammatical_references": {
            "panini": "Derived as an Upapada compound: 'mayas' + √kṛ + suffix 'aca' (with 's' to 's' by visarga sandhi rules) -> 'mayaskara' + dative singular 'ṅe' -> 'mayaskarāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "शिवाय": {
        "meanings": {
            "english": "To Śiva (the auspicious, peaceful, and stainless one).",
            "nirukta": "Derived from √śī (to lie down, in whom all things rest) + suffix 'van' or 'ac'. (1) 'Śeti sarvaṃ jagat asmin' — He in whom the entire universe rests at dissolution. (2) 'Vaśi' (control) transposed becomes 'Śiva'.",
            "vedantic": "The non-dual, pure consciousness (Turiya) which is stainless, free from attributes, and the substratum of all reality."
        },
        "grammatical_references": {
            "panini": "Derived from root √śī (शीङ् स्वप्ने, Adādi-gaṇa, 2.0026) with Uṇādi suffix 'van' -> 'śiva' + dative singular 'ṅe' -> 'śivāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under auspicious words.",
            "amara_kosha": "Listed in Svargavarga (1.1.30) as 'śivaḥ'.",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "शिवतराय": {
        "meanings": {
            "english": "To the supremely, excessively auspicious/stainless one.",
            "nirukta": "Derived from 'śiva' + comparative suffix 'tarap' -> 'śivatara' (more auspicious than all others).",
            "vedantic": "Rudra is the absolute goodness and purity that surpasses all relative standards of good and bad; He is the ultimate reality."
        },
        "grammatical_references": {
            "panini": "Derived from 'śiva' + comparative suffix 'tarap' (तरप्) by rule 'dvivachana-vibhajyopapade...' -> 'śivatara' + dative singular 'ṅe' -> 'śivatarāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "तीर्थ्याय": {
        "meanings": {
            "english": "To the one residing in holy fords, bathing places, or sacred rivers (tīrtha).",
            "nirukta": "Derived from 'tīrtha' (ford/crossing place, from √tṛ - to cross) + suffix 'ya' (existing in).",
            "vedantic": "Rudra is present in the sacred places (tīrthas) that purify the mind and allow the devotee to cross the stream of worldly life."
        },
        "grammatical_references": {
            "panini": "Derived from 'tīrtha' + suffix 'yat' (tatra bhavaḥ) -> 'tīrthya' + dative singular 'ṅe' -> 'tīrthyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water/path synonyms.",
            "amara_kosha": "Listed in Vārivarga (1.10.13) under holy crossings: 'tīrthaṃ śāstrādhvarar-ṣiju...'."
        }
    },
    "कूल्याय": {
        "meanings": {
            "english": "To the one residing on the banks of rivers or canals (kūla).",
            "nirukta": "Derived from 'kūla' (bank/slope, from √kūl - to obstruct/enclose) + suffix 'ya'.",
            "vedantic": "Worshipping Rudra on the banks represents the boundary between the manifest world and the unmanifest consciousness, where the transition happens."
        },
        "grammatical_references": {
            "panini": "Derived from 'kūla' + suffix 'yat' -> 'kūlya' + dative singular 'ṅe' -> 'kūlyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Vārivarga (1.10.33) as 'kūlaṃ rodhaś-ca'."
        }
    },
    "पार्याय": {
        "meanings": {
            "english": "To the one residing on the far shore (pāra) of the river of saṃsāra.",
            "nirukta": "Derived from 'pāra' (far shore/limit, from √pṛ - to cross/protect) + suffix 'ya'.",
            "vedantic": "Rudra is the goal of liberation (Moksha) residing on the far shore of the ocean of ignorance."
        },
        "grammatical_references": {
            "panini": "Derived from 'pāra' + suffix 'yat' -> 'pārya' + dative singular 'ṅe' -> 'pāryāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "Listed in Vārivarga under banks: 'pāraṃ tasyāstataḥ'."
        }
    },
    "अवार्याय": {
        "meanings": {
            "english": "To the one residing on the near shore (avāra) of the river of saṃsāra.",
            "nirukta": "Derived from 'avāra' (near shore) + suffix 'ya'.",
            "vedantic": "Rudra is the immanent presence who resides right here in the midst of worldly life (saṃsāra), granting desires and guiding the Jiva."
        },
        "grammatical_references": {
            "panini": "Derived from 'avāra' + suffix 'yat' -> 'avārya' + dative singular 'ṅe' -> 'avāryāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "प्रतरणाय": {
        "meanings": {
            "english": "To the one who carries across (taraṇa) the ocean of sins through excellent (pra) means.",
            "nirukta": "Derived from prefix 'pra' + root 'tṛ' (to cross) + nominalizer 'lyuṭ' -> 'prataraṇa' (the act or instrument of crossing).",
            "vedantic": "Rudra is the divine savior who provides the ferry (bhakti/devotion) to cross the turbulent waters of worldly life."
        },
        "grammatical_references": {
            "panini": "Derived from pra-√tṛ with the suffix 'lyuṭ' (अना) by rule 'lyuṭ ca' (3.3.115) -> 'prataraṇa' + dative singular 'ṅe' -> 'prataraṇāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "उत्तरणाय": {
        "meanings": {
            "english": "To the one who lifts up (uttaraṇa) out of the world of ignorance.",
            "nirukta": "Derived from prefix 'ud' + root 'tṛ' (to cross/rise) + nominalizer 'lyuṭ' -> 'uttaraṇa'.",
            "vedantic": "Rudra is the teacher (Guru) who delivers the final knowledge of identity (Brahma-jñāna), lifting the soul out of relative existence entirely."
        },
        "grammatical_references": {
            "panini": "Derived from ud-√tṛ with suffix 'lyuṭ' -> 'uttaraṇa' + dative singular 'ṅe' -> 'uttaraṇāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "आतार्याय": {
        "meanings": {
            "english": "To the one residing in crossing places, shallows, or ferry points (ātāra).",
            "nirukta": "Derived from prefix 'आ' + root 'tṛ' (to cross) + suffix 'yat' -> 'ātārya' (existing at the ferry-crossing).",
            "vedantic": "Rudra stands at the junction points of life (birth, death, major choices), guiding the soul through transitions."
        },
        "grammatical_references": {
            "panini": "Derived from ā-√tṛ + suffix 'yat' -> 'ātārya' + dative singular 'ṅe' -> 'ātāryāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "आलाद्याय": {
        "meanings": {
            "english": "To the one residing in the deep water, whirlpools, or who is related to the individual soul (Jiva).",
            "nirukta": "Derived from 'alāda' (whirlpool or Jiva experiencing fruits) + suffix 'ya'.",
            "vedantic": "Rudra is the indwelling controller of the Jiva, who experiences the fruits of actions (karma-phala) and wanders in the whirlpool of life."
        },
        "grammatical_references": {
            "panini": "Derived from 'alāda' + suffix 'yat' -> 'ālādya' + dative singular 'ṅe' -> 'ālādyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    },
    "शष्प्याय": {
        "meanings": {
            "english": "To the one residing in the young green grass (śaṣpa) on riverbanks.",
            "nirukta": "Derived from 'śaṣpa' (young grass/sprout) + suffix 'ya'.",
            "vedantic": "Rudra is the tender, fresh aspect of nature, showing the divine beauty in the smallest blade of grass."
        },
        "grammatical_references": {
            "panini": "Derived from 'śaṣpa' + suffix 'yat' -> 'śaṣpya' + dative singular 'ṅe' -> 'śaṣpyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under plant/grass synonyms.",
            "amara_kosha": "Listed in Vanauṣadhivarga (2.4.148) as 'bāla-tṛṇaṃ śaṣpam'."
        }
    },
    "फेन्याय": {
        "meanings": {
            "english": "To the one residing in the foam (phena) of waters.",
            "nirukta": "Derived from 'phena' (foam, from √phiph/√phan - to sound/boil) + suffix 'ya'.",
            "vedantic": "Rudra is present in the foam, representing the transient, insubstantial names and forms of the universe, which are but foam on the ocean of consciousness."
        },
        "grammatical_references": {
            "panini": "Derived from 'phena' + suffix 'yat' -> 'pheny' + dative singular 'ṅe' -> 'phenyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed in Vārivarga (1.10.6) as 'pheno dindīraḥ'."
        }
    },
    "सिकत्याय": {
        "meanings": {
            "english": "To the one residing in the sands (sikatā).",
            "nirukta": "Derived from 'sikatā' (sand, from √sic - to sprinkle/pour) + suffix 'ya'.",
            "vedantic": "Rudra is the infinite multiplicity of the universe, like the grains of sand on a riverbank, all resting in Him."
        },
        "grammatical_references": {
            "panini": "Derived from 'sikatā' + suffix 'yat' (by rule 'sikatābhyo ca') -> 'sikatya' + dative singular 'ṅe' -> 'sikatyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under earth/soil synonyms.",
            "amara_kosha": "Listed in Bhūmivarga (2.1.6) as 'vāluka... sikatāḥ'.",
            "abhidhana_ratnamala": "Listed under earth synonyms."
        }
    },
    "प्रवाह्याय": {
        "meanings": {
            "english": "To the one residing in the flowing current (pravāha) of the river.",
            "nirukta": "Derived from 'pravāha' (flow/current, from pra-√vah - to flow/carry) + suffix 'ya'.",
            "vedantic": "Rudra is the dynamic, continuous stream of cosmic time and life, carrying all creatures in His flow."
        },
        "grammatical_references": {
            "panini": "Derived from pra-√vah + suffix 'yat' -> 'pravāhya' + dative singular 'ṅe' -> 'pravāhyāya'.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "N/A",
            "amara_kosha": "N/A",
            "abhidhana_ratnamala": "N/A"
        }
    }
}

# Add alias for accent variants
WORD_DB["नमो॒"] = WORD_DB["नमो"]
WORD_DB["नमः॑"] = WORD_DB["नमः"]
WORD_DB["नमः॒"] = WORD_DB["नमः"]
WORD_DB["नम॒-"] = WORD_DB["नमः"]
WORD_DB["नम"] = WORD_DB["नमः"]

# Helper to normalize words for DB lookup
def clean_for_db(w):
    w = w.strip().replace('।', '').replace('॥', '')
    # Strip accents
    accents = [chr(i) for i in range(0x0951, 0x0955)] + [chr(i) for i in range(0x1CD0, 0x1CFA)] + ['\u1cf4', '\u1cf2', '\u1cf7']
    for acc in accents:
        w = w.replace(acc, '')
    # Strip hyphens
    w = w.replace('-', '')
    # Check direct match
    if w in WORD_DB:
        return w
    return w

# Token mappings for Samhita
SAMHITA_TOKEN_MAPS = {
    # Anuvakam 7
    (7, 1): [("नमो॑", [1]), ("दु॒न्दु॒भ्या॑य", [2]), ("चाहन॒न्या॑य", [3, 4]), ("च॒", [5])],
    (7, 2): [("नमो॑", [1]), ("धृ॒ष्णवे॑", [2]), ("च", [3]), ("प्रमृ॒शाय॑", [4]), ("च॒", [5])],
    (7, 3): [("नमो॑", [1]), ("दू॒ताय॑", [2]), ("च॒", [3]), ("प्रहि॑ताय", [4]), ("च॒", [5])],
    (7, 4): [("नमो॑", [1]), ("निष॒ङ्गिणे॑", [2]), ("चेषुधि॒मते॑", [3, 4]), ("च॒", [5])],
    (7, 5): [("नम॑स्ती॒क्ष्णेष॑वे", [1, 2]), ("चायु॒धिने॑", [3, 4]), ("च॒", [5])],
    (7, 6): [("नमः॑", [1]), ("स्वायु॒धाय॑", [2]), ("च", [3]), ("सु॒धन्व॑ने", [4]), ("च॒", [5])],
    (7, 7): [("नम॒-स्स्रुत्या॑य", [1, 2]), ("च॒", [3]), ("पथ्या॑य", [4]), ("च॒", [5])],
    (7, 8): [("नमः॑", [1]), ("का॒ट्या॑य", [2]), ("च", [3]), ("नी॒प्या॑य", [4]), ("च॒", [5])],
    (7, 9): [("नम॒-स्सूद्या॑य", [1, 2]), ("च", [3]), ("सर॒स्या॑य", [4]), ("च॒", [5])],
    (7, 10): [("नमो॑", [1]), ("ना॒द्याय॑", [2]), ("च", [3]), ("वैश॒न्ताय॑", [4]), ("च॒", [5])],
    (7, 11): [("नमः॒", [1]), ("कूप्या॑य", [2]), ("चाव॒ट्या॑य", [3, 4]), ("च॒", [5])],
    (7, 12): [("नमो॒", [1]), ("वर्​ष्या॑य", [2]), ("चाव॒र​ष्याय॑", [3, 4]), ("च॒", [5])],
    (7, 13): [("नमो॑", [1]), ("मे॒घ्या॑य", [2]), ("च", [3]), ("विद्यु॒त्या॑य", [4]), ("च॒", [5])],
    (7, 14): [("नम", [1]), ("ई॒ध्रिया॑य", [2]), ("चात॒प्या॑य", [3, 4]), ("च॒", [5])],
    (7, 15): [("नमो॒", [1]), ("वात्या॑य", [2]), ("च॒", [3]), ("रेष्मि॑याय", [4]), ("च॒", [5])],
    (7, 16): [("नमो॑", [1]), ("वास्त॒व्या॑य", [2]), ("च", [3]), ("वास्तु॒पाय॑", [4]), ("च", [5])],
    
    # Anuvakam 8
    (8, 1): [("नम॒-स्सोमा॑य", [1, 2]), ("च", [3]), ("रु॒द्राय॑", [4]), ("च॒", [5])],
    (8, 2): [("नम॑स्ता॒म्राय॑", [1, 2]), ("चारु॒णाय॑", [3, 4]), ("च॒", [5])],
    (8, 3): [("नमः॑", [1]), ("श॒ङ्गाय॑", [2]), ("च", [3]), ("पशु॒पत॑ये", [4]), ("च॒", [5])],
    (8, 4): [("नम", [1]), ("उ॒ग्राय॑", [2]), ("च", [3]), ("भी॒माय॑", [4]), ("च॒", [5])],
    (8, 5): [("नमो॑", [1]), ("अग्रेव॒धाय॑", [2]), ("च", [3]), ("दूरेव॒धाय॑", [4]), ("च॒", [5])],
    (8, 6): [("नमो॑", [1]), ("ह॒न्त्रे", [2]), ("च॒", [3]), ("हनी॑यसे", [4]), ("च॒", [5])],
    (8, 7): [("नमो॑", [1]), ("वृ॒क्षेभ्यो॒", [2]), ("हरि॑केशेभ्यो॒", [3])],
    (8, 8): [("नम॑स्ता॒राय॒", [1, 2])],
    (8, 9): [("नम॑श्श॒म्भवे॑", [1, 2]), ("च", [3]), ("मयो॒भवे॑", [4]), ("च॒", [5])],
    (8, 10): [("नमः॑", [1]), ("शङ्क॒राय॑", [2]), ("च", [3]), ("मयस्क॒राय॑", [4]), ("च॒", [5])],
    (8, 11): [("नमः॑", [1]), ("शि॒वाय॑", [2]), ("च", [3]), ("शि॒वत॑राय", [4]), ("च॒", [5])],
    (8, 12): [("नम॒स्तीर्थ्या॑य", [1, 2]), ("च॒", [3]), ("कूल्या॑य", [4]), ("च॒", [5])],
    (8, 13): [("नमः॑", [1]), ("पा॒र्या॑य", [2]), ("चावा॒र्या॑य", [3, 4]), ("च॒", [5])],
    (8, 14): [("नमः॑", [1]), ("प्र॒तर॑णाय", [2]), ("चो॒त्तर॑णाय", [3, 4]), ("च॒", [5])],
    (8, 15): [("नम॑", [1]), ("आता॒र्या॑य", [2]), ("चाला॒द्या॑य", [3, 4]), ("च॒", [5])],
    (8, 16): [("नम॒-श्शष्प्या॑य", [1, 2]), ("च॒", [3]), ("फेन्या॑य", [4]), ("च॒", [5])],
    (8, 17): [("नमः॑", [1]), ("सिक॒त्या॑य", [2]), ("च", [3]), ("प्रवा॒ह्या॑य", [4]), ("च", [5])]
}

def strip_accents(text):
    accents = [chr(i) for i in range(0x0951, 0x0955)] + [chr(i) for i in range(0x1CD0, 0x1CFA)] + ['\u1cf4', '\u1cf2', '\u1cf7']
    for acc in accents:
        text = text.replace(acc, '')
    text = re.sub(r'\s+', ' ', text)
    return text

def get_split_index(token_text):
    if token_text.startswith("नम॑स्") or token_text.startswith("नम॑श्"):
        return 5
    elif token_text.startswith("नम॒-स्") or token_text.startswith("नम॒-श्"):
        return 6
    elif token_text.startswith("चो॒"):
        return 3
    elif token_text.startswith("चा") or token_text.startswith("चे"):
        return 2
    return len(token_text) // 2

def tokenize_stream(text, expected_word_mappings):
    tokens = []
    current_idx = 0
    text_len = len(text)
    
    for token_text, word_ids in expected_word_mappings:
        idx = text.find(token_text, current_idx)
        if idx != -1:
            if idx > current_idx:
                gap_text = text[current_idx:idx]
                tokens.append({
                    "text": gap_text,
                    "word_ids": []
                })
            tokens.append({
                "text": token_text,
                "word_ids": word_ids
            })
            current_idx = idx + len(token_text)
            
    if current_idx < text_len:
        tokens.append({
            "text": text[current_idx:],
            "word_ids": []
        })
        
    return tokens

def compute_samhita_spans(samhita_text, samhita_tokens):
    spans = {}
    current_idx = 0
    
    for token in samhita_tokens:
        text = token["text"]
        word_ids = token["word_ids"]
        token_len = len(text)
        if not word_ids:
            current_idx += token_len
            continue
            
        token_start = samhita_text.find(text, current_idx)
        token_end = token_start + token_len
        current_idx = token_end
        
        if len(word_ids) == 1:
            wid = word_ids[0]
            spans[wid] = {
                "start": token_start,
                "end": token_end,
                "text": text
            }
        elif len(word_ids) == 2:
            wid1, wid2 = word_ids[0], word_ids[1]
            split_idx = get_split_index(text)
            spans[wid1] = {
                "start": token_start,
                "end": token_start + split_idx,
                "text": text[:split_idx]
            }
            spans[wid2] = {
                "start": token_start + split_idx,
                "end": token_end,
                "text": text[split_idx:]
            }
            
    return spans

def parse_combined_commentary(text):
    sayana_part = ""
    bhatta_part = ""
    
    if "Sayana's Commentary:" in text:
        parts = text.split("Sayana's Commentary:")
        right = parts[1]
        if "Bhatta-Bhaskara-Bhashya:" in right:
            sparts = right.split("Bhatta-Bhaskara-Bhashya:")
            sayana_part = sparts[0].strip()
            bhatta_part = sparts[1].strip()
        else:
            sayana_part = right.strip()
    elif "Bhatta-Bhaskara-Bhashya:" in text:
        parts = text.split("Bhatta-Bhaskara-Bhashya:")
        sayana_part = parts[0].strip()
        bhatta_part = parts[1].strip()
    else:
        sayana_part = text.strip()
        
    bhatta_part = clean_trailing_salutations(bhatta_part)
    sayana_part = clean_trailing_salutations(sayana_part)
    
    return sayana_part, bhatta_part

def clean_trailing_salutations(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        l = line.strip()
        if l.startswith("Salutation to") or l.startswith("Homage to") or l.startswith("|| He speaks the") or l.endswith("ends the Seventh Anuvaka.") or l.endswith("ends the Eighth Anuvaka."):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines).strip()

def load_sanskrit_bhashyas_by_text_match(samhita_text, page_path):
    sayana_sanskrit = ""
    bhatta_sanskrit = ""
    
    if not page_path or not os.path.exists(page_path):
        return "", ""
        
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    norm_samhita = strip_accents(samhita_text).replace(' ', '')
    
    lines = content.split('\n')
    mantra_idx = -1
    for idx, line in enumerate(lines):
        norm_line = strip_accents(line).replace(' ', '').replace('॥', '').replace('।', '')
        if norm_samhita in norm_line or norm_line in norm_samhita:
            if not any(marker in line for marker in ["सा०", "भ०", "भाष्य"]):
                mantra_idx = idx
                break
                
    if mantra_idx == -1:
        # Fallback search for unique keyword matching
        words_to_match = [w for w in norm_samhita if len(w) > 4]
        for idx, line in enumerate(lines):
            norm_line = strip_accents(line).replace(' ', '')
            if any(w in norm_line for w in words_to_match):
                if not any(marker in line for marker in ["सा०", "भ०", "भाष्य"]):
                    mantra_idx = idx
                    break
                    
    if mantra_idx == -1:
        # Fallback to simple line match or returning empty if completely not found
        return "", ""
        
    commentary_lines = []
    for idx in range(mantra_idx + 1, len(lines)):
        line = lines[idx].strip()
        if not line:
            continue
        if "॥" in line and any(c.isdigit() or c in "१२३४५६७८९०" for c in line) and not any(marker in line for marker in ["सा०", "भ०", "भाष्य", "व्याख्यात"]):
            break
        commentary_lines.append(line)
        
    sayana_parts = []
    bhatta_parts = []
    current_bhashya = None
    
    for line in commentary_lines:
        if "सा० मा०" in line or "सा० भा०" in line or "सायणभाष्यम्" in line:
            sayana_parts.append(line)
            current_bhashya = 'sayana'
        elif "भ० मा० मा०" in line or "भ० भा० भा०" in line or "भ० सा० भा०" in line or "भ० मा०" in line:
            bhatta_parts.append(line)
            current_bhashya = 'bhatta'
        else:
            if current_bhashya == 'sayana':
                sayana_parts.append(line)
            elif current_bhashya == 'bhatta':
                bhatta_parts.append(line)
                
    sayana_sanskrit = ' '.join(sayana_parts).strip()
    bhatta_sanskrit = ' '.join(bhatta_parts).strip()
    
    sayana_sanskrit = re.sub(r'^(?:सा०\s*[माभा]०|सायणभाष्यम्)\s*', '', sayana_sanskrit).strip()
    bhatta_sanskrit = re.sub(r'^(?:भ०\s*[माभा]०\s*[माभा]०|भ०\s*[भासा]०\s*भा०|भ०\s*[माभा]०)\s*', '', bhatta_sanskrit).strip()
    
    return sayana_sanskrit, bhatta_sanskrit

def main():
    # Load correlated_namakam.json
    with open('/Users/Rkanadam/personal/namakam/src/correlated_namakam.json', 'r') as f:
        correlated_data = json.load(f)
        
    anuvakas = correlated_data["anuvakas"]
    
    # We want anuvakas at index 6 (id=7) and index 7 (id=8)
    for anuvaka in [anuvakas[6], anuvakas[7]]:
        anuvakam_no = anuvaka["id"]
        print(f"Processing Anuvakam {anuvakam_no}...")
        
        output_dir = ANUVAKAM7_DIR if anuvakam_no == 7 else ANUVAKAM8_DIR
        
        for mantra in anuvaka["mantras"]:
            m_id = mantra["id"]
            samhita = mantra["sanskrit"]["samhita"]
            pada = mantra["sanskrit"]["pada"]
            krama = mantra["sanskrit"]["krama"]
            
            pada_clean_tokens = [w for w in pada.split() if w not in ['।', '॥']]
            words_list = []
            
            samhita_mappings = SAMHITA_TOKEN_MAPS.get((anuvakam_no, m_id), [])
            samhita_tokens = tokenize_stream(samhita, samhita_mappings)
            samhita_spans = compute_samhita_spans(samhita, samhita_tokens)
            
            for idx, pw in enumerate(pada_clean_tokens, 1):
                clean_pw = clean_for_db(pw)
                db_word = WORD_DB.get(clean_pw, {})
                
                meanings = db_word.get("meanings", {
                    "english": f"English meaning for {clean_pw}",
                    "nirukta": f"Etymological analysis for {clean_pw}",
                    "vedantic": f"Vedantic usage of {clean_pw}"
                })
                
                grammatical = db_word.get("grammatical_references", {
                    "panini": f"Paninian root and rules for {clean_pw}",
                    "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)"
                })
                
                lexico = db_word.get("lexicographical_references", {
                    "nighantu": "N/A",
                    "amara_kosha": "N/A",
                    "abhidhana_ratnamala": "N/A"
                })
                
                word_obj = {
                    "id": idx,
                    "pada_form": pw,
                    "samhita_span": samhita_spans.get(idx, {
                        "start": 0,
                        "end": len(pw),
                        "text": pw
                    }),
                    "meanings": meanings,
                    "grammatical_references": grammatical,
                    "lexicographical_references": lexico
                }
                
                words_list.append(word_obj)
                
            pada_word_mappings = []
            w_idx = 1
            for pt in pada.split():
                if pt in ['।', '॥']:
                    continue
                pada_word_mappings.append((pt, [w_idx]))
                w_idx += 1
            pada_tokens = tokenize_stream(pada, pada_word_mappings)
            
            krama_word_mappings = []
            N = len(pada_clean_tokens)
            k_step_idx = 1
            for kp in krama.split(' । '):
                kp_clean = kp.strip().replace('॥', '').strip()
                if not kp_clean:
                    continue
                if k_step_idx < N:
                    word_ids = [k_step_idx, k_step_idx + 1]
                elif k_step_idx == N:
                    word_ids = [N]
                else:
                    word_ids = []
                
                krama_word_mappings.append((kp_clean, word_ids))
                k_step_idx += 1
                
            krama_tokens = tokenize_stream(krama, krama_word_mappings)
            
            raw_sayana_trans = mantra["translations"].get("sayana", "")
            sayana_eng, bhatta_eng = parse_combined_commentary(raw_sayana_trans)
            
            r_page = mantra["sources"].get("rudradhyaya_page")
            if r_page:
                full_page_path = os.path.join('/Users/Rkanadam/personal/namakam', r_page)
                sayana_sanskrit, bhatta_sanskrit = load_sanskrit_bhashyas_by_text_match(samhita, full_page_path)
            else:
                sayana_sanskrit, bhatta_sanskrit = "", ""
                
            abhinava_eng = mantra["translations"].get("abhinava_shankara", "")
            abhinava_sanskrit = mantra["commentaries_sanskrit"].get("abhinava_shankara", "")
            
            commentaries = {
                "sayana": {
                    "rishi": "Atreya" if anuvakam_no == 7 else "Nārada",
                    "chandas": "Mahāvirāṭ" if anuvakam_no == 7 else "Anuṣṭup",
                    "devata": "Śambhu",
                    "sanskrit": sayana_sanskrit,
                    "english": sayana_eng
                },
                "bhatta_bhaskara": {
                    "rishi": "Atreya" if anuvakam_no == 7 else "Nārada",
                    "chandas": "Mahāvirāṭ" if anuvakam_no == 7 else "Anuṣṭup",
                    "devata": "Śambhu",
                    "sanskrit": bhatta_sanskrit,
                    "english": bhatta_eng
                },
                "abhinava_shankara": {
                    "rishi": "Atreya" if anuvakam_no == 7 else "Nārada",
                    "chandas": "Mahāvirāṭ" if anuvakam_no == 7 else "Anuṣṭup",
                    "devata": "Śambhu",
                    "sanskrit": abhinava_sanskrit,
                    "english": abhinava_eng
                }
            }
            
            mantra_data = {
                "id": m_id,
                "samhita": samhita,
                "pada": pada,
                "krama": krama,
                "samhita_tokens": samhita_tokens,
                "pada_tokens": pada_tokens,
                "krama_tokens": krama_tokens,
                "words": words_list,
                "commentaries": commentaries
            }
            
            out_file = os.path.join(output_dir, f"mantra{m_id}.json")
            with open(out_file, 'w', encoding='utf-8') as out_f:
                json.dump(mantra_data, out_f, indent=2, ensure_ascii=False)
                
        print(f"Finished Anuvakam {anuvakam_no}. Saved files in {output_dir}")

if __name__ == "__main__":
    main()
