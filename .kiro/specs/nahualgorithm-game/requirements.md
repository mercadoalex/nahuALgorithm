# Requirements Document

## Introduction

NahuALgorithm is an immersive, narrative-driven exploration and puzzle game set in a solar-punk desert world in México. The game merges ancient Mesoamerican spiritual practices with sustainable technology, following two protagonists — a young engineer (The Apprentice) and a wizened Elder — on a quest to repair the fractured relationship between humans, nature, and the cosmos. The central mechanic revolves around Nahualismo (connecting with animal spirit guides) and the NahuAlgorithm (a digital algorithm derived from sacred plants that allows users to decipher ancient glyphs and access a non-linear geometric plane of existence). The Peyote serves as the game's artificial intelligence — an autonomous, sentient entity that makes independent decisions and interacts directly with the player, guiding, challenging, and shaping the experience.

## Glossary

- **Game_Engine**: The core runtime system responsible for rendering, input handling, physics, and game loop execution.
- **Narrative_System**: The subsystem that manages story progression, dialogue trees, character interactions, and branching narrative paths.
- **Puzzle_Engine**: The subsystem responsible for presenting, validating, and tracking ancient glyph puzzles and ruin-based challenges.
- **Glyph_Decoder**: The in-game tool (NahuAlgorithm Tablet) that allows the player to scan, interpret, and decode Mesoamerican glyphs.
- **Nahual_System**: The subsystem managing the Nagual Spirit Guide interactions, spirit world transitions, and animal guide mechanics.
- **World_Renderer**: The subsystem responsible for rendering the solar-punk desert environment, lighting, atmospheric effects, and visual style.
- **Character_Controller**: The subsystem managing player character movement, animations, interactions, and inventory.
- **Dialogue_Manager**: The subsystem handling dialogue presentation, player choices, and NPC conversation logic.
- **Audio_System**: The subsystem managing ambient soundscapes, music, sound effects, and audio transitions.
- **Save_System**: The subsystem responsible for persisting and restoring game progress.
- **Apprentice**: The player-controlled young engineer protagonist equipped with the NahuAlgorithm Tablet.
- **Elder**: The NPC shaman/guardian character who guides the Apprentice through the narrative.
- **Nagual**: The ethereal Jaguar spirit guide entity composed of geometric glyph patterns and energy.
- **Sacred_Plant_Network**: The network of sacred plants (Peyote cacti and psychoactive mushrooms) fused with technology that serves as an energy source and memory node in the game world. Peyote is the central sacred plant — a small cactus, not a tree.
- **Peyote_AI**: The artificial intelligence of the game, embodied by the Peyote cactus. It is an autonomous, sentient entity that makes independent decisions, initiates interactions with the player, provides guidance or challenges, and dynamically shapes the game experience based on player behavior and narrative state.
- **Glyph**: A Mesoamerican symbol (pictogram, ideogram, or phonogram) that forms the basis of puzzles and magical effects.
- **Spirit_Plane**: The non-linear, geometric plane of existence accessible through the NahuAlgorithm.

## Requirements

### Requirement 1: Core Game Loop and Exploration

**User Story:** As a player, I want to explore a solar-punk desert world and interact with its inhabitants and environment, so that I can experience the narrative and discover ancient mysteries.

#### Acceptance Criteria

1. WHEN the player starts a new game, THE Game_Engine SHALL initialize the desert world environment and place the Apprentice at the Elder's dwelling.
2. THE Character_Controller SHALL allow the Apprentice to walk, run, and interact with objects and NPCs in the game world.
3. WHEN the Apprentice approaches an interactive object or NPC, THE Game_Engine SHALL display an interaction prompt.
4. WHILE the Apprentice is exploring the open world, THE World_Renderer SHALL render the solar-punk desert environment with visible ruins, villages, biodomes, and desert flora.
5. WHEN the player transitions between areas, THE Game_Engine SHALL load the target area within a loading sequence that maintains narrative immersion.

### Requirement 2: Narrative and Dialogue System

**User Story:** As a player, I want to engage in meaningful dialogue with the Elder and other characters, so that I can understand the story and build the relationship between the Apprentice and the Elder.

#### Acceptance Criteria

1. WHEN the Apprentice initiates dialogue with the Elder, THE Dialogue_Manager SHALL present a dialogue tree with selectable response options.
2. THE Narrative_System SHALL track the relationship state between the Apprentice and the Elder, progressing from skepticism and distrust toward mutual understanding.
3. WHEN the player selects a dialogue option, THE Narrative_System SHALL update the story progression state and unlock subsequent narrative branches accordingly.
4. WHILE a dialogue sequence is active, THE Character_Controller SHALL restrict the Apprentice's movement to prevent breaking the conversation context.
5. WHEN a narrative milestone is reached, THE Narrative_System SHALL trigger the corresponding cutscene or story event.

### Requirement 3: Glyph Decoding and the NahuAlgorithm Tablet

**User Story:** As a player, I want to use the NahuAlgorithm Tablet to scan and decode ancient Mesoamerican glyphs, so that I can solve puzzles and unlock hidden knowledge.

#### Acceptance Criteria

