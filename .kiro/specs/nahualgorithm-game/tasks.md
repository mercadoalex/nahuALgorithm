# Implementation Plan: NahuALgorithm Game

## Overview

Incremental implementation of NahuALgorithm — a narrative-driven exploration and puzzle game built with Godot 4 + GDScript, a Python/FastAPI AI backend, and a hybrid Peyote AI architecture. Tasks are ordered to build foundational systems first (Event Bus, data models, save system), then layer on gameplay systems (narrative, glyphs, puzzles, Nahual), and finally integrate the Peyote AI and presentation layers. GDScript is the primary language for all game systems; Python is used for the generative AI microservice. Testing uses GdUnit4 (GDScript) and pytest + Hypothesis (Python).

## Tasks

- [-] 1. Set up project structure, Event Bus, and core data models
  - [x] 1.1 Create Godot 4 project structure and directory layout
    - Create project directories: `scripts/core/`, `scripts/systems/`, `scripts/ai/`, `scripts/ui/`, `scenes/`, `resources/`, `tests/unit/`, `tests/property/`
    - Create Python backend directory: `ai_backend/` with FastAPI project skeleton (`main.py`, `routes/`, `models/`, `tests/`)
    - Set up `project.godot` with initial configuration
    - _Requirements: 1.1_

  - [~] 1.2 Implement Event Bus (autoload singleton)
    - Create `scripts/core/event_bus.gd` as an AutoLoad singleton
    - Implement `publish(event: Dictionary)`, `subscribe(event_type: String, handler: Callable)`, `unsubscribe(subscription)` methods
    - Define `GameEvent` structure: `{ type: String, timestamp: float, payload: Dictionary }`
    - Register as AutoLoad in `project.godot`
    - _Requirements: 1.1 (foundation for all inter-system communication)_

  - [~] 1.3 Define core data models and enums in GDScript
    - Create `scripts/core/models/glyph.gd` — Glyph resource with `id`, `classification`, `symbol`, `meaning`, `phonetic`, `is_complete`, `missing_segments`
    - Create `scripts/core/models/game_state.gd` — GameState resource with all fields from design (player_position, current_area, narrative_state, glyph_codex, puzzle_states, nahual_state, peyote_ai_state, etc.)
    - Create `scripts/core/models/player_context.gd` — PlayerContext, PlayerAction, InteractionPattern
    - Create `scripts/core/models/area_data.gd` — AreaData, AreaConnection, Interactable
    - Create `scripts/core/enums.gd` — GlyphClassification, MovementSpeed, PeyoteDecisionType, AudioProfile enums
    - _Requirements: 3.2, 3.6, 10.1, 11.2_

  - [ ]* 1.4 Write unit tests for Event Bus
    - Test publish/subscribe/unsubscribe lifecycle using GdUnit4
    - Test multiple subscribers receive the same event
    - Test unsubscribed handlers are not called
    - _Requirements: 1.1_

- [ ] 2. Implement Glyph Decoder and Codex system
  - [ ] 2.1 Implement Glyph encoding and parsing (round-trip codec)
    - Create `scripts/systems/glyph_decoder.gd`
    - Implement `encode_glyph(glyph: Glyph) -> String` using deterministic format: `{classification}:{id}:{symbol}:{meaning}:{phonetic|_}:{is_complete}:{missing_segments}`
    - Implement `parse_glyph(encoded: String) -> Glyph` as the inverse
    - Handle edge cases: special characters in symbol/meaning, empty phonetic, empty missing_segments
    - _Requirements: 3.6_

  - [ ]* 2.2 Write property test: Glyph encoding round trip
    - **Property 9: Glyph encoding round trip**
    - Generate random valid Glyph objects (all three classifications, varying completeness)
    - Assert `parse_glyph(encode_glyph(glyph))` produces equivalent Glyph
    - Use GdUnit4 with manual fuzzing or Hypothesis via Python bridge
    - **Validates: Requirements 3.6**

  - [ ] 2.3 Implement glyph scanning, classification, and decoding
    - Implement `scan_glyph(surface_id: String) -> Dictionary` — returns raw glyph data from a surface
    - Implement `classify_glyph(raw_data: Dictionary) -> String` — returns exactly one of 'pictogram', 'ideogram', 'phonogram'
    - Implement `decode_glyph(raw_data: Dictionary) -> Glyph` — returns decoded Glyph with non-empty meaning
    - Handle corrupted/incomplete glyphs: return `is_complete = false` with populated `missing_segments`
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 2.4 Write property tests for glyph classification and incomplete detection
    - **Property 6: Glyph classification completeness** — for any valid scanned glyph, classification is exactly one of the three types and meaning is non-empty
    - **Property 7: Incomplete glyph detection** — for any glyph with `is_complete = false`, `missing_segments` is non-empty
    - **Validates: Requirements 3.2, 3.3**

  - [ ] 2.5 Implement Glyph Codex (persistent collection)
    - Create `scripts/systems/glyph_codex.gd`
    - Implement `add_to_codex(glyph: Glyph)`, `get_by_id(id: String) -> Glyph`, `get_by_classification(type: String) -> Array[Glyph]`, `get_all() -> Array[Glyph]`
    - Store glyphs with classification, decoded meaning, and discovery location
    - _Requirements: 3.4, 3.5_

  - [ ]* 2.6 Write property test: Codex storage and retrieval
    - **Property 8: Glyph codex storage and retrieval**
    - For any decoded glyph added to codex, retrieving by ID returns glyph with classification, meaning, and discovery location intact
    - **Validates: Requirements 3.4, 3.5**

