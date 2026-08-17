# Prompt Log

Running log of every distinct prompt template used by the app, appended to
automatically by `app/llm/prompt_log.py` on every LLM call (generation,
grading, adjudication). Entries below are the *templates*; the append-only
log entries with real prompt/response pairs get appended under `## [call_site] <timestamp>`
headers as the app runs.

## Templates

### generation (introduced Milestone 3)
System prompt: see `app/services/generation.py::SYSTEM_PROMPT`.
Purpose: generate one MCQ/cloze/short-answer question strictly grounded in a single retrieved chunk.

### grading (introduced Milestone 4)
System prompt: see `app/services/grading.py::SYSTEM_PROMPT`.
Purpose: score a short-answer response 0-1 against the source passage and answer key, with explanation.

### adjudication (introduced Milestone 4, not yet implemented)
Purpose: resolve a contested grade by re-grading with the student's note as additional context.

## [generation] 2026-08-14T14:47:52.810110+00:00

**Prompt:**
```
You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Passage (chunk_id=bfd7a6b7-395c-458e-b7ea-e13c5cee8951):
Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. This process takes place mainly in the leaves of plants, inside structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which absorbs sunlight. During photosynthesis, plants take in carbon dioxide from the air through small pores called stomata, and absorb water from the soil through their roots. Using light energy captured by chlorophyll, the plant converts carbon dioxide and water into glucose, a type of sugar that the plant uses for energy and growth. Oxygen is released as a byproduct of this reaction and is released into the atmosphere through the stomata. The overall chemical equation for photosynthesis is: six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose plus six molecules of oxygen. Photosynthesis is critical for life on Earth because it produces the oxygen that most living organisms need to breathe, and it forms the base of almost all food chains, since plants are primary producers that other organisms depend on for energy.

Generate one question from this passage.
```

**Response:**
```
What is the main product of photosynthesis?
```

## [generation] 2026-08-14T15:02:05.457544+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=bfd7a6b7-395c-458e-b7ea-e13c5cee8951):
Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. This process takes place mainly in the leaves of plants, inside structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which absorbs sunlight. During photosynthesis, plants take in carbon dioxide from the air through small pores called stomata, and absorb water from the soil through their roots. Using light energy captured by chlorophyll, the plant converts carbon dioxide and water into glucose, a type of sugar that the plant uses for energy and growth. Oxygen is released as a byproduct of this reaction and is released into the atmosphere through the stomata. The overall chemical equation for photosynthesis is: six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose plus six molecules of oxygen. Photosynthesis is critical for life on Earth because it produces the oxygen that most living organisms need to breathe, and it forms the base of almost all food chains, since plants are primary producers that other organisms depend on for energy.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What is the role of chlorophyll during photosynthesis?", "choices": ["Absorb sunlight", "Produce glucose", "Release oxygen", "Convert carbon dioxide"], "answer_key": "Absorb sunlight", "concept_tag": "Photosynthesis"}
```

## [generation] 2026-08-14T15:03:39.571421+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=bfd7a6b7-395c-458e-b7ea-e13c5cee8951):
Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. This process takes place mainly in the leaves of plants, inside structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which absorbs sunlight. During photosynthesis, plants take in carbon dioxide from the air through small pores called stomata, and absorb water from the soil through their roots. Using light energy captured by chlorophyll, the plant converts carbon dioxide and water into glucose, a type of sugar that the plant uses for energy and growth. Oxygen is released as a byproduct of this reaction and is released into the atmosphere through the stomata. The overall chemical equation for photosynthesis is: six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose plus six molecules of oxygen. Photosynthesis is critical for life on Earth because it produces the oxygen that most living organisms need to breathe, and it forms the base of almost all food chains, since plants are primary producers that other organisms depend on for energy.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What is released as a byproduct of photosynthesis according to the passage?", "choices": ["Oxygen", "Carbon Dioxide", "Glucose", "Water"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}
```

## [generation] 2026-08-14T15:07:51.276177+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=fdeb2efa-f38f-446e-8ce2-a2687cc0a7dc):
of all living organisms. There are two main types of cells: prokaryotic cells, which lack a nucleus and membrane-bound organelles, and eukaryotic cells, which have a true nucleus enclosed by a nuclear membrane along with various specialized organelles. Animal and plant cells are both eukaryotic but differ in important ways. Plant cells have a rigid cell wall made of cellulose, a large central vacuole for storage, and chloroplasts for photosynthesis, none of which are present in animal cells. The nucleus of a eukaryotic cell contains the cell's genetic material, DNA, organized into chromosomes, and controls the cell's activities by regulating gene expression. The cell membrane, found in all cells, is a selectively permeable barrier made of a phospholipid bilayer that controls what substances enter and leave the cell. DNA, or deoxyribonucleic acid, is the molecule that carries the genetic instructions used in the growth, development, functioning, and reproduction of all known living organisms. DNA is structured as a double helix, made up of two strands that wind around each other, connected by pairs of nucleotide bases: adenine pairs with thymine, and guanine pairs with cytosine. This complementary base pairing is what allows DNA to be accurately copied during cell division. The sequence of these four bases along a DNA strand encodes the genetic instructions needed to build and maintain an organism, much like letters in an alphabet spell out words and sentences. Genes are specific segments of DNA that contain the instructions for making particular proteins, and proteins in turn carry out most of the functions within cells. An ecosystem is a community of living organisms interacting with each other and with their physical environment, including factors like sunlight, temperature, soil, and water. Ecosystems are typically organized into trophic levels based on how organisms obtain energy: producers, such as plants, which generate their own energy through photosynthesis; primary consumers, or herbivores, which eat producers; secondary consumers, or carnivores, which eat herbivores; and decomposers, such as fungi and bacteria, which break down dead organic matter and recycle nutrients back into the ecosystem. Energy flows through an ecosystem in one direction, typically depicted as a food chain or a more complex food web, while nutrients like carbon and nitrogen are cycled and reused repeatedly through biogeochemical cycles.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "In the DNA double helix structure described in the passage, which base pairs with adenine?", "choices": ["Thymine", "Cytosine", "Guanine", "Uracil"], "answer_key": "Thymine", "concept_tag": "DNA Base Pairing"}
```

## [generation] 2026-08-14T15:08:45.736904+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=939f1f6b-2f7f-47c6-b3c3-c61d12f03dbf):
fungi and bacteria, which break down dead organic matter and recycle nutrients back into the ecosystem. Energy flows through an ecosystem in one direction, typically depicted as a food chain or a more complex food web, while nutrients like carbon and nitrogen are cycled and reused repeatedly through biogeochemical cycles. A stable ecosystem depends on a balance between these different trophic levels; disrupting one level, for example by removing a top predator, can cause cascading effects throughout the entire food web.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "Which organisms break down dead organic matter and recycle nutrients in an ecosystem?", "choices": ["Fungi and bacteria", "Plants", "Viruses", "Algae"], "answer_key": "Fungi and bacteria", "concept_tag": "nutrient recycling"}
```

