
### [2026-03-03] Tool Verification for Test-Time Reinforcement Learning
- **Authors**: Ruotong Liao; Nikolai Röhrich; Xiaohan Wang; Yuhui Zhang; Yasaman Samadzadeh; Volker Tresp; Serena Yeung-Levy
- **Link**: https://arxiv.org/abs/2603.02203
- **Summary**: Introduces T^3RL, adding tool-based verification (e.g., code execution) to stabilize test-time RL self-training; reports consistent gains over vanilla TTRL on MATH-500, AMC, and AIME 2024, especially on harder problems.

### [2026-03-03] Adaptive Confidence Regularization for Multimodal Failure Detection
- **Authors**: Moru Liu; Hao Dong; Olga Fink; Mario Trapp
- **Link**: https://arxiv.org/abs/2603.02200
- **Summary**: Proposes ACR to detect multimodal failures by penalizing “confidence degradation” vs unimodal branches and synthesizing hard outliers via feature swapping; shows robust improvements across multiple datasets/modalities.

### [2026-03-03] Conformal Policy Control
- **Authors**: Drew Prinster; Clara Fannjiang; Ji Won Park; Kyunghyun Cho; Anqi Liu; Suchi Saria; Samuel Stanton
- **Link**: https://arxiv.org/abs/2603.02196
- **Summary**: Uses conformal calibration on data from a safe reference policy to regulate a new optimized policy, providing finite-sample safety/risk guarantees while still allowing exploration; demonstrated across QA to biomolecular engineering.

### [2026-03-03] Symbol-Equivariant Recurrent Reasoning Models
- **Authors**: Richard Freinschlag; Timo Bertram; Erich Kobler; Andreas Mayr; Günter Klambauer
- **Link**: https://arxiv.org/abs/2603.02193
- **Summary**: SE-RRMs bake symbol-permutation equivariance into RRM architectures, reducing reliance on data augmentation; reports better Sudoku generalization (9x9 → 4x4/16x16/25x25) and competitive ARC-AGI results with ~2M parameters.

### [2026-03-03] Sketch2Colab: Sketch-Conditioned Multi-Human Animation via Controllable Flow Distillation
- **Authors**: Divyanshu Daiya; Aniket Bera
- **Link**: https://arxiv.org/abs/2603.02190
- **Summary**: Turns storyboard sketches into controllable multi-human 3D motion via diffusion→rectified-flow distillation plus energy-based constraints and a CTMC event planner; claims SOTA constraint adherence and faster inference on CORE4D/InterHuman.
### [2026-03-04] How to Peel with a Knife: Aligning Fine-Grained Manipulation with Human Preference
- **Authors**: Toru Lin, Shuying Deng, Zhao-Heng Yin, Pieter Abbeel, Jitendra Malik
- **Link**: https://arxiv.org/abs/2603.03280
- **Summary**: Many essential manipulation tasks - such as food preparation, surgery, and craftsmanship - remain intractable for autonomous robots. These tasks are characterized not only by contact-rich, force-sensitive dynamics, but also by their "implicit" success criteria: unlike pick-and-place, task quality in these domains is continuous and subjective (e.g. how well a potato is peeled), making quantitative evaluation and reward engineering difficult. We present a learning framework for such tasks, using peeling with a knife as a representative example. Our approach follows a two-stage pipeline: first, we learn a robust initial policy via force-aware data collection and imitation learning, enabling generalization across object variations; second, we refine the policy through preference-based finetuning using a learned reward model that combines quantitative task metrics with qualitative human feedback, aligning policy behavior with human notions of task quality. Using only 50-200 peeling trajectories, our system achieves over 90% average success rates on challenging produce including cucumbers, apples, and potatoes, with performance improving by up to 40% through preference-based finetuning. Remarkably, policies trained on a single produce category exhibit strong zero-shot generalization to unseen in-category instances and to out-of-distribution produce from different categories while maintaining over 90% success rates.