- [ ] 3. Checkpoint — Core data models and glyph system
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement Save System with round-trip serialization
  - [ ] 4.1 Implement GameState serialization and deserialization
    - Create `scripts/systems/save_system.gd`
    - Implement `serialize_game_state(state: GameState) -> String` using JSON with custom handling for Vector3, Dictionary (Map), and nested resources
    - Implement `deserialize_game_state(json: String) -> GameState` as the inverse
    - Implement `save(slot_id: int, state: GameState) -> Dictionary` returning `{ success: bool, error: String }`
    - Implement `load(slot_id: int) -> GameState` returning null on failure/corruption
    - Implement `get_slot_info() -> Array[Dictionary]`, `delete_save(slot_id: int) -> bool`
    - Enforce `MAX_SAVE_SLOTS = 3`; reject slot IDs outside `[0, MAX_SAVE_SLOTS)`
    - Handle write failures: return `success = false` with error message, preserve previous save data
    - Handle corrupted saves: return null, mark slot as corrupted
    - _Requirements: 10.1, 10.2, 10.3, 10.5_

  - [ ]* 4.2 Write property test: Game state save/load round trip
    - **Property 22: Game state save/load round trip**
    - Generate random valid GameState objects (with Vector3, Maps, nested state)
    - Assert `load(slot, save(slot, state))` produces equivalent GameState
    - **Validates: Requirements 10.1, 10.2, 10.5, 11.10**

  - [ ]* 4.3 Write property test: Save failure preserves previous data
    - **Property 23: Save failure preserves previous data**
    - Simulate write failures; assert previous save data remains intact and loadable
    - Assert failure returns `success = false` with non-empty error
    - **Validates: Requirements 10.3**

  - [ ]* 4.4 Write property test: Sacred plant nodes are save points
    - **Property 18: Sacred plant nodes are save points**
    - For any plant node marked as save point, saving succeeds and persists complete game state
    - **Validates: Requirements 6.5**