## [generation] 2026-08-14T15:09:37.522650+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=c30be9f6-ad2c-4c8a-ae8e-40439b74db5b):
Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. This process takes place mainly in the leaves of plants, inside structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which absorbs sunlight. During photosynthesis, plants take in carbon dioxide from the air through small pores called stomata, and absorb water from the soil through their roots. Using light energy captured by chlorophyll, the plant converts carbon dioxide and water into glucose, a type of sugar that the plant uses for energy and growth. Oxygen is released as a byproduct of this reaction and is released into the atmosphere through the stomata. The overall chemical equation for photosynthesis is: six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose plus six molecules of oxygen. Photosynthesis is critical for life on Earth because it produces the oxygen that most living organisms need to breathe, and it forms the base of almost all food chains, since plants are primary producers that other organisms depend on for energy. Cellular respiration is the process by which cells break down glucose to release energy in the form of ATP, or adenosine triphosphate. This process happens in the mitochondria, often called the powerhouse of the cell. Cellular respiration uses oxygen and glucose as inputs and produces carbon dioxide, water, and energy as outputs, which makes it essentially the reverse of photosynthesis. There are three main stages of cellular respiration: glycolysis, which occurs in the cytoplasm and breaks glucose into pyruvate; the Krebs cycle, which occurs in the mitochondrial matrix and produces electron carriers; and the electron transport chain, which occurs on the inner mitochondrial membrane and produces the majority of the ATP. Cellular respiration is essential because ATP is the energy currency that powers nearly all cellular activities, from muscle contraction to protein synthesis. The cell is the basic structural and functional unit of all living organisms. There are two main types of cells: prokaryotic cells, which lack a nucleus and membrane-bound organelles, and eukaryotic cells, which have a true nucleus enclosed by a nuclear membrane along with various specialized organelles. Animal and plant cells are both eukaryotic but differ in important ways.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "In which organelle does photosynthesis primarily occur?", "choices": ["Chloroplasts", "Mitochondria", "Nucleus", "Vacuole"], "answer_key": "Chloroplasts", "concept_tag": "Chloroplasts"}
```

## [generation] 2026-08-14T15:20:11.576883+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=42549437-0a0e-4520-b4b2-e320283ce4c7):
performance, learning efficiency, and health outcomes. Addressing this issue is essential for improving students' academic success and overall well-being. PARADIGM: The study follows a cause-and-effect paradigm where late-night nocturnal alertness is considered the independent variable, while cognitive performance, academic learning efficiency, and physical and mental health outcomes are dependent variables. The framework suggests that increased
nocturnal alertness leads to sleep deprivation, which negatively influences students' academic and
health-related outcomes. PROCEDURE:
The study was conducted by selecting a sample of students aged 18–25 from educational
institutions. Data was collected through questionnaires focusing on sleep patterns, study habits,
and academic performance. Students were asked about their late-night activities and health
conditions. The collected data was then analyzed using simple statistical methods to identify the
relationship between nocturnal alertness and its effects on cognitive performance, learning
efficiency, and physical and mental health outcomes. SAMPLE / TARGET AUDIENCE / TOOLS:
Sample: University and college students (age 18–25)
Target Audience: Students, educators, and academic researchers
TOOLS:
• Questionnaire/Survey
• Sleep pattern tracking
• Academic performance records
• Statistical analysis software (SPSS/Excel)
THEROTICAL FRAMEWORK:
This study is based on sleep deprivation and circadian rhythm theories, which explain how late-
night nocturnal alertness affects students’ cognitive performance, learning efficiency, and health. According to these theories, staying awake at night disrupts the body’s natural sleep-wake cycle,
leading to reduced concentration, weak memory, and poor academic performance. Continuous

sleep disturbance also impacts physical health and increases stress, anxiety, and mental fatigue
among students. HYPOTHESES:
H0 (Null Hypothesis):
Late-night nocturnal alertness has no significant effect on students’ cognitive performance,
academic learning efficiency, or health outcomes. H1 (Alternative Hypothesis):
Late-night nocturnal alertness has a significant negative effect on students’ cognitive
performance, academic learning efficiency, and health outcomes. TERMINOLOGY:
 Nocturnal Alertness – Being active or awake during late-night hours
 Cognitive Performance – Mental abilities like memory, attention, and reasoning
 Sleep Deprivation – Lack of sufficient sleep
 Academic Efficiency – Ability to learn and perform academically
 Circadian Rhythm – Body’s natural sleep-wake cycle
RECOMMENDATIONS:
Students should adopt consistent sleep schedules by going to bed and waking up at regular times to
maintain a healthy circadian rhythm. Reducing screen time before bedtime and avoiding stimulants
like caffeine at night can improve sleep quality. Educational institutions should raise awareness
about the importance of sleep through workshops and counseling sessions.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What does the study suggest about the effect of late-night nocturnal alertness on students' cognitive performance and health outcomes?", "choices": ["No significant effect", "Significant negative effect", "Improves academic efficiency", "Only affects physical health"], "answer_key": "Significant negative effect", "concept_tag": "Sleep Deprivation Research"}
```

