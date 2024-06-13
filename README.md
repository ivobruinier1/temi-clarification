# Human-Robot Interaction Transcripts Dataset

This repository contains a dataset of transcripts from human-robot interactions collected in a Wizard of Oz setting. The interactions cover three different scenarios and have been annotated for clarification types with spans.

## Dataset Description

The dataset includes transcripts of conversations between humans and a robot, where the robot's responses were controlled by a human operator. The three scenarios are designed to capture a variety of interaction contexts:

1. **Scenario 1: Turn Around for QR Code Scanning**
2. **Scenario 2: Check if the Light is On or Off in a Seprate Room**
3. **Scenario 3: Get a Book from a Separate Room**

### Annotations

Each transcript is annotated with the following details:

- **Clarification Turns**: Turns that include clarification dialogue
- **Clarification Types**: Types of clarifications requested during the interaction.
- **Spans**: The exact segments of text where the clarifications occur.

## Data Format


Certainly! Here is the code for the README file in Markdown format, which you can copy and paste directly into your GitHub repository's README.md file.

markdown
Code kopiëren
# Human-Robot Interaction Transcripts Dataset

This repository contains a dataset of transcripts from human-robot interactions collected in a Wizard of Oz setting. The interactions cover three different scenarios and have been annotated for clarification types with spans.

## Dataset Description

The dataset includes transcripts of conversations between humans and a robot, where the robot's responses were controlled by a human operator. The three scenarios are designed to capture a variety of interaction contexts:

1. **Scenario 1: Turn Around**
2. **Scenario 2: Check if the Light is On or Off**
3. **Scenario 3: Get a Book from a Separate Room**

### Annotations

Each transcript is annotated with the following details:

- **Clarification Types**: Types of clarifications requested during the interaction.
- **Spans**: The exact segments of text where the clarifications occur.

## Data Format

The dataset is organized into directories, with annotations provided in JSON and XML format.


### Sample Annotation XML Format

<dialogue>
  <metadata>
    <gender>Female</gender>
    <age_group>36+</age_group>
    <nationality>Dutch</nationality>
    <first_language>Dutch</first_language>
    <english_skills>Basic</english_skills>
    <education>Secondary education</education>
    <tech_savviness>Intermediate</tech_savviness>
    <date_of_interaction>24/05/2024</date_of_interaction>
    <amount_of_turns>60</amount_of_turns>
    <distinct_clarification_type_count>4</distinct_clarification_type_count>
    <amount_of_interactions>6</amount_of_interactions>
  </metadata>
  <entry>
    <start_ms>240</start_ms>
    <speaker>Participant</speaker>
    <text>come over</text>
    <clarification_turn/>
    <clarification_type/>
  </entry>
  <entry>
    <start_ms>3374</start_ms>
    <speaker>TEMI</speaker>
    <text>sure ((temi comes to participant)) (25.0)</text>
    <clarification_turn/>
    <clarification_type/>
  </entry>
  <entry>
    <start_ms>29234</start_ms>
    <speaker>TEMI</speaker>
    <text>hi there {Participant} how can i help you</text>
    <clarification_turn/>
    <clarification_type/>
  </entry>
....
</dialogue>

## Usage

To use this dataset, clone the repository and load the transcripts and annotations into your analysis tool of choice.