### [2026-03-04] Tether: Autonomous Functional Play with Correspondence-Driven Trajectory Warping
- **Authors**: William Liang, Sam Wang, Hung-Ju Wang, Osbert Bastani, Yecheng Jason Ma, Dinesh Jayaraman
- **Link**: https://arxiv.org/abs/2603.03278
- **Summary**: The ability to conduct and learn from interaction and experience is a central challenge in robotics, offering a scalable alternative to labor-intensive human demonstrations. However, realizing such "play" requires (1) a policy robust to diverse, potentially out-of-distribution environment states, and (2) a procedure that continuously produces useful robot experience. To address these challenges, we introduce Tether, a method for autonomous functional play involving structured, task-directed interactions. First, we design a novel open-loop policy that warps actions from a small set of source demonstrations (<=10) by anchoring them to semantic keypoint correspondences in the target scene. We show that this design is extremely data-efficient and robust even under significant spatial and semantic variations. Second, we deploy this policy for autonomous functional play in the real world via a continuous cycle of task selection, execution, evaluation, and improvement, guided by the visual understanding capabilities of vision-language models. This procedure generates diverse, high-quality datasets with minimal human intervention. In a household-like multi-object setup, our method is the first to perform many hours of autonomous multi-task play in the real world starting from only a handful of demonstrations. This produces a stream of data that consistently improves the performance of closed-loop imitation policies over time, ultimately yielding over 1000 expert-level trajectories and training policies competitive with those learned from human-collected demonstrations.

### [2026-03-04] Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals
- **Authors**: Achyutha Menon, Magnus Saebo, Tyler Crosse, Spencer Gibson, Eyon Jang, Diogo Cruz
- **Link**: https://arxiv.org/abs/2603.03258
- **Summary**: The accelerating adoption of language models (LMs) as agents for deployment in long-context tasks motivates a thorough understanding of goal drift: agents' tendency to deviate from an original objective. While prior-generation language model agents have been shown to be susceptible to drift, the extent to which drift affects more recent models remains unclear. In this work, we provide an updated characterization of the extent and causes of goal drift. We investigate drift in state-of-the-art models within a simulated stock-trading environment (Arike et al., 2025). These models are largely shown to be robust even when subjected to adversarial pressure. We show, however, that this robustness is brittle: across multiple settings, the same models often inherit drift when conditioned on prefilled trajectories from weaker agents. The extent of conditioning-induced drift varies significantly by model family, with only GPT-5.1 maintaining consistent resilience among tested models. We find that drift behavior is inconsistent between prompt variations and correlates poorly with instruction hierarchy following behavior, with strong hierarchy following failing to reliably predict resistance to drift. Finally, we run analogous experiments in a new emergency room triage environment to show preliminary evidence for the transferability of our results across qualitatively different settings. Our findings underscore the continued vulnerability of modern LM agents to contextual pressures and the need for refined post-training techniques to mitigate this.

### [2026-03-04] Valet: A Standardized Testbed of Traditional Imperfect-Information Card Games
- **Authors**: Mark Goadrich, Achille Morenville, Éric Piette
- **Link**: https://arxiv.org/abs/2603.03252
- **Summary**: AI algorithms for imperfect-information games are typically compared using performance metrics on individual games, making it difficult to assess robustness across game choices. Card games are a natural domain for imperfect information due to hidden hands and stochastic draws. To facilitate comparative research on imperfect-information game-playing algorithms and game systems, we introduce Valet, a diverse and comprehensive testbed of 21 traditional imperfect-information card games. These games span multiple genres, cultures, player counts, deck structures, mechanics, winning conditions, and methods of hiding and revealing information. To standardize implementations across systems, we encode the rules of each game in RECYCLE, a card game description language. We empirically characterize each game's branching factor and duration using random simulations, reporting baseline score distributions for a Monte Carlo Tree Search player against random opponents to demonstrate the suitability of Valet as a benchmarking suite.