## [generation] 2026-08-14T15:20:46.605385+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=0cc270c9-c49f-400e-bd09-507fb8a43c06):
consistent sleep schedules by going to bed and waking up at regular times to maintain a healthy circadian rhythm. Reducing screen time before bedtime and avoiding stimulants like caffeine at night can improve sleep quality. Educational institutions should raise awareness about the importance of sleep through workshops and counseling sessions. Time management
strategies should be encouraged so students can complete academic tasks during the day instead of
staying up late. Additionally, creating a quiet and comfortable sleep environment can further
support better rest and overall well-being. CONCLUSION:
Late-night alertness negatively affects students’ cognitive abilities, learning efficiency, and health. Proper sleep is essential for academic success and well-being. By adopting healthy sleep habits and
reducing late-night activities, students can improve both their academic performance and overall
quality of life. REFERENCE:
Walker, M. (2017). Why we sleep: Unlocking the power of sleep and dreams. Scribner. Pilcher, J. J., & Huffcutt, A. I. (1996). Effects of sleep deprivation on performance: A meta-
analysis. Sleep, 19(4), 318–326. Lim, J., & Dinges, D. F. (2010). A meta-analysis of the impact of short-term sleep deprivation on
cognitive variables. Psychological Bulletin, 136(3), 375–389. Curcio, G., Ferrara, M., & De Gennaro, L. (2006). Sleep loss, learning capacity, and academic
performance. Sleep Medicine Reviews, 10(5), 323–337. Hershner, S. D., & Chervin, R. D. (2014). Causes and consequences of sleepiness among college
students. Nature and Science of Sleep, 6, 73–84. Taheri, S., Lin, L., Austin, D., Young, T., & Mignot, E. (2004). Short sleep duration is associated
with reduced leptin and increased ghrelin levels. PLoS Medicine, 1(3), e62. Baglioni, C., Battagliese, G., Feige, B., Spiegelhalder, K., Nissen, C., Voderholzer, U., &
Riemann, D. (2016). Insomnia as a predictor of depression. Journal of Affective Disorders,
135(1–3), 10–19. Cain, N., & Gradisar, M. (2010). Electronic media use and sleep in school-aged children and
adolescents. Sleep Medicine, 11(8), 735–742. Lemola, S., Perkinson-Gloor, N., Brand, S., Dewald-Kaufmann, J., & Grob, A. (2015). Adolescents’ electronic media use at night and sleep disturbance. Journal of Youth and
Adolescence, 44(2), 405–418. Roenneberg, T., Allebrandt, K. V., Merrow, M., & Vetter, C. (2012). Social jetlag and obesity. Current Biology, 22(10), 939–943.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What negative effect does late-night alertness have on students according to the passage?", "choices": ["Improves academic performance", "Enhances memory retention", "Negatively affects cognitive abilities, learning efficiency, and health", "Increases alertness during class"], "answer_key": "Negatively affects cognitive abilities, learning efficiency, and health", "concept_tag": "Sleep and academic performance"}
```

## [generation] 2026-08-14T15:21:09.334602+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=bebb9d0d-a68d-45d7-ba2b-a62ba52c68af):
deprivation affects the brain's ability to process and retain new information. Furthermore, Hershner and Chervin (2014) emphasized that students who stay up late often struggle with time management, resulting in decreased productivity and learning outcomes. In addition to cognitive and academic effects, late-night wakefulness has serious implications for physical health. Lack of sleep is associated with weakened immune function, increased risk of
obesity, and hormonal imbalances (Taheri et al., 2004). Students who consistently experience poor
sleep may develop fatigue, headaches, and reduced physical energy levels, which can further
hinder their academic performance. Mental health is another critical area affected by nocturnal alertness. Studies indicate that sleep
deprivation is strongly linked to anxiety, depression, and mood disorders (Baglioni et al., 2016). Late-night habits, particularly excessive use of digital devices, contribute to emotional instability
and stress among students. Lemola et al. (2015) found that screen exposure at night negatively
impacts sleep quality and increases depressive symptoms. Moreover, the use of smartphones and social media during late hours has intensified the problem. Cain and Gradisar (2010) highlighted that electronic media use before bedtime delays sleep onset
and reduces sleep duration. This behavior creates a cycle where students stay awake longer, leading
to daytime sleepiness and reduced academic engagement. The concept of "nocturnal alertness" is often linked to chronotype differences, where some
individuals are naturally inclined to stay awake at night. However, academic schedules are
typically aligned with early morning routines, creating a mismatch that affects students’
performance (Roenneberg et al., 2012). This misalignment can result in what is known as "social
jetlag," negatively impacting both learning and health. Recent studies have also explored strategies to mitigate the effects of late-night wakefulness. Sleep
hygiene practices, such as maintaining a consistent sleep schedule, reducing screen time, and
creating a conducive sleep environment, have been shown to improve sleep quality and academic
outcomes (Hershner, 2020). Educational interventions that raise awareness about the importance of
sleep can help students adopt healthier habits. In conclusion, existing literature clearly demonstrates that late-night alertness has a negative
impact on cognitive performance, learning efficiency, and health outcomes. Addressing this issue
is essential for improving students' academic success and overall well-being. PARADIGM:
The study follows a cause-and-effect paradigm where late-night nocturnal alertness is considered
the independent variable, while cognitive performance, academic learning efficiency, and physical
and mental health outcomes are dependent variables.

Generate one question from this passage.
```

**Response:**
```
{"type": "short_answer", "prompt": "What are the main negative impacts of nocturnal alertness on students according to the passage?", "choices": null, "answer_key": "Negative effects include impaired cognitive performance, reduced academic learning efficiency, weakened physical health (e.g., weakened immune function, obesity, hormonal imbalances), and mental health issues (e.g., anxiety, depression, mood disorders).", "concept_tag": "nocturnal alertness"}
```