- [ ] 5. Implement Narrative System and Dialogue Manager
  - [ ] 5.1 Implement Narrative System core
    - Create `scripts/systems/narrative_system.gd`
    - Implement `get_story_state() -> StoryState`, `update_story_progression(choice: Dictionary) -> StoryState`
    - Implement `get_relationship_state() -> Dictionary` with `apprentice_elder_trust` (float -1.0 to 1.0) and `narrative_phase` (skepticism → curiosity → acceptance → understanding)
    - Implement `trigger_milestone(milestone_id: String)`, `record_knowledge(knowledge: Dictionary)`
    - Implement `initiate_spiritual_experience(plant_id: String)`, `initiate_memory_sequence(node_id: String) -> MemorySequence`
    - Emit events via Event Bus on state changes
    - _Requirements: 2.2, 2.3, 2.5, 6.4, 8.1_

  - [ ]* 5.2 Write property tests for narrative and dialogue
    - **Property 3: Dialogue tree always has options** — initiating dialogue produces a tree with at least one option
    - **Property 4: Dialogue choices update story state** — selecting a valid option produces a different StoryState
    - **Property 5: Relationship progression is monotonic with positive choices** — positive choices yield non-decreasing trust and phase progression in order
    - **Validates: Requirements 2.1, 2.3, 2.5, 2.2**

  - [ ] 5.3 Implement Dialogue Manager with Dialogic 2 integration
    - Create `scripts/systems/dialogue_manager.gd`
    - Implement `start_dialogue(npc_id: String) -> DialogueTree`, `select_option(option_id: String) -> DialogueResult`
    - Implement `present_glyph_communication(glyph_sequence: Array[Glyph])` for Peyote AI non-verbal communication
    - Implement `present_environmental_signal(signal: Dictionary)` for environmental communication
    - Implement `is_dialogue_active() -> bool`, `end_dialogue()`
    - Integrate with Dialogic 2 plugin for dialogue tree authoring and timeline events
    - Emit `dialogue_started` and `dialogue_ended` events via Event Bus
    - _Requirements: 2.1, 2.4, 11.4_

  - [ ]* 5.4 Write property test: Movement lock during dialogue
    - **Property 2: Movement lock during dialogue**
    - For any game state with active dialogue, Character Controller reports movement locked; when no dialogue, movement is not locked by dialogue system
    - **Validates: Requirements 2.4**

  - [ ]* 5.5 Write property tests for Sacred Plant Network memory and spiritual experiences
    - **Property 16: Sacred Plant Network memory access** — connecting to a node with stored memory returns MemorySequence with non-null puzzle challenge
    - **Property 17: Memory completion updates knowledge** — completing a memory sequence records knowledge and updates story state
    - **Property 19: Spiritual experience yields reward** — completed spiritual experience grants at least one of: new insight, glyph knowledge, or narrative progression
    - **Validates: Requirements 6.1, 6.3, 6.4, 8.1, 8.3**

- [ ] 6. Implement Puzzle Engine
  - [ ] 6.1 Implement Puzzle Engine core
    - Create `scripts/systems/puzzle_engine.gd`
    - Implement `load_puzzle(puzzle_id: String) -> PuzzleState`, `submit_sequence(puzzle_id: String, sequence: Array[Glyph]) -> PuzzleResult`
    - Implement `reset_puzzle(puzzle_id: String) -> PuzzleState` — idempotent reset to initial state
    - Implement `get_puzzle_difficulty(puzzle_id: String) -> float`, `adjust_difficulty(puzzle_id: String, delta: float)`
    - Implement `get_hint_availability(puzzle_id: String) -> Dictionary`
    - Validation: correct=true iff sequence matches solution; incorrect feedback never reveals solution
    - Handle invalid sequences (wrong glyph IDs, wrong length) gracefully
    - Emit puzzle events via Event Bus
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ]* 6.2 Write property tests for puzzle validation and reset
    - **Property 10: Puzzle validation correctness** — correct=true iff sequence matches solution; incorrect feedback never contains solution
    - **Property 11: Puzzle difficulty monotonicity** — later-chapter puzzles have difficulty >= earlier-chapter puzzles
    - **Property 12: Puzzle reset idempotence** — reset after modifications returns to initial state; double-reset is idempotent
    - **Validates: Requirements 4.2, 4.3, 4.4, 4.5, 4.6**

- [ ] 7. Checkpoint — Narrative, dialogue, and puzzle systems
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement Nahual System and Spirit Plane
  - [ ] 8.1 Implement Nahual System core
    - Create `scripts/systems/nahual_system.gd`
    - Implement `is_unlocked() -> bool`, `summon_nagual()`, `dismiss_nagual()`, `is_nagual_active() -> bool`
    - Implement `get_hidden_glyphs(area: String) -> Array[Glyph]`, `get_energy_pathways(area: String) -> Array`
    - Implement `transition_to_spirit_plane(transition_point_id: String)`, `return_to_physical_world()`
    - Implement `get_spiritual_energy() -> float`, `deplete_energy(amount: float)`, `is_in_spirit_plane() -> bool`
    - Track `NahualState`: unlocked, nagual_active, in_spirit_plane, spiritual_energy (0.0–1.0), last_transition_point, discovered_pathways
    - Handle edge cases: energy clamped to 0.0, summoning while already active is idempotent, invalid transition points are no-ops
    - Auto-return to physical world when energy reaches 0
    - Emit spirit events via Event Bus
    - _Requirements: 5.1, 5.3, 5.4, 5.6_

  - [ ]* 8.2 Write property tests for Nahual System
    - **Property 13: Nagual reveals hidden elements** — glyphs/pathways visible with Nagual active is a superset of those visible when inactive
    - **Property 14: Spirit Plane transition state consistency** — after transition, `is_in_spirit_plane()` is true and transition point recorded; after return, false
    - **Property 15: Energy depletion forces return** — when energy reaches 0 in Spirit Plane, player returns to physical world at last transition point
    - **Validates: Requirements 5.3, 5.4, 5.6**