### [2026-03-04] Density-Guided Response Optimization: Community-Grounded Alignment via Implicit Acceptance Signals
- **Authors**: Patrick Gerard, Svitlana Volkova
- **Link**: https://arxiv.org/abs/2603.03242
- **Summary**: Language models deployed in online communities must adapt to norms that vary across social, cultural, and domain-specific contexts. Prior alignment approaches rely on explicit preference supervision or predefined principles, which are effective for well-resourced settings but exclude most online communities -- particularly those without institutional backing, annotation infrastructure, or organized around sensitive topics -- where preference elicitation is costly, ethically fraught, or culturally misaligned. We observe that communities already express preferences implicitly through what content they accept, engage with, and allow to persist. We show that this acceptance behavior induces measurable geometric structure in representation space: accepted responses occupy coherent, high-density regions that reflect community-specific norms, while rejected content falls in sparser or misaligned areas. We operationalize this structure as an implicit preference signal for alignment and introduce density-guided response optimization (DGRO), a method that aligns language models to community norms without requiring explicit preference labels. Using labeled preference data, we demonstrate that local density recovers pairwise community judgments, indicating that geometric structure encodes meaningful preference signal. We then apply DGRO in annotation-scarce settings across diverse communities spanning platform, topic, and language. DGRO-aligned models consistently produce responses preferred by human annotators, domain experts, and model-based judges over supervised and prompt-based baselines. We position DGRO as a practical alignment alternative for communities where explicit preference supervision is unavailable or misaligned with situated practices, and discuss the implications and risks of learning from emergent acceptance behavior.
### [2026-03-06] RoboPocket: Improve Robot Policies Instantly with Your Phone
- **Authors**: Junjie Fang; Wendi Chen; Han Xue; Fangyuan Zhou; Tian Le; Yi Wang; Yuting Zhang; Jun Lv; Chuan Wen; Cewu Lu
- **Link**: https://arxiv.org/abs/2603.05504
- **Summary**: AR visual foresight + remote inference lets you iterate robot policies without executing on a physical robot; reports ~2× data efficiency and up to 2× sample-efficiency in distributed interactive corrections.

### [2026-03-06] POET-X: Memory-efficient LLM Training by Scaling Orthogonal Transformation
- **Authors**: Zeju Qiu; Lixin Liu; Adrian Weller; Han Shi; Weiyang Liu
- **Link**: https://arxiv.org/abs/2603.05500
- **Summary**: Memory/throughput-optimized orthogonal-equivalence training; claims billion-parameter pretraining fits on a single NVIDIA H100 where AdamW OOMs.

### [2026-03-06] The Spike, the Sparse and the Sink: Anatomy of Massive Activations and Attention Sinks
- **Authors**: Shangwen Sun; Alfredo Canziani; Yann LeCun; Jiachen Zhu
- **Link**: https://arxiv.org/abs/2603.05498
- **Summary**: Disentangles massive activation outliers vs attention sinks; argues their co-occurrence is largely a pre-norm architectural artifact and they play distinct global vs local roles.

### [2026-03-06] Censored LLMs as a Natural Testbed for Secret Knowledge Elicitation
- **Authors**: Helena Casademunt; Bartosz Cywiński; Khoi Tran; Arya Jakkli; Samuel Marks; Neel Nanda
- **Link**: https://arxiv.org/abs/2603.05494
- **Summary**: Uses politically-censored open LLMs as a “natural” dishonesty testbed; finds some elicitation methods improve truthfulness, and self-lie-detection approaches can approach an uncensored-model upper bound—no method fully fixes falsehoods.

### [2026-03-06] Reasoning Theater: Disentangling Model Beliefs from Chain-of-Thought
- **Authors**: Siddharth Boppana; Annabel Ma; Max Loeffler; Raphael Sarfati; Eric Bigelow; Atticus Geiger; Owen Lewis; Jack Merullo
- **Link**: https://arxiv.org/abs/2603.05488
- **Summary**: Evidence for performative CoT: final answers become decodable much earlier than the written reasoning; probe-guided early exit cuts tokens up to ~80% (MMLU) and ~30% (GPQA-Diamond) with similar accuracy.