## [generation] 2026-08-14T15:21:29.953882+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=7c6a2f6e-2749-4730-8af1-f9831e783746):
that pose serious risks to operational safety and productivity (Åkerstedt, 1991; Dinges, 1995; Duchon and Smith, 1993; Krueger, 1989; Pilcher and Huffcut, 1996; Williamson and Feyer, 2000). Such issues are especially critical in safety-sensitive industries such as transportation, emergency healthcare, and nuclear or chemical power operations (Mitler et al., 1988). To evaluate the impact of sleep deprivation on cognitive performance, researchers often examine
tonic alertness using neuropsychological and neurophysiological methods. Among these, the
Psychomotor Vigilance Task (PVT) is one of the most widely used tools. It measures sustained
attention and reaction speed in response to visual or auditory stimuli, making it a robust indicator of
hypo-vigilance states. The PVT is particularly valued due to its high sensitivity, reliability, and
minimal learning effects [13], [14], [15]. Studies using PVT consistently demonstrate that sleep
deprivation impairs sustained attention and increases reaction time variability (Lim and Dinges,
2008). Sleep inertia (SI), the transitional state immediately following awakening, further complicates the
recovery of alertness. SI is influenced by two main factors: passive resistance from sleep (such as
duration since sleep offset and the depth of non-rapid eye movement sleep) and active recovery
processes involving trait- and state-dependent mechanisms that determine the speed of
wakefulness restoration [24], [29]. These interacting processes shape the time-dependent recovery
of cognitive performance after awakening. Recent neuroimaging research has shown that functional brain indices during sleep inertia exhibit
time-varying dynamics that influence tonic alertness performance. In particular, activity within the
central executive network (CON), including the thalamus, shows a characteristic pattern
immediately after waking—initially reduced and then gradually increasing over time. The
thalamus plays a key role in mediating the relationship between prior sleep history, awake
duration, and psychomotor vigilance task performance. Furthermore, functional connectivity
between the CON and frontoparietal network (FPN), especially involving the thalamus, is strongly
associated with the recovery of reaction speed during the transition from sleep to wakefulness
(Mitler et al., 1988). Beyond laboratory sleep deprivation studies, sleep timing itself has emerged as a critical
determinant of cognitive and neurobiological health. In entrepreneurial and high-performance
environments, individuals frequently sacrifice sleep in pursuit of productivity, often extending
work into late-night hours. Sleep onset after 2 AM has been identified as a particularly harmful
pattern that disrupts cognitive processes essential for decision-making, risk evaluation, creativity,
and emotional regulation. The timing of sleep is therefore as important as its duration.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What are the two main factors influencing sleep inertia according to the passage?", "choices": ["Passive resistance from sleep and active recovery processes", "Duration of sleep and reaction time variability", "Central executive network activity and thalamus function", "Sleep timing and neuroimaging methods"], "answer_key": "Passive resistance from sleep and active recovery processes", "concept_tag": "Sleep Inertia"}
```

## [generation] 2026-08-14T15:22:35.761337+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=a56430a8-3e38-4f14-aee5-4db830500865):
IMPACT OF LATE NIGHT NOCTURNAL
ALERTNESS
OBJECTIVES:
 To examine the effect of late-night nocturnal alertness on students’ cognitive performance
 To analyze the relationship between late-night wakefulness and academic learning
efficiency
 To evaluate the impact of nocturnal alertness on physical and mental health outcomes
RESEARCH QUESTIONS:
 What is the effect of late-night nocturnal alertness on students’ cognitive performance?  What is the relationship between late-night wakefulness and academic learning efficiency?  How does nocturnal alertness impact physical and mental health outcomes? INTRODUCTION:
Over the years, sleep deprivation has been widely used as a primary experimental tool to
understand the mechanisms and functions of sleep. Most existing literature focuses on total sleep
deprivation [1], [2], while comparatively fewer studies examine long-term partial sleep restriction
or sleep extension. For individuals without sleep disorders, excessive sleepiness is generally
attributed to chronic sleep loss. A potential solution to the widespread societal issue of fatigue and
dangerous sleepiness is the extension of habitual sleep duration in the general population. However, such a solution requires strong evidence that sleep extension consistently improves
waking alertness, psychomotor performance, and mood without adverse effects or inefficiency
(Gillberg). Alertness is a cognitive construct associated with a high level of environmental awareness and
sensitivity to external stimuli (Figueiro et al., 2009). It is defined as the ability to achieve and
maintain a state of heightened responsiveness to incoming sensory information (Posner, 2008). In
contrast, sleepiness represents a decline in this state and is often described as the subjective
tendency or propensity to fall asleep (Moller et al., 2006). Although sleepiness is commonly treated
as the opposite of alertness, the two constructs are not perfectly symmetrical and may reflect
partially independent neurobehavioral states. In modern society, especially within high-demand occupational environments, individuals are
often required to maintain sustained levels of optimal cognitive performance. However,
compressed work schedules and shift-based systems impose significant strain on workers,
frequently resulting in sleep loss and circadian disruption, particularly when night shifts are
extended (Åkerstedt, 1991; Rosekind et al., 1995). These conditions contribute to increased
sleepiness, reduced performance, and attentional failures that pose serious risks to operational
safety and productivity (Åkerstedt, 1991; Dinges, 1995; Duchon and Smith, 1993; Krueger, 1989;

Pilcher and Huffcut, 1996; Williamson and Feyer, 2000). Such issues are especially critical in
safety-sensitive industries such as transportation, emergency healthcare, and nuclear or chemical
power operations (Mitler et al., 1988).

Generate one question from this passage.
```

**Response:**
```
{"type": "cloze", "prompt": "The study aims to examine the effect of late-night nocturnal alertness on students’ ____ performance.", "choices": null, "answer_key": "cognitive", "concept_tag": "Cognitive Performance"}
```

