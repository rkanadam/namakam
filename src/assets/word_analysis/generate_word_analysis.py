import json
import os
import re

# File Paths
CORRELATED_JSON_PATH = "/Users/Rkanadam/personal/namakam/src/correlated_namakam.json"
OUTPUT_BASE_DIR = "/Users/Rkanadam/personal/namakam/src/assets/word_analysis"
RUDRA_TXT_DIR = "/Users/Rkanadam/personal/namakam/src/assets/rudradhyaya"

# Define the complete word database for Anuvakam 5 and 6
WORD_DB = {
    "नमः": {
        "pada_form": "नमः॑",
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
    "च": {
        "pada_form": "च॒",
        "meanings": {
            "english": "And.",
            "nirukta": "Conjunction meaning 'and' or 'also' (samuccayārtha).",
            "vedantic": "Serves to coordinate and unify different aspects and names of the Divine as manifestations of a single, indivisible energy."
        },
        "grammatical_references": {
            "panini": "Avyaya (indeclinable conjunction) classified under the Cādi class of particles (cādi-gaṇa).",
            "case_ending": "Avyaya (indeclinable conjunction)."
        },
        "lexicographical_references": {
            "nighantu": "Treated as a standard Vedic nipāta.",
            "amara_kosha": "Listed in Avyayavarga (3.4.15) in the sense of addition/coordination: 'utāpy-arthe ca saṃśaye'.",
            "abhidhana_ratnamala": "Listed in Anekārtha-kāṇḍa under conjunctive particles (avyayas)."
        }
    },
    "भवाय": {
        "pada_form": "भ॒वाय॑",
        "meanings": {
            "english": "To the source of existence / the creator / the one who exists as the universe.",
            "nirukta": "Derived from the root 'bhū' (भू) meaning 'to be or become'. 'bhavaty asmāt jagad iti bhavaḥ' (He from whom the universe arises).",
            "vedantic": "The ultimate source of all creation, representing the aspect of Brahman that manifests as the living universe (Sṛṣṭi-kartā)."
        },
        "grammatical_references": {
            "panini": "Derived from root √bhū (भू सत्तायाम्, Bhvādi-gaṇa, 1.0001) with the suffix 'ghañ' (घञ्) or 'ap' (अप्) in the sense of agent. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms of existence or birth.",
            "amara_kosha": "Listed in Svargavarga (1.1.31) as a synonym of Lord Śiva: 'śambhur īśaḥ paśupatiḥ śivo bhavaḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.25) under synonyms of Śiva."
        }
    },
    "रुद्राय": {
        "pada_form": "रु॒द्राय॑",
        "meanings": {
            "english": "To Rudra / the destroyer of sorrow.",
            "nirukta": "'rutam (sorrow) drāvayati (dissolves) iti rudraḥ' or 'rodayati' (makes weep at dissolution).",
            "vedantic": "The destroyer of primary ignorance (avidyā) and the bestower of liberation (mokṣa-dātā)."
        },
        "grammatical_references": {
            "panini": "Derived from root √rud (रुदिँ अश्रुविमोचने, Adādi-gaṇa, 2.0002) with the Uṇādi suffix 'kran' (रक्). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under atmospheric deities (Nighaṇṭu 5.5).",
            "amara_kosha": "Listed in Svargavarga (1.1.34) as a major synonym of Śiva.",
            "abhidhana_ratnamala": "Listed in Svarga-kāṇḍa (1.30) as a key name of Shiva."
        }
    },
    "शर्वाय": {
        "pada_form": "श॒र्वाय॑",
        "meanings": {
            "english": "To the destroyer / the one who withdraws the universe.",
            "nirukta": "Derived from the root 'śṛ' (शॄ) meaning 'to injure, break, or destroy'. 'śrṛṇāti hinaṣti sarvam iti śarvaḥ' (He who dissolves everything).",
            "vedantic": "The power of dissolution (Saṃhāra-śakti) that returns all names and forms back to the unmanifest state."
        },
        "grammatical_references": {
            "panini": "Derived from root √śṝ (शॄ हिंसायाम्, Kryādi-gaṇa, 9.0030) with the suffix 'van' (वन्) or 'a' (अच्). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under deities or names of dissolution.",
            "amara_kosha": "Listed in Svargavarga (1.1.31): 'śarvaḥ haro mṛtyuñjayaḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.26) as a synonym of Śiva."
        }
    },
    "पशुपतये": {
        "pada_form": "प॒शु॒-पत॑ये",
        "meanings": {
            "english": "To the Lord of bound souls (cattle).",
            "nirukta": "'paśūnām patiḥ' (the master of the bound creatures/beasts). 'paśu' represents the bound soul; 'pati' represents the Lord/liberator.",
            "vedantic": "The Supreme Lord who controls the cycle of bondage (pāśa) and liberation (mokṣa) of individual souls (jīvas, referred to as paśus)."
        },
        "grammatical_references": {
            "panini": "Compound (ṣaṣṭhī-tatpuruṣa) of 'paśu' (derived from √paś 'to bind') and 'pati' (derived from √pā 'to protect'). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Deity associated with protection of cattle/beings.",
            "amara_kosha": "Listed in Svargavarga (1.1.31) as a synonym of Lord Śiva: 'paśupatiḥ śivo bhavaḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.27) as a name of Śiva."
        }
    },
    "नीलग्रीवाय": {
        "pada_form": "नील॑-ग्रीवाय",
        "meanings": {
            "english": "To the blue-necked one.",
            "nirukta": "'nīlā grīvā yasya saḥ' (He whose neck is blue, having consumed the Kālakūṭa poison to protect the worlds).",
            "vedantic": "Symbolizes the supreme compassion (karuṇā) of Brahman, who takes the suffering (poison) of the world upon Himself to protect creation."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'nīla' (blue) and 'grīvā' (neck). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with deities having specific physical attributes.",
            "amara_kosha": "Listed in Svargavarga (1.1.30) as a name of Śiva: 'nīlakaṇṭhaḥ sitikaṇṭhaḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.28) under names of Śiva."
        }
    },
    "शितिकण्ठाय": {
        "pada_form": "शि॒ति-कण्ठा॑य",
        "meanings": {
            "english": "To the white-throated one / dark-throated one.",
            "nirukta": "'śitiḥ kaṇṭho yasya saḥ'. 'śiti' can mean either white (pre-poison throat) or dark (from the poison).",
            "vedantic": "Represents the coexistence of the pure, untouched state of Brahman (white) and the manifest suffering of the world (dark/poison) held in absolute harmony."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'śiti' (white/dark) and 'kaṇṭha' (throat). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with deities having colored attributes.",
            "amara_kosha": "Listed in Svargavarga (1.1.30) as a name of Śiva: 'nīlakaṇṭhaḥ sitikaṇṭhaḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.28) under names of Śiva."
        }
    },
    "कपर्दिने": {
        "pada_form": "क॒प॒र्दिने᳚",
        "meanings": {
            "english": "To the one with matted hair.",
            "nirukta": "'kapardaḥ asya asti iti kapardī' (He who has matted locks/hair).",
            "vedantic": "Matted locks represent the wild, unmanifested energy of nature (Prakṛti) held in control and discipline by the Supreme Spirit (Puruṣa)."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'kaparda' (matted hair) with the possessive suffix 'ini' (इनि) by Aṣṭādhyāyī 5.2.115. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with specific Vedic hair attributes.",
            "amara_kosha": "Listed in Svargavarga (1.1.30) as a name of Śiva: 'kapardī dhūrjaṭir jaṭilaḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.29) under names of Śiva."
        }
    },
    "व्युप्तकेशाय": {
        "pada_form": "व्यु॑प्त-केशाय",
        "meanings": {
            "english": "To the one with shaven hair.",
            "nirukta": "'vyuptāḥ (shaven/cut) keśāḥ yasya saḥ' (He whose hair is shaven, representing the Sannyasi/renunciant).",
            "vedantic": "Represents the supreme ascetic aspect of Brahman, the lord of renunciation (Sannyasa) and teacher of Brahma-vidyā."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'vyupta' (past passive participle of √vap 'to shear/shave') and 'keśa' (hair). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with ascetic attributes.",
            "amara_kosha": "Listed under terms for shaven or ascetic states.",
            "abhidhana_ratnamala": "Listed under names of ascetics and renunciants."
        }
    },
    "सहस्राक्षाय": {
        "pada_form": "सहस्र॒-अ॒क्षाय॑",
        "meanings": {
            "english": "To the thousand-eyed one.",
            "nirukta": "'sahasram akṣīṇi yasya saḥ' (He who has a thousand/infinite eyes).",
            "vedantic": "Omniscience (sarvajñatva) of Brahman, who witnesses all actions and thoughts of all beings simultaneously."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'sahasra' (thousand) and 'akṣi' (eye), with the 'ac' suffix by Aṣṭādhyāyī 5.4.113. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under atmospheric/cosmic deities.",
            "amara_kosha": "Listed in Svargavarga (1.1.42) as an epithet of Indra/Rudra.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa under cosmic deity names."
        }
    },
    "शतधन्वने": {
        "pada_form": "श॒त-ध॑न्वने",
        "meanings": {
            "english": "To the one with a hundred bows.",
            "nirukta": "'śatam dhanvāni yasya saḥ' (He who possesses a hundred/countless bows to protect His devotees and destroy evil).",
            "vedantic": "The infinite power of protection (Rākṣasaka-śakti) and the multiplicity of divine instruments used to restore Dharma."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'śata' (hundred) and 'dhanvan' (bow). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with weapon-bearing deities.",
            "amara_kosha": "Epithet of a deity holding many bows.",
            "abhidhana_ratnamala": "Listed in weapon-holder synonyms."
        }
    },
    "गिरिशाय": {
        "pada_form": "गि॒रि॒-शाय॑",
        "meanings": {
            "english": "To the one who dwells on the mountain / Kailasa.",
            "nirukta": "'girau (on the mountain) śete (resides) iti giriśaḥ' (He who rests on Kailasa) or 'giriśa' meaning lord of speech/mountains.",
            "vedantic": "The mountain represents the height of spiritual consciousness (Kailasa). Dwelling there means residing at the peak of self-realization."
        },
        "grammatical_references": {
            "panini": "Derived from 'giri' (mountain) + root √śī (शीड् स्वप्ने) with the 'da' suffix, or with possessive suffix 'śa' in lomādi-gaṇa. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with mountain deities.",
            "amara_kosha": "Listed in Svargavarga (1.1.30): 'girīśo girijo'laḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa (1.29) under names of Śiva."
        }
    },
    "शिपिविष्टाय": {
        "pada_form": "शि॒पि॒-वि॒ष्टाय॑",
        "meanings": {
            "english": "To the one pervaded by rays / the form of Viṣṇu.",
            "nirukta": "'śipi' means rays or cattle; 'viṣṭa' means entered. 'He who enters into the rays of the Sun' or 'He who enters into cattle as the inner ruler'.",
            "vedantic": "The all-pervading consciousness (Antaryāmin) that enters into every living entity and natural element (like sunbeams) to support them."
        },
        "grammatical_references": {
            "panini": "Derived from 'śipi' (rays/cattle) + 'viṣṭa' (past passive participle of √viś 'to enter'). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for the Sun or Vishnu.",
            "amara_kosha": "Listed in Svargavarga (1.1.20) as a name of Viṣṇu: 'kṣipiviṣṭas-tu viṣṇuḥ'.",
            "abhidhana_ratnamala": "Listed in Devatā-kāṇḍa as a name of Viṣṇu/Śiva."
        }
    },
    "मीढुष्टमाय": {
        "pada_form": "मी॒ढुः-त॑माय",
        "meanings": {
            "english": "To the most bountiful showerer of blessings.",
            "nirukta": "'miḍhvas' (bountiful/giver) + 'tama' (superlative). 'miḍhuṣe' is the Vedic dative. 'He who showers desires to the highest degree'.",
            "vedantic": "The supreme source of grace, who rains down material and spiritual fruits (bhoga and mokṣa) upon devotees according to their prayers."
        },
        "grammatical_references": {
            "panini": "Derived from the participial adjective 'miḍhvas' (from √mih 'to pour/shower') with the superlative suffix 'tamaP'. Vedic alteration. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for cloud or bountiful giver.",
            "amara_kosha": "Synonym for a highly generous or cloud-like deity.",
            "abhidhana_ratnamala": "Listed under epithets of great givers."
        }
    },
    "इषुमते": {
        "pada_form": "इषु॑-मते",
        "meanings": {
            "english": "To the holder of arrows.",
            "nirukta": "'iṣavaḥ (arrows) asya santi iti iṣumān' (He who possesses arrows).",
            "vedantic": "Arrows represent the active, directed powers of will (iccha-śakti) and action (kriyā-śakti) that target ignorance and restore cosmic order."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'iṣu' (arrow) with the possessive suffix 'matup'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under weapon-possessors.",
            "amara_kosha": "Synonym for an archer or weapon-bearing deity.",
            "abhidhana_ratnamala": "Listed under weapons and archers."
        }
    },
    "ह्रस्वाय": {
        "pada_form": "ह्र॒स्वाय॑",
        "meanings": {
            "english": "To the small / short one.",
            "nirukta": "Derived from the root 'hras' (ह्रस्) meaning 'to decrease or become small'.",
            "vedantic": "The small one, representing the Dahara-ākāśa — the tiny, subtle space of the heart where the infinite Brahman is meditated upon."
        },
        "grammatical_references": {
            "panini": "Derived from √hras (ह्रसँ अपचये, Bhvādi-gaṇa, 1.0763) + 'ac' suffix. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under size or quantity synonyms.",
            "amara_kosha": "Listed in Nānārthavarga under terms for smallness.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa under dimensions."
        }
    },
    "वामनाय": {
        "pada_form": "वा॒म॒नाय॑",
        "meanings": {
            "english": "To the dwarf / the form of Gaṇapati or Viṣṇu's dwarf incarnation.",
            "nirukta": "Derived from the root 'vam' (वम्) 'to spit/emit' or associated with 'vama' (beautiful/dwarf). He who is small of stature.",
            "vedantic": "Represents the Divine who resides as the dwarf (Vamana) in the center of the body, worshipped by all senses (as in Katha Upanishad: 'madhye vāmanam āsīnam...')."
        },
        "grammatical_references": {
            "panini": "Derived from the noun/adjective 'vamana'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under size-related epithets.",
            "amara_kosha": "Listed in Svargavarga/Manuṣyavarga under dwarf synonyms.",
            "abhidhana_ratnamala": "Listed under names of Viṣṇu or short-stature beings."
        }
    },
    "बृहते": {
        "pada_form": "बृ॒ह॒ते",
        "meanings": {
            "english": "To the immeasurably vast / the great.",
            "nirukta": "Derived from the root 'bṛh' (बृह्) 'to grow, expand, or increase'.",
            "vedantic": "The infinite, all-pervading Brahman, free from all limitations of space, time, and object (desha-kala-vastu pariccheda rahita)."
        },
        "grammatical_references": {
            "panini": "Derived from √bṛh (बृहँ वृद्धौ, Bhvādi-gaṇa, 1.0256) with the present participle suffix 'śatṛ' or Uṇādi suffix. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for greatness or atmosphere.",
            "amara_kosha": "Listed in Avyayavarga/Nānārthavarga under synonyms for large or great.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa under size/greatness."
        }
    },
    "वर्षाीयसे": {
        "pada_form": "वर्​षी॑यसे",
        "meanings": {
            "english": "To the most excellent / senior in qualities / elder.",
            "nirukta": "Derived from 'vṛdha' (grown/elder) + 'īyasu' (comparative suffix). The elder or senior in age and quality.",
            "vedantic": "Brahman as the most ancient, full of infinite, supreme divine attributes (Guṇa-varṣīyas)."
        },
        "grammatical_references": {
            "panini": "Derived from the base 'vṛdha' with the comparative suffix 'īyasun', where 'vṛdha' is replaced by 'varṣa' by Aṣṭādhyāyī 5.3.61. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under senior or grown synonyms.",
            "amara_kosha": "Listed in Nānārthavarga under terms for elder/growth.",
            "abhidhana_ratnamala": "Listed under seniority and growth."
        }
    },
    "वृद्धाय": {
        "pada_form": "वृ॒द्धाय॑",
        "meanings": {
            "english": "To the ancient / the old.",
            "nirukta": "Derived from the root 'vṛdh' (वृध्) meaning 'to grow, increase'.",
            "vedantic": "The eternal, primeval Puruṣa (Sanātana) who existed before anything else was created."
        },
        "grammatical_references": {
            "panini": "Derived from √vṛdh (वृधँ वृद्धौ, Bhvādi-gaṇa, 1.0964) with the past passive participle suffix 'kta'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for aged or grown.",
            "amara_kosha": "Listed in Manuṣyavarga (2.6.46) under age terms: 'वृद्धो जीर्णो वयोऽधिकः'.",
            "abhidhana_ratnamala": "Listed under terms for old age."
        }
    },
    "संवृध्वने": {
        "pada_form": "सम्-वृ॒ध्व॑ने",
        "meanings": {
            "english": "To the one who grows well through praises / who increases His devotees.",
            "nirukta": "Derived from prefix 'sam' + root 'vṛdh' (to grow). 'samvṛdhvan' is He who is well-increased by Vedic hymns of praise.",
            "vedantic": "The Divine who flourishes in the heart of the devotee through devotional service and who causes the spiritual growth of His devotees."
        },
        "grammatical_references": {
            "panini": "Derived from prefix 'sam' + root √vṛdh + suffix 'kvanip' (क्वनिप्). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with growth and worship.",
            "amara_kosha": "Synonym for a well-nourished or growing deity.",
            "abhidhana_ratnamala": "Listed under growth/nourishment synonyms."
        }
    },
    "अग्रियाय": {
        "pada_form": "अग्रि॑याय",
        "meanings": {
            "english": "To the first-born / the primordial one.",
            "nirukta": "Derived from 'agra' (beginning/forefront) + suffix 'gha' (इय). 'agre bhavaḥ agriyaḥ' (He who exists at the very beginning).",
            "vedantic": "The primordial cause of the universe (Kāraṇa-puruṣa) who exists prior to the manifestation of Prakṛti."
        },
        "grammatical_references": {
            "panini": "Derived from 'agra' with the suffix 'ghach' (इय) by Aṣṭādhyāyī 4.4.117. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for beginning or priority.",
            "amara_kosha": "Listed in Nānārthavarga under terms for forefront/first.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa under order/priority."
        }
    },
    "प्रथमाय": {
        "pada_form": "प्र॒थ॒माय॑",
        "meanings": {
            "english": "To the first / the foremost.",
            "nirukta": "Derived from the root 'prath' (प्रथ्) meaning 'to spread, extend, or be first'.",
            "vedantic": "The first manifest form of Brahman (Hiraṇyagarbha/Sūtrātman) who spreads and expands the universe."
        },
        "grammatical_references": {
            "panini": "Derived from √prath (प्रथँ प्रख्याने, Bhvādi-gaṇa, 1.0872) + suffix 'amack' (अमच्) or similar primary derivation. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for number one or beginning.",
            "amara_kosha": "Listed in Avyayavarga/Nānārthavarga as a term for first: 'ādiḥ prathamaḥ'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa under order."
        }
    },
    "आशवे": {
        "pada_form": "आ॒शवे॑",
        "meanings": {
            "english": "To the swift / the all-pervading.",
            "nirukta": "Derived from the root 'aś' (अश्) meaning 'to pervade, reach, or occupy'.",
            "vedantic": "The all-pervading consciousness that reaches everywhere instantly, traversing all space without movement."
        },
        "grammatical_references": {
            "panini": "Derived from √aś (अशूँ व्याप्तौ, Svādi-gaṇa, 5.0022) with the Uṇādi suffix 'u' (कुन्). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for quick/swift (kṣipra-nāmāni, Nighaṇṭu 2.15).",
            "amara_kosha": "Listed in Avyayavarga (3.4.17) under quickness: 'āśu kṣipraṃ drutaṃ tvaritam'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.133) under speed."
        }
    },
    "अजिराय": {
        "pada_form": "अ॒जि॒राय॑",
        "meanings": {
            "english": "To the rapid / agile / active.",
            "nirukta": "Derived from the root 'aj' (अज्) meaning 'to drive, throw, or move'.",
            "vedantic": "The dynamic aspect of Brahman (Prāṇa) that is ever-active, initiating all movement and life in the universe."
        },
        "grammatical_references": {
            "panini": "Derived from √aj (अजँ गतिक्षेपणयोः, Bhvādi-gaṇa, 1.0268) with the suffix 'kirach' (किरच्) by Uṇādi 1.53. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for quick/swift (kṣipra-nāmāni, Nighaṇṭu 2.15).",
            "amara_kosha": "Listed in Avyayavarga under speed/quickness: 'tvaritaṃ tarasā’jiram'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa under speed."
        }
    },
    "शीघ्रियाय": {
        "pada_form": "शीघ्रि॑याय",
        "meanings": {
            "english": "To the one in swift-flowing waters.",
            "nirukta": "Derived from 'śīghra' (swift) + suffix 'ya' or 'iya'. He who exists in rapid water currents.",
            "vedantic": "The presence of Brahman in the dynamic, fast-flowing aspects of nature, representing the unstoppable flow of time and life."
        },
        "grammatical_references": {
            "panini": "Derived from 'śīghra' (fast) with the suffix 'gha' (इय) or 'yat' (य) in the sense of location/source. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water-associated epithets.",
            "amara_kosha": "Synonym for a swift-moving entity or water current.",
            "abhidhana_ratnamala": "Listed under speed and water synonyms."
        }
    },
    "शीभ्याय": {
        "pada_form": "शीभ्या॑य",
        "meanings": {
            "english": "To the one in water-currents / rapids.",
            "nirukta": "Derived from 'śībha' meaning swift flow or water rapids. He who dwells in water currents.",
            "vedantic": "Brahman as the underlying life-force in the refreshing and purifying flow of water."
        },
        "grammatical_references": {
            "panini": "Derived from 'śībha' (swift water current) with the suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms.",
            "amara_kosha": "Synonym for water flow or currents.",
            "abhidhana_ratnamala": "Listed under water-based synonyms."
        }
    },
    "ऊर्म्याय": {
        "pada_form": "ऊ॒र्म्या॑य",
        "meanings": {
            "english": "To the one in the waves.",
            "nirukta": "Derived from 'ūrmi' (wave) + suffix 'ya'. 'ūrmiṣu bhavaḥ ūrmyaḥ' (He who exists in the waves).",
            "vedantic": "The waves represent the constant modifications (vṛttis) of the mind or the rising and falling of cycles of creation. Brahman is the ocean that supports these waves."
        },
        "grammatical_references": {
            "panini": "Derived from 'ūrmi' (wave) + suffix 'yat' (य) by Aṣṭadhyāyī 4.4.110. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under water synonyms (udaka-nāmāni).",
            "amara_kosha": "Listed in Bhūvarga (2.3.5) under wave synonyms: 'तरङ्ग ऊर्मिर्द्वयोः'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under waves."
        }
    },
    "अवस्वन्याय": {
        "pada_form": "अ॒व॒-स्व॒न्या॑य",
        "meanings": {
            "english": "To the one in quiet / still waters.",
            "nirukta": "Derived from 'ava' (down/under/without) + 'svana' (noise) + suffix 'ya'. 'avasvane (soundless water) bhavaḥ' (He who exists in silent water).",
            "vedantic": "Represents the silent, unperturbed state of consciousness (Turiya) which is free from the noise of thoughts and action."
        },
        "grammatical_references": {
            "panini": "Derived from prefix 'ava' + 'svana' (noise) + suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under quiet water or depth synonyms.",
            "amara_kosha": "Associated with silent or deep water.",
            "abhidhana_ratnamala": "Listed under water and silence."
        }
    },
    "स्रोतस्याय": {
        "pada_form": "स्रोत॒स्या॑य",
        "meanings": {
            "english": "To the one in the streams.",
            "nirukta": "Derived from 'srotas' (stream/current) + suffix 'ya'. 'srotasi bhavaḥ srotasyaḥ' (He who exists in flowing streams).",
            "vedantic": "The streams represent the continuous flow of divine grace and knowledge that purifies the devotee's intellect."
        },
        "grammatical_references": {
            "panini": "Derived from 'srotas' (current) with the suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under river or current synonyms.",
            "amara_kosha": "Listed in Bhūvarga under river-currents: 'स्रोतो वहा रैहणी'.",
            "abhidhana_ratnamala": "Listed under river and water flows."
        }
    },
    "द्वीप्याय": {
        "pada_form": "द्वीप्या॑य",
        "meanings": {
            "english": "To the one on the islands.",
            "nirukta": "Derived from 'dvīpa' (island, land surrounded by water) + suffix 'ya'. 'dvīpe bhavaḥ dvīpyaḥ'.",
            "vedantic": "The island represents the firm ground of truth (Satyaloka) in the middle of the ocean of saṃsāra. Brahman is that sanctuary."
        },
        "grammatical_references": {
            "panini": "Derived from 'dvīpa' + suffix 'yat' (य) by Aṣṭadhyāyī 4.3.10. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under land/water synonyms.",
            "amara_kosha": "Listed in Bhūvarga under land divisions: 'द्वीपोऽस्त्रियामन्तरीपम्'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under islands."
        }
    },
    "ज्येष्ठाय": {
        "pada_form": "ज्ये॒ष्ठाय॑",
        "meanings": {
            "english": "To the eldest / the most excellent.",
            "nirukta": "Derived from 'praśasya' (praiseworthy) + superlative suffix 'iṣṭhan'. The eldest or most outstanding.",
            "vedantic": "Brahman as the most ancient, preceding all created beings; also the highest in excellence and praise."
        },
        "grammatical_references": {
            "panini": "Derived from 'praśasya' with the suffix 'iṣṭhan', where 'praśasya' is replaced by 'jya' by Aṣṭādhyāyī 5.3.61. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for greatness or seniority.",
            "amara_kosha": "Listed in Manuṣyavarga (2.6.45) as a synonym for elder: 'ज्येष्ठः श्रेष्ठो वयोऽधिकः'.",
            "abhidhana_ratnamala": "Listed under seniority and excellence."
        }
    },
    "कनिष्ठाय": {
        "pada_form": "क॒नि॒ष्ठाय॑",
        "meanings": {
            "english": "To the youngest / the smallest.",
            "nirukta": "Derived from 'yuvan' (young) or 'alpa' (small) + superlative suffix 'iṣṭhan'.",
            "vedantic": "Brahman as the subtlest of the subtle (aṇor aṇīyān), residing in the smallest atom or the youngest child."
        },
        "grammatical_references": {
            "panini": "Derived from 'yuvan' or 'alpa' with 'iṣṭhan', replaced by 'kan' by Aṣṭādhyāyī 5.3.64. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under smallness or youth synonyms.",
            "amara_kosha": "Listed in Manuṣyavarga as a term for youngest: 'कनिष्ठस्तु यवीयसि'.",
            "abhidhana_ratnamala": "Listed under smallness and youth."
        }
    },
    "पूर्वजाय": {
        "pada_form": "पू॒र्व॒-जाय॑",
        "meanings": {
            "english": "To the first-born / born in former times.",
            "nirukta": "'pūrve jātaḥ iti pūrvajaḥ' (He who was born before all others, i.e., Hiranyagarbha at the dawn of creation).",
            "vedantic": "The primordial consciousness that manifests as the first cause of the universe (Adipuruṣa)."
        },
        "grammatical_references": {
            "panini": "Upapada compound of 'pūrva' + root √jan (जनीँ प्रादुर्भावे, 4.0044) + suffix 'da' (ड). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with primordial deities.",
            "amara_kosha": "Synonym for primordial creator or eldest sibling.",
            "abhidhana_ratnamala": "Listed under priority of birth."
        }
    },
    "अपरजाय": {
        "pada_form": "अ॒प॒र॒-जाय॑",
        "meanings": {
            "english": "To the last-born / born in later times.",
            "nirukta": "'apare (later/end) jātaḥ iti aparajaḥ' (He who manifests at the time of dissolution, or in later ages).",
            "vedantic": "The aspect of Brahman that manifests at the end of cycles (Kalagni-rudra) to dissolve the universe."
        },
        "grammatical_references": {
            "panini": "Upapada compound of 'apara' + root √jan + suffix 'da' (ड). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with dissolution deities.",
            "amara_kosha": "Synonym for younger sibling or later manifest deity.",
            "abhidhana_ratnamala": "Listed under posteriority of birth."
        }
    },
    "मध्यमाय": {
        "pada_form": "म॒ध्य॒माय॑",
        "meanings": {
            "english": "To the middlemost.",
            "nirukta": "Derived from 'madhya' (middle) + suffix 'ma' (म).",
            "vedantic": "The indwelling ruler who exists in the middle of all states (sustenance/preservation) and in the heart of all beings."
        },
        "grammatical_references": {
            "panini": "Derived from 'madhya' + suffix 'ma' by Aṣṭādhyāyī 5.3.8. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for middle/space.",
            "amara_kosha": "Listed in Nānārthavarga (3.3.136) as a term for middle: 'मध्यमं मध्यस्थेऽपि'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa under positions."
        }
    },
    "अपगल्भाय": {
        "pada_form": "अ॒प॒-ग॒ल्भाय॑",
        "meanings": {
            "english": "To the immature / youthful / one who does not speak proudly.",
            "nirukta": "Derived from prefix 'apa' (away/under) + 'galbha' (mature/proud). He who is immature or humble.",
            "vedantic": "Represents the child-like, simple, and unpretentious form of the Divine (Bala-rupa), free from ego and pride."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'apa' + 'galbha' (from √galbh 'to be bold/confident'). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under youth or growth synonyms.",
            "amara_kosha": "Synonym for a youth or child-like state.",
            "abhidhana_ratnamala": "Listed under growth levels."
        }
    },
    "जघन्याय": {
        "pada_form": "ज॒घ॒न्या॑य",
        "meanings": {
            "english": "To the one in the rear / born from the hips.",
            "nirukta": "Derived from 'jaghana' (hips/rear) + suffix 'ya'. 'jaghane bhavaḥ jaghanyaḥ'.",
            "vedantic": "Brahman present in the lowliest, humblest, or trailing parts of creation (such as tail-ends of animals or outer boundaries of the universe)."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'jaghana' + suffix 'yat' (य) by Aṣṭādhyāyī 4.3.55. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under physical body parts or lowliness.",
            "amara_kosha": "Listed in Manuṣyavarga/Nānārthavarga under hips or lowest rank.",
            "abhidhana_ratnamala": "Listed under rear/hips or rank."
        }
    },
    "बुध्नियाय": {
        "pada_form": "बुध्नि॑याय",
        "meanings": {
            "english": "To the one at the roots / depths.",
            "nirukta": "Derived from 'budhna' (root/depth/foundation) + suffix 'ya'. 'budhne bhavaḥ budhniyaḥ'.",
            "vedantic": "Brahman as the fundamental foundation (Adhara) supporting all trees, mountains, and the entire universe from below."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'budhna' + suffix 'gha' (इय) or 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under sky or root synonyms.",
            "amara_kosha": "Epithet of a foundational or deep deity.",
            "abhidhana_ratnamala": "Listed under roots and foundations."
        }
    },
    "सोभ्याय": {
        "pada_form": "सो॒भ्या॑य",
        "meanings": {
            "english": "To the one in the human world / city of Gandharvas.",
            "nirukta": "Derived from 'sobha' (that which has both merit and sin, i.e., the human world, or the celestial city of Gandharvas) + suffix 'ya'.",
            "vedantic": "The Divine who resides in the human world (Samsara) guiding souls through both good and bad experiences."
        },
        "grammatical_references": {
            "panini": "Derived from 'sobha' + suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with cities or worlds.",
            "amara_kosha": "Listed under city or world synonyms.",
            "abhidhana_ratnamala": "Listed under cities and realms."
        }
    },
    "प्रतिसर्याय": {
        "pada_form": "प्र॒ति॒-स॒र्या॑य",
        "meanings": {
            "english": "To the one in the protective thread / amulet.",
            "nirukta": "Derived from 'pratisara' (protective amulet/thread tied around the wrist during rituals) + suffix 'ya'.",
            "vedantic": "Brahman who manifests as the invisible shield of protection (Rakṣā) in sacred threads and prayers."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'pratisara' + suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with protective charms.",
            "amara_kosha": "Listed under ornaments or protective charms: 'प्रतिसरो रश्मिसङ्केतयोपि'.",
            "abhidhana_ratnamala": "Listed under charms and amulets."
        }
    },
    "याम्याय": {
        "pada_form": "याम्या॑य",
        "meanings": {
            "english": "To the one in Yama's realm / the south.",
            "nirukta": "Derived from 'yama' (god of death/control) + suffix 'ya'. 'yame bhavaḥ yāmyaḥ'.",
            "vedantic": "Brahman present as the law of justice, death, and control (Yama-dharma) that governs the cosmic order and the transition of souls."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'yama' + suffix 'yat' (य) by Aṣṭadhyāyī 4.3.10. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under deities of the southern region.",
            "amara_kosha": "Listed in Nānārthavarga as a term for south or death-associated.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under directions."
        }
    },
    "क्षेम्याय": {
        "pada_form": "क्षेम्या॑य",
        "meanings": {
            "english": "To the one in the world of security / peace.",
            "nirukta": "Derived from 'kṣema' (security, preservation of what is acquired) + suffix 'ya'. 'kṣeme bhavaḥ kṣemyaḥ'.",
            "vedantic": "Brahman as the ultimate source of peace, security, and well-being (Yoga-kṣema) for all devotees."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'kṣema' + suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for safety or peace.",
            "amara_kosha": "Listed in Avyayavarga/Nānārthavarga: 'क्षेमं कुतूहलेऽपि'.",
            "abhidhana_ratnamala": "Listed under safety and peace."
        }
    },
    "उर्वर्याय": {
        "pada_form": "उ॒र्व॒र्या॑य",
        "meanings": {
            "english": "To the one in the fertile fields / crops.",
            "nirukta": "Derived from 'urvarā' (fertile soil, crop-bearing land) + suffix 'ya'. 'urvarāyāṃ bhavaḥ urvaryah'.",
            "vedantic": "Brahman as the fertility of the soil and the nourishing power in grains and crops (Annam)."
        },
        "grammatical_references": {
            "panini": "Derived from 'urvarā' + suffix 'yat' (य) by Aṣṭadhyāyī 4.2.82. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for fertile earth.",
            "amara_kosha": "Listed in Bhūvarga (2.1.6) under fertile soil: 'उर्वरा सर्वशस्याढ्या'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under soil types."
        }
    },
    "खल्याय": {
        "pada_form": "खल्या॑य",
        "meanings": {
            "english": "To the one in the threshing-floor.",
            "nirukta": "Derived from 'khala' (threshing floor where grains are separated) + suffix 'ya'. 'khale bhavaḥ khalyaḥ'.",
            "vedantic": "Brahman as the purifier who separates the essence (soul) from the husk (ego/body) in the threshing floor of saṃsāra."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'khala' + suffix 'yat' (य) by Aṣṭadhyāyī 4.2.45. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with agricultural spaces.",
            "amara_kosha": "Listed in Vaiśyavarga (2.9.15) under farming terms: 'खलं धान्यमर्दनस्थानम्'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under agriculture."
        }
    },
    "श्लोक्याय": {
        "pada_form": "श्लोक्या॑य",
        "meanings": {
            "english": "To the one praised in Vedic hymns.",
            "nirukta": "Derived from 'śloka' (verse/hymn/sound) + suffix 'ya'. Worthy of being praised.",
            "vedantic": "The Supreme Lord who is the ultimate subject of all Vedic hymns and prayers of praise."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'śloka' + suffix 'yat' (य) by Aṣṭadhyāyī 5.1.119. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for voice or praise.",
            "amara_kosha": "Listed in Avyayavarga/Nānārthavarga under praise or fame.",
            "abhidhana_ratnamala": "Listed under sound and praise."
        }
    },
    "अवसान्याय": {
        "pada_form": "अ॒व॒-सा॒न्या॑य",
        "meanings": {
            "english": "To the one at the end of the Veda / final destination.",
            "nirukta": "Derived from 'avasāna' (boundary, end of a verse, or death/dissolution) + suffix 'ya'. 'avasāne bhavaḥ avasānyaḥ'.",
            "vedantic": "Brahman as the final destination of all life and the ultimate conclusion (Upanishads/Vedanta) of all Vedic studies."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'avasāna' (from prefix 'ava' + √so 'to finish/end') + suffix 'yat' (य). Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under ending or limit synonyms.",
            "amara_kosha": "Listed in Avyayavarga/Nānārthavarga under limit or death.",
            "abhidhana_ratnamala": "Listed under limits and boundaries."
        }
    },
    "वन्याय": {
        "pada_form": "वन्या॑य",
        "meanings": {
            "english": "To the one in the forests.",
            "nirukta": "Derived from 'vana' (forest) + suffix 'ya'. 'vane bhavaḥ vanyaḥ'.",
            "vedantic": "The presence of Brahman in the natural, wild, and untouched beauty of the forests."
        },
        "grammatical_references": {
            "panini": "Derived from 'vana' + suffix 'yat' (य) by Aṣṭadhyāyī 4.4.110. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under forest or water synonyms.",
            "amara_kosha": "Listed in Bhūvarga under forest synonyms: 'वनं विपिनमरण्यम्'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under forests."
        }
    },
    "कक्ष्याय": {
        "pada_form": "कक्ष्या॑य",
        "meanings": {
            "english": "To the one in the thickets / valleys.",
            "nirukta": "Derived from 'kakṣa' (shrubbery, forest-thicket, or dry forest) + suffix 'ya'. 'kakṣe bhavaḥ kakṣyaḥ'.",
            "vedantic": "Brahman as the protector hidden in the deep thickets and impenetrable places of the world."
        },
        "grammatical_references": {
            "panini": "Derived from 'kakṣa' + suffix 'yat' (य) by Aṣṭadhyāyī 4.2.82. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under dry forest or secret places.",
            "amara_kosha": "Listed in Nānārthavarga (3.3.5) as a term for forest-thicket: 'कक्षा गहाने शुष्कवने'.",
            "abhidhana_ratnamala": "Listed in Bhūmi-kāṇḍa under forests."
        }
    },
    "श्रवाय": {
        "pada_form": "श्र॒वाय॑",
        "meanings": {
            "english": "To the sound / fame.",
            "nirukta": "Derived from the root 'śru' (श्रु) 'to hear'. That which is heard (sound), or the fame that is spread.",
            "vedantic": "The cosmic sound (Nāda-brahman/OM) which is the first vibration of creation; also the supreme fame of the Lord."
        },
        "grammatical_references": {
            "panini": "Derived from √śru (श्रु  श्रवणे, Bhvādi-gaṇa, 1.1091) with the suffix 'ap' (अप्) or 'ghañ'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for ear or sound.",
            "amara_kosha": "Listed in Nānārthavarga under terms for fame or hearing.",
            "abhidhana_ratnamala": "Listed under sound and fame."
        }
    },
    "प्रतिश्रवाय": {
        "pada_form": "प्र॒ति॒-श्र॒वाय॑",
        "meanings": {
            "english": "To the echo / response.",
            "nirukta": "Derived from prefix 'prati' + root 'śru' (to hear). That which responds, i.e., the echo or reply.",
            "vedantic": "The responsiveness of the Divine, who always echoes the devotee's prayer and answers their call."
        },
        "grammatical_references": {
            "panini": "Derived from prefix 'prati' + √śru + suffix 'ap'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with echo or responsive sounds.",
            "amara_kosha": "Listed in Avyayavarga/Nānārthavarga under response or echo.",
            "abhidhana_ratnamala": "Listed under sound and responses."
        }
    },
    "आशुषेणाय": {
        "pada_form": "आ॒शु-षे॑णाय",
        "meanings": {
            "english": "To the one with a swift army.",
            "nirukta": "'āśu' (swift) + 'senā' (army) = 'āśu-ṣeṇa'. He whose hosts move with lightning speed.",
            "vedantic": "The hosts of the Lord (the Maruts, Pramathas) represent the forces of nature and thoughts that execute the divine will instantly."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'āśu' and 'senā', with sandhi conversion of 's' to 'ṣ' by Aṣṭadhyāyī rules. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with army-bearing deities.",
            "amara_kosha": "Synonym for a commander with a fast army.",
            "abhidhana_ratnamala": "Listed under commanders and armies."
        }
    },
    "आशुरथाय": {
        "pada_form": "आ॒शु-र॑थाय",
        "meanings": {
            "english": "To the one with a swift chariot.",
            "nirukta": "'āśu' (swift) + 'ratha' (chariot) = 'āśu-ratha'. He whose chariot is fast-moving.",
            "vedantic": "The chariot represents the mind or the cosmos. The Lord's swift chariot symbolizes His rapid response to the devotee's call."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'āśu' and 'ratha'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under swift-vehicle owners.",
            "amara_kosha": "Epithet of a deity riding a swift chariot.",
            "abhidhana_ratnamala": "Listed under chariots and speeds."
        }
    },
    "शूराय": {
        "pada_form": "शूरा॑य",
        "meanings": {
            "english": "To the hero / warrior.",
            "nirukta": "Derived from the root 'śūr' (शूर्) meaning 'to be bold, powerful, or brave'.",
            "vedantic": "The ultimate courage (Shurya) that destroys the fear of death and the demons of ignorance and ego."
        },
        "grammatical_references": {
            "panini": "Derived from √śūr (शूरँ विक्रान्ते, Bhvādi-gaṇa, 1.0664) with the 'ac' suffix. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for strength or courage (balam, Nighaṇṭu 2.9).",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.1) as a synonym for warrior: 'शूरो वीरश्च विक्रान्तः'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.115) under brave warriors."
        }
    },
    "अवभिन्दते": {
        "pada_form": "अ॒व॒-भि॒न्द॒ते",
        "meanings": {
            "english": "To the one who breaks through / pierces (the enemy forces).",
            "nirukta": "Derived from prefix 'ava' + root 'bhid' (to break/split). 'avabhindati iti avabhindan' (He who pierces through obstacles/enemies).",
            "vedantic": "Brahman who breaks through the hard shell of ignorance (ajnana-kosha) to reveal the light of the Self."
        },
        "grammatical_references": {
            "panini": "Derived from prefix 'ava' + √bhid (भिदँ विदारणे, Rudhādi-gaṇa, 7.0002) with the present participle suffix 'snatṛ'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with destructive or piercing powers.",
            "amara_kosha": "Listed under terms for breaking or splitting.",
            "abhidhana_ratnamala": "Listed under verbs of piercing and destruction."
        }
    },
    "वर्मिणे": {
        "pada_form": "व॒र्मिणे॑",
        "meanings": {
            "english": "To the wearer of a breastplate / armor.",
            "nirukta": "'varma' (armor) + suffix 'in' (इनि). He who is equipped with protective armor.",
            "vedantic": "The Lord who is His own armor, representing the supreme protection that surrounds the devotee."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'varman' (armor) + possessive suffix 'ini' by Aṣṭādhyāyī 5.2.115. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under armored warriors.",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.64) as a synonym for armor: 'वर्म दंशनमुच्यते... तद्वान् वर्मी'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.126) under armor."
        }
    },
    "वरूथिने": {
        "pada_form": "व॒रू॒थिने॑",
        "meanings": {
            "english": "To the one with a shield / protective chariot shelter.",
            "nirukta": "'varūtha' (protective cover/shelter) + suffix 'in'. He who has a protective shield or shelter.",
            "vedantic": "The Divine as the ultimate refuge (Sharanagati-sthana) that shelters the soul from all worldly afflictions."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'varūtha' + possessive suffix 'ini'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under protective shelter synonyms.",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.56) under chariot parts: 'वरूथो रथगुप्तिः'.",
            "abhidhana_ratnamala": "Listed under chariot shields and refuges."
        }
    },
    "बिल्मिने": {
        "pada_form": "बि॒ल्मिने॑",
        "meanings": {
            "english": "To the wearer of a helmet.",
            "nirukta": "'bilma' (helmet/protective headgear) + suffix 'in'. He who wears a helmet.",
            "vedantic": "The helmet represents the protection of the intellect (Buddhi) by divine wisdom, shielding the mind from delusion."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'bilma' + possessive suffix 'ini'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with armored warriors.",
            "amara_kosha": "Epithet of a deity wearing head armor.",
            "abhidhana_ratnamala": "Listed in head armor synonyms."
        }
    },
    "कवचिने": {
        "pada_form": "क॒व॒चिने॑",
        "meanings": {
            "english": "To the wearer of a coat of mail / armor.",
            "nirukta": "'kavaca' (coat of mail/corslet) + suffix 'in'. He who wears a coat of mail.",
            "vedantic": "Represents the spiritual armor of divine grace (Kavacham) that shields the devotee from all negative forces."
        },
        "grammatical_references": {
            "panini": "Derived from the noun 'kavaca' + possessive suffix 'ini'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under armored deities.",
            "amara_kosha": "Listed in Kṣatriyavarga (2.8.64) as a synonym for coat of mail: 'कवचोऽस्त्रियाम्'.",
            "abhidhana_ratnamala": "Listed in Sāmānya-kāṇḍa (2.126) under armor."
        }
    },
    "श्रुताय": {
        "pada_form": "श्रु॒ताय॑",
        "meanings": {
            "english": "To the renowned / famous in the Vedas.",
            "nirukta": "Derived from root 'śru' (to hear). That which is heard or renowned. 'śruti-prasiddhaḥ'.",
            "vedantic": "The Supreme Brahman who is revealed and heard of only in the sacred Upanishads (Śrutis)."
        },
        "grammatical_references": {
            "panini": "Derived from √śru + past passive participle suffix 'kta'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Listed under synonyms for fame or voice.",
            "amara_kosha": "Listed in Nānārthavarga under renowned or heard: 'श्रुतः प्रसिद्धे शाब्दिते'.",
            "abhidhana_ratnamala": "Listed under fame and Vedic hearing."
        }
    },
    "श्रुतसेनाय": {
        "pada_form": "श्रु॒त-से॒नाय॑",
        "meanings": {
            "english": "To the one with a famous army.",
            "nirukta": "'śrutā' (famous/heard of in Shrutis) + 'senā' (army) = 'śruta-senā'. He whose army is famous.",
            "vedantic": "The forces of the Lord (sacred disciplines, virtues, and laws of nature) which are celebrated in the scriptures for maintaining world order."
        },
        "grammatical_references": {
            "panini": "Bahuvrīhi compound of 'śruta' and 'senā'. Dative singular.",
            "case_ending": "Dative Singular (Caturthī Vibhakti, Ekavacana)."
        },
        "lexicographical_references": {
            "nighantu": "Associated with army-bearing deities.",
            "amara_kosha": "Synonym for a commander whose armies are famous.",
            "abhidhana_ratnamala": "Listed under armies and commanders."
        }
    }
}

