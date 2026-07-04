import json
import os
import re

# Base word database with roots, etymologies, Vedantic meanings, Panini roots, and dictionary references
BASE_WORDS = {
    "नमः": {
        "transliteration": "namaḥ",
        "root": "√nam (to bow, bend, submit)",
        "base_devanagari": "नमस्",
        "english_base_sg": "salutation",
        "english_base_pl": "salutations",
        "nirukta": "Derived from the root 'nam' (नम्) meaning 'to bow, bend, or submit'. In Nirukta, 'namas' is defined in the sense of bowing or honoring (namanīya).",
        "vedantic": "Interpreted as 'Na' (not) + 'mama' (mine) — indicating the complete surrender of the individual ego and the realization that nothing belongs to the limited self, but all belongs to the Supreme consciousness.",
        "nighantu": "Listed under water synonyms (udaka-nāmāni, Nighaṇṭu 1.12, item 17) and food synonyms (anna-nāmāni, Nighaṇṭu 2.7) due to its Vedic polysemous usage representing nourishment and flow.",
        "amara_kosha": "Listed in Amarakośa Avyayavarga (3.4.19) as a term indicating bowing, salutation, or reverence.",
        "abhidhana_ratnamala": "Classified in Anekārtha-kāṇḍa (5.26) under Avyayas, meaning bowing or salutation (namaskāra)."
    },
    "सहमान": {
        "transliteration": "sahamāna",
        "root": "√sah (to bear, conquer, tolerate)",
        "base_devanagari": "सहमान",
        "english_base_sg": "victorious one / one who tolerates / conqueror",
        "english_base_pl": "victorious ones",
        "nirukta": "From √sah (षहँ मर्षणे, Bhvādi-gaṇa, 1.0988) meaning to bear or conquer, with the śānac suffix (pres. participle) in the ātmanepada.",
        "vedantic": "Refers to the Lord who conquers all obstacles and tolerates the faults/sins of His devotees, transforming their hearts through patient corrective grace.",
        "nighantu": "Not directly listed in Nighaṇṭu.",
        "amara_kosha": "Related to terms for tolerance (kṣamā) and strength (sahatvam) in Amarakośa.",
        "abhidhana_ratnamala": "Associated with names of strength and tolerance in the Sāmānya-kāṇḍa."
    },
    "निव्याधिन्": {
        "transliteration": "nivyādhin",
        "root": "ni-√vyadh (to pierce/strike deeply)",
        "base_devanagari": "निव्याधिन्",
        "english_base_sg": "deep piercer / shooter",
        "english_base_pl": "deep piercers",
        "nirukta": "Prefix 'ni' (deeply/down) + root √vyadh (व्यधँ ताडने, Divādi-gaṇa, 4.0078) + suffix 'ini' (possessive/agentive). One who strikes home or pierces thoroughly.",
        "vedantic": "The Lord's power of penetration that reaches the innermost recesses of the soul, destroying the core impurities and deep-rooted ignorance.",
        "nighantu": "Associated with weaponry and piercing forces in Naighaṇṭuka-kāṇḍa.",
        "amara_kosha": "Listed under weapon operators and archers in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Associated with sharp weapons and piercing in Anekārtha-kāṇḍa."
    },
    "आव्याधिनी": {
        "transliteration": "āvyādhinī",
        "root": "ā-√vyadh (to pierce from all sides)",
        "base_devanagari": "आव्याधिनी",
        "english_base_sg": "one who pierces from all sides",
        "english_base_pl": "those (female forms) who pierce from all sides",
        "nirukta": "Prefix 'ā' (from all directions) + root √vyadh (to strike/pierce) + feminine suffix 'ṅīp' (ई). Refers to the divine feminine energies of Rudra capable of striking from all sides.",
        "vedantic": "Represents the active, dynamic powers (shakti) of the Divine that surround and pierce the ego from all directions, leaving no escape for ignorance.",
        "nighantu": "Noted under divine feminine energies in Vedic glossaries.",
        "amara_kosha": "Associated with the diverse forms of Shakti in Svargavarga.",
        "abhidhana_ratnamala": "Classified under names of goddesses and divine energies in Svarga-kāṇḍa."
    },
    "पति": {
        "transliteration": "pati",
        "root": "√pā (to protect, govern)",
        "base_devanagari": "पति",
        "english_base_sg": "lord / master / protector",
        "english_base_pl": "lords",
        "nirukta": "Derived from root √pā (पा रक्षणे, Adādi-gaṇa, 2.0051) with the suffix 'ḍati' (अति). One who guards or governs.",
        "vedantic": "The Lord is the 'Pati' (Master) of all 'Pashus' (bound souls). He binds them with the ropes of samsara and liberates them when they surrender.",
        "nighantu": "Listed under synonyms for ruler or protector (īśvara-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śabdādivarga (1.6) as 'patir bhartā marud vṛṣā' (husband/lord/master).",
        "abhidhana_ratnamala": "Classified in Sāmānya-kāṇḍa (2.12) as master or ruler (pati, svāmī)."
    },
    "ककुभ": {
        "transliteration": "kakubha",
        "root": "√kak (to stand high, be proud)",
        "base_devanagari": "ककुभ",
        "english_base_sg": "distinguished chief / peak / outstanding one",
        "english_base_pl": "distinguished chiefs",
        "nirukta": "Derived from √kak (कक लौल्ये, Bhvādi-gaṇa, 1.0886) or associated with heights/peaks. Refers to the foremost or most prominent.",
        "vedantic": "Refers to the Lord as the highest peak of reality, the supreme peak among all deities and the sovereign lord of all creation.",
        "nighantu": "Listed under synonyms for direction (diś-nāmāni, Nighaṇṭu 1.6) representing the cardinal peaks.",
        "amara_kosha": "Listed in Svargavarga (1.1.58) as direction or peak: 'kakup kakubho vā'.",
        "abhidhana_ratnamala": "Classified under directions and peaks in Anekārtha-kāṇḍa."
    },
    "निषङ्गिन्": {
        "transliteration": "niṣaṅgin",
        "root": "ni-√sañj (to attach, hold a sword/quiver)",
        "base_devanagari": "निषङ्गिन्",
        "english_base_sg": "one with a sword / one with a quiver",
        "english_base_pl": "quiver-bearers",
        "nirukta": "Prefix 'ni' + √sañj (षञ्जँ सङ्गे, Bhvādi-gaṇa, 1.1147) + suffix 'ini'. One who has a sword attached to his waist or holds a quiver.",
        "vedantic": "Symbolizes the Lord who is constantly equipped with the weapon of discrimination to cut through the false attachments of the seeker.",
        "nighantu": "Associated with swords and weapons in Naighaṇṭuka-kāṇḍa.",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.61) as sword-bearer or archer.",
        "abhidhana_ratnamala": "Classified under weapon holders in Anekārtha-kāṇḍa."
    },
    "स्तेन": {
        "transliteration": "stena",
        "root": "√sten (to steal secretly)",
        "base_devanagari": "स्तेन",
        "english_base_sg": "secret thief / stena",
        "english_base_pl": "secret thieves",
        "nirukta": "Derived from √sten (स्तेनँ चौर्ये, Bhvādi-gaṇa, 1.0577). Yāska (Nirukta) defines 'stena' as one who commits theft secretly (stenaḥ saṃstyanād vā, steyād vā).",
        "vedantic": "Salutation to the Lord as the lord of secret thieves. This reveals the all-pervasive nature of the Divine (Sarvātmatva), who exists even in the outcast and the sinner. It teaches the seeker to look past social judgments and see the singular consciousness in all.",
        "nighantu": "Listed under synonyms for thieves (stena-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdravarga (2.10.42): 'stena-vyāsa-parimoṣi-caura-taskarāḥ' (defining synonyms for thieves).",
        "abhidhana_ratnamala": "Classified under thieves/criminals in Anekārtha-kāṇḍa (5.95)."
    },
    "इषुधिमत्": {
        "transliteration": "iṣudhimat",
        "root": "iṣudhi (quiver) + matup suffix",
        "base_devanagari": "इषुधिमत्",
        "english_base_sg": "possessor of a quiver",
        "english_base_pl": "possessors of quivers",
        "nirukta": "Compound of 'iṣu' (arrow) + 'dhi' (container, from √dhā) + possessive suffix 'matup'. He who carries the arrow-holder.",
        "vedantic": "Represents the repository of all karmas and experiences. The Lord holds the quiver of cosmic results, discharging them as arrows of destiny.",
        "nighantu": "Associated with weapon containers in Vedic texts.",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.59): 'iṣudhir niṣaṅgaḥ' (quiver).",
        "abhidhana_ratnamala": "Classified under weapon accessories in Sāmānya-kāṇḍa."
    },
    "तस्कर": {
        "transliteration": "taskara",
        "root": "tat-kara (doing that, stealing openly)",
        "base_devanagari": "तस्कर",
        "english_base_sg": "open thief / highway robber / taskara",
        "english_base_pl": "open thieves / highway robbers",
        "nirukta": "Derived by Pāṇini as an irregular compound 'tat' + 'kara' with s-sūtram (P. 6.1.157). One who robs openly on paths, saying 'I will do that' (i.e. steal).",
        "vedantic": "Saluting the Lord in the form of open robbers. If the Lord is the sole reality, all actions (even those labeled as sinful by society) are part of His play. This destroys dualistic moral superiority in the seeker.",
        "nighantu": "Listed under synonyms for thieves and robbers (stena-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdravarga (2.10.42) as a synonym for thief.",
        "abhidhana_ratnamala": "Classified under thieves in Anekārtha-kāṇḍa."
    },
    "वञ्चत्": {
        "transliteration": "vañcat",
        "root": "√vañc (to cheat, deceive, move crookedly)",
        "base_devanagari": "वञ्चत्",
        "english_base_sg": "deceiver / cheat",
        "english_base_pl": "deceivers",
        "nirukta": "From √vañc (वञ्चु गत्योः, Bhvādi-gaṇa, 1.0204 or in causative: to deceive). Present participle 'at' (śatṛ). One who cheats in trade or transactions.",
        "vedantic": "The Lord is Maya, the ultimate power of delusion and deception that makes the impermanent appear permanent.",
        "nighantu": "Not directly listed in Nighaṇṭu.",
        "amara_kosha": "Related to terms for cheating (vañchana, pratāraṇa) in Vyāvahārikavarga.",
        "abhidhana_ratnamala": "Classified under deceptive agents in Anekārtha-kāṇḍa."
    },
    "परिवञ्चत्": {
        "transliteration": "parivañcat",
        "root": "pari-√vañc (to deceive thoroughly)",
        "base_devanagari": "परिवञ्चत्",
        "english_base_sg": "thorough deceiver / master cheat",
        "english_base_pl": "thorough deceivers",
        "nirukta": "Prefix 'pari' (completely) + root √vañc (to deceive) + present participle suffix. One who cheats systematically in all transactions.",
        "vedantic": "Represents the total grip of cosmic illusion (Mahamaya) that covers all aspects of the objective universe, binding the soul in complete duality.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Associated with systematic deception and delusion.",
        "abhidhana_ratnamala": "Classified under terms of deception in Anekārtha-kāṇḍa."
    },
    "स्तायु": {
        "transliteration": "stāyu",
        "root": "√stā (to steal secretly, stayus)",
        "base_devanagari": "स्तायु",
        "english_base_sg": "sneaky pilferer / stāyu",
        "english_base_pl": "sneaky pilferers",
        "nirukta": "Derived from root √stā (to steal/conceal) with the Uṇādi suffix 'yu'. Defined as an insider thief who steals from trusted associates.",
        "vedantic": "The Lord in the form of insider thieves who steal silently. It signifies that the thief is not other than the indwelling Self of all.",
        "nighantu": "Listed under synonyms for thieves (stena-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Associated with thieves and pilferers in Śūdravarga.",
        "abhidhana_ratnamala": "Associated with thieves in Anekārtha-kāṇḍa."
    },
    "निचेरु": {
        "transliteration": "niceru",
        "root": "ni-√car (to wander quietly/stealthily)",
        "base_devanagari": "निचेरु",
        "english_base_sg": "quiet wanderer / stealthy roamer",
        "english_base_pl": "quiet wanderers",
        "nirukta": "Prefix 'ni' (quietly/inwardly) + √car (चरँ गत्यर्थः, Bhvādi-gaṇa, 1.0989) + Uṇādi suffix 'eru'. One who wanders silently with the intent to steal.",
        "vedantic": "The Lord as the silent witness (sakshi) who roams in the background of all thoughts, unnoticed by the outgoing mind.",
        "nighantu": "Associated with movement and wandering in Vedic texts.",
        "amara_kosha": "Related to secret or stealthy movements in Avyayavarga.",
        "abhidhana_ratnamala": "Classified under movement terms in Anekārtha-kāṇḍa."
    },
    "परिचर": {
        "transliteration": "paricara",
        "root": "pari-√car (to wander around, attend)",
        "base_devanagari": "परिचर",
        "english_base_sg": "roamer around / attendant / servant",
        "english_base_pl": "roamers around / attendants",
        "nirukta": "Prefix 'pari' (around) + √car (to wander) + suffix 'ac'. One who roams in public spaces, markets, or acts as an attendant.",
        "vedantic": "Represents the active and dynamic aspect of consciousness that operates in the outer marketplace of the senses, serving the cosmic order.",
        "nighantu": "Noted under helper or servant synonyms in Vedic glossaries.",
        "amara_kosha": "Listed in Śūdravarga (2.10.20) as 'paricaryā paricaraḥ' (attendant/servant).",
        "abhidhana_ratnamala": "Classified under servants and helpers in Sāmānya-kāṇḍa."
    },
    "अरण्य": {
        "transliteration": "araṇya",
        "root": "√ṛ (to go) + suffix 'anya'",
        "base_devanagari": "अरण्य",
        "english_base_sg": "forest / wilderness",
        "english_base_pl": "forests / forest-dwellers / forest-thieves",
        "nirukta": "From √ṛ (to go/obtain) + suffix 'anya'. Yāska defines it as a place remote from human habitation ('araṇyam apāram', Nirukta). Here refers to forest-thieves or dwellers.",
        "vedantic": "The forest represents the untamed mind, full of wild thoughts and thieves (passions). The Lord is the controller of this untamed nature.",
        "nighantu": "Listed under synonyms for forest (araṇya-nāmāni, Nighaṇṭu 1.16).",
        "amara_kosha": "Listed in Vana-varga (2.4.1): 'araṇyaṃ vipinaṃ gahanam'.",
        "abhidhana_ratnamala": "Classified in Vana-kāṇḍa (4.1) under forest names."
    },
    "सृकाविन्": {
        "transliteration": "sṛkāvin",
        "root": "sṛkā (missile/arrow) + vin",
        "base_devanagari": "सृकाविन्",
        "english_base_sg": "possessor of missiles / sṛkāvin",
        "english_base_pl": "possessors of missiles / those armed with missiles",
        "nirukta": "From 'sṛka' (missile, from √sṛj to release) + possessive suffix 'vin' (ini by P. 5.2.115). Those who protect themselves with mechanical throwing devices.",
        "vedantic": "Refers to the weapons of cosmic destruction, showing that the physical instruments of warfare and death are forms of the Divine.",
        "nighantu": "'sṛka' is listed as a synonym for weapon or thunderbolt (vajra-nāmāni, Nighaṇṭu 2.20).",
        "amara_kosha": "Associated with weapons and arrows in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under weapons in Sāmānya-kāṇḍa."
    },
    "जिघांसत्": {
        "transliteration": "jighāmsat",
        "root": "√han (to kill, desiderative: jighāṃs)",
        "base_devanagari": "जिघांसत्",
        "english_base_sg": "one who desires to kill",
        "english_base_pl": "those who desire to kill",
        "nirukta": "Desiderative form of √han (हनँ हिंसागत्योः, Adādi-gaṇa, 2.0002) + present participle suffix 'śatṛ'. One who wishes to destroy or slay.",
        "vedantic": "Representing the destructive aspect of time (Kala), which constantly desires to dissolve all created forms back into the unmanifest source.",
        "nighantu": "Not directly listed in Nighaṇṭu.",
        "amara_kosha": "Associated with killers and enemies in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under hostile agents in Anekārtha-kāṇḍa."
    },
    "मुष्णत्": {
        "transliteration": "muṣṇat",
        "root": "√muṣ (to steal, rob, plunder)",
        "base_devanagari": "मुष्णत्",
        "english_base_sg": "plunderer / stealer / grain-thief",
        "english_base_pl": "plunderers / stealers",
        "nirukta": "From √muṣ (मुषँ स्तेये, Kryādi-gaṇa, 9.0065) + present participle suffix 'śatṛ'. One who robs or steals crops/grain from fields.",
        "vedantic": "The Lord as the stealer of the ego. Just as a grain-thief takes away the harvest, the Lord steals the crops of karmas from the devotee's mind.",
        "nighantu": "Listed under synonyms for thieves (stena-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdravarga (2.10.42) as thief or stealer.",
        "abhidhana_ratnamala": "Classified under thieves in Anekārtha-kāṇḍa."
    },
    "असिमत्": {
        "transliteration": "asimat",
        "root": "asi (sword) + matup suffix",
        "base_devanagari": "असिमत्",
        "english_base_sg": "sword-bearer",
        "english_base_pl": "sword-bearers / those armed with swords",
        "nirukta": "Compound of 'asi' (sword, from √as to throw/cut) + possessive suffix 'matup'. Those carrying swords in hand.",
        "vedantic": "The sword represents the weapon of pure discrimination (viveka-asi). The Lord is the supreme bearer of this sword that cuts the knot of ignorance.",
        "nighantu": "'asi' is listed under weapon synonyms (Nighaṇṭu).",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.56): 'asi-rśastram khadgaḥ'.",
        "abhidhana_ratnamala": "Classified under weapons in Sāmānya-kāṇḍa."
    },
    "नक्तञ्चरत्": {
        "transliteration": "naktañcarat",
        "root": "naktam-√car (to roam at night)",
        "base_devanagari": "नक्तञ्चरत्",
        "english_base_sg": "night-wanderer",
        "english_base_pl": "night-wanderers / those who roam at night",
        "nirukta": "Compound of 'naktam' (at night) + √car (to wander) + present participle 'śatṛ'. Those who operate or rob under the cover of darkness.",
        "vedantic": "Refers to the state of deep ignorance (moha). The Lord is present even in the dark, hidden, and nocturnal activities of life.",
        "nighantu": "Associated with night-roaming spirits or thieves.",
        "amara_kosha": "Listed in Rākṣasavarga (1.1.72): 'naktamcaro rātri-caraḥ'.",
        "abhidhana_ratnamala": "Classified under night-wanderers in Svarga-kāṇḍa."
    },
    "प्रकृन्त": {
        "transliteration": "prakṛnta",
        "root": "pra-√kṛt (to cut, slash)",
        "base_devanagari": "प्रकृन्त",
        "english_base_sg": "cutter / slasher / predatory thief",
        "english_base_pl": "cutters / slashers",
        "nirukta": "Prefix 'pra' + √kṛt (कृतीँ छेदने, Tudādi-gaṇa, 6.0006) + kta-pratyaya (used as agentive/noun). Those who cut down trees, slaughter animals, or slash purses.",
        "vedantic": "The Lord as the mower of life, cutting the thread of worldly attachment and dissolving the physical form at the ordained time.",
        "nighantu": "Not directly listed in Nighaṇṭu.",
        "amara_kosha": "Related to terms for cutting or dividing (cchedana) in Vyāvahārikavarga.",
        "abhidhana_ratnamala": "Classified under cutting or violent actions in Anekārtha-kāṇḍa."
    },
    "उष्णीषिन्": {
        "transliteration": "uṣṇīṣin",
        "root": "uṣṇīṣa (turban) + ini suffix",
        "base_devanagari": "उष्णीषिन्",
        "english_base_sg": "turban-wearer / king / reputable head",
        "english_base_pl": "turban-wearers",
        "nirukta": "From 'uṣṇīṣa' (turban, head-dress) + possessive suffix 'ini'. Represents kings, chieftains, or respectable leaders who wear turbans.",
        "vedantic": "The turban symbolizes authority and respect. The Lord is the ultimate crown/turban of all rulers and respectable citizens, as well as the crown of knowledge.",
        "nighantu": "Associated with ornaments and headwear in Vedic texts.",
        "amara_kosha": "Listed in Manuṣyavarga (2.6.101): 'uṣṇīṣaḥ kirīṭam' (turban/crown).",
        "abhidhana_ratnamala": "Classified under ornaments and crowns in Sāmānya-kāṇḍa."
    },
    "गिरिचर": {
        "transliteration": "giricara",
        "root": "giri-√car (to roam on mountains)",
        "base_devanagari": "गिरिचर",
        "english_base_sg": "mountain-roamer / mountain-wanderer",
        "english_base_pl": "mountain-roamers",
        "nirukta": "Compound of 'giri' (mountain) + √car (to wander/live). One who resides or roams in the high hills and caves.",
        "vedantic": "Points to the Lord who resides on Mount Kailasa, and also to the spiritual heights of consciousness (mountains) where the Self roams freely.",
        "nighantu": "Noted under mountain-dwelling deities or beings.",
        "amara_kosha": "Related to foresters and mountain-dwellers in Vanavarga.",
        "abhidhana_ratnamala": "Associated with mountains and residents in Bhūmi-kāṇḍa."
    },
    "कुलुञ्च": {
        "transliteration": "kuluñca",
        "root": "kula-√luñc (to pluck families/houses, pickpockets)",
        "base_devanagari": "कुलुञ्च",
        "english_base_sg": "plucker / pickpocket / house-thief",
        "english_base_pl": "pluckers / pickpockets / house-thieves",
        "nirukta": "From 'kula' (family/house/wealth) + √luñc (लुञ्चँ अपनयने, Tudādi-gaṇa, 6.0091) meaning to pluck or tear. Those who steal household goods or pick pockets.",
        "vedantic": "The Lord as the plucker of the fruits of action (karma-phala). He plucks away the weeds of vanity from the devotee's mind.",
        "nighantu": "Listed under synonyms for thieves (Nighaṇṭu).",
        "amara_kosha": "Associated with thieves and pickpockets in Śūdravarga.",
        "abhidhana_ratnamala": "Classified under thieves in Anekārtha-kāṇḍa."
    },
    "इषुमत्": {
        "transliteration": "iṣumat",
        "root": "iṣu (arrow) + matup suffix",
        "base_devanagari": "इषुमत्",
        "english_base_sg": "arrow-bearer",
        "english_base_pl": "arrow-bearers / those who possess arrows",
        "nirukta": "Compound of 'iṣu' (arrow, from √iṣ to go/desire) + possessive suffix 'matup'. Those equipped with arrows.",
        "vedantic": "The arrow represents the focused mind aimed at the target (Brahman). The Lord is the supreme source of these arrows of intent.",
        "nighantu": "'iṣu' is listed under weapon synonyms (Nighaṇṭu 2.20).",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.57): 'bāṇā strivyām iṣur dvayoḥ'.",
        "abhidhana_ratnamala": "Classified under weapons in Sāmānya-kāṇḍa."
    },
    "धन्वाविन्": {
        "transliteration": "dhanvāvin",
        "root": "dhanvan (bow) + vin",
        "base_devanagari": "धन्वाविन्",
        "english_base_sg": "bow-bearer",
        "english_base_pl": "bow-bearers / those who carry bows",
        "nirukta": "From 'dhanvan' (bow, from √dhanv to run/flow) + possessive suffix 'vin' (ini). Those who carry bows for warfare.",
        "vedantic": "The bow is Pinaka or the Pranava (Om) in the Upanishads (dhanur praṇavo). The Lord is the ultimate bow-bearer who launches the soul towards liberation.",
        "nighantu": "'dhanvan' is listed under weapon synonyms (Nighaṇṭu 2.20).",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.58): 'dhanuś chāpaḥ śarāsanam'.",
        "abhidhana_ratnamala": "Classified under weapons in Sāmānya-kāṇḍa."
    },
    "च": {
        "transliteration": "ca",
        "root": "conjunction 'ca'",
        "base_devanagari": "च",
        "english_base_sg": "and",
        "english_base_pl": "and",
        "nirukta": "Conjunction meaning 'and' or 'also' (samuccayārtha).",
        "vedantic": "Integrates the various dualities and forms into a single, cohesive vision of the all-pervading Brahman.",
        "nighantu": "Listed under standard Vedic nipātas (particles).",
        "amara_kosha": "Noted in Avyayavarga under conjunctions.",
        "abhidhana_ratnamala": "Classified under particles in Anekārtha-kāṇḍa."
    },
    "युष्मद्": {
        "transliteration": "yuṣmad",
        "root": "second person pronoun 'yuṣmad'",
        "base_devanagari": "युष्मद्",
        "english_base_sg": "you",
        "english_base_pl": "you all",
        "nirukta": "The pronoun of address in the second person, used enclitically as 'vaḥ' in dative/genitive plural.",
        "vedantic": "Addresses the Divine directly as 'You' (Pratyagatman), indicating that God is not a remote third-person object, but the immediate, intimate subject of our own consciousness.",
        "nighantu": "Pronouns are excluded from classical Naighaṇṭuka registers.",
        "amara_kosha": "Noted under pronominal bases in Avyayavarga.",
        "abhidhana_ratnamala": "Pronouns are excluded from classical synonym tables."
    },
    "आतन्वान": {
        "transliteration": "ātanvāna",
        "root": "ā-√tan (to string/stretch a bow)",
        "base_devanagari": "आतन्वान",
        "english_base_sg": "one who strings a bow",
        "english_base_pl": "those who are stringing their bows",
        "nirukta": "Prefix 'ā' + √tan (तनुँ विस्तारे, Tanādi-gaṇa, 8.0001) + middle participle 'śānac'. Those engaged in stringing their bows.",
        "vedantic": "The preparation of the Lord's power. Stringing the bow represents the initial outward projection of the divine will (ikṣaṇa) prior to creation.",
        "nighantu": "Associated with stretching or expanding in Vedic glossaries.",
        "amara_kosha": "Related to stretching and preparation in Vyāvahārikavarga.",
        "abhidhana_ratnamala": "Classified under active verbs in Anekārtha-kāṇḍa."
    },
    "प्रतिदधान": {
        "transliteration": "pratidadhāna",
        "root": "prati-√dhā (to place an arrow on the bowstring)",
        "base_devanagari": "प्रतिदधान",
        "english_base_sg": "one who fits an arrow",
        "english_base_pl": "those who are fitting arrows to the string",
        "nirukta": "Prefix 'prati' + √dhā (डुधाञ् धारणपोषणयोः, Juhotyādi-gaṇa, 3.0010) + middle participle 'śānac'. Those placing the arrow-head on the string.",
        "vedantic": "The immediate focusing of cosmic intent. Fitting the arrow represents the alignment of individual destiny (karma) with the divine law (dharma).",
        "nighantu": "Associated with placing or fitting in Vedic registers.",
        "amara_kosha": "Related to arrow alignment in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under active preparation verbs in Anekārtha-kāṇḍa."
    },
    "आयच्छत्": {
        "transliteration": "āyacchat",
        "root": "ā-√yam (to draw/stretch the bowstring)",
        "base_devanagari": "आयच्छत्",
        "english_base_sg": "one who draws the bow",
        "english_base_pl": "those who are drawing their bows / pulling the string",
        "nirukta": "Prefix 'ā' + √yam (यमँ उपरमे, Bhvādi-gaṇa, 1.1137) + present participle 'śatṛ'. Those pulling the string back to the ear.",
        "vedantic": "The tension of spiritual effort (sadhana). Pulling the string represents the intense focusing of energy needed to transcend the material plane.",
        "nighantu": "Associated with holding or pulling in Vedic glossaries.",
        "amara_kosha": "Related to bow pulling in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under physical action verbs in Anekārtha-kāṇḍa."
    },
    "विसृजत्": {
        "transliteration": "visṛjat",
        "root": "vi-√sṛj (to discharge, shoot)",
        "base_devanagari": "विसृजत्",
        "english_base_sg": "one who shoots / discharger",
        "english_base_pl": "those who are discharging arrows / shooting",
        "nirukta": "Prefix 'vi' + √sṛj (सृजँ विसर्गे, Tudādi-gaṇa, 6.0143) + present participle 'śatṛ'. Those releasing the arrow from the bow.",
        "vedantic": "The release of the soul towards its goal. It also symbolizes the dissolution (pralaya) of the universe when all forms are released back to the source.",
        "nighantu": "Associated with releasing or throwing in Naighaṇṭuka registers.",
        "amara_kosha": "Related to shooting and arrow-release in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under release verbs in Anekārtha-kāṇḍa."
    },
    "अस्यत्": {
        "transliteration": "asyat",
        "root": "√as (to throw, shoot, cast)",
        "base_devanagari": "अस्यत्",
        "english_base_sg": "one who shoots / launcher",
        "english_base_pl": "those who are launching / throwing arrows",
        "nirukta": "From √as (असुँ क्षेपणे, Divādi-gaṇa, 4.0108) + present participle 'śatṛ'. Those who cast or shoot arrows towards a target.",
        "vedantic": "Representing the projection of energy. The Lord casts the individual souls into the arena of samsara to exhaust their karmas.",
        "nighantu": "Listed under synonyms for throwing or launching in Vedic glossaries.",
        "amara_kosha": "Related to shooting in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under throwing actions in Anekārtha-kāṇḍa."
    },
    "विध्यत्": {
        "transliteration": "vidhyat",
        "root": "√vyadh (to pierce, hit a target)",
        "base_devanagari": "विध्यत्",
        "english_base_sg": "one who pierces / hitter",
        "english_base_pl": "those who are piercing / hitting the target",
        "nirukta": "From √vyadh (to pierce/strike) + present participle 'śatṛ'. Those who successfully hit and penetrate the target.",
        "vedantic": "The final impact of truth. The Lord's grace pierces the illusion of separation, bringing the seeker to a state of absolute unity.",
        "nighantu": "Noted under strike or hit synonyms in Vedic glossaries.",
        "amara_kosha": "Related to target penetration in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under piercing actions in Anekārtha-kāṇḍa."
    },
    "आसीन": {
        "transliteration": "āsīna",
        "root": "√ās (to sit, be seated)",
        "base_devanagari": "आसीन",
        "english_base_sg": "one who is sitting",
        "english_base_pl": "those who are sitting",
        "nirukta": "From √ās (आसँ उपवेशने, Adādi-gaṇa, 2.0013) + middle participle 'ānac' (P. 7.2.83). Those who are seated.",
        "vedantic": "The state of stillness and meditation (Dhyana). The sitting form represents the immovable, changeless aspect of the Supreme Self (Purusha).",
        "nighantu": "Associated with rest and sitting in Vedic glossaries.",
        "amara_kosha": "Related to sitting (upaveśana) in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under resting postures in Sāmānya-kāṇḍa."
    },
    "शयान": {
        "transliteration": "śayāna",
        "root": "√śī (to lie down, sleep)",
        "base_devanagari": "शयान",
        "english_base_sg": "one who is lying down",
        "english_base_pl": "those who are lying down",
        "nirukta": "From √śī (शीङ् स्वप्ने, Adādi-gaṇa, 2.0026) + middle participle 'śānac'. Those who are in a reclining or resting posture.",
        "vedantic": "Represents the latent, unmanifest state of the universe (Pralaya) and the state of deep sleep (sushupti) where all dualities dissolve.",
        "nighantu": "Associated with sleep and rest in Vedic glossaries.",
        "amara_kosha": "Related to sleeping (śayana, svapna) in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under sleeping postures in Sāmānya-kāṇḍa."
    },
    "स्वपत्": {
        "transliteration": "svapat",
        "root": "√svap (to sleep)",
        "base_devanagari": "स्वपत्",
        "english_base_sg": "one who is sleeping",
        "english_base_pl": "those who are sleeping",
        "nirukta": "From √svap (्ञिष्वप् श्ये, Adādi-gaṇa, 2.0065) + present participle 'śatṛ'. Those who are asleep.",
        "vedantic": "The Lord in the state of sleep. Shows that even in the state of unconsciousness, the supreme light of the Self continues to shine as the witness.",
        "nighantu": "Listed under synonyms for sleep or dream (Nighaṇṭu).",
        "amara_kosha": "Listed in Manuṣyavarga under sleep: 'svapnaḥ svāpo viśenayaḥ'.",
        "abhidhana_ratnamala": "Classified under sleep in Sāmānya-kāṇḍa."
    },
    "जाग्रत्": {
        "transliteration": "jāgrat",
        "root": "√jāgṛ (to wake, be awake)",
        "base_devanagari": "जाग्रत्",
        "english_base_sg": "one who is awake",
        "english_base_pl": "those who are awake",
        "nirukta": "From √jāgṛ (जागृ शीलने, Adādi-gaṇa, 2.0028) + present participle 'śatṛ'. Those who are in the waking state.",
        "vedantic": "The waking state (jagrat-avastha). The Lord exists as the objective world and the conscious self (Vaishvanara) in the waking state.",
        "nighantu": "Associated with alertness and waking in Vedic texts.",
        "amara_kosha": "Related to waking (jāgaraṇa) in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under alertness in Sāmānya-kāṇḍa."
    },
    "तिष्ठत्": {
        "transliteration": "tiṣṭhat",
        "root": "√sthā (to stand, be steady)",
        "base_devanagari": "तिष्ठत्",
        "english_base_sg": "one who is standing",
        "english_base_pl": "those who are standing",
        "nirukta": "From √sthā (ष्ठानि गतिनिवृत्तौ, Bhvādi-gaṇa, 1.1077) + present participle 'śatṛ'. Those who stand upright.",
        "vedantic": "Represents the active preservation (sthiti) of the universe. The standing posture symbolizes stability, presence, and readiness to protect.",
        "nighantu": "Associated with stability and standing in Vedic registers.",
        "amara_kosha": "Related to standing (sthāna) in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under postures in Sāmānya-kāṇḍa."
    },
    "धावत्": {
        "transliteration": "dhāvat",
        "root": "√dhāv (to run)",
        "base_devanagari": "धावत्",
        "english_base_sg": "one who is running",
        "english_base_pl": "those who are running",
        "nirukta": "From √dhāv (धावू गतिशुद्धयोः, Bhvādi-gaṇa, 1.0691) + present participle 'śatṛ'. Those who run or move swiftly.",
        "vedantic": "The Lord running to protect His devotees, as a cow runs to its calf. It indicates that the Divine is highly responsive to the call of devotion.",
        "nighantu": "Listed under synonyms for speed or running in Naighaṇṭuka-kāṇḍa.",
        "amara_kosha": "Related to speed (java, vegah) in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under motion verbs in Anekārtha-kāṇḍa."
    },
    "सभा": {
        "transliteration": "sabhā",
        "root": "saha + √bhā (to shine together)",
        "base_devanagari": "सभा",
        "english_base_sg": "assembly / congregation",
        "english_base_pl": "assemblies",
        "nirukta": "From 'saha' (together) + √bhā (to shine). A place where people sit together and shine through mutual wisdom and order.",
        "vedantic": "The assembly represents the collective consciousness. The Lord is the self of the assembly, present in the collective social order and governance.",
        "nighantu": "Listed under synonyms for assembly or congregation (sabhā-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdra-varga (2.10.1): 'sabhā samiti-samsadaḥ'.",
        "abhidhana_ratnamala": "Classified under assembly names in Sāmānya-kāṇḍa."
    },
    "सभापति": {
        "transliteration": "sabhāpati",
        "root": "sabhā + pati (lord of assembly)",
        "base_devanagari": "सभापति",
        "english_base_sg": "lord of the assembly / president",
        "english_base_pl": "lords of the assemblies / presidents",
        "nirukta": "Compound of 'sabhā' (assembly) + 'pati' (lord). He who presides over, directs, and protects the congregation.",
        "vedantic": "The Lord is the supreme intelligence that guides all assemblies and councils, maintaining justice, harmony, and cosmic law (Rta).",
        "nighantu": "Not directly listed in Nighaṇṭu.",
        "amara_kosha": "Related to rulers and presidents in Ksatriyavarga.",
        "abhidhana_ratnamala": "Classified under master/ruler in Sāmānya-kāṇḍa."
    },
    "अश्व": {
        "transliteration": "aśva",
        "root": "√aś (to pervade, travel fast)",
        "base_devanagari": "अश्व",
        "english_base_sg": "horse",
        "english_base_pl": "horses / those who lack personal property (a-sva)",
        "nirukta": "From √aś (अशूँ व्याप्तौ, Kryādi-gaṇa, 9.0062) meaning to pervade or travel fast. Etymologized by Yāska as 'aśuvyāpī' (fast-pervading). Alternatively parsed as 'a-sva' (having no property, representing ascetics).",
        "vedantic": "The horse represents the senses in the Upanishads (indriyāṇi hayān āhuḥ). The Lord is the self of the senses, and also the self of the poor and property-less (a-sva).",
        "nighantu": "Listed under synonyms for horse (aśva-nāmāni, Nighaṇṭu 1.14).",
        "amara_kosha": "Listed in Ksatriyavarga (2.8.44): 'ghoṭako vītihayo-’śvaḥ'.",
        "abhidhana_ratnamala": "Classified in Catur-aṅga-kāṇḍa (3.24) under horse names."
    },
    "अश्वपति": {
        "transliteration": "aśvapati",
        "root": "aśva + pati (lord of horses)",
        "base_devanagari": "अश्वपति",
        "english_base_sg": "lord of horses / horse-keeper / wealthy lord",
        "english_base_pl": "lords of horses",
        "nirukta": "Compound of 'aśva' (horse) + 'pati' (lord). One who controls, owns, or cares for horses. Also represents the wealthy.",
        "vedantic": "The Lord as the controller of the senses (the horses of the chariot of the body). He is the supreme chariot-driver (Sarathi) of our lives.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Associated with horse-keepers and cavalry leaders.",
        "abhidhana_ratnamala": "Classified under horse-keepers in Sāmānya-kāṇḍa."
    },
    "आव्याधिनी": {
        "transliteration": "āvyādhinī",
        "root": "ā-√vyadh (to pierce/strike from all sides)",
        "base_devanagari": "आव्याधिनी",
        "english_base_sg": "one who strikes from all sides",
        "english_base_pl": "those who strike from all sides",
        "nirukta": "See entry in Anuvakam 3. Prefix 'ā' + √vyadh + feminine suffix 'ṅīp'.",
        "vedantic": "The Lord's feminine energies of destruction that strike the ego and cleanse the soul from all directions.",
        "nighantu": "Associated with divine feminine forms.",
        "amara_kosha": "Associated with Shakti in Svargavarga.",
        "abhidhana_ratnamala": "Classified under names of goddesses."
    },
    "विविध्यन्ती": {
        "transliteration": "vividhyantī",
        "root": "vi-√vyadh (to pierce in diverse ways)",
        "base_devanagari": "विविध्यन्ती",
        "english_base_sg": "one who strikes in diverse ways",
        "english_base_pl": "those who strike in diverse ways",
        "nirukta": "Prefix 'vi' (diverse/special) + √vyadh (to pierce) + present participle feminine suffix 'śatṛ + ṅīp'. Those who pierce and wound in varied ways.",
        "vedantic": "Represents the diverse, multifaceted modes of karmic correction. The Lord corrections come in various forms to suit each soul.",
        "nighantu": "Not directly in Nighaṇṭu.",
        "amara_kosha": "Associated with active feminine forces.",
        "abhidhana_ratnamala": "Classified under active feminine forces in Anekārtha-kāṇḍa."
    },
    "उगणा": {
        "transliteration": "ugaṇā",
        "root": "ud-gaṇa (fierce/outstanding troop)",
        "base_devanagari": "उगणा",
        "english_base_sg": "member of a fierce troop / goddess",
        "english_base_pl": "members of fierce troops / fierce goddesses",
        "nirukta": "From 'ud' (mighty/fierce) + 'gaṇa' (troop). Refers to the fierce bands of divine mothers (Saptamatrikas) or Rudra's female attendants.",
        "vedantic": "The Lord manifesting in the fierce, collective forces of nature and the powerful female deities that protect the cosmic order.",
        "nighantu": "Associated with divine retinues in Vedic glossaries.",
        "amara_kosha": "Associated with the Matrikas and fierce goddesses in Svargavarga.",
        "abhidhana_ratnamala": "Classified under names of goddesses in Svarga-kāṇḍa."
    },
    "तृंहती": {
        "transliteration": "tṛṃhatī",
        "root": "√tṛh (to crush, kill, destroy)",
        "base_devanagari": "तृंहती",
        "english_base_sg": "destroying one / slayer",
        "english_base_pl": "slayers / destroying ones",
        "nirukta": "From √tṛh (तृंहँ हिंसार्थः, Bhvādi-gaṇa, 1.0847 or Kryādi-gaṇa, 9.0069) + present participle feminine 'śatṛ + ṅīp'. Those who crush or destroy.",
        "vedantic": "The force of absolute dissolution. The Lord crushes the illusions, fears, and sins of His devotees, returning them to pure peace.",
        "nighantu": "Associated with killing or crushing in Vedic texts.",
        "amara_kosha": "Related to terms for injury or killing in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under violent actions in Anekārtha-kāṇḍa."
    },
    "गृत्स": {
        "transliteration": "gṛtsa",
        "root": "√gṛdh (to covet) or √gṛ (to praise)",
        "base_devanagari": "गृत्स",
        "english_base_sg": "wise counsellor / sharp-minded one / covetous one",
        "english_base_pl": "wise counsellors / sharp-minded ones",
        "nirukta": "Derived from √gṛdh (गृधुँ अभिकाङ्क्षायाम्, Divādi-gaṇa, 4.0152) or √gṛ (to praise). Commentators define 'gṛtsa' as wise, clever, or covetous.",
        "vedantic": "The Lord as the intellect (Buddhi) in the wise, and also as the desire/covetousness in ordinary beings, showing His presence in all mental faculties.",
        "nighantu": "Listed under synonyms for wise or intelligent (medhāvi-nāmāni, Nighaṇṭu 3.15).",
        "amara_kosha": "Listed in Vyāvahārikavarga under intelligent names: 'gṛtso medhāvī'.",
        "abhidhana_ratnamala": "Classified under wise/intelligent in Sāmānya-kāṇḍa."
    },
    "गृत्सपति": {
        "transliteration": "gṛtsapati",
        "root": "gṛtsa + pati (lord of the wise)",
        "base_devanagari": "गृत्सपति",
        "english_base_sg": "lord of the wise / master of counsellors",
        "english_base_pl": "lords of the wise",
        "nirukta": "Compound of 'gṛtsa' (wise/covetous) + 'pati' (lord). He who leads and protects the assemblies of wise counsellors.",
        "vedantic": "The Lord is the supreme director of the intellect (Preraka), guiding the minds of the wise towards right judgment and liberation.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Associated with leaders of councils and wise groups.",
        "abhidhana_ratnamala": "Classified under leaders in Sāmānya-kāṇḍa."
    },
    "व्रात": {
        "transliteration": "vrāta",
        "root": "√vṛ (to choose, group)",
        "base_devanagari": "व्रात",
        "english_base_sg": "member of a band / diverse occupation",
        "english_base_pl": "members of bands / diverse occupational groups",
        "nirukta": "From √vṛ (वृञ् वरणे, Bhvādi-gaṇa, 1.1040). Yāska defines 'vrāta' as a group of people of different families and occupations who move together.",
        "vedantic": "The Lord resides in the diverse, unstructured groups of society, including wandering bands and nomadic communities, indicating His presence in all classes.",
        "nighantu": "Listed under synonyms for group or troop (vrāta-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdravarga (2.10.1): 'vrātāḥ samūhāḥ'.",
        "abhidhana_ratnamala": "Classified under groups and crowds in Sāmānya-kāṇḍa."
    },
    "व्रातपति": {
        "transliteration": "vrātapati",
        "root": "vrāta + pati (lord of bands)",
        "base_devanagari": "व्रातपति",
        "english_base_sg": "lord of the bands / leader of outcasts",
        "english_base_pl": "lords of the bands",
        "nirukta": "Compound of 'vrāta' (band/group) + 'pati' (lord). The leader of a group of outcasts or nomadic workers.",
        "vedantic": "The Lord is the protector and guide of those who live on the fringes of society, demonstrating that no group is outside the divine light.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Associated with group leaders and tribal chiefs.",
        "abhidhana_ratnamala": "Classified under group leaders in Sāmānya-kāṇḍa."
    },
    "गण": {
        "transliteration": "gaṇa",
        "root": "√gaṇ (to count, group)",
        "base_devanagari": "गण",
        "english_base_sg": "member of the retinue / troop member",
        "english_base_pl": "members of the retinues / Shiva's troops",
        "nirukta": "From √gaṇ (गणँ संख्याने, Churādi-gaṇa, 10.0381). A counted group or troop, specifically the demigod hosts of Shiva.",
        "vedantic": "The 'Gaṇas' represent the classified forces of nature. The Lord is present as every individual member of these cosmic forces.",
        "nighantu": "Listed under synonyms for group or assembly (gaṇa-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Svargavarga (1.1.8) as Shiva's host: 'pramathās tu gaṇāḥ'.",
        "abhidhana_ratnamala": "Classified under Shiva's host in Svarga-kāṇḍa."
    },
    "गणपति": {
        "transliteration": "gaṇapati",
        "root": "gaṇa + pati (lord of troops)",
        "base_devanagari": "गणपति",
        "english_base_sg": "lord of the retinue / Ganesha",
        "english_base_pl": "lords of the retinues / Ganeshas",
        "nirukta": "Compound of 'gaṇa' (troop) + 'pati' (lord). The leader of Shiva's divine hosts (Pramatha-ganas), representing Lord Ganesha.",
        "vedantic": "The Lord is the master of all categories (Gaṇas) of existence, the remover of obstacles (Vighneshvara), and the gateway to knowledge.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Listed in Svargavarga (1.1.38): 'vināyako vighnarāja-dvaimātura-gaṇādhipāḥ'.",
        "abhidhana_ratnamala": "Classified in Svarga-kāṇḍa (1.37) under names of Ganesha: 'gaṇādhipo gaṇapatiḥ'."
    },
    "विरूप": {
        "transliteration": "virūpa",
        "root": "vi-rūpa (deformed/diverse form)",
        "base_devanagari": "विरूप",
        "english_base_sg": "misshapen one / diverse-formed one",
        "english_base_pl": "misshapen ones / those of diverse forms",
        "nirukta": "Prefix 'vi' (deformed/contrary or diverse) + 'rūpa' (form). One who has unusual, grotesque, or diverse physical features.",
        "vedantic": "The Lord is present in the deformed, the disabled, and the grotesque. Beauty and ugliness are both relative projections; the Divine underlies both.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Related to terms for deformity in Manuṣyavarga.",
        "abhidhana_ratnamala": "Classified under forms and shapes in Anekārtha-kāṇḍa."
    },
    "विश्वरूप": {
        "transliteration": "viśvarūpa",
        "root": "viśva-rūpa (universal form)",
        "base_devanagari": "विश्वरूप",
        "english_base_sg": "universal-formed one",
        "english_base_pl": "universal-formed ones / those of all shapes",
        "nirukta": "Compound of 'viśva' (all/universe) + 'rūpa' (form). He whose body is the entire universe, containing all shapes and objects.",
        "vedantic": "The Visvarupa (Universal Form) of the Lord, as described in the Gita (Chapter 11). All individual forms are parts of this one cosmic body.",
        "nighantu": "Listed under synonyms for the universe or sun in Vedic registers.",
        "amara_kosha": "Listed in Svargavarga (1.1.20) as a name of the Supreme Lord or Vishnu.",
        "abhidhana_ratnamala": "Classified under names of the Supreme in Svarga-kāṇḍa."
    },
    "महत्": {
        "transliteration": "mahat",
        "root": "√mah (to grow, honor)",
        "base_devanagari": "महत्",
        "english_base_sg": "great one / mighty one",
        "english_base_pl": "great ones / mighty ones",
        "nirukta": "From √mah (महँ पूजायाम्, Bhvādi-gaṇa, 1.0858) + present participle 'śatṛ'. That which is large, honorable, or mighty.",
        "vedantic": "Refers to the great ones (Mahatmas) and the cosmic intellect (Mahat-Tattva). The Lord is the self of greatness and evolution.",
        "nighantu": "Listed under synonyms for great or large (mahat-nāmāni, Nighaṇṭu 3.3).",
        "amara_kosha": "Listed in Avyayavarga and Sāmānya-kāṇḍa as synonym for large or great: 'mahac ca bhūyaḥ'.",
        "abhidhana_ratnamala": "Classified under terms for large/great in Sāmānya-kāṇḍa."
    },
    "क्षुल्लक": {
        "transliteration": "kṣullaka",
        "root": "√kṣud (to crush, be small)",
        "base_devanagari": "क्षुल्लक",
        "english_base_sg": "small one / minor one",
        "english_base_pl": "small ones / minor ones",
        "nirukta": "From √kṣud (to crush, make small) + suffix 'ka'. That which is tiny, insignificant, or minor.",
        "vedantic": "The Lord is present in the smallest atom (aṇor aṇīyān) as well as the greatest (mahato mahīyān). The insignificant is also Divine.",
        "nighantu": "Listed under synonyms for small or minor (hrasva-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Vyāvahārikavarga (3.1) as tiny or minor: 'kṣullakaḥ kṣudraḥ'.",
        "abhidhana_ratnamala": "Classified under small/minor in Sāmānya-kāṇḍa."
    },
    "रथिन्": {
        "transliteration": "rathin",
        "root": "ratha (chariot) + ini",
        "base_devanagari": "रथिन्",
        "english_base_sg": "chariot-rider",
        "english_base_pl": "chariot-riders / those who own chariots",
        "nirukta": "From 'ratha' (chariot) + possessive suffix 'ini' (in). One who rides in or owns a chariot.",
        "vedantic": "The chariot represents the body. The 'Rathin' is the individual self (Jivatman) riding in the chariot of the body, guided by the intellect.",
        "nighantu": "Associated with speed and chariot-warriors in Vedic registers.",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.63) as chariot-rider or warrior.",
        "abhidhana_ratnamala": "Classified under chariot-warriors in Catur-aṅga-kāṇḍa."
    },
    "अरथ": {
        "transliteration": "aratha",
        "root": "a-ratha (without chariot)",
        "base_devanagari": "अरथ",
        "english_base_sg": "one without a chariot / pedestrian",
        "english_base_pl": "those without chariots / pedestrians",
        "nirukta": "Negative prefix 'a' (not) + 'ratha' (chariot). One who has no chariot and walks on foot.",
        "vedantic": "The Lord is present in both the wealthy chariot-riders and the poor pedestrians, establishing absolute equality (samatva) in the Divine vision.",
        "nighantu": "Not directly in Nighaṇṭu.",
        "amara_kosha": "Associated with foot-travelers and pedestrians in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under foot-soldiers in Catur-aṅga-kāṇḍa."
    },
    "रथ": {
        "transliteration": "ratha",
        "root": "√ramh (to speed) or √ṛ (to go)",
        "base_devanagari": "रथ",
        "english_base_sg": "chariot",
        "english_base_pl": "chariots / vehicle forms",
        "nirukta": "From √ramh (to speed) or √ṛ (to go) + suffix 'tha'. Yāska defines ratha as that which speeds ('ramhana-shila', Nirukta). Represents vehicles.",
        "vedantic": "The chariot is the physical body (rathas tu śarīram). Saluting the vehicle itself shows that the inert matter of the body is also a divine temple.",
        "nighantu": "Listed under synonyms for vehicle (ratha-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.52): 'ratho 'napānaṃ syandanaḥ' (chariot/vehicle).",
        "abhidhana_ratnamala": "Classified in Catur-aṅga-kāṇḍa (3.20) under chariot names."
    },
    "रथपति": {
        "transliteration": "rathapati",
        "root": "ratha + pati (lord of chariots)",
        "base_devanagari": "रथपति",
        "english_base_sg": "lord of chariots / chariot-owner",
        "english_base_pl": "lords of chariots",
        "nirukta": "Compound of 'ratha' (chariot) + 'pati' (lord). He who owns, directs, or commands a fleet of chariots.",
        "vedantic": "The Lord as the controller of the cosmic vehicles (stars, planets, and bodies) that move according to His laws.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Associated with chariot-owners and kings in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under vehicle masters in Sāmānya-kāṇḍa."
    },
    "सेना": {
        "transliteration": "senā",
        "root": "si (to bind) + na",
        "base_devanagari": "सेना",
        "english_base_sg": "army",
        "english_base_pl": "armies",
        "nirukta": "From √si (to bind) + suffix 'na'. An organized body of soldiers bound by a common discipline and command.",
        "vedantic": "The army represents the collective protective forces of righteousness (Dharma). The Lord is the self of these collective forces.",
        "nighantu": "Listed under synonyms for army or host (senā-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.80): 'senā camūr vahinī'.",
        "abhidhana_ratnamala": "Classified in Catur-aṅga-kāṇḍa under army names."
    },
    "सेनानी": {
        "transliteration": "senānī",
        "root": "senā + √nī (to lead an army)",
        "base_devanagari": "सेनानी",
        "english_base_sg": "commander of the army",
        "english_base_pl": "commanders of the armies",
        "nirukta": "Compound of 'senā' (army) + √nī (णीञ् प्रापणे, Bhvādi-gaṇa, 1.1049) meaning to lead. The general or commander who leads the host.",
        "vedantic": "The Lord is the supreme leader of the armies of light (Devas) fighting against the darkness (Asuras) within the human heart.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.81): 'senānīr vāhini-patiḥ'.",
        "abhidhana_ratnamala": "Classified in Catur-aṅga-kāṇḍa under army commanders."
    },
    "क्षत्तृ": {
        "transliteration": "kṣattṛ",
        "root": "√kṣad (to cut, divide, distribute, drive)",
        "base_devanagari": "क्षत्तृ",
        "english_base_sg": "chariot-driver / distributor / gatekeeper",
        "english_base_pl": "chariot-drivers / gatekeepers",
        "nirukta": "From √kṣad (क्षद् संविभागे, Bhvādi-gaṇa, 1.0964) + agentive suffix 'tṛc'. Refers to the charioteer (who drives), gatekeepers, or distributors of food/wealth.",
        "vedantic": "The Lord as the driver of the chariot of life, and the gatekeeper who controls access to the inner chamber of the heart.",
        "nighantu": "Associated with servants or charioteers in Vedic glossaries.",
        "amara_kosha": "Listed in Kṣatriyavarga (2.8.63) as sarathi (charioteer) or gatekeeper.",
        "abhidhana_ratnamala": "Classified under charioteers in Catur-aṅga-kāṇḍa."
    },
    "संग्रहीतृ": {
        "transliteration": "saṅgrahītṛ",
        "root": "sam-√grah (to hold, grasp, rein in)",
        "base_devanagari": "संग्रहीतृ",
        "english_base_sg": "rein-holder / collector / gatherer",
        "english_base_pl": "rein-holders / collectors",
        "nirukta": "Prefix 'sam' + √grah (ग्रहँ उपादाने, Kryādi-gaṇa, 9.0071) + agentive suffix 'tṛc'. One who holds the reins of the horses or collects taxes/wealth.",
        "vedantic": "The Lord as the rein-holder. He controls the reins of the senses (Prana/Mind) in the devotee who surrenders to Him.",
        "nighantu": "Associated with rein-holders and controllers in Vedic texts.",
        "amara_kosha": "Related to reins (grahaṇa, raśmi) and drivers in Kṣatriyavarga.",
        "abhidhana_ratnamala": "Classified under horse controllers in Catur-aṅga-kāṇḍa."
    },
    "तक्षन्": {
        "transliteration": "takṣan",
        "root": "√takṣ (to fashion, carve, cut wood)",
        "base_devanagari": "तक्षन्",
        "english_base_sg": "carpenter / takṣan",
        "english_base_pl": "carpenters",
        "nirukta": "From √takṣ (तक्षूँ त्वचीकरणे, Bhvādi-gaṇa, 1.0747). One who cuts, fashions, and carves wood to build houses or furniture.",
        "vedantic": "The Lord as the supreme carpenter of the universe (Vishvakarman), who fashions the names and forms (nama-rupa) of the physical world.",
        "nighantu": "Listed under craftsmen or creators in Vedic registers.",
        "amara_kosha": "Listed in Śūdravarga (2.10.6): 'takṣā tu vardhakiḥ'.",
        "abhidhana_ratnamala": "Classified under craftsmen in Sāmānya-kāṇḍa (2.80)."
    },
    "रथकार": {
        "transliteration": "rathakāra",
        "root": "ratha + √kṛ (to make chariots)",
        "base_devanagari": "रथकार",
        "english_base_sg": "chariot-maker / artisan",
        "english_base_pl": "chariot-makers / artisans",
        "nirukta": "Compound of 'ratha' (chariot) + √kṛ (to make). A skilled artisan belonging to the mixed caste whose occupation is building chariots.",
        "vedantic": "The Lord as the chariot-maker, building the physical vehicles (bodies) of all living beings to allow them to experience their karmas.",
        "nighantu": "Listed under occupational specialists in Vedic texts.",
        "amara_kosha": "Listed in Śūdravarga (2.10.8) under artisans and mixed castes.",
        "abhidhana_ratnamala": "Classified under chariot-makers in Sāmānya-kāṇḍa."
    },
    "कुलाल": {
        "transliteration": "kulāla",
        "root": "kula (heap/clay) + √al (to shape/make)",
        "base_devanagari": "कुलाल",
        "english_base_sg": "potter",
        "english_base_pl": "potters",
        "nirukta": "From 'kula' (the family or heap of clay) + √al (to shape). The craftsman who works on the wheel to fashion clay vessels.",
        "vedantic": "The potter is the classic Upanishadic analogy for the material cause. The Lord is both the potter (efficient cause) and the clay (material cause) of the cosmos.",
        "nighantu": "Listed under artisans in Naighaṇṭuka-kāṇḍa.",
        "amara_kosha": "Listed in Śūdravarga (2.10.6): 'kulālaḥ kambhakarakaḥ'.",
        "abhidhana_ratnamala": "Classified in Sāmānya-kāṇḍa (2.81) as potter (kumbhakāra)."
    },
    "कर्मार": {
        "transliteration": "karmāra",
        "root": "karman (work) + √ṛ (to go/attain)",
        "base_devanagari": "कर्मार",
        "english_base_sg": "blacksmith / artisan",
        "english_base_pl": "blacksmiths / metal-artisans",
        "nirukta": "From 'karman' (metal work/activity) + √ṛ (to go). The blacksmith or metalworker who melts and shapes iron and other metals.",
        "vedantic": "The Lord as the blacksmith who melts the rigid, cold hearts of devotees in the fire of devotion and shapes them into vessels of grace.",
        "nighantu": "Listed under metal workers in Vedic registers.",
        "amara_kosha": "Listed in Śūdravarga (2.10.9): 'karmāro lohakārakaḥ' (blacksmith).",
        "abhidhana_ratnamala": "Classified in Sāmānya-kāṇḍa (2.81) as ironworker (lohakāra)."
    },
    "पुञ्जिष्ठ": {
        "transliteration": "puñjiṣṭha",
        "root": "puñja (heap/net) + iṣṭhan (superlative)",
        "base_devanagari": "पुञ्जिष्ठ",
        "english_base_sg": "fowler / bird-catcher / sand-gatherer",
        "english_base_pl": "fowlers / bird-catchers / sand-gatherers",
        "nirukta": "From 'puñja' (heap/flock) + superlative suffix 'iṣṭhan'. Those who catch birds in flocks, or fishermen, or those who gather sand-mounds.",
        "vedantic": "The fowler catches birds using nets. The Lord as the fowler catches the flying minds of seekers in the net of His divine love.",
        "nighantu": "Associated with hunters or outcasts in Vedic glossaries.",
        "amara_kosha": "Listed in Vyādhacarita in Śūdravarga (2.10.25) as bird-catcher or hunter.",
        "abhidhana_ratnamala": "Classified under hunters in Sāmānya-kāṇḍa."
    },
    "निषाद": {
        "transliteration": "niṣāda",
        "root": "ni-√sad (to sit down, settle)",
        "base_devanagari": "निषाद",
        "english_base_sg": "mountaineer hunter / outcaste niṣāda",
        "english_base_pl": "mountaineer hunters / outcaste hunters",
        "nirukta": "From 'ni' (inwardly/down) + √sad (षद्लँ विशरणगत्यवसादनेषु, Bhvādi-gaṇa, 1.0990). The non-Vedic tribal hunter who settles in forests.",
        "vedantic": "The Niṣāda represents the lowest social outcast. Saluting the Lord as Niṣāda teaches the seeker that the Divine exists equally in the highest priest and the lowest outcast.",
        "nighantu": "Listed under synonyms for outcasts or forest-tribes (Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdravarga (2.10.22): 'niṣāda-śvapachāv ubhau'.",
        "abhidhana_ratnamala": "Classified under tribal foresters in Bhūmi-kāṇḍa."
    },
    "इषुकृत्": {
        "transliteration": "iṣukṛt",
        "root": "iṣu + √kṛ (to make arrows)",
        "base_devanagari": "इषुकृत्",
        "english_base_sg": "arrow-maker",
        "english_base_pl": "arrow-makers / arrow-manufacturers",
        "nirukta": "Compound of 'iṣu' (arrow) + √kṛ (to make). The craftsman who cuts, sharpens, and feathers arrows.",
        "vedantic": "The Lord as the arrow-maker, sharpening the intellect of the seeker to make it a fit instrument of concentration (Ekāgratā).",
        "nighantu": "Noted under weapon makers in Vedic glossaries.",
        "amara_kosha": "Listed in Śūdravarga under weapons craftsmen.",
        "abhidhana_ratnamala": "Classified under weapon craftsmen in Sāmānya-kāṇḍa."
    },
    "धन्वकृत्": {
        "transliteration": "dhanvakṛt",
        "root": "dhanvan + √kṛ (to make bows)",
        "base_devanagari": "धन्वकृत्",
        "english_base_sg": "bow-maker",
        "english_base_pl": "bow-makers / bow-manufacturers",
        "nirukta": "Compound of 'dhanvan' (bow) + √kṛ (to make). The craftsman who bends, strings, and tests bows.",
        "vedantic": "The Lord as the bow-maker, bending the rigid ego of the devotee and preparing them to launch the arrow of self-realization.",
        "nighantu": "Associated with weapon makers in Vedic texts.",
        "amara_kosha": "Listed in Śūdravarga under weapons craftsmen.",
        "abhidhana_ratnamala": "Classified under weapon craftsmen in Sāmānya-kāṇḍa."
    },
    "मृगयु": {
        "transliteration": "mṛgayu",
        "root": "mṛga + √yā (to seek/hunt animals)",
        "base_devanagari": "मृगयु",
        "english_base_sg": "hunter / seeker of beasts",
        "english_base_pl": "hunters / seekers of beasts",
        "nirukta": "From 'mṛga' (deer/wild beast) + √yā (या प्रापणे, Adādi-gaṇa, 2.0044) with 'un' suffix. One who seeks and tracks wild beasts.",
        "vedantic": "The Lord is the Hunter (Kirata). He tracks down the wild thoughts (deers) that run amok in the forest of the human mind.",
        "nighantu": "Listed under synonyms for hunter (lubdhaka-nāmāni, Nighaṇṭu).",
        "amara_kosha": "Listed in Śūdravarga (2.10.23): 'lubdhako mṛgayuḥ samaḥ'.",
        "abhidhana_ratnamala": "Classified in Sāmānya-kāṇḍa (2.86) as hunter (mṛgavyādha)."
    },
    "श्वनि": {
        "transliteration": "śvani",
        "root": "śvan + √nī (to lead dogs)",
        "base_devanagari": "श्वनि",
        "english_base_sg": "dog-keeper / dog-leader",
        "english_base_pl": "dog-keepers / those who lead dogs",
        "nirukta": "From 'śvan' (dog) + √nī (to lead). One who leads dogs on leash, typically for hunting or guarding.",
        "vedantic": "The Lord as the keeper of dogs. Symbolizes that even the handlers of impure or lower animals are instruments of the Divine order.",
        "nighantu": "Associated with hunters or dog-keepers in Vedic glossaries.",
        "amara_kosha": "Listed in Śūdravarga under hunters and keepers.",
        "abhidhana_ratnamala": "Classified under hunters in Sāmānya-kāṇḍa."
    },
    "श्वन्": {
        "transliteration": "śvan",
        "root": "√śvi (to swell, grow, breathe fast)",
        "base_devanagari": "श्वन्",
        "english_base_sg": "dog",
        "english_base_pl": "dogs",
        "nirukta": "From √śvi (to swell/grow) + suffix 'kan'. Yāska defines śvan as that which breathes fast or grows quickly ('śvasanād vā', Nirukta).",
        "vedantic": "The dog is considered ritually impure in Vedic tradition. Saluting the Lord as the dog (svabhyah) shows that the highest divinity resides in what is socially deemed lowest.",
        "nighantu": "Noted under animal registers in Vedic texts.",
        "amara_kosha": "Listed in Śūdravarga (2.10.23): 'kuras-tuniḥ śvā bhṣakaḥ'.",
        "abhidhana_ratnamala": "Classified in Anekārtha-kāṇḍa (5.42) under dog names: 'śvā kuraḥ'."
    },
    "श्वपति": {
        "transliteration": "śvapati",
        "root": "śvan + pati (lord of dogs)",
        "base_devanagari": "श्वपति",
        "english_base_sg": "lord of dogs / outcaste handler",
        "english_base_pl": "lords of dogs",
        "nirukta": "Compound of 'śvan' (dog) + 'pati' (lord). He who keeps, feeds, or breeds dogs, representing the outcaste (Chandalas).",
        "vedantic": "The Lord as the master of dogs. Points to the unity of all life, teaching the seeker to recognize the Lord in both the dog and the handler.",
        "nighantu": "Not listed in Nighaṇṭu.",
        "amara_kosha": "Listed in Śūdravarga as outcaste or dog-handler.",
        "abhidhana_ratnamala": "Classified under outcaste names in Bhūmi-kāṇḍa."
    }
}