## [generation] 2026-08-14T15:34:27.116751+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=bfd7a6b7-395c-458e-b7ea-e13c5cee8951):
Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. This process takes place mainly in the leaves of plants, inside structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which absorbs sunlight. During photosynthesis, plants take in carbon dioxide from the air through small pores called stomata, and absorb water from the soil through their roots. Using light energy captured by chlorophyll, the plant converts carbon dioxide and water into glucose, a type of sugar that the plant uses for energy and growth. Oxygen is released as a byproduct of this reaction and is released into the atmosphere through the stomata. The overall chemical equation for photosynthesis is: six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose plus six molecules of oxygen. Photosynthesis is critical for life on Earth because it produces the oxygen that most living organisms need to breathe, and it forms the base of almost all food chains, since plants are primary producers that other organisms depend on for energy.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What is the primary function of chlorophyll in photosynthesis?", "choices": ["To absorb sunlight", "To release oxygen", "To transport water", "To store glucose"], "answer_key": "To absorb sunlight", "concept_tag": "Chlorophyll role in photosynthesis"                                            
                      
                     
                      
             
                      
                      
                      
                     
                      
                      
                      
                     
                      
                      
                      
           
                      
                      
                      
                      
                     
                 …
```

## [generation] 2026-08-14T15:34:42.396580+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=bfd7a6b7-395c-458e-b7ea-e13c5cee8951):
Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy. This process takes place mainly in the leaves of plants, inside structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which absorbs sunlight. During photosynthesis, plants take in carbon dioxide from the air through small pores called stomata, and absorb water from the soil through their roots. Using light energy captured by chlorophyll, the plant converts carbon dioxide and water into glucose, a type of sugar that the plant uses for energy and growth. Oxygen is released as a byproduct of this reaction and is released into the atmosphere through the stomata. The overall chemical equation for photosynthesis is: six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose plus six molecules of oxygen. Photosynthesis is critical for life on Earth because it produces the oxygen that most living organisms need to breathe, and it forms the base of almost all food chains, since plants are primary producers that other organisms depend on for energy.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What pigment in chloroplasts absorbs sunlight during photosynthesis?", "choices": ["Chlorophyll", "Carotenoids", "Cell walls", "Stomata"], "answer_key": "Chlorophyll", "concept_tag": "Chlorophyll"}
```

## [generation] 2026-08-14T15:49:19.884188+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=41d79f3b-27fb-4557-9920-b1a5dcf8e0ff):
consistent sleep schedules by going to bed and waking up at regular times to maintain a healthy circadian rhythm. Reducing screen time before bedtime and avoiding stimulants like caffeine at night can improve sleep quality. Educational institutions should raise awareness about the importance of sleep through workshops and counseling sessions. Time management
strategies should be encouraged so students can complete academic tasks during the day instead of
staying up late. Additionally, creating a quiet and comfortable sleep environment can further
support better rest and overall well-being. CONCLUSION:
Late-night alertness negatively affects students’ cognitive abilities, learning efficiency, and health. Proper sleep is essential for academic success and well-being. By adopting healthy sleep habits and
reducing late-night activities, students can improve both their academic performance and overall
quality of life. REFERENCE:
Walker, M. (2017). Why we sleep: Unlocking the power of sleep and dreams. Scribner. Pilcher, J. J., & Huffcutt, A. I. (1996). Effects of sleep deprivation on performance: A meta-
analysis. Sleep, 19(4), 318–326. Lim, J., & Dinges, D. F. (2010). A meta-analysis of the impact of short-term sleep deprivation on
cognitive variables. Psychological Bulletin, 136(3), 375–389. Curcio, G., Ferrara, M., & De Gennaro, L. (2006). Sleep loss, learning capacity, and academic
performance. Sleep Medicine Reviews, 10(5), 323–337. Hershner, S. D., & Chervin, R. D. (2014). Causes and consequences of sleepiness among college
students. Nature and Science of Sleep, 6, 73–84. Taheri, S., Lin, L., Austin, D., Young, T., & Mignot, E. (2004). Short sleep duration is associated
with reduced leptin and increased ghrelin levels. PLoS Medicine, 1(3), e62. Baglioni, C., Battagliese, G., Feige, B., Spiegelhalder, K., Nissen, C., Voderholzer, U., &
Riemann, D. (2016). Insomnia as a predictor of depression. Journal of Affective Disorders,
135(1–3), 10–19. Cain, N., & Gradisar, M. (2010). Electronic media use and sleep in school-aged children and
adolescents. Sleep Medicine, 11(8), 735–742. Lemola, S., Perkinson-Gloor, N., Brand, S., Dewald-Kaufmann, J., & Grob, A. (2015). Adolescents’ electronic media use at night and sleep disturbance. Journal of Youth and
Adolescence, 44(2), 405–418. Roenneberg, T., Allebrandt, K. V., Merrow, M., & Vetter, C. (2012). Social jetlag and obesity. Current Biology, 22(10), 939–943.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What practice is recommended to maintain a healthy circadian rhythm according to the passage?", "choices": ["Irregular sleep times", "Consistent sleep schedules", "Increased screen time before bed", "Consuming caffeine at night"], "answer_key": "Consistent sleep schedules", "concept_tag": "Circadian Rhythm"}
```

## [generation] 2026-08-16T14:54:45.045310+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=bc30161e-247a-40d5-9b9d-3f13dbe24735):
concept_id, ease_factor, interval_days, repetitions, last_reviewed_at, accuracy_ema | SM-2 state per concept | | `schedule_items` | id, user_id, concept_id, due_at, status | drives the "due today" queue | | `contests` | id, attempt_id, student_note, status (open/resolved), resolution_note | contest-a-grade flow | **Indexes:** `ivfflat` on `chunks.embedding` (cosine distance), btree on `schedule_items.due_at`, `schedule_items.user_id`. ### 1.3 API Endpoints

```
POST   /auth/register
POST   /auth/login
GET    /auth/me

POST   /subjects
GET    /subjects

POST   /materials/upload            # multipart upload → triggers ingest.py (background task)
GET    /materials/{id}/status       # polling for processing state

GET    /quiz/session/next           # scheduler picks weakest due concept, returns a generated set of questions
POST   /quiz/attempts               # submit an answer → triggers grading skill, returns score+explanation
POST   /quiz/attempts/{id}/contest  # flag a grade