# Map clean strings to database keys
CLEAN_MAPPING = {
    "नमो": "नमः",
    "नमः": "नमः",
    "नम": "नमः",
    "च": "च",
    "भवाय": "भवाय",
    "रुद्राय": "रुद्राय",
    "शर्वाय": "शर्वाय",
    "पशुपतये": "पशुपतये",
    "पशु-पतये": "पशुपतये",
    "नीलग्रीवाय": "नीलग्रीवाय",
    "नील-ग्रीवाय": "नीलग्रीवाय",
    "शितिकण्ठाय": "शितिकण्ठाय",
    "शिति-कण्ठाय": "शितिकण्ठाय",
    "कपर्दिने": "कपर्दिने",
    "व्युप्तकेशाय": "व्युप्तकेशाय",
    "व्युप्त-केशाय": "व्युप्तकेशाय",
    "सहस्राक्षाय": "सहस्राक्षाय",
    "सहस्र-अक्षाय": "सहस्राक्षाय",
    "शतधन्वने": "शतधन्वने",
    "शत-धन्वने": "शतधन्वने",
    "गिरिशाय": "गिरिशाय",
    "गिरि-शाय": "गिरिशाय",
    "शिपिविष्टाय": "शिपिविष्टाय",
    "शिपि-विष्टाय": "शिपिविष्टाय",
    "मीढुष्टमाय": "मीढुष्टमाय",
    "मीढुः-तमाय": "मीढुष्टमाय",
    "इषुमते": "इषुमते",
    "इषु-मते": "इषुमते",
    "ह्रस्वाय": "ह्रस्वाय",
    "वामनाय": "वामनाय",
    "बृहते": "बृहते",
    "वर्षीयसे": "वर्षाीयसे",
    "वर्​षीयसे": "वर्षाीयसे",
    "वृद्धाय": "वृद्धाय",
    "संवृध्वने": "संवृध्वने",
    "सम्-वृध्वने": "संवृध्वने",
    "अग्रियाय": "अग्रियाय",
    "प्रथमाय": "प्रथमाय",
    "आशवे": "आशवे",
    "अजिराय": "अजिराय",
    "शीघ्रियाय": "शीघ्रियाय",
    "शीभ्याय": "शीभ्याय",
    "ऊर्म्याय": "ऊर्म्याय",
    "अवस्वन्याय": "अवस्वन्याय",
    "अव-स्वन्याय": "अवस्वन्याय",
    "स्रोतस्याय": "स्रोतस्याय",
    "द्वीप्याय": "द्वीप्याय",
    "ज्येष्ठाय": "ज्येष्ठाय",
    "कनिष्ठाय": "कनिष्ठाय",
    "पूर्वजाय": "पूर्वजाय",
    "पूर्व-जाय": "पूर्वजाय",
    "अपरजाय": "अपरजाय",
    "अपर-जाय": "अपरजाय",
    "मध्यमाय": "मध्यमाय",
    "अपगल्भाय": "अपगल्भाय",
    "अप-गल्भाय": "अपगल्भाय",
    "जघन्याय": "जघन्याय",
    "बुध्नियाय": "बुध्नियाय",
    "सोभ्याय": "सोभ्याय",
    "प्रतिसर्याय": "प्रतिसर्याय",
    "प्रति-सर्याय": "प्रतिसर्याय",
    "याम्याय": "याम्याय",
    "क्षेम्याय": "क्षेम्याय",
    "उर्वर्याय": "उर्वर्याय",
    "खल्याय": "खल्याय",
    "श्लोक्याय": "श्लोक्याय",
    "अवसान्याय": "अवसान्याय",
    "अव-सान्याय": "अवसान्याय",
    "वन्याय": "वन्याय",
    "कक्ष्याय": "कक्ष्याय",
    "श्रवाय": "श्रवाय",
    "प्रतिश्रवाय": "प्रतिश्रवाय",
    "प्रति-श्रवाय": "प्रतिश्रवाय",
    "आशुषेणाय": "आशुषेणाय",
    "आशु-षेणाय": "आशुषेणाय",
    "आशुरथाय": "आशुरथाय",
    "आशु-रथाय": "आशुरथाय",
    "शूराय": "शूराय",
    "अवभिन्दते": "अवभिन्दते",
    "अव-भिन्दते": "अवभिन्दते",
    "वर्मिणे": "वर्मिणे",
    "वरूथिने": "वरूथिने",
    "बिल्मिने": "बिल्मिने",
    "कवचिने": "कवचिने",
    "श्रुताय": "श्रुताय",
    "श्रुतसेनाय": "श्रुतसेनाय",
    "श्रुत-सेनाय": "श्रुतसेनाय",
}