- [ ] 9. Implement Sacred Plant Network
  - [ ] 9.1 Implement Sacred Plant Network system
    - Create `scripts/systems/sacred_plant_network.gd`
    - Implement `connect_to_node(node_id: String) -> MemorySequence`, `get_available_nodes() -> Array[PlantNode]`
    - Implement `complete_memory_sequence(node_id: String, result: Dictionary)`, `is_save_point(node_id: String) -> bool`
    - Define PlantNode resource: id, position, type ('peyote' | 'mushroom'), has_memory, is_save_point
    - Define MemorySequence: id, fragments, puzzle_challenge, knowledge
    - Wire save point functionality to Save System
    - Emit memory and save events via Event Bus
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 10. Checkpoint — Nahual and Sacred Plant Network systems
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement Game Engine and Character Controller
  - [ ] 11.1 Implement Game Engine core loop
    - Create `scripts/core/game_engine.gd`
    - Implement `initialize(config: Dictionary)`, `_process(delta)` and `_physics_process(delta)` update loops
    - Implement `load_area(area_id: String)` with loading sequence that maintains narrative immersion
    - Implement `get_interactables_in_range(position: Vector3, radius: float) -> Array[Interactable]`
    - Implement `show_interaction_prompt(interactable)` and `hide_interaction_prompt()` — display prompt when player is within range, hide when outside
    - Wire area loading to Event Bus
    - _Requirements: 1.1, 1.3, 1.4, 1.5_

  - [ ] 11.2 Implement Character Controller
    - Create `scripts/systems/character_controller.gd` extending CharacterBody3D
    - Implement `move(direction: Vector2, speed: int)` with WALK and RUN speeds
    - Implement `interact(target)` — triggers interaction with nearest interactable
    - Implement `set_movement_locked(locked: bool)` — used by Dialogue Manager to lock movement during dialogue
    - Implement `get_position() -> Vector3`, `get_animation_state() -> String`
    - Subscribe to `dialogue_started`/`dialogue_ended` events to auto-lock/unlock movement
    - _Requirements: 1.2, 2.4_

  - [ ]* 11.3 Write property test: Interaction prompt proximity
    - **Property 1: Interaction prompt proximity**
    - For any interactable and any player position within range, prompt is displayed; outside range, no prompt
    - **Validates: Requirements 1.3**

- [ ] 12. Implement Peyote AI — GDScript local layer
  - [ ] 12.1 Implement Peyote AI core decision engine (GDScript)
    - Create `scripts/ai/peyote_ai.gd`
    - Implement `initialize(game_state: GameState)`, `on_game_event(event: Dictionary)`
    - Implement `evaluate_player_context(context: PlayerContext) -> PeyoteDecision` using behavior tree + weighted decision logic
    - Decision types: GUIDE, CHALLENGE, WITHHOLD, REVEAL_PATH, ADJUST_DIFFICULTY, INITIATE_VISION, BECOME_CRYPTIC
    - Communication methods: 'glyph_sequence', 'environmental_change', 'audio_signal' — never conventional text
    - Implement `tick(delta: float)` autonomous update cycle — subscribes to Event Bus, reacts asynchronously, never blocks game loop
    - Implement `get_internal_state() -> PeyoteInternalState`, `set_internal_state(state: PeyoteInternalState)`
    - Track: trust_level, crypticness, revealed_paths, interaction_history, current_disposition
    - Implement fallback content pools for offline mode (pre-authored visions, glyph interpretations)
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.7_

  - [ ] 12.2 Implement Peyote AI behavior adaptation logic
    - Implement defiance detection: when player ignores or acts against guidance, increase `crypticness` monotonically
    - Implement disposition transitions: sufficient defiance shifts disposition toward 'cryptic' or 'withholding'
    - Implement state evolution: distinct action sequences on same initial state produce different internal states
    - Implement difficulty adjustment: Peyote AI adjusts puzzle difficulty and hint availability via Puzzle Engine
    - Implement coordination with Nahual System: INITIATE_VISION and spirit-related decisions emit events consumable by Nahual System
    - _Requirements: 11.5, 11.7, 11.8, 11.9_

  - [ ]* 12.3 Write property tests for Peyote AI decisions
    - **Property 24: Peyote AI produces valid decisions for any context** — for any valid PlayerContext, decision type is a valid PeyoteDecisionType
    - **Property 25: Peyote AI communicates non-verbally** — communicationMethod is always one of the three non-verbal methods
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.4**

  - [ ]* 12.4 Write property tests for Peyote AI state evolution and adaptation
    - **Property 26: Peyote AI state evolves with interactions** — distinct action sequences produce different internal states
    - **Property 27: Defiance increases crypticness** — defiant actions yield non-decreasing crypticness; sufficient defiance shifts disposition
    - **Property 28: Peyote AI coordinates with Nahual System** — spiritual decisions produce events consumable by Nahual System
    - **Validates: Requirements 11.7, 11.8, 11.9**