# Add minor sandhi matches and plural variations
LEMMA_MAPPING = {
    "नमः": "नमः", "नमो": "नमः", "नमस्ते": "नमः", "नम": "नमः", "नमस्": "नमः",
    "सहमानाय": "सहमान",
    "निव्याधिने": "निव्याधिन्", "निव्याधिन": "निव्याधिन्",
    "आव्याधिनीनाम्": "आव्याधिनी", "आव्याधिनीभ्यः": "आव्याधिनी", "आव्याधिनीभ्यो": "आव्याधिनी",
    "पतये": "पति", "पतिभ्यः": "पति", "पतिभ्यो": "पति", "पतिभ्यश्च": "पति",
    "ककुभाय": "ककुभ",
    "निषङ्गिणे": "निषङ्गिन्", "निषङ्गिण": "निषङ्गिन्",
    "स्तेनानाम्": "स्तेन",
    "इषुधिमते": "इषुधिमत्",
    "तस्कराणाम्": "तस्कर",
    "वञ्चते": "वञ्चत्",
    "परिवञ्चते": "परिवञ्चत्",
    "स्तायूनाम्": "स्तायु",
    "निचेरवे": "निचेरु",
    "परिचराय": "परिचर",
    "अरण्यानाम्": "अरण्य", "अरण्याणाम्": "अरण्य",
    "सृकाविभ्यः": "सृकाविन्", "सृकाविभ्यो": "सृकाविन्",
    "जिघांसद्भ्यः": "जिघांसत्", "जिघांसद्भ्यो": "जिघांसत्",
    "मुष्णताम्": "मुष्णत्",
    "असिमद्भ्यः": "असिमत्", "असिमद्भ्यो": "असिमत्",
    "नक्तञ्चरद्भ्यः": "नक्तञ्चरत्", "नक्तञ्चरद्भ्यो": "नक्तञ्चरत्",
    "प्रकृन्तानाम्": "प्रकृन्त",
    "उष्णीषिणे": "उष्णीषिन्",
    "गिरिचराय": "गिरिचर",
    "कुलुञ्चानाम्": "कुलुञ्च",
    "इषुमद्भ्यः": "इषुमत्", "इषुमद्भ्यो": "इषुमत्",
    "धन्वाविभ्यः": "धन्वाविन्", "धन्वाविभ्यो": "धन्वाविन्",
    "च": "च", "च॒": "च",
    "वः": "युष्मद्", "वः॒": "युष्मद्",
    "आतन्वानेभ्यः": "आतन्वान", "आतन्वानेभ्यो": "आतन्वान",
    "प्रतिदधानेभ्यः": "प्रतिदधान", "प्रतिदधानेभ्यो": "प्रतिदधान",
    "आयच्छद्भ्यः": "आयच्छत्", "आयच्छद्भ्यो": "आयच्छत्",
    "विसृजद्भ्यः": "विसृजत्", "विसृजद्भ्यो": "विसृजत्", "विसृजञ्ज्यञ्च": "विसृजत्",
    "अस्यद्भ्यः": "अस्यत्", "अस्यद्भ्यो": "अस्यत्",
    "विध्यद्भ्यः": "विध्यत्", "विध्यद्भ्यो": "विध्यत्",
    "आसीनेभ्यः": "आसीन", "आसीनेभ्यो": "आसीन",
    "शयानेभ्यः": "शयान", "शयानेभ्यो": "शयान",
    "स्वपद्भ्यः": "स्वपत्", "स्वपद्भ्यो": "स्वपत्",
    "जाग्रद्भ्यः": "जाग्रत्", "जाग्रद्भ्यो": "जाग्रत्",
    "तिष्ठद्भ्यः": "तिष्ठत्", "तिष्ठद्भ्यो": "तिष्ठत्",
    "धावद्भ्यः": "धावत्", "धावद्भ्यो": "धावत्",
    "सभाभ्यः": "सभा", "सभाभ्यो": "सभा",
    "सभापतिभ्यः": "सभापति", "सभापतिभ्यो": "सभापति", "सभापतिभ्यश्च": "सभापति",
    "अश्वेभ्यः": "अश्व", "अश्वेभ्यो": "अश्व",
    "अश्वपतिभ्यः": "अश्वपति", "अश्वपतिभ्यो": "अश्वपति", "अश्वपतिभ्यश्च": "अश्वपति",
    "विविध्यन्तीभ्यः": "विविध्यन्ती", "विविध्यन्तीभ्यो": "विविध्यन्ती",
    "उगणाभ्यः": "उगणा", "उगणाभ्यो": "उगणा",
    "तृंहतीभ्यः": "तृंहती", "तृंहतीभ्यो": "तृंहती", "तृग्ं-हतीभ्यश्च": "तृंहती",
    "गृत्सेभ्यः": "गृत्स", "गृत्सेभ्यो": "गृत्स",
    "गृत्सपतिभ्यः": "गृत्सपति", "गृत्सपतिभ्यो": "गृत्सपति", "गृत्सपतिभ्यश्च": "गृत्सपति",
    "व्रातेभ्यः": "व्रात", "व्रातेभ्यो": "व्रात",
    "व्रातपतिभ्यः": "व्रातपति", "vव्रातपतिभ्यो": "व्रातपति", "व्रातपतिभ्यश्च": "व्रातपति",
    "गणेभ्यः": "गण", "गणेभ्यो": "गण",
    "गणपतिभ्यः": "गणपति", "गणपतिभ्यो": "गणपति", "गणपतिभ्यश्च": "गणपति",
    "विरूपेभ्यः": "विरूप", "विरूपेभ्यो": "विरूप", "विरूपेभ्यश्च": "विरूप",
    "विश्वरूपेभ्यः": "विश्वरूप", "विश्वरूपेभ्यो": "विश्वरूप", "विश्वरूपेभ्यश्च": "विश्वरूप",
    "महद्भ्यः": "महत्", "महद्भ्यो": "महत्",
    "क्षुल्लकेभ्यः": "क्षुल्लक", "क्षुल्लकेभ्यो": "क्षुल्लक",
    "रथिभ्यः": "रथिन्", "रथिभ्यो": "रथिन्",
    "अरथेभ्यः": "अरथ", "अरथेभ्यो": "अरथ",
    "रथेभ्यः": "रथ", "रथेभ्यो": "रथ",
    "रथपतिभ्यः": "रथपति", "रथपतिभ्यो": "रथपति", "रथपतिभ्यश्च": "रथपति",
    "सेनाभ्यः": "सेना", "सेनाभ्यो": "सेना",
    "सेनानिभ्यः": "सेनानी", "सेनानिभ्यो": "सेनानी", "सेनानिभ्यश्च": "सेनानी",
    "क्षत्तृभ्यः": "क्षत्तृ", "क्षत्तृभ्यो": "क्षत्तृ", "क्षत्तृभ्यश्च": "क्षत्तृ",
    "संग्रहीतृभ्यः": "संग्रहीतृ", "संग्रहीतृभ्यो": "संग्रहीतृ", "संग्रहीतृभ्यश्च": "संग्रहीतृ",
    "तक्षभ्यः": "तक्षन्", "तक्षभ्यो": "तक्षन्",
    "रथकारेभ्यः": "रथकार", "रथकारेभ्यो": "रथकार", "रथकारेभ्यश्च": "रथकार",
    "कुलालेभ्यः": "कुलाल", "कुलालेभ्यो": "कुलाल",
    "कर्मारेभ्यः": "कर्मार", "कर्मारेभ्यो": "कर्मार",
    "पुञ्जिष्ठेभ्यः": "पुञ्जिष्ठ", "पुञ्जिष्ठेभ्यो": "पुञ्जिष्ठ",
    "निषादेभ्यः": "निषाद", "निषादेभ्यो": "निषाद",
    "इषुकृद्भ्यः": "इषुकृत्", "इषुकृद्भ्यो": "इषुकृत्",
    "धन्वकृद्भ्यः": "धन्वकृत्", "धन्वकृद्भ्यो": "धन्वकृत्",
    "मृगयुभ्यः": "मृगयु", "मृगयुभ्यो": "मृगयु",
    "श्वनिभ्यः": "श्वनि", "श्वनिभ्यो": "श्वनि",
    "श्वभ्यः": "श्वन्", "श्वभ्यो": "श्वन्",
    "श्वपतिभ्यः": "श्वपति", "श्वपतिभ्यो": "श्वपति", "श्वपतिभ्यश्च": "श्वपति"
}