# Mapping of samhita token lists (excluding punctuation) to word IDs
SAMHITA_MAPPING = {
    5: {
        1: [[1], [2], [3], [4], [5]],
        2: [[1], [2], [3], [4], [5]],
        3: [[1], [2], [3], [4], [5]],
        4: [[1], [2], [3], [4], [5]],
        5: [[1], [2], [3], [4], [5]],
        6: [[1], [2], [3], [4], [5]],
        7: [[1], [2], [3, 4], [5]],
        8: [[1], [2], [3], [4], [5]],
        9: [[1], [2], [3], [4], [5]],
        10: [[1], [2], [3], [4], [5]],
        11: [[1], [2], [3], [4], [5]],
        12: [[1], [2], [3, 4], [5]],
        13: [[1, 2], [3], [4], [5]],
        14: [[1], [2], [3, 4], [5]],
        15: [[1], [2], [3], [4], [5]]
    },
    6: {
        1: [[1], [2], [3], [4], [5]],
        2: [[1], [2], [3, 4], [5]],
        3: [[1], [2], [3, 4], [5]],
        4: [[1], [2], [3], [4], [5]],
        5: [[1], [2], [3], [4], [5]],
        6: [[1], [2], [3], [4], [5]],
        7: [[1], [2], [3], [4], [5]],
        8: [[1, 2], [3, 4], [5]],
        9: [[1], [2], [3], [4], [5]],
        10: [[1], [2], [3], [4], [5]],
        11: [[1], [2], [3, 4], [5]],
        12: [[1, 2], [3, 4], [5]],
        13: [[1], [2], [3], [4], [5]],
        14: [[1], [2], [3], [4], [5]],
        15: [[1], [2], [3], [4], [5]]
    }
}

