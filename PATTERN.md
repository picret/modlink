# AI Abstraction Pattern

## Overview
A software pattern for defining human-computer and computer-computer interaction. This establishes definitions that enable agents to integrate with agents and people.

## Definitions

- **Person:** An individual interacting with the system; not a software definition.
- **Platform:** A system that hosts Agents and gives access to Capabilities.
- **Agent:** A lifecycle-aware service capable of handling Actions and altering the Context state.
- **State:** The current data, information, or condition of the system, which can be altered through actions.
- **Action:** An operation triggered by an Agent or a person that can change the state.
- **Capability:** An identifier describing an Agent's ability to perform Actions.
- **Context:** A carrier for States and Capabilities that are relevant for an Agent.
- **Authentication:** A system that authorizes an Agent or Person to access one or more Capabilities.
- **Permission:** A platform rule that allows an Agent to perform Actions or access State.

## Platform Agent

Each platform must define Agents that can perform Actions described by Capabilities.

### Examples
- **SpeechToText:** Converts spoken language captured through a platform microphone into text.
- **TextToSpeech:** Converts text into spoken language through a platform speaker.
- **TextGeneration:** Converts text into responses through a platform interface.
- **WakeWordAgent** Wakes up the platform when a specific word or phrase is spoken.
- **MicrophoneAgent:** Captures audio data from a platform's microphone.
- **NetworkAgent:** Connects to the internet and retrieves data from a platform's network.
- **AlarmAgent:** Wakes up the platform at a specific time or interval.
- **StorageAgent:** Saves and retrieves data from a platform's storage system.

## Application Agent

An application can be a collection of Agents and Capabilities to create a new Agent. This allows for smaller, more focused Agents to combine into a larger, more complex Agents. This also makes it possible to create levels of abstraction for the interactions between Agents. For example, a Health Coach Agent should not have the capability to spend money without the Financial Advisor Agent's permission. The kitchen assistant, and the skin routine assistant may have similar capabilities, but different contexts.

### Examples
- **Navigation Assistant:** Provides directions, traffic updates, and points of interest.
- **Learning Companion:** Personalizes educational content and fosters learning.
- **Health Coach:** Guides health goals by keeping track of stats dates and goals.
- **Skin Routine Assistant:** Manages skincare routines and provides recommendations.
- **Personal Assistant:** Manages personal tasks, schedules, and reminders.
- **Financial Advisor:** Manages and advises on personal or communal financial health.
- **Career Mentor:** Supports career development based on market trends and personal aspirations.
- **Workflow Manager:** Streamlines individual and organizational processes for efficiency.
- **Kitchen Assistant:** Provides personalized cooking assistance. Creates or follows recipes, maintains alarms, and translates reviews.
- **Language Teacher:** Teaches languages through speech, text, and conversation.
