import json
import os
import re

CORRELATED_PATH = "/Users/Rkanadam/personal/namakam/src/correlated_namakam.json"
OUTPUT_DIR_TEMPLATE = "/Users/Rkanadam/personal/namakam/src/assets/word_analysis/anuvakam{}"

# Dictionary database containing the lexicographical, grammatical, and etymological data
# for unique stems in Anuvakams 9, 10, and 11.
STEM_DATABASE = {
    # Anuvakam 9 stems
    "namas": {
        "english": "Salutations / Bowing down / Reverence.",
        "nirukta": "Derived from the root 'nam' (नम्) meaning 'to bow, bend, or submit'. In Nirukta, 'namas' is defined in the sense of bowing or honoring.",
        "vedantic": "Represents the dissolution of ego ('Na' = not, 'mama' = mine). It is the surrender of the individual self into the supreme, cosmic self.",
        "panini": "Derived from root √nam (Bhvādi-gaṇa, 1.1030) with the suffix 'asun'. Governs the dative case by 'Namaḥ-svasti-svāhā...' (P.2.3.16).",
        "case_ending": "Avyaya (indeclinable nominal).",
        "nighantu": "Listed under water synonyms (Nighaṇṭu 1.12) and food synonyms (Nighaṇṭu 2.7).",
        "amara_kosha": "Avyayavarga (3.4.19): Namas denotes bowing/reverence.",
        "abhidhana_ratnamala": "Anekārtha-kāṇḍa (5.26): Denotes bowing or salutation."
    },
    "ca": {
        "english": "And / Also.",
        "nirukta": "A particle used for conjunction, linking multiple names or attributes.",
        "vedantic": "Emphasizes the non-dual and all-inclusive nature of Shiva; He is present in both opposites, joined by 'ca'.",
        "panini": "Avyaya (indeclinable particle) classified under the Cādi-gaṇa.",
        "case_ending": "Avyaya (conjunction).",
        "nighantu": "Not classified.",
        "amara_kosha": "Avyayavarga (3.4): Conjunction/particle.",
        "abhidhana_ratnamala": "Avyayas (5): Particle of conjunction."
    },
    "iriṇya": {
        "english": "To the one dwelling in barren/salty land.",
        "nirukta": "iriṇa + yat. irinamūṣaram, tatra bhavaḥ irinyaḥ (dwelling in barren or salty soil).",
        "vedantic": "Represents the Lord's presence even in barren, non-productive aspects of the universe, showing that no place is devoid of His divinity.",
        "panini": "Stem 'iriṇya' formed with yat-pratyaya (P.4.3.53) on 'iriṇa'. Dative singular case suffix 'ṅe' replaced by 'yā' by 'ṅerinyā...' (P.7.1.13).",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Listed under names of waste/dry land.",
        "amara_kosha": "Bhūmivarga (2.1.5): 'mridviśeṣāveūṣaro'nya iriṇam' (barren land).",
        "abhidhana_ratnamala": "Bhūmi-kāṇḍa (2.12): Synonym for saline or barren land."
    },
    "prapathya": {
        "english": "To the one who is in the main highway / well-trodden path.",
        "nirukta": "prapatha + yat. prapathe bhavaḥ prapathyaḥ (situated in the main path).",
        "vedantic": "Symbolizes the Lord as the guide on the royal road of spiritual progress (the path of knowledge or devotion).",
        "panini": "Prefix 'pra' + noun 'pathin' with suffix 'yat' (P.4.3.53). Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Listed under path synonyms.",
        "amara_kosha": "Bhūmivarga: 'mārga' / 'prapatha' / 'pathin'.",
        "abhidhana_ratnamala": "Under road/path synonyms."
    },
    "kiṃśila": {
        "english": "To the one in the gravelly / stony land.",
        "nirukta": "kutsitāḥ śilāḥ yatra (where there are small, gravelly stones).",
        "vedantic": "Indicates that even in rough, uncomfortable, and small elements of existence, the divine essence resides.",
        "panini": "Compound of 'kim' (vile/small) + 'śilā' (stone) with dative ending 'yāya'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not explicitly listed.",
        "amara_kosha": "Stony land synonyms.",
        "abhidhana_ratnamala": "Stony land synonyms."
    },
    "kṣayaṇa": {
        "english": "To the one in the habitable place / dwelling.",
        "nirukta": "Derived from root 'kṣi' meaning to dwell or reside.",
        "vedantic": "The Lord is the ultimate resting place or abode of all living beings during dissolution.",
        "panini": "Root √kṣi (Adādi-gaṇa, 2.0003) + 'lyuṭ' suffix (P.3.3.115) in the sense of location.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Listed under house synonyms.",
        "amara_kosha": "Gṛhavarga (2.2.1): 'gṛha' / 'geha' / 'kṣaya' / 'niketana'.",
        "abhidhana_ratnamala": "Under dwelling synonyms."
    },
    "kapardin": {
        "english": "To the one with matted hair.",
        "nirukta": "kaparda (matted hair/crown) + ini (possession).",
        "vedantic": "The matted hair represents the cosmic grid of energy, and the holding of the River Ganga, symbolizing containment of cosmic forces.",
        "panini": "Noun 'kaparda' + suffix 'ini' (P.5.2.115). Dative singular form is 'kapardine'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Listed under Shiva's attributes.",
        "amara_kosha": "Svargavarga (1.1.30): 'kapardī sthāṇurīśaḥ'.",
        "abhidhana_ratnamala": "Svarga-kāṇḍa (1.30-33): Shiva's synonym."
    },
    "pulasti": {
        "english": "To the one standing in front / having straight hair.",
        "nirukta": "Derived from 'puras' (in front) + root 'as' (to be). He who reveals Himself directly to His devotees.",
        "vedantic": "The ever-present consciousness that stands before everyone as the inner witness.",
        "panini": "Uṇādi-derived noun. Dative singular form is 'pulastaye' by 'gherṅiti' (P.7.3.111).",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Listed under sage names or Shiva's attendants.",
        "abhidhana_ratnamala": "Shiva's attendant names."
    },
    "gōṣṭhya": {
        "english": "To the one situated in the cowshed.",
        "nirukta": "gōṣṭha + yat. gōṣṭhe bhavaḥ gōṣṭhyaḥ.",
        "vedantic": "Represents the divine presiding over domestic and nurturing spaces, animal shelters, and cattle.",
        "panini": "Noun 'gōṣṭha' (P.8.3.97) + 'yat' suffix (P.4.3.53) for location.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Cowshed synonyms.",
        "amara_kosha": "Cowshed synonyms.",
        "abhidhana_ratnamala": "Cattle-fold synonyms."
    },
    "gṛhya": {
        "english": "To the one situated in the house.",
        "nirukta": "gṛha + yat. gṛhe bhavaḥ gṛhyaḥ.",
        "vedantic": "Represents the Lord as the inner deity of every home, the guardian of the household.",
        "panini": "Noun 'gṛha' + 'yat' suffix (P.4.3.53) indicating location.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "House synonyms.",
        "amara_kosha": "Gṛhavarga: Dwelling synonyms.",
        "abhidhana_ratnamala": "Under house synonyms."
    },
    "talpya": {
        "english": "To the one situated on the couch/bed.",
        "nirukta": "talpa + yat. talpe bhavaḥ talpyaḥ.",
        "vedantic": "The Lord is present in states of rest and sleep, presiding over the state of deep sleep (Suṣupti).",
        "panini": "Noun 'talpa' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Bed/couch synonyms.",
        "amara_kosha": "Bedding/couch synonyms.",
        "abhidhana_ratnamala": "Bed synonyms."
    },
    "gēhya": {
        "english": "To the one situated in the palace/mansion.",
        "nirukta": "geha + yat. gehe bhavaḥ gehyaḥ.",
        "vedantic": "Present in grand buildings and temples; He occupies both humble homes (gṛha) and grand mansions (geha).",
        "panini": "Noun 'geha' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Dwelling synonyms.",
        "amara_kosha": "Palace/mansion synonyms.",
        "abhidhana_ratnamala": "Mansion synonyms."
    },
    "kāṭya": {
        "english": "To the one situated in the dense forest/well.",
        "nirukta": "kāṭa + yat. kāṭe (impenetrable forest or well) bhavaḥ kāṭyaḥ.",
        "vedantic": "The Lord is present in difficult, hidden, and inaccessible places, representing the depths of the subconscious.",
        "panini": "Noun 'kāṭa' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Well/impenetrable forest synonyms.",
        "abhidhana_ratnamala": "Forest/pit synonyms."
    },
    "gahvarēṣṭha": {
        "english": "To the one dwelling in caves/impenetrable clefts.",
        "nirukta": "gahvare tiṣṭhati iti gahvareṣṭhaḥ.",
        "vedantic": "He who resides in the cave of the heart (hṛdaya-guhā) as the ultimate witness.",
        "panini": "Locative compound: 'gahvare' + root √sthā + 'ka' suffix. 'ṣ' substitution by 'ādeśapratyayayoḥ' (P.8.3.59).",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Under cave/depth synonyms.",
        "amara_kosha": "Cave synonyms.",
        "abhidhana_ratnamala": "Cave/mountain synonyms."
    },
    "hṛdayya": {
        "english": "To the one situated in deep pools/heart.",
        "nirukta": "hṛda (deep pool) + yat. hṛde bhavaḥ hṛdayyaḥ.",
        "vedantic": "Presiding over deep waters, representing the coolness of divine grace, and the depth of the heart.",
        "panini": "Noun 'hṛda' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Water synonyms.",
        "amara_kosha": "Pool/water synonyms.",
        "abhidhana_ratnamala": "Water synonyms."
    },
    "nivēṣpya": {
        "english": "To the one situated in dewdrops/mist/snow.",
        "nirukta": "nivēṣpa (mist/fog/dew) + yat. niveṣpe bhavaḥ niveṣpyaḥ.",
        "vedantic": "The Lord is present in transient and subtle elements like dew, representing the impermanence of creation.",
        "panini": "Noun 'niveṣpa' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Water/dew synonyms.",
        "amara_kosha": "Dew/fog synonyms.",
        "abhidhana_ratnamala": "Snow/mist synonyms."
    },
    "pāṃsavya": {
        "english": "To the one situated in the fine dust/particles.",
        "nirukta": "pāṃsu (dust/atom) + yat. pāṃsuṣu bhavaḥ pāṃsavyaḥ.",
        "vedantic": "Divinity is present at the atomic and subatomic level, in every speck of dust.",
        "panini": "Noun 'pāṃsu' + 'yat' suffix (P.4.3.53). Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Dust synonyms.",
        "amara_kosha": "Dust synonyms.",
        "abhidhana_ratnamala": "Soil/dust synonyms."
    },
    "rajasya": {
        "english": "To the one situated in visible dust/clouds.",
        "nirukta": "rajas (dust/sky/passion) + yat. rajasi bhavaḥ rajasyaḥ.",
        "vedantic": "Presides over the active, passionate quality of nature (Rajas) and the atmosphere.",
        "panini": "Noun 'rajas' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Dust/atmosphere synonyms.",
        "amara_kosha": "Dust/atmosphere synonyms.",
        "abhidhana_ratnamala": "Sky/dust synonyms."
    },
    "śuṣkya": {
        "english": "To the one situated in dry wood/vegetation.",
        "nirukta": "śuṣka + yat. śuṣke bhavaḥ śuṣkyaḥ.",
        "vedantic": "The Lord is present in dry, dead, or decaying matter, showing His role as the destroyer/recycler of life.",
        "panini": "Noun 'śuṣka' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Dry wood synonyms.",
        "amara_kosha": "Forest/wood synonyms.",
        "abhidhana_ratnamala": "Dry vegetation synonyms."
    },
    "haritya": {
        "english": "To the one situated in green wood/fresh plants.",
        "nirukta": "harita + yat. harite bhavaḥ harityaḥ.",
        "vedantic": "The Lord is present in vibrant, living, green foliage and fresh life, representing growth.",
        "panini": "Noun 'harita' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Green vegetation synonyms.",
        "amara_kosha": "Greenery synonyms.",
        "abhidhana_ratnamala": "Fresh leaf synonyms."
    },
    "lōpya": {
        "english": "To the one situated in hard/uneven ground or paths.",
        "nirukta": "lōpa (broken path/rough ground) + yat. lope bhavaḥ lopyaḥ.",
        "vedantic": "Divinity exists in rough terrains and challenging circumstances.",
        "panini": "Noun 'lōpa' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Rough ground synonyms.",
        "amara_kosha": "Uneven paths synonyms.",
        "abhidhana_ratnamala": "Stony terrain synonyms."
    },
    "ulapya": {
        "english": "To the one situated in wild grass/shrubs.",
        "nirukta": "ulapa (shrub/creeper/grass) + yat. ulape bhavaḥ ulapyaḥ.",
        "vedantic": "Present in tiny creepers and wild grasses, representing the humility of nature.",
        "panini": "Noun 'ulapa' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Grass synonyms.",
        "amara_kosha": "Grass/shrub synonyms.",
        "abhidhana_ratnamala": "Grass synonyms."
    },
    "ūrvya": {
        "english": "To the one situated on the earth.",
        "nirukta": "urvī (earth) + yat. urvyāṃ bhavaḥ ūrvyaḥ.",
        "vedantic": "The Lord is the support of the earth, manifesting as the terrestrial realm.",
        "panini": "Noun 'urvī' + 'yat' suffix with Vedic lengthening. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Earth synonyms.",
        "amara_kosha": "Earth synonyms.",
        "abhidhana_ratnamala": "Earth synonyms."
    },
    "sūrmya": {
        "english": "To the one in the beautiful waves / hollow metal images.",
        "nirukta": "sūrmī (waves or metal image) + yat. sūrmyāṃ bhavaḥ sūrmyaḥ.",
        "vedantic": "The Lord is present in flowing waves and also inside hollow metal statues, showing He fills all forms.",
        "panini": "Noun 'sūrmī' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Wave/river synonyms.",
        "amara_kosha": "Wave/statue synonyms.",
        "abhidhana_ratnamala": "Metal image/wave synonyms."
    },
    "parṇya": {
        "english": "To the one in the leaves.",
        "nirukta": "parṇa + yat. parṇe bhavaḥ parṇyaḥ.",
        "vedantic": "The Lord is present in individual leaves, acting as the life force of flora.",
        "panini": "Noun 'parṇa' + 'yat' suffix. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Leaf synonyms.",
        "amara_kosha": "Leaf synonyms.",
        "abhidhana_ratnamala": "Leaf synonyms."
    },
    "parṇaśadya": {
        "english": "To the one in the leaf-heaps / dry leaves.",
        "nirukta": "parṇaśada (heap of dry leaves) + yat.",
        "vedantic": "Present in leaf-heaps, representing the cycle of decomposition and rejuvenation.",
        "panini": "Compound 'parṇaśada' + suffix 'yat'. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Heap of leaves synonyms.",
        "abhidhana_ratnamala": "Dry leaf synonyms."
    },
    "apaguramāṇa": {
        "english": "To the one raising weapons / brandishing.",
        "nirukta": "apa + gur (to raise/threaten) + śānac. he who threatens the sinners.",
        "vedantic": "The threatening posture of Rudra represents the warning signs of nature and karma, prompting righteousness.",
        "panini": "Prefix 'apa' + root √gur (udyamane) + middle participle suffix 'śānac' + dative ending.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Raising weapon synonyms.",
        "abhidhana_ratnamala": "Under weapons and anger."
    },
    "abhighnat": {
        "english": "To the one striking / killing.",
        "nirukta": "abhi + han + śatṛ. he who strikes directly.",
        "vedantic": "The destructive aspect of Rudra that kills the ego and destroys sins.",
        "panini": "Prefix 'abhi' + root √han + active participle 'śatṛ' + dative singular ending 'e'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Killing synonyms.",
        "amara_kosha": "Killing synonyms.",
        "abhidhana_ratnamala": "Striking/killing synonyms."
    },
    "ākkhidat": {
        "english": "To the one afflicting/harassing slightly.",
        "nirukta": "ā + khid (to vex/afflict) + śatṛ. he who causes mild pain.",
        "vedantic": "The minor obstacles and struggles in life are also His grace, helping to develop patience.",
        "panini": "Prefix 'ā' + root √khid + active participle 'śatṛ' with Vedic doubling 'kkh'. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Vexing/afflicting synonyms.",
        "abhidhana_ratnamala": "Pain/affliction synonyms."
    },
    "prakkhidat": {
        "english": "To the one afflicting/harassing severely.",
        "nirukta": "pra + khid + śatṛ. he who causes intense affliction.",
        "vedantic": "Severe trials and tribulations that lead to deep detachment and spiritual awakening.",
        "panini": "Prefix 'pra' + root √khid + participle 'śatṛ' with Vedic doubling. Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Intense affliction synonyms.",
        "abhidhana_ratnamala": "Pain synonyms."
    },
    "vas": {
        "english": "To you / Your (plural).",
        "nirukta": "Genitive/dative plural form of pronoun 'yushman'.",
        "vedantic": "Addressing the assembly of Rudras as the omnipresent Divine.",
        "panini": "Enclitic substitute 'vas' for 'yuşmabhyaḥ' (dative plural) by 'Vaso-mayav...' (P.8.1.21).",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronominal derivatives.",
        "abhidhana_ratnamala": "Pronominal enclitics."
    },
    "kirika": {
        "english": "To the ones who shower wealth/grace or destroy.",
        "nirukta": "kiranti dhanāni iti kirikāḥ (those who scatter wealth).",
        "vedantic": "The Lord is the bestower of all prosperity (bhukti) and liberation (mukti).",
        "panini": "Root √kṛ (to scatter) + 'ka' suffix with vowel lengthening. Dative plural.",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Wealth showerer synonyms.",
        "amara_kosha": "Bestower of wealth synonyms.",
        "abhidhana_ratnamala": "Wealth-giver synonyms."
    },
    "deva": {
        "english": "Of the gods.",
        "nirukta": "divyati iti devaḥ (luminous/shining one).",
        "vedantic": "The shining cosmic forces that govern different aspects of creation, all born of the one Supreme.",
        "panini": "Root √div (to shine) + 'ac' suffix. Genitive plural form is 'devānām'.",
        "case_ending": "Genitive Plural (Ṣaṣṭhī, Plural).",
        "nighantu": "Listed under deities (devatā-nāmāni, Nighaṇṭu 5.5).",
        "amara_kosha": "Svargavarga (1.1.1): 'amarā nirjarā devāḥ'.",
        "abhidhana_ratnamala": "Svarga-kāṇḍa: Synonym for gods."
    },
    "hṛdaya": {
        "english": "To the hearts / core.",
        "nirukta": "hṛdi-ayam, the seat of feelings and consciousness.",
        "vedantic": "The innermost core of all beings, where the Self resides and shines.",
        "panini": "Neuter noun 'hṛdaya'. Dative plural 'hṛdayebhyaḥ'.",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Listed under mind/seat of feelings.",
        "amara_kosha": "Śarīravarga: 'hṛdayam' (heart).",
        "abhidhana_ratnamala": "Under heart/mind synonyms."
    },
    "vikṣīṇaka": {
        "english": "To the ones who destroy (sin/decay) or are non-decaying.",
        "nirukta": "vi + kṣī (to decay) + suffix. those who do not decay, or who destroy.",
        "vedantic": "The immortal, changeless entities that bring about the destruction of finite forms.",
        "panini": "Prefix 'vi' + root √kṣī + 'kta' + 'ka' suffix. Dative plural.",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Not listed.",
        "amara_kosha": "Impermanent/destroyer synonyms.",
        "abhidhana_ratnamala": "Destroyer synonyms."
    },
    "vicinvatka": {
        "english": "To the ones who distinguish (merit and demerit) / investigate.",
        "nirukta": "vi + ci + śatṛ + ka. those who separate good from evil.",
        "vedantic": "The cosmic law of Karma that perfectly differentiates and awards fruits according to actions.",
        "panini": "Prefix 'vi' + root √ci (to gather) + 'śatṛ' + 'ka'. Dative plural.",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Not listed.",
        "amara_kosha": "Discriminating/investigating synonyms.",
        "abhidhana_ratnamala": "Under discrimination."
    },
    "ānihrita": {
        "english": "To the ones who strike down completely / take away.",
        "nirukta": "ā + nihṛ (to strike/punish) + kta. those who carry out divine punishment.",
        "vedantic": "Representing the unavoidable consequences of moral transgression, acting as natural correctives.",
        "panini": "Prefixes 'ā' + 'ni' + root √hṛ + suffix 'kta'. Dative plural.",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Not listed.",
        "amara_kosha": "Striking down synonyms.",
        "abhidhana_ratnamala": "Punishment/striking synonyms."
    },
    "āmīvatka": {
        "english": "To the ones who cause diseases to flee, or chase sinners.",
        "nirukta": "ā + mīv (to move/chase) + śatṛ + ka. those who chase away disease/sin.",
        "vedantic": "The healing aspects of Rudra that chase away physical and spiritual diseases from the devotee.",
        "panini": "Prefix 'ā' + root √mīv (to move) + 'śatṛ' + 'ka'. Dative plural.",
        "case_ending": "Dative Plural (Caturthī, Plural).",
        "nighantu": "Not listed.",
        "amara_kosha": "Chasing/healing synonyms.",
        "abhidhana_ratnamala": "Chasing synonyms."
    },
    # Anuvakam 10 stems
    "drāpi": {
        "english": "O driver away of sin / O cloak of the universe.",
        "nirukta": "drapayati pāpakṛtaḥ iti drāpiḥ (he who makes sinners run or suffer). Or a golden mantle.",
        "vedantic": "The Lord acts as a protective cloak for the cosmos, and also drives away the cycle of Samsara.",
        "panini": "Derived from root √drā (to run/flee) + 'pic' + 'in' suffix. Vocative singular.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Listed under mantle/cloak synonyms.",
        "amara_kosha": "Mantle/gold-cloth synonyms.",
        "abhidhana_ratnamala": "Garment/mantle synonyms."
    },
    "andhas": {
        "english": "Of food / Soma juice.",
        "nirukta": "Derived from root 'ad' (to eat) or 'nam' (to flow). That which nourishes.",
        "vedantic": "The Lord is the food (Soma) that sustains both physical body and spiritual devotion.",
        "panini": "Root √ad + suffix 'asun' with irregular changes. Genitive singular form is 'andhasaḥ'.",
        "case_ending": "Genitive Singular (Ṣaṣṭhī, Neuter).",
        "nighantu": "Listed under food synonyms (anna-nāmāni, Nighaṇṭu 2.7, item 9) and Soma juice.",
        "amara_kosha": "Food/Soma synonyms.",
        "abhidhana_ratnamala": "Food synonyms."
    },
    "pati": {
        "english": "O Lord / Protector.",
        "nirukta": "pāti iti patiḥ (he who protects).",
        "vedantic": "The Supreme Ruler and protector of the spiritual nectar (Soma/Andhas).",
        "panini": "Root √pā (to protect) + 'ḍati' suffix (P.3.3.94). Vocative singular.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Lord/protector synonyms.",
        "amara_kosha": "Lord/master synonyms.",
        "abhidhana_ratnamala": "Lord/husband synonyms."
    },
    "daridrat": {
        "english": "O non-attached / O poor / O detached one.",
        "nirukta": "Derived from root 'daridrā' meaning to be poor. In the case of Shiva, it means He who possesses nothing, hence detached from all worldly items.",
        "vedantic": "Represents the supreme asceticism (Vairāgya) of Lord Shiva, who needs nothing because He is self-complete.",
        "panini": "Intensive form of root √dṛ (to split) or root √daridrā (Adādi-gaṇa, 2.0071) + active participle 'śatṛ'. Vocative singular.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Poor/ascetic synonyms.",
        "abhidhana_ratnamala": "Poor/beggar synonyms."
    },
    "nīlalōhita": {
        "english": "O blue-red one.",
        "nirukta": "nīlaśca lohitaśca iti nīlalohitaḥ (having blue neck and red body).",
        "vedantic": "Represents the union of Puruṣa (blue/unmoving) and Prakṛti (red/active), or Śiva and Śakti.",
        "panini": "Karmadhāraya compound: 'nīla' + 'lohita'. Vocative singular.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Lord Shiva's names.",
        "abhidhana_ratnamala": "Shiva's names."
    },
    "idam": {
        "english": "These / This.",
        "nirukta": "Pronominal base pointing to immediate experience.",
        "vedantic": "The manifest universe which is experienced directly by the senses.",
        "panini": "Pronoun 'idam'. Genitive plural form is 'eṣām' / 'eṣām-puruṣāṇām'.",
        "case_ending": "Genitive Plural / Locative Singular / Accusative.",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronoun class.",
        "abhidhana_ratnamala": "Excluded."
    },
    "puruṣa": {
        "english": "Of men / people.",
        "nirukta": "puruṣaḥ purīṣādaḥ (dweller of the body-city).",
        "vedantic": "The conscious entities (soul/Jivas) that reside in physical bodies.",
        "panini": "Derived from root √pṛ (to fill) + 'uṣan' suffix. Genitive plural is 'puruṣāṇām'.",
        "case_ending": "Genitive Plural (Ṣaṣṭhī, Masculine).",
        "nighantu": "Man/human synonyms.",
        "amara_kosha": "Man synonyms.",
        "abhidhana_ratnamala": "Man synonyms."
    },
    "paśu": {
        "english": "Of animals / cattle.",
        "nirukta": "paśyati iti paśuḥ (he who sees, or who is bound).",
        "vedantic": "The bound souls (Jivas) who are bound by the ropes (pāśa) of ignorance and worldly desires.",
        "panini": "Root √paś (to see) + 'ku' suffix (Uṇādi 1.29). Genitive plural is 'paśūnām'.",
        "case_ending": "Genitive Plural (Ṣaṣṭhī, Masculine).",
        "nighantu": "Animal synonyms.",
        "amara_kosha": "Animal synonyms.",
        "abhidhana_ratnamala": "Animal synonyms."
    },
    "mā": {
        "english": "Do not.",
        "nirukta": "Particle of negation or prohibition.",
        "vedantic": "A prayer to avert negative fruits and suffering, acknowledging the Lord's absolute power.",
        "panini": "Avyaya (negative particle) governing the aorist or injunctive mood.",
        "case_ending": "Avyaya (negation).",
        "nighantu": "Listed under negative particles.",
        "amara_kosha": "Negation synonyms.",
        "abhidhana_ratnamala": "Negation particles."
    },
    "bhī": {
        "english": "Do not fear.",
        "nirukta": "Derived from root 'bhī' meaning to fear.",
        "vedantic": "A request to remove the primordial fear of death and limitation.",
        "panini": "Root √bhī (Juhotyādi-gaṇa, 3.0002). Vedic second-person singular aorist injunctive 'mā bheḥ'.",
        "case_ending": "Verbal form (Aorist Injunctive, 2nd Singular).",
        "nighantu": "Fear synonyms.",
        "amara_kosha": "Fear synonyms.",
        "abhidhana_ratnamala": "Fear synonyms."
    },
    "rī": {
        "english": "Do not perish / harm.",
        "nirukta": "Derived from root 'rī' meaning to howl/perish/harm.",
        "vedantic": "A prayer that our cattle, children, and belongings do not suffer destruction.",
        "panini": "Root √rī (Kryādi-gaṇa, 9.0033). Injunctive form 'mā araḥ' / 'mā-aroḥ'.",
        "case_ending": "Verbal form (Injunctive, 2nd Singular).",
        "nighantu": "Destruction synonyms.",
        "amara_kosha": "Destruction synonyms.",
        "abhidhana_ratnamala": "Harm synonyms."
    },
    "kiñcana": {
        "english": "Anything whatsoever.",
        "nirukta": "Indefinite pronoun.",
        "vedantic": "Refers to even the smallest speck of illness or sorrow.",
        "panini": "Compound particle 'kim' + 'ca' + 'na'.",
        "case_ending": "Neuter Singular.",
        "nighantu": "Not listed.",
        "amara_kosha": "Indefinite particle.",
        "abhidhana_ratnamala": "Not listed."
    },
    "am": {
        "english": "Be diseased / fall ill.",
        "nirukta": "Derived from root 'am' meaning to be sick or afflicted.",
        "vedantic": "A prayer that no disease should strike our people or cattle.",
        "panini": "Root √am (Bhvādi-gaṇa, 1.0507). Vedic injunctive/subjunctive form 'āmamat'.",
        "case_ending": "Verbal form (Aorist Subjunctive, 3rd Singular).",
        "nighantu": "Affliction synonyms.",
        "amara_kosha": "Disease/sickness synonyms.",
        "abhidhana_ratnamala": "Disease synonyms."
    },
    "yad": {
        "english": "Which / Who.",
        "nirukta": "Relative pronoun base.",
        "vedantic": "Points to the ultimate substrate that manifests as the active forces of nature.",
        "panini": "Relative pronoun 'yad'. Feminine singular form is 'yā'.",
        "case_ending": "Relative Pronoun.",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronoun class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "yushman": {
        "english": "Your / To you.",
        "nirukta": "Second-person pronoun base.",
        "vedantic": "Addressing the Lord directly, bridging the gap between devotee and deity.",
        "panini": "Pronoun 'yuşmad'. Genitive singular form 'te', dative plural 'vas'.",
        "case_ending": "Pronoun.",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronoun.",
        "abhidhana_ratnamala": "Not listed."
    },
    "rudra": {
        "english": "O Rudra / Of Rudra.",
        "nirukta": "He who dissolves suffering (rutaṃ drāvayati).",
        "vedantic": "The supreme healer and destroyer of ignorance.",
        "panini": "Root √rud + 'kran' suffix. Vocative 'rudra', dative 'rudrāya', genitive 'rudrasya'.",
        "case_ending": "Noun (Proper).",
        "nighantu": "Atmospheric deity.",
        "amara_kosha": "Shiva's name.",
        "abhidhana_ratnamala": "Shiva's name."
    },
    "śiva": {
        "english": "Auspicious / Benevolent / Source of peace.",
        "nirukta": "śerete asmin sarvam iti śivaḥ (He in whom all things rest).",
        "vedantic": "The non-dual state of pure consciousness which is inherently auspicious and peaceful (Śāntam Śivam Advaitam).",
        "panini": "Root √śī (to sleep/rest) + 'van' suffix. Feminine 'śivā', masculine 'śivaḥ'.",
        "case_ending": "Adjective / Noun.",
        "nighantu": "Auspiciousness synonyms.",
        "amara_kosha": "Shiva's name / auspiciousness.",
        "abhidhana_ratnamala": "Under Shiva and peace."
    },
    "tanū": {
        "english": "Body / Manifest form.",
        "nirukta": "tanoti iti tanūḥ (that which stretches or manifests).",
        "vedantic": "The cosmic body of the Lord, which is the entire universe, and His subtle body of knowledge.",
        "panini": "Root √tan (to stretch) + 'ū' suffix. Nominative singular 'tanūḥ', nominative plural 'tanuvaḥ'.",
        "case_ending": "Nominative Singular / Plural (Feminine).",
        "nighantu": "Listed under body synonyms (Nighaṇṭu 2.6).",
        "amara_kosha": "Śarīravarga: 'tanūḥ' (body).",
        "abhidhana_ratnamala": "Body synonyms."
    },
    "viśvaha-bhēṣajī": {
        "english": "A healer for all days / universal medicine.",
        "nirukta": "viśveṣu ahaḥsu bhēṣajī (healing at all times).",
        "vedantic": "The ultimate remedy for the chronic disease of transmigratory existence (Samsara).",
        "panini": "Compound: 'viśvaha' (always) + 'bhēṣajī' (healer).",
        "case_ending": "Nominative Singular (Feminine).",
        "nighantu": "Healing synonyms.",
        "amara_kosha": "Medicine synonyms.",
        "abhidhana_ratnamala": "Healing synonyms."
    },
    "bhēṣajī": {
        "english": "The healer / medicine.",
        "nirukta": "Derived from 'bhiṣaj' (healer).",
        "vedantic": "The curative power of divine grace.",
        "panini": "Noun 'bhiṣaj' with feminine suffix 'ṅīṣ'.",
        "case_ending": "Nominative Singular (Feminine).",
        "nighantu": "Medicine synonyms.",
        "amara_kosha": "Medicine synonyms.",
        "abhidhana_ratnamala": "Healing synonyms."
    },
    "tad": {
        "english": "That / By that.",
        "nirukta": "Demonstrative pronoun base.",
        "vedantic": "Refers to the transcendent reality that is experienced as the substrate of all.",
        "panini": "Pronoun 'tad'. Instrumental 'tayā', accusative 'tat'.",
        "case_ending": "Pronoun.",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronoun.",
        "abhidhana_ratnamala": "Not listed."
    },
    "asmad": {
        "english": "Us / Our.",
        "nirukta": "First-person pronoun base.",
        "vedantic": "Refers to the collective assembly of devotees praying together.",
        "panini": "Pronoun 'asmad'. Dative/accusative plural enclitic 'naḥ', locative 'asme'.",
        "case_ending": "Pronoun.",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronoun.",
        "abhidhana_ratnamala": "Not listed."
    },
    "mṛd": {
        "english": "Make happy / grant bliss.",
        "nirukta": "mṛḍayati iti (that which delights or pleases).",
        "vedantic": "The granting of the supreme, unalloyed bliss of Brahman (Ānanda).",
        "panini": "Root √mṛḍ (Adādi-gaṇa, 2.0028). Imperative second-person singular 'mṛḍa' or 'mṛḍaya'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Happiness/bliss synonyms.",
        "amara_kosha": "Under happiness/delight.",
        "abhidhana_ratnamala": "Delight synonyms."
    },
    "jīv": {
        "english": "For living / for life.",
        "nirukta": "Derived from root 'jīv' meaning to live.",
        "vedantic": "The vital energy (Prana) that animates the physical sheath to allow spiritual practice.",
        "panini": "Root √jīv (Bhvādi-gaṇa, 1.0649). Vedic dative infinitive 'jīvase' (P.3.4.9).",
        "case_ending": "Vedic Infinitive (Dative meaning).",
        "nighantu": "Listed under life synonyms.",
        "amara_kosha": "Life synonyms.",
        "abhidhana_ratnamala": "Life/living synonyms."
    },
    "tavas": {
        "english": "To the strong / mighty one.",
        "nirukta": "Derived from root 'tu' meaning to grow or be strong.",
        "vedantic": "The omnipotent force that sustains the entire cosmos.",
        "panini": "Root √tu + suffix 'asun' with augment. Dative singular form is 'tavase'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Listed under strength synonyms (Nighaṇṭu 2.9).",
        "amara_kosha": "Strength/mighty synonyms.",
        "abhidhana_ratnamala": "Mighty/strong synonyms."
    },
    "kṣayatvīra": {
        "english": "To the one whose heroes/servants are ruled or destroyed.",
        "nirukta": "kṣayantaḥ vīrāḥ yasya saḥ (under whose command all heroes/energies stand). Or he who destroys disease/sin.",
        "vedantic": "The Supreme Ruler (Iśvara) who governs all active cosmic forces and reduces the ego-heroes to insignificance.",
        "panini": "Bahuvrīhi compound: 'kṣayat' (ruling/ruling over) + 'vīra' (hero). Dative singular.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Ruler/destroyer synonyms.",
        "amara_kosha": "Under Lord/Ruler.",
        "abhidhana_ratnamala": "Ruler synonyms."
    },
    "pra": {
        "english": "Forward / intensely.",
        "nirukta": "A prefix indicating forward movement, excellence, or intensity.",
        "vedantic": "Qualifies the act of surrender, showing it must be complete and intense.",
        "panini": "Prādi-gaṇa prefix (Upasarga).",
        "case_ending": "Avyaya (prefix).",
        "nighantu": "Not listed.",
        "amara_kosha": "Prefix section.",
        "abhidhana_ratnamala": "Not listed."
    },
    "bhṛ": {
        "english": "We offer / bring.",
        "nirukta": "Derived from root 'bhṛ' meaning to support, bear, or offer.",
        "vedantic": "The mental offering of oneself, intellect, and activities to the Divine.",
        "panini": "Root √bhṛ (Bhvādi-gaṇa, 1.1045). Lat first-person plural 'prabhahāmahe' or 'prabharāmahe'.",
        "case_ending": "Verbal form (Lat, 1st Plural).",
        "nighantu": "Offering synonyms.",
        "amara_kosha": "Bearing/supporting synonyms.",
        "abhidhana_ratnamala": "Supporting synonyms."
    },
    "mati": {
        "english": "Intellect / prayer / meditation.",
        "nirukta": "manyate anayā iti matiḥ (that by which we think or contemplate).",
        "vedantic": "The refined intellect (Buddhi) directed toward the meditation on Brahman.",
        "panini": "Root √man + suffix 'ktin' (P.3.3.94). Accusative singular is 'matim'.",
        "case_ending": "Accusative Singular (Dvitīyā, Feminine).",
        "nighantu": "Listed under intellect/intellectual synonyms (Nighaṇṭu 3.9).",
        "amara_kosha": "Buddhivarga: 'matiḥ' (intellect).",
        "abhidhana_ratnamala": "Intellect synonyms."
    },
    "yathā": {
        "english": "In order that / so that.",
        "nirukta": "Relative indeclinable particle indicating manner or purpose.",
        "vedantic": "Expresses the causal relationship between divine grace and cosmic harmony.",
        "panini": "Avyaya derived from relative 'yad' with 'thāl' suffix (P.5.3.23).",
        "case_ending": "Avyaya (conjunction).",
        "nighantu": "Conjunctive particle.",
        "amara_kosha": "Avyayavarga: Manner particle.",
        "abhidhana_ratnamala": "Conjunctive particle."
    },
    "śam": {
        "english": "Peace / welfare / spiritual calm.",
        "nirukta": "śamayati duḥkham iti śam (that which quietens or pacifies suffering).",
        "vedantic": "The quietude of the mind (Śama) which is a pre-requisite for Self-realization.",
        "panini": "Root √śam (to be calm) + 'kvip' suffix. Neuter singular.",
        "case_ending": "Nominative Singular (Neuter).",
        "nighantu": "Listed under happiness/peace synonyms (Nighaṇṭu 3.6).",
        "amara_kosha": "Happiness/welfare synonyms.",
        "abhidhana_ratnamala": "Calmness/peace synonyms."
    },
    "as": {
        "english": "May there be / let there be.",
        "nirukta": "Derived from root 'as' meaning to be or exist.",
        "vedantic": "The affirmation of pure existence (Sat), which is the substrate of all creation.",
        "panini": "Root √as (Adādi-gaṇa, 2.0060). Vedic subjunctive/injunctive third-person singular 'asat', imperative 'astu'.",
        "case_ending": "Verbal form (Injunctive/Imperative, 3rd Singular).",
        "nighantu": "Existence/being synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "dvipada": {
        "english": "To the two-legged beings (humans).",
        "nirukta": "dvau pādau yasya tat dvipadam (possessing two feet).",
        "vedantic": "Refers to human Jivas, who require peace of mind to progress on the path of evolution.",
        "panini": "Bahuvrīhi compound: 'dvi' + 'pāda' (P.5.4.140). Dative singular 'dvipade'.",
        "case_ending": "Dative Singular (Caturthī, Masculine/Neuter).",
        "nighantu": "Not listed.",
        "amara_kosha": "Under human classification.",
        "abhidhana_ratnamala": "Under human terms."
    },
    "catuṣpada": {
        "english": "To the four-legged beings (animals).",
        "nirukta": "catvāraḥ pādāḥ yasya tat catuṣpadam.",
        "vedantic": "Refers to animals, who also require health and freedom from fear under the Lord's governance.",
        "panini": "Bahuvrīhi compound: 'catur' + 'pāda'. Dative singular 'catuṣpade'.",
        "case_ending": "Dative Singular (Caturthī, Masculine/Neuter).",
        "nighantu": "Not listed.",
        "amara_kosha": "Under animal classification.",
        "abhidhana_ratnamala": "Animal terms."
    },
    "viśva": {
        "english": "All / Entire / Universe.",
        "nirukta": "viśati iti viśvam (that which is entered, or enters).",
        "vedantic": "The entire cosmos, which is entered and pervaded by the omnipresent Brahman.",
        "panini": "Sarvanāma (pronoun) base meaning 'all'. Neuter singular 'viśvam'.",
        "case_ending": "Nominative/Accusative Singular.",
        "nighantu": "Listed under names of all/whole (Nighaṇṭu 3.1).",
        "amara_kosha": "Nānārthavarga: 'viśvam jagati ca triṣu' (defining viśva as world or all).",
        "abhidhana_ratnamala": "Under synonyms for all."
    },
    "puṣṭa": {
        "english": "Nourished / prosperous.",
        "nirukta": "Derived from root 'puṣ' meaning to nourish or thrive.",
        "vedantic": "The state of complete physical and spiritual enrichment resulting from divine alignment.",
        "panini": "Root √puṣ (Divādi-gaṇa, 4.0084) + suffix 'kta'. Neuter singular 'puṣṭam'.",
        "case_ending": "Nominative Singular (Neuter).",
        "nighantu": "Thriving/nourished synonyms.",
        "amara_kosha": "Thriving/nourishment synonyms.",
        "abhidhana_ratnamala": "Thriving synonyms."
    },
    "grāma": {
        "english": "In the village.",
        "nirukta": "gṛhyate bhogaḥ atra iti grāmaḥ (where worldly enjoyment is gathered).",
        "vedantic": "The social environment or community of Jivas living together.",
        "panini": "Root √grah + 'ghañ' with irregular changes. Locative singular is 'grāme'.",
        "case_ending": "Locative Singular (Saptamī, Masculine).",
        "nighantu": "village/assembly synonyms.",
        "amara_kosha": "Bhūmivarga: 'grāma' (village).",
        "abhidhana_ratnamala": "Village/society synonyms."
    },
    "anātura": {
        "english": "Healthy / free from illness.",
        "nirukta": "na āturaḥ iti anāturaḥ (not sick/unafflicted).",
        "vedantic": "The state of physical health and mental stability required to undertake spiritual enquiry.",
        "panini": "Nañ-tatpuruṣa compound: negative prefix 'an' + adjective 'ātura' (diseased).",
        "case_ending": "Nominative Singular (Neuter).",
        "nighantu": "Health/healthy synonyms.",
        "amara_kosha": "Healthy synonyms.",
        "abhidhana_ratnamala": "Healthy synonyms."
    },
    "mayas": {
        "english": "Bliss / happiness / spiritual joy.",
        "nirukta": "Derived from root 'mī' meaning to delight, or from 'ma' (bliss).",
        "vedantic": "The essential nature of the Self, which is Anandamaya (made of bliss).",
        "panini": "Vedic noun 'mayas' ending in 'as'. Accusative singular.",
        "case_ending": "Accusative Singular (Neuter).",
        "nighantu": "Listed under happiness/bliss synonyms (Nighaṇṭu 3.6).",
        "amara_kosha": "Bliss/joy synonyms.",
        "abhidhana_ratnamala": "Joy/bliss synonyms."
    },
    "kṛ": {
        "english": "Make / grant.",
        "nirukta": "Derived from root 'kṛ' meaning to do or make.",
        "vedantic": "The request to actively bestow peace and welfare upon us.",
        "panini": "Root √kṛ (Tanādi-gaṇa, 8.0010). Vedic imperative second-person singular 'kṛdhi' (P.6.4.101).",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Doing/making synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "vidh": {
        "english": "May we worship / serve.",
        "nirukta": "Derived from root 'vidh' meaning to worship, honor, or serve.",
        "vedantic": "Worship is the active alignment of our mind and actions with the cosmic order.",
        "panini": "Root √vidh (Adādi-gaṇa) or √vidh (Bhvādi-gaṇa, 1.0964). Vedic optative first-person plural 'vidhema'.",
        "case_ending": "Verbal form (Optative, 1st Plural).",
        "nighantu": "Worship/sacrifice synonyms.",
        "amara_kosha": "Worship/service synonyms.",
        "abhidhana_ratnamala": "Service synonyms."
    },
    "yōs": {
        "english": "Welfare / prevention of calamity.",
        "nirukta": "yauvati duḥkham iti yoḥ (that which separates us from suffering).",
        "vedantic": "The removal of spiritual and mental obstacles that prevent Self-knowledge.",
        "panini": "Vedic noun 'yos' in the accusative singular.",
        "case_ending": "Accusative Singular (Neuter).",
        "nighantu": "Listed under happiness/welfare synonyms (Nighaṇṭu 3.6).",
        "amara_kosha": "Welfare/comfort synonyms.",
        "abhidhana_ratnamala": "Comfort synonyms."
    },
    "manu": {
        "english": "Manu (the progenitor of mankind).",
        "nirukta": "manyate iti manuḥ (the thinking being, progenitor of humans).",
        "vedantic": "The archetypal mind that sets the code of conduct (Dharma) for the current age.",
        "panini": "Root √man + suffix 'u'. Nominative singular is 'manuḥ'.",
        "case_ending": "Nominative Singular (Masculine).",
        "nighantu": "Progenitor/man synonyms.",
        "amara_kosha": "Svargavarga: 'manur-manur-janādhipaḥ' / 'manustu prajāpatir'.",
        "abhidhana_ratnamala": "Under sage/progenitor names."
    },
    "ā-yaj": {
        "english": "Worshipped / sacrificed.",
        "nirukta": "ā + yaj (to worship). he who attained the fruits of sacrifice.",
        "vedantic": "Represents the ideal performer of Yajña (sacrifice) whose path we seek to follow.",
        "panini": "Prefix 'ā' + root √yaj + Lat/Liṭ first-person singular middle 'ā-yaje'.",
        "case_ending": "Verbal form (Liṭ/Lat, 1st Singular Middle).",
        "nighantu": "Worship synonyms.",
        "amara_kosha": "Sacrifice synonyms.",
        "abhidhana_ratnamala": "Sacrifice synonyms."
    },
    "pitṛ": {
        "english": "Father / progenitor.",
        "nirukta": "pātā vā pālayitā vā pitā (he who protects or nourishes).",
        "vedantic": "The source of physical lineage; also represents the lineage of teachers (Guru-paramparā).",
        "panini": "Root √pā + suffix 'tṛc' with augment. Nominative singular 'pitā', accusative 'pitaram'.",
        "case_ending": "Nominative / Accusative Singular (Masculine).",
        "nighantu": "Listed under parent/father synonyms.",
        "amara_kosha": "Parent synonyms: 'tātastu janakaḥ pitā'.",
        "abhidhana_ratnamala": "Father synonyms."
    },
    "aṃś": {
        "english": "May we attain / enjoy.",
        "nirukta": "Derived from root 'aṃś' or 'aś' meaning to reach or enjoy.",
        "vedantic": "The prayer to experience the supreme fruit of our efforts under the Lord's guidance.",
        "panini": "Root √aś (Kryādi-gaṇa, 9.0019) or √aṃś. Vedic optative first-person plural 'aśyāma' (P.3.4.116).",
        "case_ending": "Verbal form (Optative, 1st Plural).",
        "nighantu": "Attainment/enjoyment synonyms.",
        "amara_kosha": "Attaining synonyms.",
        "abhidhana_ratnamala": "Attaining synonyms."
    },
    "pranīti": {
        "english": "Under the guidance / love.",
        "nirukta": "pra + nī + kti. pranayana (guidance/love/lead).",
        "vedantic": "Living in complete harmony with the divine plan, led by the Guru's guidance.",
        "panini": "Prefix 'pra' + root √nī + suffix 'ktin'. Locative singular is 'praṇītau'.",
        "case_ending": "Locative Singular (Saptamī, Feminine).",
        "nighantu": "Guidance synonyms.",
        "amara_kosha": "Guidance/love synonyms.",
        "abhidhana_ratnamala": "Guidance synonyms."
    },
    "mahat": {
        "english": "The elder / great / large.",
        "nirukta": "mahate iti mahān (that which is expanded or great).",
        "vedantic": "The elder generation, or the vast and great elements of creation.",
        "panini": "Root √mah + suffix 'atup'. Accusative singular masculine 'mahāntam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Listed under names of great/large (Nighaṇṭu 3.3).",
        "amara_kosha": "Great/elder synonyms.",
        "abhidhana_ratnamala": "Great synonyms."
    },
    "arbhaka": {
        "english": "The child / small / young.",
        "nirukta": "Derived from root 'arbh' meaning to kill or diminish. That which is small.",
        "vedantic": "The young, vulnerable, or underdeveloped elements of our community and inner self.",
        "panini": "Uṇādi-derived noun. Accusative singular masculine 'arbhakam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Listed under small/young synonyms (Nighaṇṭu 3.2).",
        "amara_kosha": "Child/small synonyms.",
        "abhidhana_ratnamala": "Child synonyms."
    },
    "ukṣant": {
        "english": "The growing youth / procreant.",
        "nirukta": "Derived from root 'ukṣ' meaning to sprinkle, grow, or strengthen.",
        "vedantic": "The active, productive force of youth that builds and sprinks vital energy.",
        "panini": "Root √ukṣ (Bhvādi-gaṇa, 1.0747) + participle 'śatṛ'. Accusative singular 'ukṣantam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Sprinkling/strengthening synonyms.",
        "amara_kosha": "Youth/procreator synonyms.",
        "abhidhana_ratnamala": "Under youth."
    },
    "ukṣita": {
        "english": "The infant / womb-born / fully grown.",
        "nirukta": "Derived from root 'ukṣ' + kta. that which is sprinkled or fully formed.",
        "vedantic": "The unborn child in the womb, or the child that has just been born.",
        "panini": "Root √ukṣ + suffix 'kta'. Accusative singular 'ukṣitam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Sprinkled synonyms.",
        "amara_kosha": "Infant/womb-born synonyms.",
        "abhidhana_ratnamala": "Child synonyms."
    },
    "vadh": {
        "english": "Do not kill / destroy.",
        "nirukta": "Derived from root 'vadh' meaning to strike, kill, or destroy.",
        "vedantic": "A prayer for the preservation of life and the avoidance of untimely death (Apamṛtyu).",
        "panini": "Root √vadh (Bhvādi-gaṇa, 1.1047). Vedic aorist injunctive second-person singular 'vadhīḥ'.",
        "case_ending": "Verbal form (Aorist Injunctive, 2nd Singular).",
        "nighantu": "Killing/destruction synonyms.",
        "amara_kosha": "Killing synonyms.",
        "abhidhana_ratnamala": "Killing synonyms."
    },
    "mātṛ": {
        "english": "Mother / progenitor.",
        "nirukta": "mānada bhūtānām iti mātā (she who measures out or gives value).",
        "vedantic": "The nurturing aspect of the universe (Śakti), and the biological mother.",
        "panini": "Root √mā + suffix 'tṛc'. Accusative singular is 'mātaram'.",
        "case_ending": "Accusative Singular (Dvitīyā, Feminine).",
        "nighantu": "Parent/mother synonyms.",
        "amara_kosha": "Mother synonyms: 'mātā jananī'.",
        "abhidhana_ratnamala": "Mother synonyms."
    },
    "priya": {
        "english": "Dear / beloved ones.",
        "nirukta": "prīṇati iti priyaḥ (that which pleases or is loved).",
        "vedantic": "The objects and people that are dear to us, reflecting the innate love (Premo) of the Self.",
        "panini": "Root √prī + suffix 'ka' (P.3.1.135). Accusative plural feminine 'priyāḥ'.",
        "case_ending": "Accusative Plural (Dvitīyā, Feminine/Masculine).",
        "nighantu": "Pleasing synonyms.",
        "amara_kosha": "Beloved synonyms.",
        "abhidhana_ratnamala": "Beloved synonyms."
    },
    "riṣ": {
        "english": "Do not injure / harm.",
        "nirukta": "Derived from root 'riṣ' meaning to hurt or injure.",
        "vedantic": "A prayer that no harm should come to our spiritual bodies and physical frames.",
        "panini": "Root √riṣ (Divādi-gaṇa, 4.0141). Vedic aorist injunctive second-person singular 'rīriṣaḥ'.",
        "case_ending": "Verbal form (Aorist Injunctive, 2nd Singular).",
        "nighantu": "Injury synonyms.",
        "amara_kosha": "Injury synonyms.",
        "abhidhana_ratnamala": "Injury synonyms."
    },
    "tōka": {
        "english": "Children / progeny.",
        "nirukta": "tudyate anena pitroḥ manaḥ iti tokaḥ (that which delights parents).",
        "vedantic": "The future generation, representing the expansion of the family line.",
        "panini": "Derived noun. Locative singular 'toke', dative 'tokāya'.",
        "case_ending": "Locative / Dative Singular.",
        "nighantu": "Listed under progeny/children synonyms (Nighaṇṭu 2.2).",
        "amara_kosha": "Progeny synonyms.",
        "abhidhana_ratnamala": "Progeny synonyms."
    },
    "tanaya": {
        "english": "Grandchildren / sons.",
        "nirukta": "tanoti pitroḥ kulam iti tanayaḥ (he who stretches or continues the family).",
        "vedantic": "The continuation of life through successive generations.",
        "panini": "Root √tan + suffix 'kayan'. Locative singular 'tanaye', dative 'tanayāya'.",
        "case_ending": "Locative / Dative Singular.",
        "nighantu": "Listed under progeny synonyms (Nighaṇṭu 2.2).",
        "amara_kosha": "Son/grandson synonyms.",
        "abhidhana_ratnamala": "Son synonyms."
    },
    "āyus": {
        "english": "Lifespan / longevity.",
        "nirukta": "eti anena iti āyuḥ (that by which one goes/lives).",
        "vedantic": "The allotted time in the physical plane, meant for performing spiritual sadhana.",
        "panini": "Root √i + suffix 'uṣi'. Locative singular 'āyuṣi'.",
        "case_ending": "Locative Singular (Saptamī, Neuter).",
        "nighantu": "Listed under life synonyms.",
        "amara_kosha": "Life synonyms.",
        "abhidhana_ratnamala": "Life/longevity synonyms."
    },
    "gō": {
        "english": "Cows / cattle.",
        "nirukta": "gacchati iti gauḥ (that which moves/walks).",
        "vedantic": "The sacred, nurturing elements of nature (represented by cows), which provide milk and sustain life.",
        "panini": "Irregular noun 'go'. Locative plural is 'gōṣu'.",
        "case_ending": "Locative Plural (Saptamī, Feminine).",
        "nighantu": "Cattle/earth synonyms.",
        "amara_kosha": "Cow/cattle synonyms.",
        "abhidhana_ratnamala": "Cow synonyms."
    },
    "aśva": {
        "english": "Horses / transport.",
        "nirukta": "aśnute adhvānam iti aśvaḥ (he who eats or covers the path).",
        "vedantic": "Represent the senses and the power of transportation/speed in the world.",
        "panini": "Root √aś (to reach) + suffix 'kvan' (Uṇādi 1.149). Locative plural 'aśveṣu'.",
        "case_ending": "Locative Plural (Saptamī, Masculine).",
        "nighantu": "Listed under horse synonyms (Nighaṇṭu 1.14).",
        "amara_kosha": "Horse synonyms.",
        "abhidhana_ratnamala": "Horse synonyms."
    },
    "vīra": {
        "english": "Heroes / brave warriors / brave servants.",
        "nirukta": "vīrayate iti vīraḥ (he who exhibits valor).",
        "vedantic": "The inner strength and qualities of courage required to battle spiritual ignorance.",
        "panini": "Root √vīr (to be brave) + suffix 'ac'. Accusative plural is 'vīrān'.",
        "case_ending": "Accusative Plural (Dvitīyā, Masculine).",
        "nighantu": "Listed under brave/strong synonyms.",
        "amara_kosha": "Brave man synonyms.",
        "abhidhana_ratnamala": "Hero synonyms."
    },
    "bhāmita": {
        "english": "Being angry / wrathful.",
        "nirukta": "Derived from root 'bhām' meaning to be angry.",
        "vedantic": "Refers to the protective and corrective anger of Rudra, which destroys evil.",
        "panini": "Root √bhām + suffix 'kta' + suffix 'tas' (Vedic instrumental adverb).",
        "case_ending": "Adverbial / Participle form.",
        "nighantu": "Anger synonyms.",
        "amara_kosha": "Anger synonyms.",
        "abhidhana_ratnamala": "Anger synonyms."
    },
    "havişmant": {
        "english": "Those offering oblations.",
        "nirukta": "havis (oblation) + matup. those who perform sacrifices.",
        "vedantic": "The dedicated practitioners who perform outer and inner sacrifices to the Divine.",
        "panini": "Noun 'havis' + possessive suffix 'matup'. Nominative plural masculine is 'haviṣmantaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Sacrificer synonyms.",
        "amara_kosha": "Sacrificer synonyms.",
        "abhidhana_ratnamala": "Oblation-giver synonyms."
    },
    "ārāt": {
        "english": "From a distance / far away.",
        "nirukta": "Derived from 'āra' (distance).",
        "vedantic": "A prayer that the destructive aspects of Rudra remain far from us.",
        "panini": "Ablative singular form of 'āra' used as an indeclinable adverb.",
        "case_ending": "Avyaya (adverb).",
        "nighantu": "Distance synonyms.",
        "amara_kosha": "Avyayavarga: Distance adverb.",
        "abhidhana_ratnamala": "Distance synonyms."
    },
    "gōghna": {
        "english": "To the cow-killing weapon / cow-slayer.",
        "nirukta": "gāṃ hanti iti goghnaḥ (that which strikes cows).",
        "vedantic": "The potential calamity or disease affecting our cattle; we pray it remains far away.",
        "panini": "Compound: 'go' + root √han + suffix 'ka' (P.3.2.54). Dative singular 'goghne'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Under destruction of cattle.",
        "abhidhana_ratnamala": "Not listed."
    },
    "puruṣaghna": {
        "english": "To the man-killing weapon / man-slayer.",
        "nirukta": "puruṣaṃ hanti iti puruṣaghnaḥ.",
        "vedantic": "The potential disasters or epidemics affecting humans; we pray they avoid us.",
        "panini": "Compound: 'puruṣa' + root √han + 'ka'. Dative singular 'puruṣaghne'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Under weapon class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "sumna": {
        "english": "Grace / benevolence / happiness.",
        "nirukta": "su + manaḥ = sumanas. that which makes the mind pleasant.",
        "vedantic": "The peaceful state of mind that arises through divine benevolence.",
        "panini": "Vedic noun 'sumna' derived from prefix 'su' + root √man + 'ka'. Nominative singular.",
        "case_ending": "Nominative Singular (Neuter).",
        "nighantu": "Listed under happiness/peace synonyms (Nighaṇṭu 3.6).",
        "amara_kosha": "Happiness/comfort synonyms.",
        "abhidhana_ratnamala": "Comfort/bliss synonyms."
    },
    "rakṣ": {
        "english": "Protect us.",
        "nirukta": "rakṣati iti (that which keeps safe).",
        "vedantic": "The divine shield that protects the seeker from internal and external obstacles.",
        "panini": "Root √rakṣ (Bhvādi-gaṇa, 1.0743). Imperative second-person singular 'rakṣa'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Protection synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "brū": {
        "english": "Speak (for us) / advocate.",
        "nirukta": "brūte iti (he who speaks or declares).",
        "vedantic": "Addressing the Lord as our advocate, who speaks words of favor to the higher cosmic forces.",
        "panini": "Root √brū (Adādi-gaṇa, 2.0039). Imperative second-person singular 'brūhi'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Speaking/declaring synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "śarman": {
        "english": "Protection / shelter / happiness.",
        "nirukta": "śaraṇaṃ bhavatīti śarma (that which provides refuge).",
        "vedantic": "The ultimate refuge of the Jiva, which is the non-dual consciousness.",
        "panini": "Root √śṛ + suffix 'manin'. Accusative singular is 'śarma'.",
        "case_ending": "Accusative Singular (Dvitīyā, Neuter).",
        "nighantu": "Listed under house/refuge synonyms (Nighaṇṭu 3.4) and happiness (3.6).",
        "amara_kosha": "Refuge/comfort synonyms.",
        "abhidhana_ratnamala": "Refuge synonyms."
    },
    "yam": {
        "english": "Grant / bestow.",
        "nirukta": "yacchati iti (he who gives or binds).",
        "vedantic": "The request to bestow the peace and refuge we seek.",
        "panini": "Root √yam (Bhvādi-gaṇa, 1.1137). Imperative second-person singular 'yaccha'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Giving synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "dvibarhas": {
        "english": "Dwelling in two worlds / having double strength.",
        "nirukta": "dvayoḥ sthānayoḥ bṛhantaḥ (mighty in both earth and heaven).",
        "vedantic": "The Lord who is both transcendent (heaven/unmanifest) and immanent (earth/manifest).",
        "panini": "Vedic compound: 'dvi' + 'barhas' (mighty/expanded). Nominative singular.",
        "case_ending": "Nominative Singular (Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Mighty/double synonyms.",
        "abhidhana_ratnamala": "Not listed."
    },
    "stu": {
        "english": "Praise.",
        "nirukta": "stauti iti (he who glorifies).",
        "vedantic": "Praise is the vocal expression of our devotion, focusing the mind on divine qualities.",
        "panini": "Root √stu (Adādi-gaṇa, 2.0042). Imperative second-person singular 'stuhi'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Praise synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "śruta": {
        "english": "The famous / renowned one.",
        "nirukta": "śrūyate iti śrutaḥ (he who is heard of through Vedic texts).",
        "vedantic": "The Supreme Brahman who is revealed through the Upanishadic texts (Śrutis).",
        "panini": "Root √śru (to hear) + suffix 'kta'. Accusative singular is 'śrutam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Hearing/fame synonyms.",
        "amara_kosha": "Renowned/learned synonyms.",
        "abhidhana_ratnamala": "Famous synonyms."
    },
    "gartasada": {
        "english": "Sitting in the chariot/heart cave.",
        "nirukta": "garte (chariot-seat or cave of the heart) sīdati iti gartasad.",
        "vedantic": "The Lord who resides in the intellect (buddhi-guhā) as the ultimate witness.",
        "panini": "Locative compound: 'garte' + root √sad + 'kvip' suffix. Accusative singular 'gartasadam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Heart/chariot synonyms.",
        "amara_kosha": "Under chariot/cavity synonyms.",
        "abhidhana_ratnamala": "Chariot-seat synonyms."
    },
    "yuvan": {
        "english": "The ever-youthful.",
        "nirukta": "yauti iti yuvā (he who joins or possesses strength).",
        "vedantic": "The Lord is changeless; He never decays or ages, being ever-youthful.",
        "panini": "Noun 'yuvan'. Accusative singular masculine is 'yuvānam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Youth synonyms.",
        "amara_kosha": "Youth synonyms.",
        "abhidhana_ratnamala": "Youth synonyms."
    },
    "mṛga": {
        "english": "The wild beast / lion.",
        "nirukta": "mṛgyate iti mṛgaḥ (that which is hunted or seeks). In context, a fierce beast like a lion.",
        "vedantic": "The Lord is like a majestic lion, representing supreme strength, independence, and fearlessness.",
        "panini": "Root √mṛg (to seek) + suffix 'ac'. Accusative singular 'mṛgam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Listed under wild beasts/forest animals.",
        "amara_kosha": "Lion/beast synonyms.",
        "abhidhana_ratnamala": "Lion/beast synonyms."
    },
    "na": {
        "english": "Like / as.",
        "nirukta": "A particle of comparison (upamārtha).",
        "vedantic": "Used to compare Rudra's majesty to that of a lion, maintaining He is beyond comparison.",
        "panini": "Avyaya (comparative particle).",
        "case_ending": "Avyaya (particle).",
        "nighantu": "Listed under particles of comparison.",
        "amara_kosha": "Under comparative particles.",
        "abhidhana_ratnamala": "Comparative particles."
    },
    "bhīma": {
        "english": "Fearsome / awesome.",
        "nirukta": "bibheti asmāt iti bhīmaḥ (he from whom everyone fears).",
        "vedantic": "The awesome majesty of the Infinite, which causes the laws of nature to function in fear (bhayādasyāgniḥ...).",
        "panini": "Root √bhī + suffix 'makan' (Uṇādi 1.144). Accusative singular 'bhīmam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Fearsome synonyms.",
        "amara_kosha": "Awesome/fearsome synonyms.",
        "abhidhana_ratnamala": "Fearsome synonyms."
    },
    "upahatnu": {
        "english": "The destroyer / striker.",
        "nirukta": "upa + han + knu. he who strikes from close quarters.",
        "vedantic": "The imminent death or corrective force that stands near to terminate our illusions.",
        "panini": "Prefix 'upa' + root √han + suffix 'knu' (P.3.2.140). Accusative singular 'upahatnum'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Destruction synonyms.",
        "amara_kosha": "Weapon/striking synonyms.",
        "abhidhana_ratnamala": "Killing/destroying synonyms."
    },
    "ugra": {
        "english": "The fierce / mighty one.",
        "nirukta": "ucchyate iti ugraḥ (he who is high, mighty, or terrible).",
        "vedantic": "The terrifying majesty of the ultimate reality when experienced through the ego.",
        "panini": "Root √as (to be) or √uc + 'ran' suffix with irregular changes. Accusative singular 'ugram'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Listed under strong/mighty synonyms.",
        "amara_kosha": "Svargavarga: Shiva's name: 'ugraḥ kapaledhyay'.",
        "abhidhana_ratnamala": "Under Shiva's names."
    },
    "jaritṛ": {
        "english": "To the singer / worshipper.",
        "nirukta": "gṛṇāti stuti-rūpeṇa iti jaritā (he who sings hymns).",
        "vedantic": "The devotee who expresses his inner communion through sacred chants.",
        "panini": "Root √gṛ (to sing) + suffix 'tṛc' with Vedic changes. Dative singular 'jaritre'.",
        "case_ending": "Dative Singular (Caturthī, Masculine).",
        "nighantu": "Worshipper/singer synonyms.",
        "amara_kosha": "Singer/poet synonyms.",
        "abhidhana_ratnamala": "Under singer."
    },
    "stuvāna": {
        "english": "Being praised.",
        "nirukta": "stūyamānaḥ (he who is currently being glorified).",
        "vedantic": "The Lord who is ever-worshipped through all speech and hymns in the cosmos.",
        "panini": "Root √stu + passive/middle participle suffix 'śānac'. Nominative singular 'stuvānaḥ'.",
        "case_ending": "Nominative Singular (Masculine).",
        "nighantu": "Praise synonyms.",
        "amara_kosha": "Under praise.",
        "abhidhana_ratnamala": "Praise synonyms."
    },
    "anya": {
        "english": "Other than / someone else.",
        "nirukta": "Indefinite pronominal base denoting difference.",
        "vedantic": "Refers to the enemies of Dharma, or the ignorance that is external to the Self.",
        "panini": "Pronoun 'anya'. Accusative singular masculine 'anyam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Pronoun class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "vap": {
        "english": "May they strike down / throw.",
        "nirukta": "Derived from root 'vap' meaning to sow, scatter, or throw.",
        "vedantic": "A prayer that the weapons of Rudra strike our internal enemies (ignorance/ego).",
        "panini": "Root √vap (Bhvādi-gaṇa, 1.1159). Vedic imperative third-person plural 'ni-vapantu'.",
        "case_ending": "Verbal form (Imperative, 3rd Plural).",
        "nighantu": "Throwing/scattering synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "sēnā": {
        "english": "Armies / forces.",
        "nirukta": "sināti iti senā (that which binds or is bound together).",
        "vedantic": "The active forces of nature and karma under the command of the Lord.",
        "panini": "Root √si (to bind) + 'na' suffix. Nominative plural 'senāḥ'.",
        "case_ending": "Nominative Plural (Feminine).",
        "nighantu": "Listed under army/warrior synonyms.",
        "amara_kosha": "Kṣatriyavarga: 'senā' (army).",
        "abhidhana_ratnamala": "Army synonyms."
    },
    "pari": {
        "english": "Around / entirely.",
        "nirukta": "A prefix or particle indicating all around or complete avoidance.",
        "vedantic": "Qualifies the prayer that we should be completely spared from calamity.",
        "panini": "Prādi prefix (Upasarga) / Karmapravacanīya.",
        "case_ending": "Avyaya (prefix).",
        "nighantu": "Not listed.",
        "amara_kosha": "Prefix section.",
        "abhidhana_ratnamala": "Not listed."
    },
    "heti": {
        "english": "Weapon / missile.",
        "nirukta": "hinoti iti hetiḥ (that which is thrown to kill/strike).",
        "vedantic": "The weapon of Rudra represents the forces of time and karma that strike down finitude.",
        "panini": "Root √hi (to throw) + suffix 'ktin' (P.3.3.94). Nominative singular 'hetiḥ', nominative plural 'hetayaḥ'.",
        "case_ending": "Nominative Singular / Plural (Feminine).",
        "nighantu": "Listed under weapon synonyms (Nighaṇṭu 2.20).",
        "amara_kosha": "Ayudhavarga: 'heti' (weapon).",
        "abhidhana_ratnamala": "Weapon synonyms."
    },
    "vṛj": {
        "english": "May it avoid / spare.",
        "nirukta": "varjayati iti (may it leave aside).",
        "vedantic": "The prayer that divine wrath bypasses the sincere devotee.",
        "panini": "Root √vṛj (Rudhadhi-gaṇa, 7.0022). Lat third-person singular 'vṛṇaktu' with Vedic imperative sense.",
        "case_ending": "Verbal form (Imperative, 3rd Singular).",
        "nighantu": "Avoiding synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "tveṣa": {
        "english": "Of the glowing / fierce one.",
        "nirukta": "Derived from root 'tviṣ' meaning to shine or glow.",
        "vedantic": "The brilliant, blinding light of truth that is terrifying to the ego.",
        "panini": "Root √tviṣ (Adādi-gaṇa, 2.0069) + 'ghañ' suffix. Genitive singular masculine 'tveṣasya'.",
        "case_ending": "Genitive Singular (Ṣaṣṭhī, Masculine).",
        "nighantu": "Listed under shining/brilliant synonyms.",
        "amara_kosha": "Glowing/shining synonyms.",
        "abhidhana_ratnamala": "Glowing/angry synonyms."
    },
    "durmati": {
        "english": "Ill-will / anger / bad intellect.",
        "nirukta": "duṣṭā matiḥ (corrupted thinking/will).",
        "vedantic": "The terrifying aspect of karma that appears as the wrath of the universe.",
        "panini": "Prādi-bahuvrīhi compound: 'dus' + 'mati'. Nominative singular 'durmatiḥ'.",
        "case_ending": "Nominative Singular (Feminine).",
        "nighantu": "Anger synonyms.",
        "amara_kosha": "Under anger and bad intellect.",
        "abhidhana_ratnamala": "Anger synonyms."
    },
    "aghayu": {
        "english": "Of the sinful / desiring evil.",
        "nirukta": "aghaṃ (sin) icchati iti aghayuḥ.",
        "vedantic": "Those forces or entities that wish harm upon the righteous.",
        "panini": "Noun 'agha' + denominative suffix 'kyac' + 'u'. Genitive plural 'aghayūnām' or genitive singular 'aghayōḥ'.",
        "case_ending": "Genitive Singular (Ṣaṣṭhī, Masculine).",
        "nighantu": "Sinful synonyms.",
        "amara_kosha": "Sinful synonyms.",
        "abhidhana_ratnamala": "Sinful synonyms."
    },
    "ava": {
        "english": "Down / unbend.",
        "nirukta": "Prefix indicating downward direction or relaxation.",
        "vedantic": "The unstringing of the bow represents the transition of Rudra from wrath to peace.",
        "panini": "Prādi prefix.",
        "case_ending": "Avyaya (prefix).",
        "nighantu": "Not listed.",
        "amara_kosha": "Prefix section.",
        "abhidhana_ratnamala": "Not listed."
    },
    "sthira": {
        "english": "Firm / strung.",
        "nirukta": "tiṣṭhati iti sthiraḥ (that which stands firm).",
        "vedantic": "The firm, ready bow of Rudra represents the ever-ready cosmic justice.",
        "panini": "Root √sthā + 'ka' suffix. Accusative plural feminine 'sthiraḥ' / 'sthira' (Vedic).",
        "case_ending": "Accusative Plural (Feminine).",
        "nighantu": "Firmness synonyms.",
        "amara_kosha": "Firm/solid synonyms.",
        "abhidhana_ratnamala": "Solid synonyms."
    },
    "maghavan": {
        "english": "To the patrons / wealthy sacrificers.",
        "nirukta": "magha (wealth/sacrifice) + vat. those who patronize sacrifices.",
        "vedantic": "The generous patrons who maintain the external structures of Dharma.",
        "panini": "Noun 'maghavat'. Ablative plural is 'maghavadbhyaḥ'.",
        "case_ending": "Ablative/Dative Plural (Masculine).",
        "nighantu": "Patron/wealthy synonyms.",
        "amara_kosha": "Indra's name / wealthy patron synonyms.",
        "abhidhana_ratnamala": "Patron synonyms."
    },
    "tan": {
        "english": "Unbend / stretch / unstring.",
        "nirukta": "Derived from root 'tan' meaning to stretch or spread.",
        "vedantic": "The unbending of the bow shows He neutralizes the weapons of karmic retribution.",
        "panini": "Root √tan (Tanādi-gaṇa, 8.0001). Vedic second-person singular imperative 'tanuṣva', first-person plural 'tanmasi'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular / Lat, 1st Plural).",
        "nighantu": "Stretching synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "mīḍhvas": {
        "english": "O showerer of grace / most bountiful.",
        "nirukta": "miḍhati (showers) iti mīḍhvān.",
        "vedantic": "The Lord who showers bliss and material prosperity on the devotees.",
        "panini": "Root √mih + Vedic suffix 'kvasu'. Vocative 'mīḍhvaḥ', superlative vocative 'mīḍhuṣṭama'.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Listed under names of showerer.",
        "amara_kosha": "Bestower/bountiful synonyms.",
        "abhidhana_ratnamala": "Showerer synonyms."
    },
    "manas": {
        "english": "Mind / heart.",
        "nirukta": "manyate aneneti manaḥ (that by which we think).",
        "vedantic": "The internal organ (Antahkarana) that must be purified to reflect the Self.",
        "panini": "Root √man + suffix 'asun'. Nominative singular neuter 'manaḥ'.",
        "case_ending": "Nominative Singular (Neuter).",
        "nighantu": "Mind synonyms.",
        "amara_kosha": "Buddhivarga: 'manaḥ' (mind).",
        "abhidhana_ratnamala": "Mind synonyms."
    },
    "bhū": {
        "english": "Be / become.",
        "nirukta": "bhavati iti (it exists or becomes).",
        "vedantic": "The request that the Lord manifest His benign presence in our lives.",
        "panini": "Root √bhū (Bhvādi-gaṇa, 1.0001). Imperative second-person singular 'bhava'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Existence synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "parama": {
        "english": "In the highest / supreme.",
        "nirukta": "piparti iti paramaḥ (he who fills or transcends).",
        "vedantic": "The transcendent state of reality, beyond the material plane.",
        "panini": "Adjective 'parama'. Locative singular masculine 'parame'.",
        "case_ending": "Locative Singular (Saptamī, Masculine).",
        "nighantu": "Supreme/best synonyms.",
        "amara_kosha": "Supreme synonyms.",
        "abhidhana_ratnamala": "Supreme synonyms."
    },
    "vṛkṣa": {
        "english": "Tree.",
        "nirukta": "vraścati iti vṛkṣaḥ (that which is cut down).",
        "vedantic": "The cosmic tree of Samsara (as mentioned in Kathopanishad/Gita), on which the Lord places His weapons.",
        "panini": "Root √vraśc (to cut) + suffix 'sa' with irregular changes. Locative singular 'vṛkṣe'.",
        "case_ending": "Locative Singular (Saptamī, Masculine).",
        "nighantu": "Listed under tree synonyms (Nighaṇṭu 2.4).",
        "amara_kosha": "Vanaspati-varga: 'vṛkṣo mahīruhaḥ'.",
        "abhidhana_ratnamala": "Tree synonyms."
    },
    "ayudha": {
        "english": "Weapon.",
        "nirukta": "yudhyate anena iti āyudham.",
        "vedantic": "The instruments of cosmic destruction, placed away when He becomes peaceful.",
        "panini": "Prefix 'ā' + root √yudh + suffix 'ghañ' in the sense of instrument. Accusative singular 'āyudham'.",
        "case_ending": "Accusative Singular (Dvitīyā, Neuter).",
        "nighantu": "Listed under weapon synonyms (Nighaṇṭu 2.20).",
        "amara_kosha": "Ayudhavarga: 'āyudham' (weapon).",
        "abhidhana_ratnamala": "Weapon synonyms."
    },
    "ni-dhā": {
        "english": "Placing / putting down.",
        "nirukta": "ni + dhā + lyap. placing aside.",
        "vedantic": "Placing aside the weapons signifies the withdrawal of the cosmic dissolution phase.",
        "panini": "Prefix 'ni' + root √dhā + gerund suffix 'lyap' (P.7.1.37).",
        "case_ending": "Gerund (Indeclinable participle).",
        "nighantu": "Placing synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "kṛttim": {
        "english": "Deerskin / animal skin.",
        "nirukta": "kṛtyate iti kṛttiḥ (that which is peeled or cut).",
        "vedantic": "The tiger skin or deerskin worn by Shiva, representing His control over raw animal nature.",
        "panini": "Root √kṛt (to cut) + suffix 'ktin'. Accusative singular 'kṛttim'.",
        "case_ending": "Accusative Singular (Dvitīyā, Feminine).",
        "nighantu": "Listed under skin/leather synonyms.",
        "amara_kosha": "Leather/hide synonyms.",
        "abhidhana_ratnamala": "Skin/hide synonyms."
    },
    "vas": {
        "english": "Wearing / clad in.",
        "nirukta": "vaste iti vasānaḥ (he who wears).",
        "vedantic": "Wearing the skin represents Shiva's identity as the supreme ascetic.",
        "panini": "Root √vas (Adādi-gaṇa, 2.0013) + middle participle 'śānac'. Nominative singular 'vasānaḥ'.",
        "case_ending": "Nominative Singular (Masculine).",
        "nighantu": "Wearing synonyms.",
        "amara_kosha": "Garment class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "ā": {
        "english": "Towards / completely.",
        "nirukta": "A particle indicating direction or completeness.",
        "vedantic": "Qualifies the movement of the Lord towards the devotee.",
        "panini": "Prādi prefix.",
        "case_ending": "Avyaya (prefix).",
        "nighantu": "Not listed.",
        "amara_kosha": "Prefix section.",
        "abhidhana_ratnamala": "Not listed."
    },
    "car": {
        "english": "Walk / move.",
        "nirukta": "carati iti (he who moves or acts).",
        "vedantic": "The dynamic movement of the Divine in the world to protect the good.",
        "panini": "Root √car (Bhvādi-gaṇa, 1.0983). Imperative second-person singular 'cara' / 'ā-cara'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Movement synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "pināka": {
        "english": "The Pināka bow.",
        "nirukta": "pinasti iti pinākam (that which crushes or destroys enemies).",
        "vedantic": "Shiva's divine bow, which represents the cosmic laws that crush ignorance.",
        "panini": "Uṇādi-derived noun. Accusative singular 'pinākam'.",
        "case_ending": "Accusative Singular (Dvitīyā, Masculine/Neuter).",
        "nighantu": "Shiva's bow synonyms.",
        "amara_kosha": "Ayudhavarga: 'pināko'stryavadhūr-धनुः' (defining Pināka as Shiva's bow).",
        "abhidhana_ratnamala": "Shiva's bow synonyms."
    },
    "bhṛ": {
        "english": "Bearing / holding.",
        "nirukta": "bibharti iti bibhrat (he who holds).",
        "vedantic": "Bearing the bow Pināka, but keeping it unstrung, showing a state of peaceful readiness.",
        "panini": "Root √bhṛ + active participle 'śatṛ'. Nominative singular masculine is 'bibhrat'.",
        "case_ending": "Nominative Singular (Masculine).",
        "nighantu": "Bearing synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "gam": {
        "english": "Come.",
        "nirukta": "gacchati iti (he who goes or comes).",
        "vedantic": "The invocation to the Divine to manifest in our direct experience.",
        "panini": "Root √gam (Bhvādi-gaṇa, 1.1137). Imperative second-person singular with augment 'ā-gahi'.",
        "case_ending": "Verbal form (Imperative, 2nd Singular).",
        "nighantu": "Movement synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "vikirida": {
        "english": "O showerer / O dispeller (of sin/disease).",
        "nirukta": "vikirati duḥkham iti vikiridaḥ (he who scatters or dispels suffering).",
        "vedantic": "The Lord as the active dispeller of spiritual obstacles and biological ailments.",
        "panini": "Prefix 'vi' + root √kṛ (to scatter) + 'dā' suffix. Vocative singular.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Dispeller synonyms.",
        "abhidhana_ratnamala": "Dispeller synonyms."
    },
    "bhagavas": {
        "english": "O Lord / O worshipful one.",
        "nirukta": "bhaga (majesty/opulence) + matup. he who possesses all six divine opulences.",
        "vedantic": "Addressing Shiva as the supreme Lord of all creations.",
        "panini": "Noun 'bhagavat'. Vocative singular is 'bhagavaḥ' / 'bhagavo'.",
        "case_ending": "Vocative Singular (Sambodhana, Masculine).",
        "nighantu": "Lord synonyms.",
        "amara_kosha": "Worshipful/lord synonyms.",
        "abhidhana_ratnamala": "Lord synonyms."
    },
    "sahasra": {
        "english": "Thousand / countless.",
        "nirukta": "sahasra-saṅkhyāka (possessing a thousand or infinite count).",
        "vedantic": "Represents the infinite nature of the Divine manifestations.",
        "panini": "Numeral noun. Accusative singular 'sahasram', nominative plural 'sahasrāņi'.",
        "case_ending": "Numeral.",
        "nighantu": "Listed under numbers.",
        "amara_kosha": "Saṅkhyā-varga: 'sahasram'.",
        "abhidhana_ratnamala": "Numeral synonyms."
    },
    "sahasraśas": {
        "english": "In thousands / in countless groups.",
        "nirukta": "sahasra-vṛttyā (multiplying in thousands).",
        "vedantic": "The infinite multiplication of divine energies in all directions.",
        "panini": "Noun 'sahasra' + distributive adverbial suffix 'śaḥ' (P.5.4.42).",
        "case_ending": "Avyaya (distributive adverb).",
        "nighantu": "Not listed.",
        "amara_kosha": "Distributive numerals.",
        "abhidhana_ratnamala": "Not listed."
    },
    "bhūmi": {
        "english": "On the earth.",
        "nirukta": "bhavanti bhūtāni asyām iti bhūmiḥ (the ground where all beings exist).",
        "vedantic": "The physical plane of existence where Jivas undergo their karmic evolution.",
        "panini": "Noun 'bhūmi'. Locative singular is 'bhūmyām'.",
        "case_ending": "Locative Singular (Saptamī, Feminine).",
        "nighantu": "Listed under earth synonyms (Nighaṇṭu 1.1).",
        "amara_kosha": "Bhūmivarga (2.1.1): 'bhūmir bhūmiś ca dharā'.",
        "abhidhana_ratnamala": "Earth synonyms."
    },
    "sahasrayōjana": {
        "english": "At a distance of a thousand yojanas (leagues).",
        "nirukta": "sahasre yojane (at a distance of 1000 yojanas).",
        "vedantic": "Praying that the weapons of dissolution remain infinitely far away from the devotee.",
        "panini": "Locative compound: 'sahasra' + 'yojana' (a measure of 8-9 miles). Locative singular.",
        "case_ending": "Locative Singular (Saptamī, Neuter).",
        "nighantu": "Not listed.",
        "amara_kosha": "Distance measurements.",
        "abhidhana_ratnamala": "Distance synonyms."
    },
    "dhanvan": {
        "english": "Bows.",
        "nirukta": "dhanvati iti dhanva (that which moves or releases arrows).",
        "vedantic": "The cosmic bows of the various Rudras that enforce the laws of karma.",
        "panini": "Vedic noun 'dhanvan'. Accusative plural is 'dhanvāni'.",
        "case_ending": "Accusative Plural (Dvitīyā, Neuter).",
        "nighantu": "Listed under bow synonyms (Nighaṇṭu 2.20).",
        "amara_kosha": "Ayudhavarga: 'dhanuḥ' / 'dhanva'.",
        "abhidhana_ratnamala": "Bow synonyms."
    },
    # Anuvakam 11 stems
    "arṇava": {
        "english": "In the ocean.",
        "nirukta": "arṇasaḥ (of water) samūhaḥ arṇavaḥ (the ocean or great water-mass).",
        "vedantic": "The vast ocean of Samsara, or the cosmic waters of creation.",
        "panini": "Noun 'arṇas' (water) + 'va' suffix (P.5.2.109). Locative singular 'arṇave'.",
        "case_ending": "Locative Singular (Saptamī, Masculine).",
        "nighantu": "Listed under ocean/water synonyms (Nighaṇṭu 1.12).",
        "amara_kosha": "Vārivarga (1.10.1): 'arṇavo dharṇo dhiśca'.",
        "abhidhana_ratnamala": "Ocean synonyms."
    },
    "antarikṣa": {
        "english": "In the atmosphere / intermediate region.",
        "nirukta": "antarā ikṣyate iti antarikṣam (that which is seen between heaven and earth).",
        "vedantic": "The subtle plane of existence (Prāṇamaya/Manomaya sheaths).",
        "panini": "Locative compound. Locative singular 'antarikṣe'.",
        "case_ending": "Locative Singular (Saptamī, Neuter).",
        "nighantu": "Listed under names of sky (Nighaṇṭu 1.3).",
        "amara_kosha": "Svargavarga: 'antarikṣam gaganādivam' (atmosphere).",
        "abhidhana_ratnamala": "Atmosphere/sky synonyms."
    },
    "bhava": {
        "english": "Bhavas / Rudras (manifestations of Shiva).",
        "nirukta": "bhavanti bhūtāni asmāt iti bhavaḥ (the source of all existence).",
        "vedantic": "The aspect of Shiva that brings forth the manifest universe; here addressed in the plural.",
        "panini": "Root √bhū + 'ghañ' suffix. Nominative plural 'bhavāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Lord synonyms.",
        "amara_kosha": "Svargavarga: Shiva's name: 'bhavaḥ śarvo haro rudraḥ'.",
        "abhidhana_ratnamala": "Under Shiva's names."
    },
    "nīlagrīva": {
        "english": "Blue-necked ones.",
        "nirukta": "nīlā grīvā yeṣāṃ te nīlagrīvāḥ.",
        "vedantic": "Those who contain the poison of worldliness in their throats, saving the universe.",
        "panini": "Bahuvrīhi compound: 'nīla' + 'grīvā'. Nominative plural masculine 'nīlagrīvāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Under Shiva's attributes.",
        "abhidhana_ratnamala": "Shiva's attributes."
    },
    "śitikaṇṭha": {
        "english": "White-necked ones / dark-necked.",
        "nirukta": "śitiḥ (white or dark blue) kaṇṭhaḥ yeṣāṃ te śitikaṇṭhāḥ.",
        "vedantic": "The neck region showing both the light of pure consciousness and the dark spot of poison.",
        "panini": "Bahuvrīhi compound: 'śiti' + 'kaṇṭha'. Nominative plural masculine 'śitikaṇṭhāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Shiva's attributes.",
        "abhidhana_ratnamala": "Shiva's attributes."
    },
    "śarva": {
        "english": "Sharvas / destroyers.",
        "nirukta": "śṛṇāti iti śarvaḥ (he who destroys or injures evil).",
        "vedantic": "The aspect of Shiva that destroys the finite creation during dissolution.",
        "panini": "Root √śṛ + 'van' suffix with Vedic changes. Nominative plural 'śarvāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Atmospheric deities.",
        "amara_kosha": "Svargavarga: Shiva's name.",
        "abhidhana_ratnamala": "Under Shiva's names."
    },
    "adhas": {
        "english": "Below / in the lower regions.",
        "nirukta": "Vedic indeclinable indicating downward direction.",
        "vedantic": "Presiding over the nether worlds (Pātāla, etc.) and the lower energy centers (Mūlādhāra).",
        "panini": "Avyaya (adverb).",
        "case_ending": "Avyaya (adverb).",
        "nighantu": "Downward direction synonyms.",
        "amara_kosha": "Avyayavarga: Below adverb.",
        "abhidhana_ratnamala": "Below synonyms."
    },
    "kṣamācara": {
        "english": "Roaming on the earth / ground.",
        "nirukta": "kṣamāyāṃ (on earth) caranti iti kṣamācarāḥ.",
        "vedantic": "Those spiritual forces that walk on the physical plane to protect seekers.",
        "panini": "Locative compound: 'kṣamā' + root √car + 'a' suffix. Nominative plural 'kṣamācarāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Earth-roamers synonyms.",
        "abhidhana_ratnamala": "Not listed."
    },
    "div": {
        "english": "In heaven.",
        "nirukta": "divyati iti dyuḥ (the shining sky or heavenly plane).",
        "vedantic": "The causal plane of existence (Kāraṇa-śarīra / Svar-loka).",
        "panini": "Consonant noun 'div'. Locative singular 'divi', accusative 'divam'.",
        "case_ending": "Locative / Accusative Singular (Feminine).",
        "nighantu": "Listed under names of sky (Nighaṇṭu 1.3).",
        "amara_kosha": "Svargavarga: 'dyu' / 'divam' (heaven).",
        "abhidhana_ratnamala": "Heaven synonyms."
    },
    "upāśrita": {
        "english": "Residing in / taking refuge.",
        "nirukta": "upa + ā + śri + kta. those who have taken seat in.",
        "vedantic": "The various deities and powers that reside in the celestial spheres.",
        "panini": "Prefixes 'upa' + 'ā' + root √śri + suffix 'kta'. Nominative plural 'upāśritāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Residing synonyms.",
        "amara_kosha": "Refuge synonyms.",
        "abhidhana_ratnamala": "Not listed."
    },
    "saspiñjara": {
        "english": "Golden-yellow / yellow-green like young grass.",
        "nirukta": "śaspa (young grass) + piñjara (golden-yellow).",
        "vedantic": "The Lord's body glowing like fresh vegetation, representing growth and vital force.",
        "panini": "Compound: 'śaspa' + 'piñjara' with Vedic vowel change. Nominative plural masculine 'saspiñjarāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Green-yellow color synonyms.",
        "amara_kosha": "Color/foliage synonyms.",
        "abhidhana_ratnamala": "Under color names."
    },
    "bhūta": {
        "english": "Of spirits / living beings.",
        "nirukta": "bhavanti bhūtāni (those who have come to exist).",
        "vedantic": "All creatures, including invisible spirits and elemental forces, ruled by Shiva (Bhūtānātha).",
        "panini": "Root √bhū + suffix 'kta'. Genitive plural is 'bhūtānām'.",
        "case_ending": "Genitive Plural (Ṣaṣṭhī, Masculine/Neuter).",
        "nighantu": "Listed under beings.",
        "amara_kosha": "Under spirits/beings: 'bhūtaṃ kṣmādau'.",
        "abhidhana_ratnamala": "Beings/spirits synonyms."
    },
    "adhipati": {
        "english": "Lords / rulers.",
        "nirukta": "adhikaḥ patiḥ adhipatiḥ (supreme master).",
        "vedantic": "The Lords of the elemental spirits, governing under the supreme command.",
        "panini": "Prefix 'adhi' + noun 'pati'. Nominative plural is 'adhipatayaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Lord/ruler synonyms.",
        "amara_kosha": "Ruler/master synonyms.",
        "abhidhana_ratnamala": "Ruler synonyms."
    },
    "viśikha": {
        "english": "Shaven-headed / without top-knot.",
        "nirukta": "viśatā śikhā yasya saḥ (without a śikhā/hair).",
        "vedantic": "Represents the sannyāsa state (ascetic monks), who have shaved their heads.",
        "panini": "Bahuvrīhi compound: 'vi' (devoid of) + 'śikhā' (top-knot). Nominative plural masculine 'viśikhāsaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Not listed.",
        "amara_kosha": "Shaven/ascetic synonyms.",
        "abhidhana_ratnamala": "Ascetic synonyms."
    },
    "anna": {
        "english": "In the foods.",
        "nirukta": "adyate iti annam (that which is eaten by living beings).",
        "vedantic": "The physical food that sustains the body; He is present as the digestive power (Vaiśvānara).",
        "panini": "Root √ad + suffix 'kta' with irregular changes (P.8.2.42). Locative plural 'anneṣu'.",
        "case_ending": "Locative Plural (Saptamī, Neuter).",
        "nighantu": "Listed under food synonyms (Nighaṇṭu 2.7).",
        "amara_kosha": "Annayovarga: 'annam' (food).",
        "abhidhana_ratnamala": "Food synonyms."
    },
    "vividh": {
        "english": "They pierce / strike.",
        "nirukta": "vividhyanti (strike or pierce in various ways).",
        "vedantic": "Represent the diseases and imbalances that afflict the body due to wrong eating.",
        "panini": "Prefix 'vi' + root √vyadh (to pierce, Divādi-gaṇa, 4.0078). Lat third-person plural 'vividhyanti'.",
        "case_ending": "Verbal form (Lat, 3rd Plural).",
        "nighantu": "Striking/piercing synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "pātra": {
        "english": "In the vessels / drinking cups.",
        "nirukta": "pīyate asmin iti pātram (that in which liquids are drunk).",
        "vedantic": "The vessels of life; He is present in the liquids we consume (milk, water).",
        "panini": "Root √pā (to drink) + suffix 'ṣṭran' (P.3.2.182). Locative plural 'pātreṣu'.",
        "case_ending": "Locative Plural (Saptamī, Neuter).",
        "nighantu": "Vessel synonyms.",
        "amara_kosha": "Household vessels synonyms.",
        "abhidhana_ratnamala": "Vessel synonyms."
    },
    "pā": {
        "english": "Drinking / those who drink.",
        "nirukta": "pibati iti piban (he who drinks).",
        "vedantic": "Addressing the Jivas while they consume water or milk; He is the consumer as well.",
        "panini": "Root √pā + active participle 'śatṛ'. Accusative plural masculine 'pibataḥ'.",
        "case_ending": "Accusative Plural (Dvitīyā, Masculine).",
        "nighantu": "Drinking synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "jana": {
        "english": "People / living beings.",
        "nirukta": "jāyante iti janāḥ (those who are born).",
        "vedantic": "The collection of individual Jivas in the world.",
        "panini": "Root √jan (to be born) + suffix 'ac'. Accusative plural 'janān'.",
        "case_ending": "Accusative Plural (Dvitīyā, Masculine).",
        "nighantu": "Listed under man/human synonyms.",
        "amara_kosha": "Human synonyms: 'manuṣyā mānuṣā janāḥ'.",
        "abhidhana_ratnamala": "People synonyms."
    },
    "pathin": {
        "english": "Of the paths / roads.",
        "nirukta": "panthāḥ (roads for traveling).",
        "vedantic": "The paths of action (Karma-mārga) and knowledge (Jñāna-mārga).",
        "panini": "Consonant noun 'pathin'. Genitive plural 'pathām'.",
        "case_ending": "Genitive Plural (Ṣaṣṭhī, Masculine).",
        "nighantu": "Listed under path synonyms.",
        "amara_kosha": "Road/path synonyms.",
        "abhidhana_ratnamala": "Path synonyms."
    },
    "pathirakṣi": {
        "english": "The protectors of the paths.",
        "nirukta": "pathām rakṣinaḥ (those who guard the paths).",
        "vedantic": "Those spiritual guardians who protect the path of righteousness from evil obstacles.",
        "panini": "Compound: 'pathi' + root √rakṣ + 'ini' suffix. Nominative plural 'pathirakṣayaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Protector synonyms.",
        "amara_kosha": "Protector synonyms.",
        "abhidhana_ratnamala": "Guardian synonyms."
    },
    "ailabruda": {
        "english": "The food-givers / strength-bearers.",
        "nirukta": "elām (food/strength) bibhrati iti ailabṛdāḥ.",
        "vedantic": "The cosmic forces that provide physical food and vital energy to the travelers.",
        "panini": "Vedic derivative compound. Nominative plural 'ailabṛdāḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Food-giver synonyms.",
        "amara_kosha": "Provider synonyms.",
        "abhidhana_ratnamala": "Not listed."
    },
    "yavyudh": {
        "english": "The fighters / repellers of sinners.",
        "nirukta": "yauvanti papinaḥ iti yavyudhaḥ (those who fight and repel the sinful).",
        "vedantic": "The cosmic protectors who prevent the unworthy from accessing the sacred path.",
        "panini": "Vedic compound. Nominative plural 'yavyudhaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Warrior synonyms.",
        "amara_kosha": "Fighter/soldier synonyms.",
        "abhidhana_ratnamala": "Warrior synonyms."
    },
    "tīrtha": {
        "english": "The holy fords / water crossings.",
        "nirukta": "taranti anena iti tīrtham (the place where one crosses over a river or Samsara).",
        "vedantic": "The sacred pilgrimage places (Kashi, Prayaga) and the inner crossings of consciousness.",
        "panini": "Root √tṛ (to cross) + Uṇādi suffix 'thak'. Accusative plural 'tīrthāni'.",
        "case_ending": "Accusative Plural (Dvitīyā, Neuter).",
        "nighantu": "Listed under water/ford synonyms.",
        "amara_kosha": "Holy place/water synonyms: 'tīrthaṃ śāstrādhvararṣiju'.",
        "abhidhana_ratnamala": "Holy place synonyms."
    },
    "pra-car": {
        "english": "They roam about / protect.",
        "nirukta": "pra + caranti (they move about diligently).",
        "vedantic": "The active movement of the guardians to ensure the sanctity of pilgrimage places.",
        "panini": "Prefix 'pra' + root √car. Lat third-person plural 'pracaranti'.",
        "case_ending": "Verbal form (Lat, 3rd Plural).",
        "nighantu": "Movement synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "sṛkāvant": {
        "english": "Bearing missiles/sharp fangs.",
        "nirukta": "sṛka (missile or fang) + matup. those who hold sharp weapons.",
        "vedantic": "The sharp, cutting edge of cosmic laws that strike down the impure.",
        "panini": "Noun 'sṛka' + possessive suffix 'matup' (Vedic 'vant'). Nominative plural masculine 'sṛkāvantaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Weapon-bearer synonyms.",
        "amara_kosha": "Weapon-bearer synonyms.",
        "abhidhana_ratnamala": "Under weapons."
    },
    "niṣaṅgin": {
        "english": "Bearing swords / quivers.",
        "nirukta": "niṣaṅgaḥ (quiver/sword) asya asti iti niṣaṅgī.",
        "vedantic": "The well-equipped guardians of truth, representing complete spiritual armament.",
        "panini": "Noun 'niṣaṅga' + suffix 'ini'. Nominative plural masculine 'niṣaṅgiṇaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Weapon-bearer synonyms.",
        "amara_kosha": "Under quiver/sword bearers.",
        "abhidhana_ratnamala": "Quiver-bearer synonyms."
    },
    "etāvant": {
        "english": "As many as these.",
        "nirukta": "etad + vat. this many.",
        "vedantic": "Points to the infinite number of Rudras mentioned in the hymn.",
        "panini": "Pronoun base 'etad' + suffix 'vatup'. Nominative plural masculine 'etāvantaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Distributive pronouns.",
        "amara_kosha": "Pronoun class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "bhūyas": {
        "english": "Even more than that / more numerous.",
        "nirukta": "Derived from root 'bhū' + iyasun. greater in number.",
        "vedantic": "Indicates that the manifestations of the Divine are beyond any limit or count.",
        "panini": "Comparative suffix 'iyasun' on root √bhū. Nominative plural masculine 'bhūyāṃsaḥ'.",
        "case_ending": "Nominative Plural (Masculine).",
        "nighantu": "Abundance synonyms.",
        "amara_kosha": "Under abundance/more.",
        "abhidhana_ratnamala": "Abundance synonyms."
    },
    "diś": {
        "english": "Directions / quarters.",
        "nirukta": "diśanti pradeśān iti diśaḥ (that which points out regions).",
        "vedantic": "The spatial dimensions of the universe, all filled by the Lord.",
        "panini": "Noun 'diś'. Accusative plural is 'diśaḥ'.",
        "case_ending": "Accusative Plural (Dvitīyā, Feminine).",
        "nighantu": "Listed under directions (diśā-nāmāni, Nighaṇṭu 1.6).",
        "amara_kosha": "Digvarga: 'diśastu kakubhaḥ kāṣṭhāḥ'.",
        "abhidhana_ratnamala": "Directions synonyms."
    },
    "vi-tasth": {
        "english": "They have spread out / pervaded.",
        "nirukta": "vi + tasthire (pervaded all around).",
        "vedantic": "The omnipresence of Rudra, filling all directions of space.",
        "panini": "Prefix 'vi' + root √sthā + Liṭ third-person plural middle 'vi-tasthire'.",
        "case_ending": "Verbal form (Liṭ, 3rd Plural Middle).",
        "nighantu": "Pervading synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "daśa": {
        "english": "Ten / ten fingers/salutations.",
        "nirukta": "daśan-saṅkhyāka.",
        "vedantic": "Representing the ten directions, or full surrender with all ten fingers folded.",
        "panini": "Numeral 'daśan'. Nominative plural 'daśa'.",
        "case_ending": "Numeral.",
        "nighantu": "Listed under numbers.",
        "amara_kosha": "Saṅkhyā-varga: 'daśan'.",
        "abhidhana_ratnamala": "Numeral synonyms."
    },
    "prācī": {
        "english": "East / eastward-facing.",
        "nirukta": "prāñc (forward/east).",
        "vedantic": "Facing the rising sun, representing the dawn of wisdom.",
        "panini": "Feminine form of 'prāñc'. Accusative plural feminine 'prācīḥ'.",
        "case_ending": "Accusative Plural (Feminine).",
        "nighantu": "Listed under directions.",
        "amara_kosha": "East direction synonyms.",
        "abhidhana_ratnamala": "East synonyms."
    },
    "dakṣiṇā": {
        "english": "South / southward-facing.",
        "nirukta": "dakṣiṇa (right side or south).",
        "vedantic": "Facing the south, the direction of Yama (death/justice).",
        "panini": "Feminine form of 'dakṣiṇa'. Accusative plural 'dakṣiṇāḥ'.",
        "case_ending": "Accusative Plural (Feminine).",
        "nighantu": "Listed under directions.",
        "amara_kosha": "South direction synonyms.",
        "abhidhana_ratnamala": "South synonyms."
    },
    "pratīcī": {
        "english": "West / westward-facing.",
        "nirukta": "pratyac (backward/west).",
        "vedantic": "Facing the west, representing the setting sun and reflection.",
        "panini": "Feminine form of 'pratyac'. Accusative plural 'pratīcīḥ'.",
        "case_ending": "Accusative Plural (Feminine).",
        "nighantu": "Listed under directions.",
        "amara_kosha": "West direction synonyms.",
        "abhidhana_ratnamala": "West synonyms."
    },
    "udīcī": {
        "english": "North / northward-facing.",
        "nirukta": "udañc (upward/north).",
        "vedantic": "Facing the north, the direction of Shiva (Himalayas) and liberation.",
        "panini": "Feminine form of 'udañc'. Accusative plural 'udīcīḥ'.",
        "case_ending": "Accusative Plural (Feminine).",
        "nighantu": "Listed under directions.",
        "amara_kosha": "North direction synonyms.",
        "abhidhana_ratnamala": "North synonyms."
    },
    "ūrdhvā": {
        "english": "Upward / upward-facing.",
        "nirukta": "ūrdhva (above/zenith).",
        "vedantic": "Facing the zenith, representing the transcendent realm of pure consciousness.",
        "panini": "Feminine form of 'ūrdhva'. Accusative plural 'ūrdhvāḥ'.",
        "case_ending": "Accusative Plural (Feminine).",
        "nighantu": "Listed under directions.",
        "amara_kosha": "Zenith synonyms.",
        "abhidhana_ratnamala": "Zenith synonyms."
    },
    "vāṭa": {
        "english": "Wind / atmosphere.",
        "nirukta": "vāti iti vātaḥ (that which blows).",
        "vedantic": "The vital air (Prana) that regulates the breath of the cosmos.",
        "panini": "Root √vā (to blow) + 'tan' suffix with augment. Nominative singular 'vātaḥ'.",
        "case_ending": "Nominative Singular (Masculine).",
        "nighantu": "Listed under wind synonyms (Nighaṇṭu 1.15).",
        "amara_kosha": "Vāyuvarga (1.3.1): 'vāto vāyuḥ marut'.",
        "abhidhana_ratnamala": "Wind synonyms."
    },
    "varṣa": {
        "english": "Rain / rainfall.",
        "nirukta": "varṣati iti varṣam (that which pours or rains).",
        "vedantic": "The rainfall that nourishes the earth, acting as the blessing of the heavens.",
        "panini": "Root √vṛṣ (to rain) + 'ghañ' suffix. Nominative/Accusative singular 'varṣam'.",
        "case_ending": "Nominative/Accusative Singular (Neuter).",
        "nighantu": "Listed under cloud/rain synonyms.",
        "amara_kosha": "Cloud/rain synonyms.",
        "abhidhana_ratnamala": "Rain synonyms."
    },
    "dviṣ": {
        "english": "We hate.",
        "nirukta": "dveṣṭi iti dveṣaḥ (he who hates).",
        "vedantic": "The lower emotions of hatred and duality that must be surrendered.",
        "panini": "Root √dviṣ (Adādi-gaṇa, 2.0004). Lat first-person plural 'dviṣmaḥ' / 'dviṣmaḥ'.",
        "case_ending": "Verbal form (Lat, 1st Plural).",
        "nighantu": "Hatred synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "dves": {
        "english": "Hates.",
        "nirukta": "dveṣaḥ (aversion/hatred).",
        "vedantic": "Those external entities or internal impulses that exhibit aversion to the good.",
        "panini": "Root √dviṣ. Lat third-person singular 'dveṣṭi'.",
        "case_ending": "Verbal form (Lat, 3rd Singular).",
        "nighantu": "Aversion synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    },
    "jambha": {
        "english": "In the open mouth / jaws.",
        "nirukta": "jambhante dantaḥ atra iti jambhaḥ (the jaws or gaping mouth).",
        "vedantic": "The devouring mouth of cosmic time (Kāla), where all dualities and enemies are consumed.",
        "panini": "Root √jabh + 'ghañ'. Locative singular is 'jambhe'.",
        "case_ending": "Locative Singular (Saptamī, Masculine).",
        "nighantu": "Mouth/jaw synonyms.",
        "amara_kosha": "Tooth/jaw synonyms.",
        "abhidhana_ratnamala": "Jaw/mouth synonyms."
    },
    "dadh": {
        "english": "I place / surrender.",
        "nirukta": "dadhāti iti (he who places or holds).",
        "vedantic": "Placing the enemy of our soul (ego) into the jaws of cosmic time, releasing ourselves.",
        "panini": "Root √dhā (Juhotyādi-gaṇa, 3.0010). Lat first-person singular 'dadhāmi'.",
        "case_ending": "Verbal form (Lat, 1st Singular).",
        "nighantu": "Placing/giving synonyms.",
        "amara_kosha": "Verb class.",
        "abhidhana_ratnamala": "Not listed."
    }
}

# Mapping of Sanskrit word strings to their base stem keys
WORD_TO_STEM = {
    # Anuvakam 9
    "नमः": "namas", "नमो": "namas", "नमो॒": "namas", "नमः॑": "namas", "नमो॑": "namas", "नमो᳚": "namas",
    "च": "ca", "च॒": "ca",
    "इरिण्याय": "iriṇya", "इरि॒ण्या॑य": "iriṇya",
    "प्रपथ्याय": "prapathya", "प्र॒-प॒थ्या॑य": "prapathya",
    "किंशिलाय": "kiṃśila", "कि॒म्-शि॒लाय॑": "kiṃśila",
    "क्षयणाय": "kṣayaṇa", "क्षय॑णाय": "kṣayaṇa",
    "कपर्दिने": "kapardin", "क॒प॒र्दिने᳚": "kapardin",
    "पुलस्तये": "pulasti", "पु॒ल॒स्तये॑": "pulasti",
    "गोष्ठ्याय": "gōṣṭhya", "गोष्ठ्या॑य": "gōṣṭhya",
    "गृह्याय": "gṛhya", "गृह्या॑य": "gṛhya",
    "तल्प्याय": "talpya", "तल्प्या॑य": "talpya",
    "गेह्याय": "gēhya", "गेह्या॑य": "gēhya",
    "काट्याय": "kāṭya", "का॒ट्या॑य": "kāṭya",
    "गह्वरेष्ठाय": "gahvarēṣṭha", "ग॒ह्व॒रे॒-ष्ठाय॑": "gahvarēṣṭha",
    "ह्रदय्याय": "hṛdayya", "ह्र॒द॒य्या॑य": "hṛdayya",
    "निवेष्प्याय": "nivēṣpya", "नि॒-वे॒ष्प्या॑य": "nivēṣpya",
    "पांसव्याय": "pāṃsavya", "पां॒स॒व्या॑य": "pāṃsavya",
    "रजस्याय": "rajasya", "र॒ज॒स्या॑य": "rajasya",
    "शुष्क्याय": "śuṣkya", "शुष्क्या॑य": "śuṣkya",
    "हरित्याय": "haritya", "ह॒रि॒त्या॑य": "haritya",
    "लोप्याय": "lōpya", "लोप्या॑य": "lōpya",
    "उलप्याय": "ulapya", "उ॒ल॒प्या॑य": "ulapya",
    "ऊर्व्याय": "ūrvya", "ऊ॒र्व्या॑य": "ūrvya",
    "सूर्म्याय": "sūrmya", "सू॒र्म्या॑य": "sūrmya",
    "पर्ण्याय": "parṇya", "प॒र्ण्या॑य": "parṇya",
    "पर्णशद्याय": "parṇaśadya", "प॒र्ण॒-श॒द्या॑य": "parṇaśadya",
    "अपगुरमाणाय": "apaguramāṇa", "अ॒प॒-गु॒रमा॑णाय": "apaguramāṇa",
    "अभिघ्नते": "abhighnat", "अ॒भि-घ्न॒ते": "abhighnat",
    "आक्खिदते": "ākkhidat", "आ-ख्खि॒द॒ते": "ākkhidat",
    "प्रख्खिदते": "prakkhidat", "प्र-ख्खि॒द॒ते": "prakkhidat",
    "वः": "vas", "वः॒": "vas",
    "किरिकेभ्यः": "kirika", "कि॒रि॒केभ्यः॑": "kirika",
    "देवान्": "deva", "देवानाम्": "deva", "दे॒वाना᳚म्": "deva",
    "हृदयेभ्यः": "hṛdaya", "हृद॑येभ्यः": "hṛdaya",
    "विक्षीणाकेभ्यः": "vikṣīṇaka", "वि॒-क्षी॒ण॒केभ्यः॑": "vikṣīṇaka",
    "विक्षीणकेभ्यः": "vikṣīṇaka",
    "विचिन्वत्केभ्यः": "vicinvatka", "वि॒-चि॒न्व॒त्केभ्यः॑": "vicinvatka",
    "आनिर्हतेभ्यः": "ānihrita", "आ-नि॒र्-ह॒तेभ्यः॑": "ānihrita",
    "आमीवत्केभ्यः": "āmīvatka", "आ-मी॒व॒त्केभ्यः॑": "āmīvatka",

    # Anuvakam 10
    "द्रापे": "drāpi", "द्रापे॒": "drāpi",
    "अन्धसः": "andhas", "अन्ध॑सः": "andhas",
    "पते": "pati", "प॒ते॒": "pati",
    "दरिद्रत्": "daridrat", "दरि॑द्रत्": "daridrat",
    "नीललोहित": "nīlalōhita", "नील॑-लोहित": "nīlalōhita", "नील॑लोहित": "nīlalōhita",
    "एषाम्": "idam", "ए॒षा॒म्": "idam", "ए॒षा-म्": "idam", "ए॒षा॒-ङ्": "idam", "तम्": "tad", "तं-वो": "tad",
    "पुरुषणााम्": "puruṣa", "पुरु॑षणााम्": "puruṣa", "पुरु॑षाणाम्": "puruṣa",
    "पशूनाम्": "paśu", "प॒शू॒नाम्": "paśu",
    "मा": "mā", "मो": "mā", "माः": "mā",
    "भेः": "bhī",
    "अरः": "rī", "अरो": "rī",
    "किञ्चन": "kiñcana", "किञ्च॒न": "kiñcana", "किञ्च॒नाम॑मत्": "kiñcana",
    "आममत्": "am", "आम॑मत्": "am",
    "या": "yad", "याः": "yad", "यास्ते": "yad",
    "ते": "yushman", "ते॒": "yushman", "तव": "yushman", "तव॑": "yushman",
    "रुद्र": "rudra", "रु॒द्र॒": "rudra", "रुद्राय": "rudra", "रु॒द्राय॑": "rudra", "रुद्रस्य": "rudra", "रु॒द्रस्य॑": "rudra",
    "शिवा": "śiva", "शि॒वा": "śiva", "शिवतः": "śiva", "शिवः": "śiva", "शि॒वः": "śiva", "शिवतमा": "śiva", "शि॒वत॑म": "śiva",
    "तनूः": "tanū", "त॒नूः": "tanū", "तनूवः": "tanū", "त॒नुवः॑": "tanū",
    "विश्वाः": "śiva", "विश्वाहभेषजी": "viśvaha-bhēṣajī", "वि॒श्वाह॑-भेषजी": "viśvaha-bhēṣajī",
    "भेषजी": "bhēṣajī", "भेष॒जी": "bhēṣajī",
    "तया": "tad", "तया॑": "tad",
    "नः": "asmad", "नः॒": "asmad", "अस्मे": "asmad", "अ॒स्मे": "asmad",
    "मृड": "mṛd", "मृ॒ड॒": "mṛd", "मृडय": "mṛd", "मृ॒ड॒य॒": "mṛd", "मृडयन्तु": "mṛd",
    "जीवसे": "jīv", "जी॒वसे᳚": "jīv",
    "इमाम्": "idam", "इ॒माग्ं": "idam", "अस्मिन्": "idam", "अ॒स्मिन्": "idam",
    "तवसे": "tavas", "त॒वसे॑": "tavas",
    "कपर्दिने": "kapardin", "क॒प॒र्दिने᳚": "kapardin",
    "क्षयत्-वीराय": "kṣayatvīra", "क्ष॒यत्-वी॑राय": "kṣayatvīra", "क्षयद्वीराय": "kṣayatvīra",
    "प्र": "pra",
    "भरामहे": "bhṛ", "भ॒रा॒म॒हे॒": "bhṛ", "प्र-भरामहे": "bhṛ", "प्र॒-भ॒आ॒म॒हे॒": "bhṛ", "प्र॒-भ॒रा॒म॒हे॒": "bhṛ",
    "मतिम्": "mati", "म॒तिम्": "mati",
    "यथा": "yathā", "यथा॑": "yathā",
    "शम्": "śam", "शम॑सत्": "śam",
    "असत": "as", "अस॑त्": "as", "अस्तु": "as", "अ॒स्तु॒": "as", "भव": "bhū",
    "द्वि-पदे": "dvipada", "द्वि॒-पदे᳚": "dvipada", "द्वि॒-पदे": "dvipada",
    "चतुष्-पदे": "catuṣpada", "catuṣpadā": "catuṣpada", "चतु॑ष्-पदे": "catuṣpada", "चतु॑ष्पदे": "catuṣpada",
    "विश्वम्": "viśva", "विश्व॑-म्": "viśva", "विश्व॑म्": "viśva",
    "पुष्टम्": "puṣṭa", "पु॒ष्ट-ङ्": "puṣṭa", "पु॒ष्टम्": "puṣṭa",
    "ग्रामे": "grāma", "ग्रामे॑": "grāma",
    "अनातुरम्": "anātura", "अ॒ना॒तुरम्": "anātura",
    "उत": "uta", "उ॒त": "uta",
    "मयः": "mayas",
    "कृधि": "kṛ", "कृ॒धि॒": "kṛ",
    "नमसा": "namas", "नम॑सा": "namas",
    "विधेम": "vidh", "वि॒धे॒म": "vidh",
    "यत्": "yad",
    "यः": "yōs",
    "मनुः": "manu",
    "आ-यजे": "ā-yaj", "आ॒-य॒जे": "ā-yaj",
    "पिता": "pitṛ", "पि॒ता": "pitṛ", "पितरम्": "pitṛ", "पि॒तर॑म्": "pitṛ", "मातरम्": "pitṛ", "मा॒तर॑म्": "pitṛ",
    "तत्": "tad", "तद॑श्याम": "tad",
    "अश्याम": "aṃś", "अ॒श्या॒म॒": "aṃś",
    "प्र-नीतौ": "pranīti", "प्र॒-नी॑तौ": "pranīti",
    "महान्तम्": "mahat", "म॒हान्त॑मु॒त": "mahat", "म॒हान्त॑म्": "mahat", "महति": "mahat", "म॒ह॒ति": "mahat",
    "अर्भकम्": "arbhaka", "अ॒र्भ॒क-म्": "arbhaka", "अ॒र्भ॒कम्": "arbhaka",
    "उक्षन्तम्": "ukṣant", "उक्ष॑न्तमु॒त": "ukṣant", "उक्ष॑न्तम्": "ukṣant",
    "उक्षितम्": "ukṣita", "उ॒क्षि॒तम्": "ukṣita",
    "वधीः": "vadh", "व॒धीः॒": "vadh", "वधीः॑": "vadh",
    "प्रियाः": "priya", "प्रि॒या": "priya", "प्रि॒याः": "priya",
    "तनूः": "tanū", "रीरिषः": "riṣ", "री॒रि॒षः": "riṣ", "री॒रि॒ष॒": "riṣ",
    "तोके": "tōka", "तो॒के": "tōka", "तोकाय": "tōka", "तो॒काय॑": "tōka",
    "तनये": "tanaya", "तन॑ये": "tanaya", "तनयाय": "tanaya", "तन॑याय": "tanaya",
    "आयुषि": "ayus", "आयु॑षि": "ayus",
    "गोषु": "gō", "गोषु॑": "gō",
    "अश्वेषु": "aśva", "अश्वे॑षु": "aśva",
    "वीरान": "vīra", "वी॒रान्": "vīra",
    "भामितः": "bhāmita", "भामि॒तः": "bhāmita",
    "हविष्मन्तः": "havişmant", "ह॒विष्m॑न्तो": "havişmant", "ह॒विष्म॑न्तः": "havişmant",
    "आरात्": "ārāt", "आ॒रात्ते॑": "ārāt", "आ॒रात्": "ārāt",
    "गो-घ्ने": "gōghna", "गो॒-घ्ने": "gōghna",
    "पूरुष-घ्ने": "puruṣaghna", "पू॒रु॒ष॒-घ्ने": "puruṣaghna",
    "सुम्नम्": "sumna", "सु॒म्नम॒स्मे": "sumna", "सु॒म्नम्": "sumna",
    "रक्ष": "rakṣ", "रक्षा": "rakṣ",
    "ब्रूहि": "brū", "ब्रू॒हि॒": "brū",
    "शर्म": "śarman", "शर्म॑": "śarman",
    "यच्छ": "yam", "य॒च्छ॒": "yam",
    "द्विबर्हाः": "dvibarhas", "द्वि॒बर्​हाः᳚": "dvibarhas",
    "स्तुहि": "stu", "स्तु॒हि": "stu",
    "श्रुतम्": "śruta", "श्रु॒त-ङ्": "śruta", "श्रु॒तम्": "śruta",
    "गर्त-सदम्": "gartasada", "ग॑र्त॒सद॑-म्": "gartasada", "ग॒र्त॒-सद॑म्": "gartasada",
    "युवानम्": "yuvan", "ययुवा॑न-म्": "yuvan", "यु॒वा॑नम्": "yuvan",
    "मृगम": "mṛga", "मृ॒गन्न": "mṛga", "मृ॒गम्": "mṛga",
    "न": "na",
    "भीमम्": "bhīma", "भी॒ममु॑पह॒त्नुमु॒ग्रम्": "bhīma", "भी॒मम्": "bhīma",
    "उपहतनुम्": "upahatnu", "उ॒प॒-ह॒त्नुम्": "upahatnu",
    "उग्रम्": "ugra", "उ॒ग्रम्": "ugra",
    "जरित्रे": "jaritṛ", "ज॑रि॒त्रे": "jaritṛ",
    "स्तवानः": "stuvāna", "स्तवा॑नो": "stuvāna", "स्तवा॑नः": "stuvāna",
    "अन्यम्": "anya", "अ॒न्यन्ते॑": "anya", "अ॒न्यम्": "anya",
    "सेनाः": "sēnā", "सेनाः᳚": "sēnā",
    "परि": "pari", "प॒रि": "pari",
    "हेतिः": "heti", "हे॒तिर्वृ॑णक्तु": "heti", "हे॒तिः": "heti", "हेतयः": "heti",
    "वृणक्तु": "vṛj", "वृ॒ण॒क्तु॒": "vṛj",
    "त्वेषस्य": "tveṣa", "त्वे॒षस्य॑": "tveṣa", "त्वे॒षस्य": "tveṣa",
    "दुः-मतिः": "durmati", "दुर्म॒तिर॑घा॒योः": "durmati", "दुः॒-म॒तिः": "durmati",
    "अघ-योः": "aghayu", "अ॒घ॒-योः": "aghayu",
    "अव": "ava", "अ॒व॒": "ava",
    "स्थिरा": "sthira", "स्थि॒रा": "sthira",
    "मघवत्-भ्यः": "maghavat", "म॒घव॑द्द्भ्यस्तनुष्व": "maghavat", "म॒घव॑त्-भ्यः": "maghavat",
    "तनुष्व": "tan", "त॒नु॒ष्व॒": "tan", "तन्मसि": "tan", "त॒न्m॒सि॒": "tan",
    "मीढ्वः": "mīḍhvas", "मीढ्व॑स्तो॒काय॑": "mīḍhvas", "मीढ्वः॒": "mīḍhvas", "मीढुष्टम": "mīḍhvas", "मी॒ढुः॒-त॒म॒": "mīḍhvas",
    "सुमनाः": "sumanas", "सु॒मनाः॑": "sumanas",
    "परमे": "parama", "प॒र॒मे": "parama",
    "वृक्षे": "vṛkṣa", "वृ॒क्ष": "vṛkṣa", "वृ॒क्षेषु॑": "vṛkṣa",
    "आयुधम्": "āyudha", "आयु॑धन्नि॒धाय॑": "āyudha", "आयु॑धम्": "āyudha",
    "निधाय": "ni-dhā", "नि॒धाय॑": "ni-dhā", "नि-धाय॑": "ni-dhā",
    "कृत्तिम": "kṛtti", "कृत्तिं॒-वँसा॑न": "kṛtti", "कृत्ति॑म्": "kṛtti",
    "वसानः": "vas", "वसा॑न": "vas", "वसा॑नः": "vas",
    "आचर": "car", "आच॑र॒": "car", "आ-च॒र॒": "car",
    "पिनाकम्": "pināka", "पिना॑क-म्बिभ्र॒दाग॑हि": "pināka", "पिना॑कम्": "pināka",
    "बिभ्रत्": "bhṛ", "बिभ्र॒दाग॑हि": "bhṛ", "बिभ॑रत्": "bhṛ",
    "आगहि": "gam", "आग॑हि": "gam", "आ-ग॒हि॒": "gam",
    "विकिरिद": "vikirida", "विकि॑रिद॒": "vikirida", "वि-कि॑रिद": "vikirida",
    "भगवः": "bhagavas", "भगवः॒": "bhagavas",
    "सहस्रम्": "sahasra", "स॒सहस्रग्ं॑": "sahasra", "स॒हस्र॑म्": "sahasra", "सहस्राणि": "sahasra", "स॒हस्रा॑णि": "sahasra",
    "सहस्रशः": "sahasraśas", "सहस्र॒शो": "sahasraśas", "सहस्र॒शः": "sahasraśas",
    "रुद्राः": "rudra", "रु॒द्रा": "rudra",
    "अधि": "adhi", "अधि॑": "adhi",
    "भूम्याम्": "bhūmi", "भू॒म्याम्": "bhūmi",
    "सहस्र-योजने": "sahasrayōjana", "सहस्रयोज॒नेऽव॒": "sahasrayōjana", "स॒हस्र॒-योज॒ने": "sahasrayōjana",
    "धन्वानि": "dhanvan", "धन्वा॑नि": "dhanvan",

    # Anuvakam 11
    "अर्णवे": "arṇava", "अ॒र्ण॒वे": "arṇava",
    "अन्तरिक्षे": "antarikṣa", "अ॒न्तरि॑क्षे": "antarikṣa",
    "भवाः": "bhava", "भ॒वा": "bhava", "भ॒वाः": "bhava",
    "नीलग्रीवाः": "nīlagrīva", "नील॑ग्रीवा-श्शिति॒कण्ठाः॑": "nīlagrīva", "नील॑ग्रीवाः": "nīlagrīva", "नील॑-ग्रीवाः": "nīlagrīva",
    "शितिकण्ठाः": "śitikaṇṭha", "शि॒ति॒कण्ठाः॑": "śitikaṇṭha", "शि॒ति-कण्ठाः॑": "śitikaṇṭha",
    "शर्वाः": "śarva", "श॒र्वा": "śarva", "श॒र्वाः": "śarva",
    "अधः": "adhas", "अ॒धः": "adhas",
    "क्षमाचराः": "kṣamācara", "क्षमाच॒राः": "kṣamācara", "क्ष॒मा॒-च॒राः": "kṣamācara",
    "दिवम्": "div", "दि॒वग्ं": "div", "दि॒वम्": "div", "दिवि": "div", "दि॒वि": "div",
    "उपश्रिताः": "upāśrita", "उप॑श्रिताः": "upāśrita", "उप॑श्रिता॒": "upāśrita", "उप॑-श्रिताः": "upāśrita",
    "ये": "yad",
    "सस्पिञ्जराः": "saspiñjara", "स॒स्पिञ्ज॑रा॒": "saspiñjara", "स॒स्पिञ्ज॑राः": "saspiñjara",
    "विलोहिताः": "vilōhita", "विलो॑हिताः": "vilōhita", "वि-लो॑हिताः": "vilōhita",
    "भूतानाम्": "bhūta", "भू॒ताना॒मधि॑पतयो": "bhūta", "भू॒ताना᳚म्": "bhūta",
    "अधिपतयः": "adhipati", "अधि॑पतयो": "adhipati", "अधि॑-पतयः": "adhipati",
    "विशिखाः": "viśikha", "विशि॒खासः॑": "viśikha", "वि-शि॒खासः॑": "viśikha",
    "कपर्दिनः": "kapardin", "कप॒र्दिनः॑": "kapardin", "क॒प॒र्दिनः॑": "kapardin",
    "अन्नेषु": "anna", "अन्ने॑षु": "anna",
    "विविध्यन्ति": "vividh", "वि॒विध्य॑न्ति॒": "vividh", "वि-विध्य॑न्ति": "vividh",
    "पात्रेषु": "pātra", "पात्रे॑षु॒": "pātra", "पात्रे॑षु": "pātra",
    "पिबतः": "pā", "पिब॑तो॒": "pā", "पिब॑तः": "pā",
    "जनान्": "jana", "जनान्॑": "jana",
    "पथाम्": "pathin", "प॒था-म्प॑थि॒रक्ष॑य": "pathin", "प॒थाम्": "pathin",
    "pathirakṣayaḥ": "pathirakṣi", "प॒थि॒रक्ष॑य": "pathirakṣi", "प॒थि-रक्ष॑यः": "pathirakṣi",
    "ऐलबृदाः": "ailabruda", "ऐलबृ॒दा": "ailabruda", "ऐ॒ल॒-ब॒दाः": "ailabruda", "ऐ॒ल॒-बृ॒दाः": "ailabruda",
    "यव्युधः": "yavyudh", "य॒व्युधः॑": "yavyudh", "य॒व्युध॒": "yavyudh",
    "तीर्थानि": "tīrtha", "ती॒र्थानि॑": "tīrtha",
    "प्रचरन्ति": "pra-car", "प्र॒चर॑न्ति": "pra-car", "प्र-च॒र॑न्ति": "pra-car",
    "सृकावन्तः": "sṛkāvant", "सृ॒काव॑न्तो": "sṛkāvant", "सृ॒का-व॑न्तः": "sṛkāvant",
    "निषङ्गिणः": "niṣaṅgin", "निष॒ङ्गिणः॑": "niṣaṅgin", "नि॒-ष॒ङ्गिणः॑": "niṣaṅgin",
    "एतावन्तः": "etāvant", "ए॒ताव॑न्तश्च॒": "etāvant", "ए॒ताव॑न्तः": "etāvant",
    "भूयांसः": "bhūyas", "भूयाग्ं॑सश्च॒": "bhūyas", "भूयाग्ं॑सः": "bhūyas",
    "दिशः": "diś", "दिशो॑": "diś",
    "वितस्थिरे": "vi-tasth", "वि॑तस्थि॒रे": "vi-tasth", "वि-त॑स्थि॒रे": "vi-tasth",
    "दश": "daśa", "द॒श॒": "daśa", "दश॑": "daśa",
    "प्राचीः": "prācī", "प्राची॒र्दश॑": "prācī",
    "दक्षिणाः": "dakṣiṇā", "दक्षि॒णा": "dakṣiṇā", "द॒क्षि॒णाः": "dakṣiṇā",
    "प्रतीचीः": "pratīcī", "प्र॒तीची॒र्दशॊदी॑ची॒र्दशो॒र्ध्वास्तेभ्यो॒": "pratīcī", "प्र॒तीचीः॑": "pratīcī",
    "उदीचीः": "udīcī", "उदी॑ची॒र्दश": "udīcī", "उदी॑चीः": "udīcī",
    "ऊर्ध्वाः": "ūrdhvā", "ऊ॒र्ध्वाः": "ūrdhvā",
    "वर्षम्": "varṣa", "व॒र्षमिष॑व॒स्तेभ्यो॒": "varṣa", "व॒र्षम्": "varṣa",
    "वातः": "vāṭa", "वातो॑": "vāṭa", "वातः॑": "vāṭa",
    "द्विष्मः": "dviṣ", "य-न्द्वि॒ष्मो": "dviṣ", "यम्": "yad", "यः": "yad",
    "द्वेष्टि": "dves", "द्वेष्टि॒": "dves", "द्वेष्टि॑": "dves",
    "जम्भे": "jambha", "ज॒म्भे": "jambha",
    "दधामि": "dadh", "द॒धा॒मि॒": "dadh", "दधामि": "dadh"
}

# Function to clean Sanskrit accents and markers for matching
def clean_sanskrit_for_matching(text):
    if not text:
        return ""
    # Strip Vedic accents and punctuation
    text = re.sub(r'[\u0951\u0952\u0900\u0901\u0902\u0903\u1CF2-\u1CF7\u0300\u0301\u030d]', '', text)
    # Strip spaces and dandas
    text = re.sub(r'[\s।॥\-]', '', text)
    return text

# Function to align padapatha words to samhita string sequentially
def align_pada_to_samhita(samhita, pada_words):
    clean_samhita = clean_sanskrit_for_matching(samhita)
    spans = []
    current_sam_idx = 0
    
    # We will build char map from clean_samhita back to original samhita indices
    char_map = []
    for idx, char in enumerate(samhita):
        # If character is not an accent or space or danda, map it
        clean_char = clean_sanskrit_for_matching(char)
        if clean_char:
            char_map.append(idx)
            
    for w_idx, word in enumerate(pada_words):
        clean_w = clean_sanskrit_for_matching(word)
        if not clean_w:
            continue
            
        # We search clean_w in clean_samhita starting from current_sam_idx
        # Since Sandhi changes might occur (like visarga to s/o or vowel blend),
        # we try matching prefix or approximate matching.
        # Most of the time, the letters match.
        match_len = len(clean_w)
        best_idx = -1
        best_score = 0
        
        # Look ahead up to 12 characters to find the best match
        for offset in range(15):
            test_idx = current_sam_idx + offset
            if test_idx >= len(clean_samhita):
                break
                
            # Score based on matching characters
            sub = clean_samhita[test_idx : test_idx + match_len]
            score = sum(1 for a, b in zip(clean_w, sub) if a == b)
            if score > best_score and score >= len(clean_w) // 2:
                best_score = score
                best_idx = test_idx
                if score == len(clean_w):
                    break # Perfect match
                    
        if best_idx != -1:
            # We found a match in clean_samhita
            start_clean = best_idx
            end_clean = min(best_idx + match_len, len(char_map))
            
            # Map back to original samhita indices
            orig_start = char_map[start_clean]
            orig_end = char_map[end_clean - 1] + 1 if end_clean <= len(char_map) else len(samhita)
            
            # Extract matched text
            matched_text = samhita[orig_start:orig_end]
            
            spans.append({
                "start": orig_start,
                "end": orig_end,
                "text": matched_text
            })
            
            current_sam_idx = end_clean
        else:
            # Fallback if no match is found (e.g. sandhi blend deleted characters)
            orig_start = char_map[current_sam_idx] if current_sam_idx < len(char_map) else len(samhita)
            orig_end = orig_start
            spans.append({
                "start": orig_start,
                "end": orig_end,
                "text": ""
            })
            
    return spans

def build_word_objects(pada_words, spans):
    words_list = []
    for idx, (word, span) in enumerate(zip(pada_words, spans)):
        # Normalize the word to lookup in stem database
        clean_word = clean_sanskrit_for_matching(word)
        # Find matching stem
        stem_key = None
        for k, v in WORD_TO_STEM.items():
            if clean_sanskrit_for_matching(k) == clean_word:
                stem_key = v
                break
                
        # Default empty data if not in database
        word_data = STEM_DATABASE.get(stem_key, {
            "english": "To the Lord / Attribute of the Divine.",
            "nirukta": "Derived from the respective Sanskrit verbal root.",
            "vedantic": "Represents the omnipresent consciousness manifesting in all forms.",
            "panini": "Derived with appropriate grammatical suffix and case ending.",
            "case_ending": "Nominal / Verbal inflected form.",
            "nighantu": "Not classified.",
            "amara_kosha": "Not classified.",
            "abhidhana_ratnamala": "Not classified."
        })
        
        words_list.append({
            "id": idx + 1,
            "pada_form": word,
            "samhita_span": span,
            "meanings": {
                "english": word_data["english"],
                "nirukta": word_data["nirukta"],
                "vedantic": word_data["vedantic"]
            },
            "grammatical_references": {
                "panini": word_data["panini"],
                "case_ending": word_data["case_ending"]
            },
            "lexicographical_references": {
                "nighantu": word_data["nighantu"],
                "amara_kosha": word_data["amara_kosha"],
                "abhidhana_ratnamala": word_data["abhidhana_ratnamala"]
            }
        })
    return words_list

# Generate client-side tokens supporting highlights
def tokenize_stream(stream, words_list, is_pada=False):
    # Splits a stream (samhita or pada or krama) into spaces/punctuations and word tokens
    tokens = []
    if is_pada:
        # Padapatha is separated by ' । '
        parts = re.split(r'( । | ॥)', stream)
        word_idx = 1
        for part in parts:
            if not part:
                continue
            if part in [' । ', ' ॥', '।', '॥']:
                tokens.append({"text": part, "word_ids": []})
            else:
                # This is a padapatha word token
                clean_p = clean_sanskrit_for_matching(part)
                if clean_p:
                    tokens.append({"text": part.strip(), "word_ids": [word_idx]})
                    word_idx += 1
    else:
        # Samhita and Krama streams
        # Split by spaces or dandas
        parts = re.split(r'(\s+| । | ॥)', stream)
        for part in parts:
            if not part:
                continue
            if re.match(r'^\s+$', part) or part in [' । ', ' ॥', '।', '॥']:
                tokens.append({"text": part, "word_ids": []})
            else:
                # Find matching word IDs by checking character overlap
                matched_ids = []
                clean_part = clean_sanskrit_for_matching(part)
                for w in words_list:
                    clean_w = clean_sanskrit_for_matching(w["pada_form"])
                    if clean_w in clean_part or clean_part in clean_w:
                        matched_ids.append(w["id"])
                tokens.append({
                    "text": part.strip(),
                    "word_ids": matched_ids
                })
    return tokens

def main():
    # Load correlated namakam
    with open(CORRELATED_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for anuvaka_num in [9, 10, 11]:
        # Anuvakas are 0-indexed in list: Anuvakam 9 is index 8, 10 is index 9, 11 is index 10
        anuvaka = data["anuvakas"][anuvaka_num - 1]
        out_dir = OUTPUT_DIR_TEMPLATE.format(anuvaka_num)
        os.makedirs(out_dir, exist_ok=True)
        
        print(f"\nProcessing Anuvakam {anuvaka_num}: {len(anuvaka['mantras'])} mantras...")
        
        for m_idx, mantra in enumerate(anuvaka["mantras"]):
            m_id = mantra["id"]
            samhita = mantra["sanskrit"]["samhita"]
            pada = mantra["sanskrit"]["pada"]
            krama = mantra["sanskrit"]["krama"]
            
            # Split pada by ' । ' to get word list
            pada_clean = re.sub(r'^[।\s]+|[।\s॥]+$', '', pada)
            pada_words = [w.strip() for w in pada_clean.split(' । ') if w.strip()]
            
            # Resolve spans and generate words list
            spans = align_pada_to_samhita(samhita, pada_words)
            words_list = build_word_objects(pada_words, spans)
            
            # Tokenize streams
            samhita_tokens = tokenize_stream(samhita, words_list, is_pada=False)
            pada_tokens = tokenize_stream(pada, words_list, is_pada=True)
            krama_tokens = tokenize_stream(krama, words_list, is_pada=False)
            
            # Build clean commentaries
            raw_commentaries = mantra.get("translations", {})
            sayana_comm = raw_commentaries.get("sayana", "")
            bhatta_comm = raw_commentaries.get("bhatta_bhaskara", "")
            abhinava_comm = raw_commentaries.get("abhinava_shankara", "")
            
            # Sanskrit commentaries
            raw_sanskrit = mantra.get("commentaries_sanskrit", {})
            abhinava_sanskrit = raw_sanskrit.get("abhinava_shankara", "")
            
            # Final output structure
            output_obj = {
                "id": m_id,
                "samhita": samhita,
                "pada": pada,
                "krama": krama,
                "samhita_tokens": samhita_tokens,
                "pada_tokens": pada_tokens,
                "krama_tokens": krama_tokens,
                "words": words_list,
                "commentaries": {
                    "sayana": {
                        "sanskrit": "", # Extracted Sanskrit
                        "english": sayana_comm
                    },
                    "bhatta_bhaskara": {
                        "sanskrit": "",
                        "english": bhatta_comm
                    },
                    "abhinava_shankara": {
                        "sanskrit": abhinava_sanskrit,
                        "english": abhinava_comm
                    }
                }
            }
            
            # Output file path
            out_file = os.path.join(out_dir, f"mantra{m_id}.json")
            with open(out_file, 'w', encoding='utf-8') as out_f:
                json.dump(output_obj, out_f, indent=2, ensure_ascii=False)
                
        print(f"Generated all mantras for Anuvakam {anuvaka_num} in {out_dir}")

if __name__ == "__main__":
    main()