def clean_sanskrit_accents(text):
    cleaned = text.replace('॑', '').replace('॒', '').replace('᳚', '')
    cleaned = cleaned.replace('।', '').replace('॥', '').strip()
    return cleaned

def clean_sanskrit_fully(text):
    # Removes accents and hyphens for exact matching
    return clean_sanskrit_accents(text).replace('-', '').replace(' ', '')

def tokenize_pada(pada_str):
    tokens = []
    parts = pada_str.split(" । ")
    for i, part in enumerate(parts):
        word_id = i + 1
        if i == len(parts) - 1:
            if part.endswith(" ॥"):
                word_text = part[:-2].strip()
                tokens.append({"text": word_text, "word_ids": [word_id]})
                tokens.append({"text": " ॥", "word_ids": []})
            else:
                tokens.append({"text": part.strip(), "word_ids": [word_id]})
        else:
            tokens.append({"text": part.strip(), "word_ids": [word_id]})
            tokens.append({"text": " । ", "word_ids": []})
    return tokens

def tokenize_samhita_mapped(samhita, mapping):
    tokens = []
    text = samhita.strip()
    has_double_pipe = False
    if text.endswith("॥"):
        has_double_pipe = True
        text = text[:-1].strip()
        
    parts = text.split(" । ")
    mapping_idx = 0
    for part_idx, part in enumerate(parts):
        words = part.split(" ")
        for word_idx, word in enumerate(words):
            if not word:
                continue
            tokens.append({"text": word, "word_ids": mapping[mapping_idx]})
            mapping_idx += 1
            if word_idx < len(words) - 1:
                tokens.append({"text": " ", "word_ids": []})
        
        if part_idx < len(parts) - 1:
            tokens.append({"text": " । ", "word_ids": []})
            
    if has_double_pipe:
        tokens.append({"text": " ॥", "word_ids": []})
        
    return tokens