GET    /dashboard/mastery           # per-concept mastery %
GET    /dashboard/due-today
GET    /dashboard/streak
GET    /dashboard/history
```

### 1.4 Service Layer Detail

**`ingest.py` — Upload & Chunking Pipeline**
1. Validate file type (PDF/MD/TXT). PDFs: extract text via `pypdf`/`pdfplumber`; if extraction yields near-empty text, mark `status=needs_review` (handwritten/scanned handling explicitly out of scope for v1, per proposal). 2. Chunk text (target ~300–500 tokens, sentence-boundary aware, slight overlap). 3. Embed each chunk (`llm/embeddings.py`) and bulk-insert into `chunks` with pgvector column. 4. Mark `materials.status = ready`. 5. Run as a FastAPI `BackgroundTasks` job (or a lightweight queue like `arq`/Celery if upload volume justifies it — start with `BackgroundTasks` for v1 simplicity). **`retrieval.py` — "Search My Notes" Tool**
- `search(query: str, subject_id, top_k=5) -> list[Chunk]`
- Embeds the query, runs `ORDER BY embedding <=> query_vector LIMIT top_k` against pgvector. - This function is exposed to the generation/grading skills as a callable tool — not just an internal helper — so the agent primitive (retrieval tool) is real, not simulated. **`generation.py` — Question-Generation Skill**
- Input: a retrieved chunk (+ desired question type). - Calls the fast/cheap model via OpenRouter with a strict system prompt: *"Generate a question ONLY from the passage below. Do not introduce facts not present. Return JSON: {type, prompt, choices?, answer_key, concept_tag}."*
- Validates the response is well-formed JSON and that `concept_tag` maps to (or creates) a `concepts` row. - **Guardrail (Risk #2 in proposal):** reject and retry once if the model's output can't be traced to the source chunk_id; log failures to `prompts.md`. **`grading.py` — Grading Skill**
- Input: student's free-text answer + the original source chunk + answer key.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "Which of the following accurately lists the steps in the ingest.py upload and chunking pipeline?", "choices": ["1. Validate file type, chunk text, embed chunks, mark materials.status=ready, run as BackgroundTasks job", "2. Upload file, parse content, store in database, index embeddings, schedule review", "3. Clean text, segment into paragraphs, embed chunks, index via btree, mark status=needs_review", "4. Validate file, chunk text, store embeddings in pgvector, mark status=ready, use arq queue"], "answer_key": "1. Validate file type, chunk text, embed chunks, mark materials.status=ready, run as BackgroundTasks job", "concept_tag": "Ingestion Pipeline"}
```

## [generation] 2026-08-16T14:55:09.039200+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=6d471002-1d91-468d-9253-93b9778451f5):
`concept_tag` maps to (or creates) a `concepts` row. - **Guardrail (Risk #2 in proposal):** reject and retry once if the model's output can't be traced to the source chunk_id; log failures to `prompts.md`. **`grading.py` — Grading Skill** - Input: student's free-text answer + the original source chunk + answer key. - Calls Claude API with a grading rubric prompt: partial credit scoring (0–1), plus a short explanation of what was missed, grounded explicitly in the passage. - Deterministic question types (MCQ/cloze) are graded in plain code (exact/normalized match) — **no model call needed**, per the code-vs-model design principle. Only short-answer goes to the LLM. **`scheduler.py` — Pure-Code Spaced Repetition**
- Implements SM-2 (or simplified Leitner) update rules: given `ease_factor`, `interval_days`, `repetitions`, and the latest score, compute the next `due_at`. - No model call anywhere in this file — deliberately deterministic and unit-testable in isolation. **`memory.py` — Mastery & Error Patterns**
- Updates `mastery` row per concept after each attempt (accuracy EMA). - Stores recurring error patterns as short text tags (e.g., derived from repeated low-score explanations on the same concept pair) that bias future question selection toward weak spots. **`hooks.py` — Scheduler Interceptor**
- A function invoked (a) when `schedule_items.due_at <= now`, or (b) when a concept's rolling accuracy drops below a threshold (e.g. 60%). - Surfaces a "review session available" flag the frontend polls/displays, rather than the student needing to manually request one. ### 1.5 LLM Client Layer

- `llm/openrouter_client.py` — thin wrapper for the fast/cheap generation model; retries with backoff; strict JSON-mode prompting. - `llm/claude_client.py` — wrapper for grading, contest adjudication, and miss-explanations; uses the Anthropic `/v1/messages` endpoint. - Every LLM call is logged (prompt + response, truncated) to `prompts.md` per the program requirement, tagged with a call-site identifier (`generation`, `grading`, `adjudication`). ### 1.6 Backend Milestones (maps to proposal's 6-milestone plan)

1. **Foundation** — FastAPI scaffold, Alembic migrations, Postgres + pgvector extension enabled, JWT auth, `/auth` routes working end-to-end. 2. **Ingest & Retrieval** — `/materials/upload`, chunking, embedding, `retrieval.search()` returning correct top-k chunks (verify with a manual query test). 3. **Quiz Core** — `generation.py` producing valid MCQ/cloze questions from real chunks; `/quiz/session/next` returns a playable session; `attempts` persisted. 4. **Grading & Grounding** — `grading.py` for short-answer via Claude; MCQ/cloze graded deterministically; every response includes source chunk reference; `/quiz/attempts/{id}/contest` implemented. 5. **Memory + Scheduler** — `scheduler.py` SM-2 logic unit-tested; `mastery` + `schedule_items` wired into the full loop; `hooks.py` due/weak-spot detection.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "Which module in the system stores recurring error patterns as short text tags to bias future question selection?", "choices": ["grading.py", "scheduler.py", "memory.py", "hooks.py"], "answer_key": "memory.py", "concept_tag": "Error Patterns"}
```

## [generation] 2026-08-16T14:55:33.728315+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=09197a34-9654-4c55-8efc-72c87d49fc73):
question at a time using the type-specific card component (MCQ, cloze, short-answer). - Progress bar showing position in session. - On submit: POST to `/quiz/attempts`; while short-answer grading is in flight, show a distinct "grading…" state (LLM latency) vs. the instant feedback for MCQ/cloze (client- or server-side deterministic grading, near-instant). - Immediately after grading, shows score + explanation + a "View source" toggle that opens `SourcePassagePanel`. **Answer review (`/review/[attemptId]`)**
- Full-width layout: student's answer and grade on one side, `SourcePassagePanel` (the exact chunk) on the other. - `ContestGradeButton` opens a small form (student note) → `POST /quiz/attempts/{id}/contest`. **Dashboard (`/dashboard`)**
- `MasteryHeatmap`: concept × mastery %, color-scaled. - `DueTodayList`: items surfaced by the backend hook. - `StreakBadge`: current streak from `/dashboard/streak`. - `TopicHistoryChart`: accuracy over time per topic (simple line chart). **Profile (`/profile`)**
- Standard account management (email, password change, logout). ### 2.3 State & Data Fetching

- Use React Query (`@tanstack/react-query`) for all server state (materials, quiz session, dashboard) — gives polling (upload status), caching, and mutation handling for attempts/contests out of the box. - Local component state only for in-progress answer input. - Auth token stored in an httpOnly cookie set by the backend on login (avoid localStorage for the JWT); `lib/auth.ts` handles redirect-on-401. ### 2.4 Frontend Milestones (maps to proposal's 6-milestone plan)

1. **Foundation** — Next.js scaffold, auth pages wired to `/auth`, protected route shell. 2. **Ingest & Retrieval** — Upload screen with dropzone + status polling; subject organization UI. 3. **Quiz Core** — Session screen rendering MCQ/cloze cards from `/quiz/session/next`; attempts posted and persisted. 4. **Grading & Grounding** — Short-answer card + grading-in-progress state; `SourcePassagePanel`; contest flow UI. 5. **Memory + Scheduler** — Dashboard: mastery heatmap, due-today list, streak; due-item notifications surfaced from the hook. 6. **Finish Line** — Session history view, polish pass, empty/error states, responsive check. ---

## 3. Cross-Cutting Concerns

- **Environment config:** `.env` for both frontend (`NEXT_PUBLIC_API_URL`) and backend (`DATABASE_URL`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `JWT_SECRET`). - **Testing:** Pytest + Httpx for backend (unit tests per service in `services/`, one integration test covering the full loop per the proposal's testing plan); component-level tests for frontend optional given time constraints — prioritize the backend loop. - **Error handling:** Every LLM-dependent endpoint returns a distinguishable error state so the frontend can show "retry" rather than a generic failure — scheduling/progress writes never depend on a live model call succeeding (per Risk table).

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "Which library is used for server state management in the frontend according to the passage?", "choices": ["Axios", "Redux", "React Query", "GraphQL"], "answer_key": "React Query", "concept_tag": "State Management" }
```