def clean_accents(text):
    if not text:
        return ""
    # Remove Vedic combining marks
    # U+0951 (udatta), U+0952 (anudatta), U+1CDC (svarita)
    # also remove spaces, pipes, hyphens for matching
    cleaned = re.sub(r'[\u0951\u0952\u1cdc]', '', text)
    cleaned = cleaned.replace("॒", "").replace("॑", "").replace("᳚", "").replace("ꣻ", "")
    return cleaned

def clean_for_match(text):
    cleaned = clean_accents(text)
    # Remove non-devanagari helper characters like hyphens, avagraha
    cleaned = cleaned.replace("-", "").replace("ऽ", "").strip()
    return cleaned

def get_inflected_grammar(pada_form, base_lemma, base_info):
    form_clean = clean_for_match(pada_form)
    devanagari = base_info["base_devanagari"]
    english_sg = base_info["english_base_sg"]
    english_pl = base_info["english_base_pl"]
    
    if form_clean.endswith("भ्यः") or form_clean.endswith("भ्यो") or form_clean.endswith("भ्यस्") or "भ्य" in form_clean:
        case_ending = "Dative Plural (Caturthī Vibhakti, Bahuvacana)"
        english = f"To the {english_pl}."
        panini = f"Derived from the nominal stem {devanagari} + the dative plural case-ending 'bhyas' (caturthī-bahuvacana) by 'Svaujasmauṭchasta...' (P. 4.1.2). By P. 8.2.7 (na-lopaḥ prātipadikāntasya) if stem ends in 'n', the 'n' is dropped before 'bhyas'. Governed by 'Namaḥ-svasti...' (P. 2.3.16) in relation to the word 'namaḥ'."
    elif form_clean.endswith("आनाम्") or form_clean.endswith("णाम्") or form_clean.endswith("ताम्") or form_clean.endswith("नाम्"):
        case_ending = "Genitive Plural (Ṣaṣṭhī Vibhakti, Bahuvacana)"
        english = f"Of the {english_pl}."
        panini = f"Derived from the nominal stem {devanagari} + the genitive plural case-ending 'ām' (ṣaṣṭhī-bahuvacana) by 'Svaujasmauṭchasta...' (P. 4.1.2). The augment 'nuṭ' is added by 'Hrasvanadyāpo nuṭ' (P. 7.1.54) and vowel is lengthened by 'Nāmi' (P. 6.4.3), yielding final form."
    elif form_clean.endswith("ाय"):
        case_ending = "Dative Singular (Caturthī Vibhakti, Ekavacana)"
        english = f"To the {english_sg}."
        panini = f"Derived from the nominal stem {devanagari} + the dative singular case-ending 'ṅe' (caturthī-ekavacana) by 'Svaujasmauṭchasta...' (P. 4.1.2). The 'ṅe' suffix is replaced by 'ya' after an 'a'-ending nominal stem by 'Geryaḥ' (P. 7.1.13), and the preceding 'a' is lengthened by 'Ato dīrgho yañi' (P. 7.3.101), yielding '{pada_form}'. Governed by 'Namaḥ-svasti...' (P. 2.3.16) in relation to 'namaḥ'."
    elif form_clean.endswith("े") or form_clean.endswith("ये"):
        case_ending = "Dative Singular (Caturthī Vibhakti, Ekavacana)"
        english = f"To the {english_sg}."
        panini = f"Derived from the nominal stem {devanagari} + the dative singular case-ending 'ṅe' (caturthī-ekavacana) by 'Svaujasmauṭchasta...' (P. 4.1.2). For '-in', '-i', '-u' or consonant stems, appropriate guna or sandhi rules apply. Governed by 'Namaḥ-svasti...' (P. 2.3.16) in relation to 'namaḥ'."
    elif base_lemma == "नमः":
        case_ending = "Avyaya (indeclinable nominal form/noun)"
        english = "Salutations / Bowing down / Reverence."
        panini = "Derived from the verbal root √nam (नमुँ प्रह्वत्वे शब्दे च, Bhvādi-gaṇa, 1.1030) with the suffix 'asun' (असुन्) by Uṇādi 4.188. Governs the dative case (caturthī vibhakti) by 'Namaḥ-svasti...' (P. 2.3.16)."
    elif base_lemma == "च":
        case_ending = "Avyaya (indeclinable conjunction)"
        english = "And."
        panini = "Indeclinable particle (nipāta) functioning as a coordinator (samuccayārtha) by P. 1.4.57."
    elif base_lemma == "युष्मद्" or form_clean == "वः":
        case_ending = "Dative Plural (Caturthī Vibhakti, Bahuvacana)"
        english = "To you all."
        panini = "Enclitic/substituted form (ādeśa) of the second-person pronoun 'yuṣmad' (युष्मद्) in the dative plural by 'Bahuvacanasya vas-nasau' (P. 8.1.21)."
    else:
        case_ending = "Nominal Form"
        english = f"{english_sg}"
        panini = f"Derived from stem {devanagari} with standard declension."

    return case_ending, english, panini