- [ ] 13. Implement Peyote AI — Python/FastAPI generative backend
  - [ ] 13.1 Implement FastAPI generative AI service
    - Create `ai_backend/main.py` with FastAPI app
    - Create `ai_backend/routes/peyote.py` with `POST /peyote/generate-vision` endpoint
    - Input: PlayerContext + PeyoteInternalState (JSON)
    - Output: GenerativeContent with type ('vision_narrative', 'glyph_interpretation', 'emergent_communication'), content string, optional glyph_sequence and environmental_effects
    - Create `ai_backend/services/prompt_composer.py` — composes LLM prompts from player context
    - Create `ai_backend/services/llm_provider.py` — configurable LLM provider (AWS Bedrock, Anthropic Claude, OpenAI)
    - Implement timeout handling and graceful degradation
    - _Requirements: 11.1, 11.6_

  - [ ] 13.2 Implement GDScript HTTP client for AI backend
    - Create `scripts/ai/ai_client.gd` using Godot's HTTPRequest node
    - Implement `request_generative_content(context: PlayerContext, state: PeyoteInternalState) -> GenerativeContent`
    - Implement `is_online_mode() -> bool` — check if LLM service is reachable
    - Non-blocking: use signals/callbacks, never block game loop
    - Fallback: when service unavailable, return null so GDScript layer uses local content pools
    - _Requirements: 11.1 (hybrid architecture)_

  - [ ]* 13.3 Write Python property tests for generative AI service
    - Use pytest + Hypothesis to generate random PlayerContext and PeyoteInternalState inputs
    - Assert endpoint always returns valid GenerativeContent with correct type field
    - Assert service handles malformed input gracefully (returns 422 or default content)
    - _Requirements: 11.1, 11.2_

- [ ] 14. Checkpoint — Peyote AI (local + remote) complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Implement World Renderer and visual systems
  - [ ] 15.1 Implement World Renderer core
    - Create `scripts/systems/world_renderer.gd`
    - Implement `render_environment(area: AreaData, lighting: Dictionary)` — render solar-punk desert with ruins, villages, biodomes, desert flora
    - Implement `render_character(character_data: Dictionary)` — Apprentice and Elder with design-specified visual details
    - Implement `render_nagual(position: Vector3, active: bool)` — translucent ethereal jaguar with geometric glyph patterns, gold/blue light
    - Implement `render_sacred_plants(nodes: Array[PlantNode])` — Peyote cacti and mushrooms with technological glow
    - Implement `apply_spirit_plane_visuals()` / `remove_spirit_plane_visuals()` — geometric non-linear visual shift
    - Implement `apply_spiritual_distortion(intensity: float)` / `remove_spiritual_distortion()` — altered perception effects for spiritual experiences
    - Implement `render_glyph_effect(glyph: Glyph, position: Vector3)` — active glyph cyan/electric blue light effects
    - Implement `render_interaction_prompt(position: Vector3, label: String)`
    - Apply color palette: terra-cotta/ocher base, jade/moss green, electric cyan/blue for tech, obsidian black, copper/gold/turquoise heritage, twilight blue/purple environment
    - Avoid alien/extraterrestrial, generic punk, or Avatar-franchise aesthetics
    - _Requirements: 5.2, 5.5, 6.2, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 8.2, 8.4_