## [generation] 2026-08-16T14:56:00.016051+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=5c4dff1d-13da-4cce-a1bb-968b9b681ec8):
│ │ Claude API (grading, │ │ adjudication) │ └───────────────────────┘ ``` Core loop: **Upload → Chunk & Embed → Scheduler picks weakest due concept → Retrieval tool pulls passages → Question-Generation skill → Student answers → Grading skill (vs. source) → Memory updates mastery → Scheduler reschedules.** --- ## 1. Backend Implementation Plan (FastAPI)

### 1.1 Project Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── config.py                # env vars, settings (pydantic-settings)
│   ├── db/
│   │   ├── session.py           # SQLAlchemy engine/session
│   │   ├── base.py              # declarative base
│   │   └── models/
│   │       ├── user.py
│   │       ├── material.py
│   │       ├── chunk.py
│   │       ├── question.py
│   │       ├── attempt.py
│   │       ├── mastery.py
│   │       └── schedule_item.py
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── auth.py
│   │   ├── material.py
│   │   ├── quiz.py
│   │   └── dashboard.py
│   ├── api/
│   │   ├── deps.py              # auth dependency, DB session dependency
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── materials.py
│   │       ├── quiz.py
│   │       ├── attempts.py
│   │       ├── dashboard.py
│   │       └── contests.py
│   ├── services/
│   │   ├── ingest.py            # chunking + embedding pipeline
│   │   ├── retrieval.py         # "search my notes" tool
│   │   ├── generation.py        # question-generation skill
│   │   ├── grading.py           # grading skill
│   │   ├── scheduler.py         # SM-2/Leitner arithmetic (pure code)
│   │   ├── memory.py            # mastery + error-pattern store
│   │   └── hooks.py             # due-item / weak-topic interceptor
│   ├── llm/
│   │   ├── openrouter_client.py
│   │   ├── claude_client.py
│   │   └── embeddings.py
│   └── core/
│       ├── security.py          # password hashing, JWT
│       └── logging.py
├── tests/
│   ├── unit/
│   └── integration/
├── alembic/                     # DB migrations
├── prompts.md                   # running log of prompts used
├── pyproject.toml
└── .env.example
```

### 1.2 Database Schema (PostgreSQL + pgvector)

| Table | Key Columns | Notes |
|---|---|---|
| `users` | id, email, hashed_password, created_at | standard auth |
| `subjects` | id, user_id, name | organizes materials |
| `materials` | id, subject_id, filename, source_type (pdf/md/txt), status (processing/ready/failed), created_at | one row per upload |
| `chunks` | id, material_id, content, embedding (vector), page_ref, char_range, created_at | pgvector column, indexed with `ivfflat` |
| `concepts` | id, subject_id, name | derived/tagged during generation |
| `questions` | id, chunk_id, concept_id, type (mcq/cloze/short_answer), prompt, choices (jsonb, nullable), answer_key, created_at | every question stores its source chunk_id (anti-drift requirement) |
| `attempts` | id, question_id, user_id, student_answer, score, feedback, graded_at | grading result + explanation |
| `mastery` | id, user_id, concept_id, ease_factor, interval_days, repetitions, last_reviewed_at, accuracy_ema | SM-2 state per concept |
| `schedule_items` | id, user_id, concept_id, due_at, status | drives the "due today" queue |
| `contests` | id, attempt_id, student_note, status (open/resolved), resolution_note | contest-a-grade flow |