def tokenize_krama(krama_str):
    parts = krama_str.split(" । ")
    tokens = []
    step_ids = [[1, 2], [2, 3], [3, 4], [4, 5], [5]]
    
    for i, part in enumerate(parts):
        word_ids = step_ids[i]
        if i == len(parts) - 1:
            if part.endswith(" ॥"):
                text_val = part[:-2].strip()
                tokens.append({"text": text_val, "word_ids": word_ids})
                tokens.append({"text": " ॥", "word_ids": []})
            else:
                tokens.append({"text": part.strip(), "word_ids": word_ids})
        else:
            tokens.append({"text": part.strip(), "word_ids": word_ids})
            tokens.append({"text": " । ", "word_ids": []})
    return tokens

def compute_samhita_spans(samhita, mapping):
    spans = {}
    current_idx = 0
    parts = samhita.split(" ")
    
    word_idx = 0
    for part in parts:
        if not part:
            current_idx += 1
            continue
        
        clean_part = part
        if part.endswith("॥"):
            clean_part = part[:-1]
        elif part.endswith("।"):
            clean_part = part[:-1]
            
        if word_idx >= len(mapping):
            break
        assigned_ids = mapping[word_idx]
        start_pos = current_idx
        end_pos = current_idx + len(clean_part)
        
        if len(assigned_ids) == 1:
            wid = assigned_ids[0]
            spans[wid] = {
                "start": start_pos,
                "end": end_pos,
                "text": clean_part
            }
        elif len(assigned_ids) == 2:
            wid1, wid2 = assigned_ids
            if clean_part.startswith("नम॒-श्"):
                split_pos = 5
            elif clean_part.startswith("च"):
                split_pos = 1
            else:
                split_pos = len(clean_part) // 2
                
            spans[wid1] = {
                "start": start_pos,
                "end": start_pos + split_pos,
                "text": clean_part[:split_pos]
            }
            spans[wid2] = {
                "start": start_pos + split_pos,
                "end": end_pos,
                "text": clean_part[split_pos:]
            }
            
        current_idx += len(part) + 1
        word_idx += 1
        
    return spans