- [ ] 16. Implement Audio System
  - [ ] 16.1 Implement Audio System with adaptive profiles
    - Create `scripts/systems/audio_system.gd`
    - Implement `play_ambient(profile: String)` — profiles: 'desert_exploration', 'ruin_interior', 'spirit_plane', 'spiritual_experience'
    - Implement `transition_audio(from: String, to: String, duration: float)` — smooth crossfade between profiles
    - Implement `set_dialogue_mode(active: bool)` — lower ambient volume during dialogue
    - Implement `play_sound_effect(effect_id: String)`, `play_peyote_signal(signal: Dictionary)`
    - Subscribe to Event Bus: area transitions trigger profile changes, dialogue events trigger volume adjustment
    - Handle missing audio assets gracefully (log warning, continue silently)
    - Handle transition-during-transition (new replaces current smoothly)
    - Integrate with FMOD or Wwise plugin for adaptive audio
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

  - [ ]* 16.2 Write property tests for Audio System
    - **Property 20: Audio profile matches area type** — active profile corresponds to area type (desert→desert_exploration, ruin→ruin_interior, spirit→spirit_plane, spiritual→spiritual_experience)
    - **Property 21: Dialogue lowers ambient audio** — when dialogue active, ambient volume is lower than default
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**

- [ ] 17. Checkpoint — Presentation layer (renderer + audio)
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 18. Wire all systems together via Event Bus
  - [ ] 18.1 Integrate Peyote AI with game systems
    - Subscribe Peyote AI to all relevant Event Bus events (glyph_decoded, puzzle_solved, area_entered, dialogue_completed, spirit_event, memory_accessed)
    - Wire Peyote AI decisions to Puzzle Engine (difficulty adjustment), Nahual System (spirit manifestation), World Renderer (environmental changes), Audio System (audio signals), Dialogue Manager (glyph communication)
    - Implement Peyote AI spiritual experience control: when Peyote triggers a spiritual experience, it controls the sequence of visions/memories/challenges via Narrative System
    - Ensure Peyote AI never blocks the game loop — all reactions are asynchronous via Event Bus
    - _Requirements: 11.1, 11.5, 11.6, 11.9_

  - [ ] 18.2 Integrate Narrative System with all subsystems
    - Wire dialogue choices to Narrative System story progression
    - Wire milestone triggers to cutscene/story events
    - Wire Sacred Plant Network memory completion to knowledge recording
    - Wire spiritual experience completion to reward granting (insight, glyph knowledge, or narrative progression)
    - Wire Character Controller movement lock to dialogue active state
    - _Requirements: 2.3, 2.4, 2.5, 6.4, 8.1, 8.3_

  - [ ] 18.3 Integrate Save System with Sacred Plant Network
    - Wire Sacred Plant Network save points to Save System
    - On save: serialize complete GameState including all subsystem states (narrative, glyphs, puzzles, nahual, peyote AI, inventory, position)
    - On load: deserialize and restore all subsystem states, place Apprentice at corresponding plant node
    - _Requirements: 6.5, 10.1, 10.2_

  - [ ] 18.4 Integrate area transitions with renderer and audio
    - Wire Game Engine area loading to World Renderer environment rendering
    - Wire area transitions to Audio System profile changes
    - Wire Spirit Plane transitions to both visual and audio shifts
    - Wire spiritual experiences to distortion effects and audio profile
    - _Requirements: 1.4, 1.5, 5.4, 5.5, 9.1, 9.2, 9.3_

- [ ] 19. Implement Peyote AI spiritual experience sequences
  - [ ] 19.1 Implement spiritual experience flow
    - Create `scripts/systems/spiritual_experience.gd`
    - Implement guided spiritual experience sequence: Elder guides Apprentice to sacred plant → Peyote AI initiates sequence → visual distortion + audio shift → vision/memory/challenge sequence → reward granting
    - Peyote AI controls the sequence content (visions, memories, challenges) based on player context
    - Use generative content from Python backend when available; fall back to pre-authored content pools
    - On completion: grant at least one of new insight, decoded glyph knowledge, or narrative progression
    - Emit events for each phase of the experience
    - _Requirements: 8.1, 8.2, 8.3, 11.6_

- [ ] 20. Final checkpoint — Full integration
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- GDScript is used for all Godot game systems; Python/FastAPI for the generative AI backend only
- The game is fully playable offline (GDScript-only AI); the Python/LLM service adds generative depth when available
- Property tests validate the 28 correctness properties from the design document
- GdUnit4 is used for GDScript testing; pytest + Hypothesis for Python backend testing
- Checkpoints are placed after each major system group to catch integration issues early
- Each task references specific requirements for traceability
