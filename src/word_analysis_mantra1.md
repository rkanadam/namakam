# Word-by-Word Analysis of Sri Rudram: Anuvakam 1, Mantra 1 (Unified Edition)

This document presents a comprehensive, word-by-word breakdown of the first mantra of the first anuvaka of Sri Rudram. Each individual word (un-sandhied, as found in the *padapāṭha*) is mapped to its exact span within the original *saṃhitā* text, with multi-layered interpretations including:
* **English Translation**
* **Nirukta** (Yāska's Vedic etymologies)
* **Vedantic Interpretation**
* **Grammatical References** (Pāṇinian verbal roots, suffixes, and rules of case assignment)
* **Lexicographical References** (Vedic *Nighaṇṭu*, classical *Amarakośa*, and 10th-century *Abhidhānaratnamālā* of Halāyudha Bhaṭṭa)

The fully-tokenized unified dataset is located at [anuvakam1.json](file:///Users/Rkanadam/personal/namakam/src/anuvakam1.json) (where Mantra 1 has been fully enriched), and the isolated sample dataset is at [anuvakam1_words_sample.json](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json).

---

## The Mantra
* **Saṃhitā**: `नम॑स्ते रुद्र म॒न्यव॑ उ॒तोत॒ इष॑वे॒ नमः॑ । नम॑स्ते अस्तु॒ धन्व॑ने बा॒हुभ्या॑मु॒त ते॒ नमः॑ ॥`
* **Padapāṭha**: `नमः॑ । ते॒ । रु॒द्र॒ । म॒न्यवे᳚ । उ॒तो इति॑ । उ॒त । इष॑वे । नमः॑ । नमः॑ । ते॒ । अ॒स्तु॒ । धन्व॑ने । बा॒हुभ्या᳚म् । उ॒त । ते॒ । नमः॑ ॥`

---

## Word-by-Word Analysis Table

The character offsets below are **0-indexed** relative to the Unicode representation of the `saṃhitā` text, where combining accent marks count as independent characters (e.g. `म॒न्यव॑` is index 14 to 21).

| Index | Pada Form | Samhita Span (Indices) | Samhita Text | English Meaning |
| :---: | :--- | :---: | :---: | :--- |
| **1** | [नमः॑](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L53) | `0 : 5` | `नम॑स्` | Salutations / Bowing down / Reverence. |
| **2** | [ते॒](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L77) | `5 : 7` | `ते` | To you / Your. |
| **3** | [रु॒द्र॒](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L95) | `8 : 13` | `रुद्र` | O Rudra. |
| **4** | [म॒न्यवे᳚](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L113) | `14 : 21` | `म॒न्यव॑` | To your anger / wrath / righteous indignation. |
| **5** | [उ॒तो](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L131) | `22 : 26` | `उ॒तो` | And also / Moreover. |
| **6** | [उ॒त](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L149) | `26 : 28` | `त॒` | And. |
| **7** | [इष॑वे](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L167) | `29 : 35` | `इष॑वे॒` | To your arrow. |
| **8** | [नमः॑](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L185) | `36 : 40` | `नमः॑` | Salutations. |
| **-** | `।` | `41 : 42` | `।` | *Danda (Punctuation)* |
| **9** | [नमः॑](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L200) | `43 : 48` | `नम॑स्` | Salutations. |
| **10** | [ते॒](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L215) | `48 : 50` | `ते` | To you / Your. |
| **11** | [अ॒स्तु॒](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L230) | `51 : 57` | `अस्तु॒` | Let there be / May there be. |
| **12** | [धन्व॑ने](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L248) | `58 : 65` | `धन्व॑ने` | To your bow. |
| **13** | [बा॒हुभ्या᳚म्](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L266) | `66 : 77` | `बा॒हुभ्या॑म` | To your two arms. |
| **14** | [उ॒त](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L284) | `77 : 80` | `ु॒त` | And. |
| **15** | [ते॒](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L299) | `81 : 84` | `ते॒` | To you / Your. |
| **16** | [नमः॑](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json#L314) | `85 : 89` | `नमः॑` | Salutations. |
| **-** | `॥` | `90 : 91` | `॥` | *Double Danda (Punctuation)* |

---

## Detailed Word-by-Word Breakdowns

### 1 & 9. नमः॑ (namaḥ)
* **English Meaning**: Salutations, bowing down, reverent prostration.
* **Nirukta/Etymology**: From root **√nam** (नम्) meaning "to bend/bow". Yāska's *Nirukta* defines it as bowing down (*namanīya*) and paying homage.
* **Vedantic Meaning**: Synthesized as **na mama** ("not mine"), indicating the surrender of the ego (*ahaṃkāra*) and doership (*kartṛtva*).
* **Grammatical (Pāṇini)**:
  * **Root**: √nam (नमुँ प्रह्वत्वे शब्दे च, Bhvādi-gaṇa, 1.1030).
  * **Suffix**: nominal suffix *asun* (असुन्).
  * **Rule Governed**: Governs the dative case (*caturthī vibhakti*) on related words (manyave, ishave, dhanvane, bahubhyam) by the Aṣṭādhyāyī sūtra: **नमःस्वस्तिस्वाहास्वधालंवषड्योगाच्च (2.3.16)**.
  * **Inflection**: Avyaya (indeclinable).
* **Lexicographical**:
  * **Nighaṇṭu**: Listed under *udaka-nāmāni* (water synonyms, Nighaṇṭu 1.12, item 17) and *anna-nāmāni* (food synonyms, Nighaṇṭu 2.7).
  * **Amarakośa**: Classified under Avyayavarga (3.4.19) as an indeclinable representing bowing or reverence.
  * **Abhidhānaratnamālā**: Classified in Anekārtha-kāṇḍa (5.26) under Avyayas, meaning bowing or salutation (namaskāra).

### 2, 10 & 15. ते॒ (te)
* **English Meaning**: To you / Your.
* **Nirukta/Etymology**: Genitive/dative singular of the second-person pronoun **yushmad** (युष्मद्).
* **Vedantic Meaning**: Refers to the Supreme consciousness as the immediate "You" (the inner Self or *Pratyagātman*).
* **Grammatical (Pāṇini)**:
  * Substituted enclitic form (*ādeśa*) of the pronoun *yushmad* in the dative case (caturthī-ekavacana) by the Aṣṭādhyāyī sūtra: **तेमयावेकवचनस्य (8.1.22)**.
  * **Inflection**: Dative Singular.
* **Lexicographical**: Pronouns and enclitics are generally excluded from standard synonym-tables (*Nighaṇṭu* & *Abhidhānaratnamālā*).

### 3. रु॒द्र॒ (rudra)
* **English Meaning**: O Rudra.
* **Nirukta/Etymology**:
  1. *Rudra rautīti sataḥ* (He who roars).
  2. *Rodayater vā* (He who makes others weep at cosmic dissolution).
  3. *Rutam (sorrow/ignorance) dravayati (dissolves) iti Rudrah* (He who dissolves suffering and ignorance).
* **Vedantic Meaning**: The supreme reality that destroys the primary cause of suffering—*avidyā* (spiritual ignorance).
* **Grammatical (Pāṇini)**:
  * **Root**: √rud (रुदिँ अश्रुविमोचने, Adādi-gaṇa, 2.0002).
  * **Suffix**: Uṇādi suffix **kran** (रक्) by the Uṇādi-sūtra: **रुलरिक्सृप्युपिनमिरुदिभ्यः क्रन् (Uṇādi 2.22 / 2.24)**. The suffix *kran* is *k-it*, preventing guṇa strengthening of the vowel *u*.
  * **Inflection**: Vocative Singular (Sambodhana-Prathamā, Ekavacana).
* **Lexicographical**:
  * **Nighaṇṭu**: Listed under atmospheric deities (*devatā-nāmāni*, Nighaṇṭu 5.5).
  * **Amarakośa**: Listed in Svargavarga (1.1.34) as a major synonym of Shiva: **रुद्रः स्थाणुरुमापतिः**.
  * **Abhidhānaratnamālā**: Listed in Svarga-kāṇḍa (1.30-33) as a key name of Lord Shiva: 'rudras-tryambaka-īśānaḥ'.

### 4. म॒न्यवे᳚ (manyave)
* **English Meaning**: To your anger / wrath / righteous indignation.
* **Nirukta/Etymology**: From root **√man** (मन्) meaning "to think, know, or be angry". In *Nirukta*, *manyu* is defined as anger (*krodha*), representing righteous divine wrath directed at cosmic order correction.
* **Vedantic Meaning**: The cosmic corrective force of Dharma that dissolves the limited ego.
* **Grammatical (Pāṇini)**:
  * **Root**: √man (मनँ ज्ञाने, Divādi-gaṇa, 4.0073 or मनुँ अवबोधने, Tanādi-gaṇa, 8.0009).
  * **Suffix**: Uṇādi suffix **yu** (यु) by the Uṇādi-sūtra: **क्रुमन्दोर्युः (Uṇādi 3.20)**.
  * **Case**: Governed in the dative case (caturthī) due to the presence of *namas* (2.3.16).
  * **Inflection**: Dative Singular.
* **Lexicographical**:
  * **Nighaṇṭu**: Listed under synonyms of anger (*krodha-nāmāni*, Nighaṇṭu 2.13) and synonyms of intellect (*prajñā-nāmāni*, Nighaṇṭu 3.9).
  * **Amarakośa**: Listed in Nānārthavarga (3.3.188) with three distinct meanings: **मन्युर् दैन्ये क्रतौ क्रुधि** (sorrow, sacrifice, and anger).
  * **Abhidhānaratnamālā**: Listed in Anekārtha-kāṇḍa (5.82) under polysemous nouns, denoting anger (krodha), grief (śoka), and sacrifice (yajña).

### 5. उ॒तो (uto)
* **English Meaning**: And also / Moreover.
* **Nirukta/Etymology**: Vedic conjunctive particle combining *uta* (and) and *u* (also) representing emphasis (*samuccayārtha*).
* **Vedantic Meaning**: Links the unmanifest determination (anger) to manifest weapons (bow/arrows) as non-dual.
* **Grammatical (Pāṇini)**:
  * Vedic compound particle combining *uta* + *u* (उत + उ). By Sandhi, *a + u* forms *o*. It is a pragṛhya vowel by **निपात एकाजनाङ् (1.1.14)** and does not undergo further sandhi in Vedic recitation.
  * **Inflection**: Avyaya.
* **Lexicographical**: Classified as a Vedic particle (*nipāta*).

### 6 & 14. उ॒त (uta)
* **English Meaning**: And / Also.
* **Nirukta/Etymology**: Conjunction meaning "and" or "also".
* **Vedantic Meaning**: Coordinates different instruments of divine play (*līlā*).
* **Grammatical (Pāṇini)**:
  * Avyaya classified under the Cādi class of particles (*cādi-gaṇa*).
  * **Inflection**: Avyaya.
* **Lexicographical**:
  * **Amarakośa**: Listed in Avyayavarga (3.4.15) for addition/coordination: **उताप्यर्थे च संशये**.
  * **Abhidhānaratnamālā**: Listed in Anekārtha-kāṇḍa under conjunctive particles (avyayas).

### 7. इष॑वे (iṣave)
* **English Meaning**: To your arrow.
* **Nirukta/Etymology**: From root **√iṣ** (इष्) meaning "to speed/throw". Yāska defines *iṣu* as *iṣur iṣateḥ gatikarmaṇaḥ* (that which is propelled).
* **Vedantic Meaning**: The arrow represents the focused mind (*sādhana*) or the individual soul (*jīvātman*) targeted at Brahman (as in Mundaka Upanishad 2.2.4).
* **Grammatical (Pāṇini)**:
  * **Root**: √iṣ (इषुँ गत्यौ, Tudādi-gaṇa, 6.0076).
  * **Suffix**: Uṇādi suffix **u** (उ) by Uṇādi-sūtra: **इषेरूच् (Uṇādi 1.22)**.
  * **Case**: Governed in the dative case (caturthī) by the presence of *namas* (2.3.16).
  * **Inflection**: Dative Singular.
* **Lexicographical**:
  * **Nighaṇṭu**: Listed under weapons and thunderbolts (*vajra-nāmāni*, Nighaṇṭu 2.17).
  * **Amarakośa**: Listed in Kṣatriyavarga (2.8.91) as a synonym for arrow: **बाणाजौ खगकाण्डॉस्त्रविशिखाः शरपत्रिणौ रोपिकु... द्वयोरिषुः**.
  * **Abhidhānaratnamālā**: Listed in Sāmānya-kāṇḍa (2.124) under weapons, with synonyms like 'śara', 'bāṇa', and 'viśikha'.

### 11. अ॒स्तु॒ (astu)
* **English Meaning**: Let there be / May there be.
* **Nirukta/Etymology**: Imperative 3rd person singular of the root **√as** (अस्) "to be".
* **Vedantic Meaning**: Willing submission and alignment of the individual will with the divine order.
* **Grammatical (Pāṇini)**:
  * **Root**: √as (अस् भुवि, Adādi-gaṇa, 2.0060).
  * **Form**: Imperative Mood (*loṭ-lakāra*, prathama-puruṣa, ekavacana). Suffix *ti* becomes *tu* by the rule **एरुः (3.4.86)**.
  * **Inflection**: Tiṅanta (Verb), 3rd Person Singular.
* **Lexicographical**:
  * **Amarakośa**: Listed in Avyayavarga as a particle of assent or existence.
  * **Abhidhānaratnamālā**: Verb-based particle under Avyayas.

### 12. धन्व॑ने (dhanvane)
* **English Meaning**: To your bow.
* **Nirukta/Etymology**: From root **√dhanv** (धन्व्) "to run/flow". Nirukta derives *dhanvan* as *dhanvanty asmād āpaḥ* (that from which waters run, i.e., the atmosphere). For a bow, it is the support from which arrows speed.
* **Vedantic Meaning**: The bow represents the sacred Pranava (OM) or the Upanishadic teachings which support the soul (arrow) in targeting Brahman.
* **Grammatical (Pāṇini)**:
  * **Root**: √dhanv (धन्विँ गत्यर्थः, Bhvādi-gaṇa, 1.0694).
  * **Suffix**: Derived with suffix *kanin* or *vanip* by Uṇādi sūtra: **धन्वेरच् (Uṇādi 1.121)** or equivalent base derivation.
  * **Case**: Governed in the dative case (caturthī) by the presence of *namas* (2.3.16).
  * **Inflection**: Dative Singular.
* **Lexicographical**:
  * **Nighaṇṭu**: Listed under synonyms of the atmosphere (*antarikṣa-nāmāni*, Nighaṇṭu 1.3).
  * **Amarakośa**: Listed in Kṣatriyavarga (2.8.84) as a synonym for bow: **चापकार्मुककोदण्डशरासनानि धनुः**.
  * **Abhidhānaratnamālā**: Listed in Sāmānya-kāṇḍa (2.121) under weapons, alongside 'cāpa', 'kārmuka', and 'kodanda'.

### 13. बा॒हुभ्या᳚म् (bāhubhyām)
* **English Meaning**: To your two arms.
* **Nirukta/Etymology**: From root **√bah** (बह्) meaning "to grow/increase/be strong".
* **Vedantic Meaning**: Represents the dual operational powers of Brahman: *nigraha* (restraint of evil) and *anugraha* (bestowal of grace).
* **Grammatical (Pāṇini)**:
  * **Root**: √bah (बहँ वृद्धौ, Bhvādi-gaṇa, 1.0772).
  * **Suffix**: Uṇādi suffix **ku** (कु) by Uṇādi-sūtra: **बहेर्कुः (Uṇādi 1.28)**.
  * **Case**: Governed in the dative case (caturthī) by relation to *namas* (2.3.16).
  * **Inflection**: Dative Dual.
* **Lexicographical**:
  * **Nighaṇṭu**: Listed under synonyms of strength and physical limbs (*balam*, Nighaṇṭu 2.9).
  * **Amarakośa**: Listed in Manuṣyavarga (2.6.77) under limbs: **भुजो बाहुः प्रवेष्टोऽस्त्री**.
  * **Abhidhānaratnamālā**: Listed in Samanya-kāṇḍa (2.54) under body parts, with synonyms 'doh' and 'bhuja'.

---

> [!NOTE]
> The unified JSON database has been updated with these Sanskrit commentaries in [anuvakam1.json](file:///Users/Rkanadam/personal/namakam/src/anuvakam1.json) and [anuvakam1_words_sample.json](file:///Users/Rkanadam/personal/namakam/src/anuvakam1_words_sample.json).