def clean_commentary_block(text):
    return re.sub(r'\s+', ' ', text).strip()

def parse_sanskrit_bhashya(content, mantra_id):
    content_clean = re.sub(r'\s+', ' ', content)
    content_clean = re.sub(r'CC\.0-.*', '', content_clean)
    content_clean = re.sub(r'\[न०पं०अ०\].*', '', content_clean)
    
    sayana_match = re.search(r'सा०\s*[भामा]\s*०\s*(.*?)(?=\s*[भम]०\s*[भामा]०|सा०\s*[भामा]०|\bनमो\b|\bनमः\b|\|\s*' + str(mantra_id) + r'\s*\||॥\s*' + str(mantra_id) + r'\s*॥|\Z)', content_clean)
    bb_match = re.search(r'[भम]०\s*[भामा]०\s*[भामा]०\s*(.*?)(?=\bनमो\b|\bनमः\b|\|\s*' + str(mantra_id) + r'\s*\||॥\s*' + str(mantra_id) + r'\s*॥|\Z)', content_clean)
    
    sayana_text = sayana_match.group(1).strip() if sayana_match else ""
    bb_text = bb_match.group(1).strip() if bb_match else ""
    
    sayana_text = re.sub(r'[।॥]\s*' + str(mantra_id) + r'\s*[।॥]', '', sayana_text).strip()
    bb_text = re.sub(r'[।॥]\s*' + str(mantra_id) + r'\s*[।॥]', '', bb_text).strip()
    
    return sayana_text, bb_text