def process_anuvakam(anuvaka_data):
    anuvaka_id = anuvaka_data["id"]
    print(f"Processing Anuvaka {anuvaka_id}...")
    
    # Target directory
    output_dir = f"/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam{anuvaka_id}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Store list of commentaries for propagation
    # In correlated_namakam.json, commentaries are consolidated under specific mantras.
    # We will first collect all commentaries, then associate them properly.
    all_commentaries = []
    
    for idx, m in enumerate(anuvaka_data["mantras"]):
        m_id = m["id"]
        samhita = m["sanskrit"]["samhita"]
        pada = m["sanskrit"]["pada"]
        krama = m["sanskrit"]["krama"]
        
        # Split pada into words
        # e.g. "नमः॑ । सह॑मानाय ।" -> ["नमः॑", "सह॑मानाय"]
        # Skip separators like "।", "॥", "इति" if they stand alone
        pada_parts = [p.strip() for p in pada.split(" । ") if p.strip()]
        if pada_parts and pada_parts[-1].endswith(" ॥"):
            pada_parts[-1] = pada_parts[-1][:-2].strip()
        
        words = []
        word_id = 1
        
        # We will build the words array
        # First we resolve sandhi to match our base lemmas
        for p in pada_parts:
            # Check if there is an "इति" in the token (e.g. "उ॒तो इति॑")
            # If so, the word is before "इति"
            subparts = p.split(" इति")
            p_word = subparts[0].strip()
            
            clean_w = clean_accents(p_word)
            # Find base lemma
            lemma = None
            for k in [clean_w, clean_for_match(clean_w), p_word, clean_accents(p)]:
                if k in LEMMA_MAPPING:
                    lemma = LEMMA_MAPPING[k]
                    break
            
            if not lemma:
                # Try fallback by stripping hyphens and accents
                stripped = clean_for_match(p_word)
                for k in LEMMA_MAPPING:
                    if clean_for_match(k) == stripped:
                        lemma = LEMMA_MAPPING[k]
                        break
            
            if not lemma:
                # Hardcoded fallbacks for any leftovers
                print(f"Warning: Lemma not found for '{p_word}' (pada: {p})")
                lemma = "नमः"  # fallback
            
            base_info = BASE_WORDS[lemma]
            case_ending, english_inflected, panini_rules = get_inflected_grammar(p_word, lemma, base_info)
            
            # Estimate samhita span by simple substring searching in samhita
            # Note: in Sanskrit, sandhi changes the word forms, so we look for clean match
            start_idx = 0
            end_idx = 0
            # Clean samhita for matching
            clean_sam = clean_accents(samhita)
            clean_word_match = clean_accents(p_word).replace("-", "")
            
            # Simple heuristic: find the clean_word_match or part of it in clean_sam
            # We can also do a sliding window search
            best_match_idx = -1
            best_len = 0
            for i in range(len(clean_sam)):
                for j in range(i+2, len(clean_sam)+1):
                    sub = clean_sam[i:j]
                    if sub in clean_word_match or clean_word_match in sub or (sub[:3] == clean_word_match[:3] and len(sub) > 2):
                        if (j - i) > best_len:
                            best_len = j - i
                            best_match_idx = i
            
            if best_match_idx != -1:
                start_idx = best_match_idx
                end_idx = best_match_idx + best_len
            
            word_obj = {
                "id": word_id,
                "pada_form": p_word,
                "samhita_span": {
                    "start": start_idx,
                    "end": end_idx,
                    "text": samhita[start_idx:end_idx] if end_idx > start_idx else p_word
                },
                "meanings": {
                    "english": english_inflected,
                    "nirukta": base_info["nirukta"],
                    "vedantic": base_info["vedantic"]
                },
                "grammatical_references": {
                    "panini": panini_rules,
                    "case_ending": case_ending
                },
                "lexicographical_references": {
                    "nighantu": base_info["nighantu"],
                    "amara_kosha": base_info["amara_kosha"],
                    "abhidhana_ratnamala": base_info["abhidhana_ratnamala"]
                }
            }
            words.append(word_obj)
            word_id += 1
            
        # Tokenize samhita stream
        # Split by spaces and punctuation, keeping track of indices and word mappings
        sam_tokens = []
        # We can split samhita by spaces and keep them as tokens
        # e.g. "नम॒: सह॑मानाय निव्या॒धिन॑"
        sam_parts = re.split(r'(\s+|-|।|॥)', samhita)
        current_w_id = 1
        for part in sam_parts:
            if not part:
                continue
            
            # Determine word_ids
            w_ids = []
            clean_part = clean_for_match(part)
            if clean_part and clean_part not in ['।', '॥', ':', '']:
                # Find which word in our words list matches this token
                # In many cases, it matches the current_w_id
                if current_w_id <= len(words):
                    w_ids = [current_w_id]
                    # Check if this token is a sandhi combination of multiple words
                    # e.g. "आव्या॒धिनी॑ना॒-म्पत॑ये॒" -> आव्याधिनीनाम् (current) + पतये (next)
                    if current_w_id + 1 <= len(words):
                        next_w_clean = clean_for_match(words[current_w_id]["pada_form"])
                        if next_w_clean in clean_part or clean_part.endswith("म्पतये"):
                            w_ids.append(current_w_id + 1)
                            current_w_id += 1
                    current_w_id += 1
            
            sam_tokens.append({
                "text": part,
                "word_ids": w_ids
            })
            
        # Tokenize pada stream
        pada_tokens = []
        pada_parts_raw = re.split(r'(\s*।\s*|\s*॥\s*|\s+)', pada)
        current_w_id = 1
        for part in pada_parts_raw:
            if not part:
                continue
            w_ids = []
            clean_part = clean_for_match(part)
            if clean_part and clean_part not in ['।', '॥', '', 'इति']:
                if current_w_id <= len(words):
                    w_ids = [current_w_id]
                    current_w_id += 1
            elif 'इति' in part:
                # "इति" is combined with previous word, e.g. "उ॒तो इति॑"
                # so it maps to the previous word
                if current_w_id - 1 > 0:
                    w_ids = [current_w_id - 1]
            
            pada_tokens.append({
                "text": part,
                "word_ids": w_ids
            })
            
        # Tokenize krama stream
        krama_tokens = []
        krama_parts = re.split(r'(\s*।\s*|\s*॥\s*)', krama)
        # In krama, each block contains two words, e.g. "नमः॑ सह॑मानाय"
        # We need to map them to the correct word IDs in the words list
        # Let's keep a pointer to the current word ID
        # Krama lists words as: 1-2, 2-3, 3-4, etc.
        # So we can match them sequentially!
        current_krama_w_id = 1
        for part in krama_parts:
            if not part:
                continue
            w_ids = []
            clean_part = clean_for_match(part)
            if clean_part and clean_part not in ['।', '॥', '']:
                # Split the block into individual words
                sub_words = [sw.strip() for sw in part.split() if sw.strip()]
                for sw in sub_words:
                    clean_sw = clean_for_match(sw)
                    if clean_sw == 'इति':
                        continue
                    # Find a matching word in the vicinity of current_krama_w_id
                    matched = False
                    for offset in [-1, 0, 1, 2]:
                        check_id = current_krama_w_id + offset
                        if 1 <= check_id <= len(words):
                            check_word_clean = clean_for_match(words[check_id - 1]["pada_form"])
                            if clean_sw == check_word_clean or clean_sw in check_word_clean or check_word_clean in clean_sw:
                                if check_id not in w_ids:
                                    w_ids.append(check_id)
                                matched = True
                    # If not matched, just use the current index
                    if not matched and current_krama_w_id <= len(words):
                        w_ids.append(current_krama_w_id)
                # Advance pointer if we completed a pair
                if len(w_ids) >= 2:
                    current_krama_w_id = min(w_ids) + 1
            krama_tokens.append({
                "text": part,
                "word_ids": w_ids
            })
            
        # Extract commentaries from correlated_namakam.json
        translations = m.get("translations", {})
        comm_sans = m.get("commentaries_sanskrit", {})
        
        # Build commentaries object
        commentary_obj = {
            "sayana": {
                "rishi": "Manduka" if anuvaka_id == 2 else ("Sri Rudra" if anuvaka_id == 3 else "Sri Rudra"),
                "chandas": "Maha-Gayatri" if anuvaka_id == 2 else ("Brihati" if anuvaka_id == 3 else "Anushtup"),
                "devata": "Rudra",
                "sanskrit": "",
                "english": translations.get("sayana", "")
            },
            "bhatta_bhaskara": {
                "rishi": "Manduka" if anuvaka_id == 2 else ("Sri Rudra" if anuvaka_id == 3 else "Sri Rudra"),
                "chandas": "Maha-Gayatri" if anuvaka_id == 2 else ("Brihati" if anuvaka_id == 3 else "Anushtup"),
                "devata": "Rudra",
                "sanskrit": "",
                "english": translations.get("bhatta_bhaskara", "")
            },
            "abhinava_shankara": {
                "rishi": "Atreya" if anuvaka_id == 3 and m_id == 1 else ("Sri Rudra" if anuvaka_id == 3 else "Sri Rudra"),
                "chandas": "Anushtup" if anuvaka_id == 3 and m_id == 1 else ("Brihati" if anuvaka_id == 3 else "Anushtup"),
                "devata": "Shambhu" if anuvaka_id == 3 and m_id == 1 else "Sri Rudra",
                "sanskrit": comm_sans.get("abhinava_shankara", ""),
                "english": translations.get("abhinava_shankara", "")
            }
        }
        
        # Save temp info to resolve empty groupings later
        all_commentaries.append({
            "id": m_id,
            "words": words,
            "samhita": samhita,
            "pada": pada,
            "krama": krama,
            "samhita_tokens": sam_tokens,
            "pada_tokens": pada_tokens,
            "krama_tokens": krama_tokens,
            "commentaries": commentary_obj
        })

    # Propagate consolidated commentaries
    # If a mantra has empty commentaries, we copy the non-empty consolidated ones from nearby mantras in the group.
    # Group mappings for Anuvakam 3:
    # - Mantras 1, 2, 3 are commented on together. Consolidated in Mantra 2.
    # - Mantras 4, 5 are commented on together. Consolidated in Mantra 5.
    # - Mantras 6, 7, 8 are commented on together. Consolidated in Mantra 6.
    # - Mantras 9 to 16 are commented on together. Consolidated in Mantra 11 or 14.
    # Group mappings for Anuvakam 4:
    # - Mantras 8 through 16 are commented on together. Consolidated in Mantra 1.
    
    if anuvaka_id == 3:
        # Group 1: 1, 2, 3
        # Sanskrit is in Mantra 2, Sāyana English is in Mantra 2/3, Abhinava English is in Mantra 2/3 (which has Mantra 4 text? Wait, we will use it)
        g1_sayana_eng = all_commentaries[1]["commentaries"]["sayana"]["english"] or all_commentaries[2]["commentaries"]["sayana"]["english"]
        g1_bhatta_eng = all_commentaries[1]["commentaries"]["bhatta_bhaskara"]["english"] or all_commentaries[2]["commentaries"]["bhatta_bhaskara"]["english"]
        g1_abhinava_eng = all_commentaries[1]["commentaries"]["abhinava_shankara"]["english"] or all_commentaries[2]["commentaries"]["abhinava_shankara"]["english"]
        g1_abhinava_sans = all_commentaries[1]["commentaries"]["abhinava_shankara"]["sanskrit"]
        
        for idx in [0, 1, 2]:
            if not all_commentaries[idx]["commentaries"]["sayana"]["english"]:
                all_commentaries[idx]["commentaries"]["sayana"]["english"] = g1_sayana_eng
            if not all_commentaries[idx]["commentaries"]["bhatta_bhaskara"]["english"]:
                all_commentaries[idx]["commentaries"]["bhatta_bhaskara"]["english"] = g1_bhatta_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"] = g1_abhinava_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"] = g1_abhinava_sans
                
        # Group 2: 4, 5
        g2_sayana_eng = all_commentaries[3]["commentaries"]["sayana"]["english"] or all_commentaries[4]["commentaries"]["sayana"]["english"]
        g2_abhinava_eng = all_commentaries[4]["commentaries"]["abhinava_shankara"]["english"] or all_commentaries[3]["commentaries"]["abhinava_shankara"]["english"]
        g2_abhinava_sans = all_commentaries[4]["commentaries"]["abhinava_shankara"]["sanskrit"]
        
        for idx in [3, 4]:
            if not all_commentaries[idx]["commentaries"]["sayana"]["english"]:
                all_commentaries[idx]["commentaries"]["sayana"]["english"] = g2_sayana_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"] = g2_abhinava_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"] = g2_abhinava_sans

        # Group 3: 6, 7, 8
        g3_sayana_eng = all_commentaries[5]["commentaries"]["sayana"]["english"]
        g3_abhinava_eng = all_commentaries[5]["commentaries"]["abhinava_shankara"]["english"]
        g3_abhinava_sans = all_commentaries[5]["commentaries"]["abhinava_shankara"]["sanskrit"]
        
        for idx in [5, 6, 7]:
            if not all_commentaries[idx]["commentaries"]["sayana"]["english"]:
                all_commentaries[idx]["commentaries"]["sayana"]["english"] = g3_sayana_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"] = g3_abhinava_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"] = g3_abhinava_sans

        # Group 4: 9 to 16
        g4_sayana_eng = all_commentaries[12]["commentaries"]["sayana"]["english"] or all_commentaries[15]["commentaries"]["sayana"]["english"]
        g4_abhinava_eng = all_commentaries[10]["commentaries"]["abhinava_shankara"]["english"] or all_commentaries[13]["commentaries"]["abhinava_shankara"]["english"]
        g4_abhinava_sans = all_commentaries[10]["commentaries"]["abhinava_shankara"]["sanskrit"] or all_commentaries[13]["commentaries"]["abhinava_shankara"]["sanskrit"]
        
        for idx in range(8, 16):
            if not all_commentaries[idx]["commentaries"]["sayana"]["english"]:
                all_commentaries[idx]["commentaries"]["sayana"]["english"] = g4_sayana_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"] = g4_abhinava_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"] = g4_abhinava_sans

    elif anuvaka_id == 4:
        # For Anuvakam 4, commentaries are consolidated in Mantra 1
        g_sayana_eng = all_commentaries[0]["commentaries"]["sayana"]["english"]
        g_abhinava_eng = all_commentaries[0]["commentaries"]["abhinava_shankara"]["english"]
        g_abhinava_sans = all_commentaries[0]["commentaries"]["abhinava_shankara"]["sanskrit"]
        
        # Propagate to all mantras if empty
        for idx in range(len(all_commentaries)):
            if not all_commentaries[idx]["commentaries"]["sayana"]["english"]:
                all_commentaries[idx]["commentaries"]["sayana"]["english"] = g_sayana_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["english"] = g_abhinava_eng
            if not all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"]:
                all_commentaries[idx]["commentaries"]["abhinava_shankara"]["sanskrit"] = g_abhinava_sans

    # Save to files
    for m in all_commentaries:
        filename = f"{output_dir}/mantra{m['id']}.json"
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(m, outfile, ensure_ascii=False, indent=2)
        print(f"  Saved {filename}")

def main():
    # Load correlated_namakam.json
    with open('/Users/Rkanadam/personal/namakam/src/correlated_namakam.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    anuvakas = data.get("anuvakas", [])
    
    for a in anuvakas:
        a_id = a.get("id")
        if a_id in [3, 4]:
            process_anuvakam(a)
            
    print("\nProcessing complete! All JSON files written successfully.")

if __name__ == "__main__":
    main()
