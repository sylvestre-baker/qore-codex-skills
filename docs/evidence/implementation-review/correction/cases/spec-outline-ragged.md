<!-- qore-spec/1 -->
~~~~gherkin
Feature: Probe
  Scenario Outline: AC01 Test
    Given <input>
    When executed
    Then output
    Examples:
      | input |
      | x | y |
~~~~
Coverage: AC01 -> US1
```mermaid
sequenceDiagram
 A->>B: Check
```