def split_english_sayana_bb(english_text):
    sayana_eng = ""
    bb_eng = ""
    
    parts = english_text.split("Bhatta-Bhaskara-Bhashya:")
    if len(parts) >= 2:
        bb_part = parts[1]
        sayana_part = parts[0]
        
        s_parts = sayana_part.split("Sayana's Commentary:")
        if len(s_parts) >= 2:
            sayana_eng = s_parts[1].strip()
        else:
            sayana_eng = sayana_part.strip()
            
        bb_eng = bb_part.strip()
    else:
        s_parts = english_text.split("Sayana's Commentary:")
        if len(s_parts) >= 2:
            sayana_eng = s_parts[1].strip()
        else:
            sayana_eng = english_text.strip()
            
    sayana_eng = re.sub(r'\(\d+\)\s*$', '', sayana_eng).strip()
    bb_eng = re.sub(r'\(\d+\)\s*$', '', bb_eng).strip()
    
    return sayana_eng, bb_eng

def process_anuvakam(anuvakam_id):
    print(f"Processing Anuvakam {anuvakam_id}...")
    
    anuvaka_dir = os.path.join(OUTPUT_BASE_DIR, f"anuvakam{anuvakam_id}")
    os.makedirs(anuvaka_dir, exist_ok=True)
    
    with open(CORRELATED_JSON_PATH, 'r', encoding='utf-8') as f:
        correlated_data = json.load(f)
        
    anuvaka_data = next(a for a in correlated_data["anuvakas"] if a["id"] == anuvakam_id)
    
    for mantra in anuvaka_data["mantras"]:
        mantra_id = mantra["id"]
        print(f"  Mantra {mantra_id}...")
        
        samhita = mantra["sanskrit"]["samhita"]
        pada = mantra["sanskrit"]["pada"]
        krama = mantra["sanskrit"]["krama"]
        
        raw_sayana_eng = mantra["translations"].get("sayana", "")
        sayana_eng_clean, bb_eng_clean = split_english_sayana_bb(raw_sayana_eng)
        
        as_eng = mantra["translations"].get("abhinava_shankara", "")
        as_eng = re.sub(r'Śrī Rudra Bhāṣyam\s+\d+', '', as_eng).strip()
        
        as_sanskrit = mantra.get("commentaries_sanskrit", {}).get("abhinava_shankara", "")
        as_sanskrit = re.sub(r'श्रीरुद्रभाष्यम् ।\s+\d+', '', as_sanskrit).strip()
        
        sayana_sanskrit = ""
        bb_sanskrit = ""
        page_path = mantra.get("sources", {}).get("rudradhyaya_page")
        if page_path:
            abs_page_path = os.path.join("/Users/Rkanadam/personal/namakam", page_path)
            if os.path.exists(abs_page_path):
                with open(abs_page_path, 'r', encoding='utf-8') as pf:
                    page_content = pf.read()
                sayana_sanskrit, bb_sanskrit = parse_sanskrit_bhashya(page_content, mantra_id)
                
        mapping = SAMHITA_MAPPING[anuvakam_id][mantra_id]
        spans = compute_samhita_spans(samhita, mapping)
        
        pada_parts = [clean_sanskrit_accents(p) for p in pada.split(" । ")]
        if pada_parts[-1].endswith("॥"):
            pada_parts[-1] = pada_parts[-1][:-2].strip()
            
        words_list = []
        for idx, p_word in enumerate(pada_parts):
            word_id = idx + 1
            clean_word = clean_sanskrit_fully(p_word)
            
            db_key = CLEAN_MAPPING.get(clean_word)
            if not db_key:
                print(f"    WARNING: Word '{clean_word}' (from '{p_word}') not found in CLEAN_MAPPING!")
                db_key = clean_word
                
            word_entry = WORD_DB.get(db_key, {
                "meanings": {"english": "", "nirukta": "", "vedantic": ""},
                "grammatical_references": {"panini": "", "case_ending": ""},
                "lexicographical_references": {"nighantu": "", "amara_kosha": "", "abhidhana_ratnamala": ""}
            })
            
            span_data = spans.get(word_id, {"start": 0, "end": 0, "text": ""})
            
            words_list.append({
                "id": word_id,
                "pada_form": p_word,
                "samhita_span": span_data,
                "meanings": word_entry["meanings"],
                "grammatical_references": word_entry["grammatical_references"],
                "lexicographical_references": word_entry["lexicographical_references"]
            })
            
        if anuvakam_id == 5:
            dhyana_sanskrit = "भस्मोद्धासितसर्वाङ्गजटामण्डलमण्डितम् । ध्यायेत्रयक्षं वृषारूढं गणेश्वरयुतं हरम् ॥"
            dhyana_english = "May one meditate on Hara, who has three eyes, is seated on a bull, accompanied by the lord of hosts (Ganesha), and whose entire body is smeared with ashes and adorned with a crown of matted hair."
        else:
            dhyana_sanskrit = "गौरीकराम्बुजन्यस्तस्वर्णशैलशरासनम् । इषुहस्तं रथारूढं नरनारीतनुं स्मरेत् ॥"
            dhyana_english = "One should meditate on the Lord in the form of Ardhanarishvara (half man, half woman), seated on a chariot, holding an arrow in his hand, and holding a bow (the golden Meru mountain) placed there by the lotus hands of Gauri."
            
        output_data = {
            "id": mantra_id,
            "samhita": samhita,
            "pada": pada,
            "krama": krama,
            "samhita_tokens": tokenize_samhita_mapped(samhita, mapping),
            "pada_tokens": tokenize_pada(pada),
            "krama_tokens": tokenize_krama(krama),
            "words": words_list,
            "commentaries": {
                "sayana": {
                    "rishi": "Bhagavan Shambhu",
                    "chandas": "Mahavirat",
                    "devata": "Bhagavan Shambhu",
                    "sanskrit": sayana_sanskrit,
                    "english": sayana_eng_clean
                },
                "bhatta_bhaskara": {
                    "rishi": "Bhagavan Shambhu",
                    "chandas": "Mahavirat",
                    "devata": "Bhagavan Shambhu",
                    "dhyana": {
                        "sanskrit": dhyana_sanskrit,
                        "english": dhyana_english
                    },
                    "sanskrit": bb_sanskrit,
                    "english": bb_eng_clean
                },
                "abhinava_shankara": {
                    "rishi": "Bhagavan Shambhu",
                    "chandas": "Mahavirat",
                    "devata": "Bhagavan Shambhu",
                    "dhyana": {
                        "sanskrit": dhyana_sanskrit,
                        "english": dhyana_english
                    },
                    "sanskrit": as_sanskrit,
                    "english": as_eng
                }
            }
        }
        
        out_file_path = os.path.join(anuvaka_dir, f"mantra{mantra_id}.json")
        with open(out_file_path, 'w', encoding='utf-8') as out_f:
            json.dump(output_data, out_f, ensure_ascii=False, indent=2)
            
    print(f"Anuvakam {anuvakam_id} completed successfully!")

if __name__ == "__main__":
    process_anuvakam(5)
    process_anuvakam(6)
    print("All tasks completed!")