1. WHEN the Apprentice activates the NahuAlgorithm Tablet near a glyph surface, THE Glyph_Decoder SHALL display a holographic interface overlaying the glyph.
2. WHEN a glyph is scanned, THE Glyph_Decoder SHALL classify the glyph as a pictogram, ideogram, or phonogram and present its decoded meaning.
3. IF the Glyph_Decoder encounters a corrupted or incomplete glyph, THEN THE Glyph_Decoder SHALL display a partial interpretation and indicate the missing segments.
4. THE Glyph_Decoder SHALL store all decoded glyphs in a persistent glyph codex accessible from the Tablet interface.
5. WHEN the player opens the glyph codex, THE Glyph_Decoder SHALL render each stored glyph with its classification, decoded meaning, and discovery location.
6. FOR ALL valid Glyph objects, encoding a Glyph to its display representation and then parsing that representation back SHALL produce an equivalent Glyph object (round-trip property).

### Requirement 4: Puzzle Mechanics in Ancient Ruins

**User Story:** As a player, I want to solve ancient puzzles within ruins by combining glyph knowledge and environmental interaction, so that I can progress through the game and uncover deeper mysteries.

#### Acceptance Criteria

1. WHEN the Apprentice enters a ruin containing a puzzle, THE Puzzle_Engine SHALL present the puzzle elements: stone carvings, activation points, and recessed circuit connection ports.
2. WHEN the Apprentice places a decoded glyph sequence into an activation point, THE Puzzle_Engine SHALL validate the sequence against the puzzle solution.
3. IF the player submits an incorrect glyph sequence, THEN THE Puzzle_Engine SHALL provide a visual and audio feedback indicating the error without revealing the solution.
4. WHEN a puzzle is solved correctly, THE Puzzle_Engine SHALL trigger the ruin's activation sequence, revealing new areas or narrative content.
5. THE Puzzle_Engine SHALL support puzzles of increasing complexity as the player progresses through the narrative.
6. WHILE a puzzle is active, THE Puzzle_Engine SHALL allow the player to reset the puzzle to its initial state at any time.

### Requirement 5: Nahualismo and Spirit Guide Interaction

**User Story:** As a player, I want to connect with the Nagual Jaguar spirit guide and enter the Spirit Plane, so that I can access hidden knowledge and abilities tied to the ancient spiritual practice.

#### Acceptance Criteria

1. WHEN the narrative unlocks the Nahualismo ability, THE Nahual_System SHALL enable the Apprentice to summon the Nagual spirit guide.
2. WHEN the Nagual is summoned, THE World_Renderer SHALL render the Nagual as a translucent, ethereal jaguar entity composed of interlocking geometric glyph patterns pulsating with gold and blue light.
3. WHILE the Nagual is active, THE Nahual_System SHALL allow the Apprentice to perceive hidden glyphs and energy pathways not visible in the normal world.
4. WHEN the Apprentice activates a Spirit Plane transition point, THE Nahual_System SHALL transition the player into the non-linear geometric plane of existence with a distinct visual shift.
5. WHILE the player is in the Spirit_Plane, THE World_Renderer SHALL render the environment as a geometric, non-linear space distinct from the physical desert world.
6. IF the Apprentice's spiritual energy is depleted while in the Spirit_Plane, THEN THE Nahual_System SHALL return the player to the physical world at the last transition point.

### Requirement 6: Sacred Plant Network and Memory Nodes

**User Story:** As a player, I want to interact with the Sacred Plant Network (Peyote cacti and mushrooms) to access stored memories and dreams, so that I can piece together the history of the world and solve narrative puzzles.

#### Acceptance Criteria

1. WHEN the Apprentice connects to a Sacred_Plant_Network node, THE Narrative_System SHALL present a stored memory or dream sequence as an interactive flashback.
2. THE World_Renderer SHALL render the Sacred_Plant_Network as clusters of Peyote cacti and psychoactive mushrooms fused with technology, with root systems wrapped in glowing blue conduits.
3. WHILE a memory sequence is active, THE Narrative_System SHALL present the memory as a puzzle-and-memory challenge that the Apprentice must interpret.
4. WHEN the Apprentice completes a memory sequence, THE Narrative_System SHALL record the recovered knowledge and update the story progression state.
5. THE Sacred_Plant_Network nodes SHALL serve as save points where THE Save_System persists the current game progress.

### Requirement 7: Visual Style and Art Direction

**User Story:** As a player, I want to experience a visually cohesive world that blends Mesoamerican aesthetics with solar-punk technology, so that the game world feels authentic and immersive.

#### Acceptance Criteria