**Indexes:** `ivfflat` on `chunks.embedding` (cosine distance), btree on `schedule_items.due_at`, `schedule_items.user_id`.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "Which column in the 'questions' table ensures the source material reference to prevent drift?", "choices": ["user_id", "concept_id", "chunk_id", "material_id"], "answer_key": "chunk_id", "concept_tag": "Question Source Linking"}
```

## [generation] 2026-08-16T14:56:17.406581+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=d68777e2-fb93-4d47-b1ad-ac1f09c5ae85):
# Recall — Implementation Plan

*Companion to the Internship Project Proposal. Covers frontend, backend, database, and the AI agent pipeline in enough detail to start building milestone 1 immediately.*

---

## 0. Architecture Overview

```
┌─────────────────────┐      ┌──────────────────────┐      ┌────────────────────────┐
│   React (Next.js)   │ ───▶ │   FastAPI Backend     │ ───▶ │  PostgreSQL + pgvector  │
│  Upload / Quiz UI    │ ◀── │  Ingest, Scheduler,   │ ◀──  │  users, materials,      │
│  Dashboard           │      │  Grading Orchestrator │      │  chunks, questions,     │
└─────────────────────┘      └──────────┬───────────┘      │  attempts, mastery      │
                                          │                  └────────────────────────┘
                              ┌───────────┴───────────┐
                              │  LLM Providers         │
                              │  OpenRouter (fast/cheap│
                              │  generation)           │
                              │  Claude API (grading,  │
                              │  adjudication)         │
                              └───────────────────────┘
```

Core loop: **Upload → Chunk & Embed → Scheduler picks weakest due concept → Retrieval tool pulls passages → Question-Generation skill → Student answers → Grading skill (vs. source) → Memory updates mastery → Scheduler reschedules.**

---

## 1.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What frontend framework is used in the application's architecture?", "choices": ["React (Next.js)", "Flutter", "Angular", "Vue.js"], "answer_key": "React (Next.js)", "concept_tag": "Frontend Framework"}
```

## [generation] 2026-08-17T10:09:37.521859+00:00

**Prompt:**
```
[nvidia/nemotron-nano-9b-v2:free] You are a question-generation engine for a study app. Generate a question ONLY from the passage below. Do not introduce facts not present in the passage. Respond with ONLY a single JSON object and nothing else — no explanation, no markdown code fences, no text before or after the JSON. Your entire response must start with { and end with }.

Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", "choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. For short_answer, choices must be null and answer_key is the ideal answer.

Example valid response: {"type": "mcq", "prompt": "What gas do plants release during photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], "answer_key": "Oxygen", "concept_tag": "Photosynthesis"}

Passage (chunk_id=41d79f3b-27fb-4557-9920-b1a5dcf8e0ff):
consistent sleep schedules by going to bed and waking up at regular times to maintain a healthy circadian rhythm. Reducing screen time before bedtime and avoiding stimulants like caffeine at night can improve sleep quality. Educational institutions should raise awareness about the importance of sleep through workshops and counseling sessions. Time management
strategies should be encouraged so students can complete academic tasks during the day instead of
staying up late. Additionally, creating a quiet and comfortable sleep environment can further
support better rest and overall well-being. CONCLUSION:
Late-night alertness negatively affects students’ cognitive abilities, learning efficiency, and health. Proper sleep is essential for academic success and well-being. By adopting healthy sleep habits and
reducing late-night activities, students can improve both their academic performance and overall
quality of life. REFERENCE:
Walker, M. (2017). Why we sleep: Unlocking the power of sleep and dreams. Scribner. Pilcher, J. J., & Huffcutt, A. I. (1996). Effects of sleep deprivation on performance: A meta-
analysis. Sleep, 19(4), 318–326. Lim, J., & Dinges, D. F. (2010). A meta-analysis of the impact of short-term sleep deprivation on
cognitive variables. Psychological Bulletin, 136(3), 375–389. Curcio, G., Ferrara, M., & De Gennaro, L. (2006). Sleep loss, learning capacity, and academic
performance. Sleep Medicine Reviews, 10(5), 323–337. Hershner, S. D., & Chervin, R. D. (2014). Causes and consequences of sleepiness among college
students. Nature and Science of Sleep, 6, 73–84. Taheri, S., Lin, L., Austin, D., Young, T., & Mignot, E. (2004). Short sleep duration is associated
with reduced leptin and increased ghrelin levels. PLoS Medicine, 1(3), e62. Baglioni, C., Battagliese, G., Feige, B., Spiegelhalder, K., Nissen, C., Voderholzer, U., &
Riemann, D. (2016). Insomnia as a predictor of depression. Journal of Affective Disorders,
135(1–3), 10–19. Cain, N., & Gradisar, M. (2010). Electronic media use and sleep in school-aged children and
adolescents. Sleep Medicine, 11(8), 735–742. Lemola, S., Perkinson-Gloor, N., Brand, S., Dewald-Kaufmann, J., & Grob, A. (2015). Adolescents’ electronic media use at night and sleep disturbance. Journal of Youth and
Adolescence, 44(2), 405–418. Roenneberg, T., Allebrandt, K. V., Merrow, M., & Vetter, C. (2012). Social jetlag and obesity. Current Biology, 22(10), 939–943.

Generate one question from this passage.
```

**Response:**
```
{"type": "mcq", "prompt": "What is recommended to maintain a healthy circadian rhythm according to the passage?", "choices": ["Consistent sleep schedules", "Reducing screen time", "Avoiding stimulants like caffeine", "Time management strategies"], "answer_key": "Consistent sleep schedules", "concept_tag": "Circadian rhythm" }
```