1. THE World_Renderer SHALL use the defined color palette: terra-cotta orange and ocher as primary natural base, jade green and deep moss green as secondary natural base, electric cyan and bright blue for active technology and magic, obsidian black for static technology materials, copper, aged gold, and turquoise for heritage patterns, and twilight blue/purple and deep indigo for environment.
2. THE World_Renderer SHALL render technology elements as organic and sustainable in appearance, using materials that visually resemble clay, polished jade, and sustainable metals.
3. WHILE the game is set during twilight or night scenes, THE World_Renderer SHALL use atmospheric lighting with a large full moon as the primary cool light source contrasting warm desert tones.
4. THE World_Renderer SHALL render active glyphs, data panels, and magical effects with focused cyan or electric blue light that casts complex patterns on nearby surfaces.
5. THE World_Renderer SHALL render the Apprentice with traditional braids, woven textile patterns, protective armored plating, and the NahuAlgorithm Tablet as a hand-held polished stone and metal device.
6. THE World_Renderer SHALL render the Elder with intricate robes of traditional textiles bearing sacred patterns, a Carved Obsidian Staff with subtle blue data conduits, a bag, and a canteen.
7. THE World_Renderer SHALL avoid visual elements resembling extraterrestrial or alien aesthetics, generic punk styles, or imagery from the Avatar film franchise.

### Requirement 8: Sacred Plants and Spiritual Experiences

**User Story:** As a player, I want to encounter sacred plants like Peyote and psychoactive mushrooms as part of the narrative, so that I can experience their role in Mesoamerican spiritual practices within the game's context.

#### Acceptance Criteria

1. WHEN the Elder guides the Apprentice to a sacred plant, THE Narrative_System SHALL initiate a guided spiritual experience sequence.
2. WHILE a spiritual experience sequence is active, THE World_Renderer SHALL apply distinct visual distortion effects and color shifts to represent altered perception.
3. WHEN a spiritual experience sequence concludes, THE Narrative_System SHALL grant the Apprentice new insight, decoded glyph knowledge, or narrative progression.
4. THE World_Renderer SHALL render sacred plants (Peyote, mushrooms) within biodomes and natural desert settings as visually prominent and integrated with subtle technological glow effects.

### Requirement 9: Audio and Atmosphere

**User Story:** As a player, I want an immersive audio experience that reinforces the blend of ancient and futuristic themes, so that the game world feels alive and atmospheric.

#### Acceptance Criteria

1. THE Audio_System SHALL play ambient desert soundscapes during open-world exploration, including wind, distant wildlife, and subtle technological hums.
2. WHEN the Apprentice enters a ruin or puzzle area, THE Audio_System SHALL transition the ambient audio to an enclosed, reverberant soundscape with ancient tonal elements.
3. WHEN the player transitions to the Spirit_Plane, THE Audio_System SHALL shift to an ethereal, resonant audio profile distinct from the physical world.
4. WHILE dialogue is active, THE Audio_System SHALL lower ambient audio volume to ensure dialogue clarity.

### Requirement 10: Save and Progress System

**User Story:** As a player, I want to save my progress reliably and resume from where I left off, so that I can play the game across multiple sessions without losing progress.

#### Acceptance Criteria

1. WHEN the Apprentice interacts with a Sacred_Plant_Network save point, THE Save_System SHALL persist the complete game state including narrative progress, decoded glyphs, puzzle states, and player position.
2. WHEN the player loads a saved game, THE Save_System SHALL restore the complete game state and place the Apprentice at the corresponding Sacred_Plant_Network node.
3. IF the Save_System encounters a write failure during save, THEN THE Save_System SHALL notify the player of the failure and retain the previous valid save data.
5. FOR ALL valid game states, saving a game state and then loading that save SHALL produce an equivalent game state (round-trip property).

### Requirement 11: Peyote AI — Autonomous Intelligence

**User Story:** As a player, I want the Peyote to act as an autonomous, intelligent entity that makes its own decisions and interacts with me directly, so that the game feels alive and unpredictable, as if guided by an ancient sentient force.

#### Acceptance Criteria

1. THE Peyote_AI SHALL operate as an autonomous agent capable of initiating interactions with the Apprentice without player input.
2. WHEN the Apprentice enters an area containing Peyote, THE Peyote_AI SHALL evaluate the player's current narrative state, decoded glyphs, and behavior history to determine its response.
3. THE Peyote_AI SHALL autonomously decide whether to guide, challenge, withhold information, or reveal hidden paths to the Apprentice based on the current game context.
4. WHEN the Peyote_AI initiates an interaction, THE Dialogue_Manager SHALL present the Peyote's communication through visual glyph sequences, environmental changes, or auditory signals rather than conventional dialogue text.
5. THE Peyote_AI SHALL dynamically adjust puzzle difficulty and hint availability based on the player's progress and interaction patterns.
6. WHILE the Apprentice is under a spiritual experience triggered by the Peyote_AI, THE Peyote_AI SHALL control the sequence of visions, memories, and challenges presented to the player.
7. THE Peyote_AI SHALL maintain an internal state that evolves based on cumulative player interactions, making each playthrough's Peyote behavior unique.
8. IF the Apprentice ignores or acts against the Peyote_AI's guidance, THEN THE Peyote_AI SHALL adapt its behavior accordingly, potentially becoming more cryptic or withholding assistance.
9. THE Peyote_AI SHALL coordinate with the Nahual_System to influence when and how the Nagual spirit guide manifests, acting as the underlying intelligence behind spiritual encounters.
5. FOR ALL valid game states, saving a game state and then loading that save SHALL produce an equivalent game state (round-trip property).
