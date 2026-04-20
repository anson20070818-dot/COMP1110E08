<a id="testing-top"></a>
<br />
<div align="center">
<h3 align="center">Smart Public Transport Advisor - Testing Documentation</h3>
  <p align="center">
    Sample test cases and evaluation scenarios for the route optimization system.
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li>
      <a href="#test-cases">Test Cases</a>
      <ul>
        <li><a href="#scenario-1-fastest-route">Scenario 1: Fastest Route</a></li>
        <li><a href="#scenario-2-cheapest-route-with-transport-filter">Scenario 2: Cheapest Route with Filter</a></li>
        <li><a href="#scenario-3-fewest-transfers">Scenario 3: Fewest Transfers</a></li>
        <li><a href="#scenario-4-excluding-a-common-mode">Scenario 4: Excluding a Common Mode</a></li>
        <li><a href="#scenario-5-error-handling-invalid-inputs-and-missing-files">Scenario 5: Error Handling</a></li>
      </ul>
    </li>
  </ol>
</details>

## Overview
This document outlines the standard test cases used to evaluate the Smart Public Transport Advisor. These scenarios demonstrate the system's ability to handle different user priorities (Fastest, Cheapest, Fewest Transfers) and apply specific transport mode filters. 

All tests below should be run using the default `network.csv` file located in the `data` folder.



## Test Cases

### Scenario 1: Fastest Route
**Goal:** Find the fastest journey from University to Seaside Mall.

* **Network File:** `network.csv`
* **Origin:** `University`
* **Destination:** `Seaside Mall`
* **First Preference:** `1`(Fastest Journeys)
* **Second Preference:** `3`(No Preference)
* **Transport Filter:** `7`(Finish Filter Input)

**Expected Result:** The program should rank the direct Metro route (University → Central Plaza → Office Hub → Seaside Mall) first, displaying a total duration of 12 minutes.

<p align="right">(<a href="#testing-top">back to top</a>)</p>

### Scenario 2: Cheapest Route with Transport Filter
**Goal:** Find the cheapest journey from University to Harbour Pier while excluding Ferry.

* **Network File:** `network.csv`
* **Origin:** `University`
* **Destination:** `Harbour Pier`
* **First Preference:** `2`(Cheapest Journeys)
* **Second Preference:** `3`(No Preference)
* **Transport Filter:** `2`(Ferry) then `6`(Finish Filter Input)

**Expected Result:** The program should correctly apply the filter to remove Ferry options and rank a route costing HK$7 first (which will take longer than the more expensive alternatives).

<p align="right">(<a href="#testing-top">back to top</a>)</p>

### Scenario 3: Fewest Transfers - Multimodal Journey
**Goal:** Minimise transfers from Central Plaza to Community Clinic, then minimise time.

* **Network File:** `network.csv`
* **Origin:** `Central Plaza`
* **Destination:** `Community Clinic`
* **First Preference:** `3`(Journeys with Fewest Transfers)
* **Second Preference:** `1`(Fastest Journeys)
* **Transport Filter:** `7`(Finish Filter Input)

**Expected Result:** All top recommended journeys should show 0 transfers. Because the first preference results in a tie (multiple 0-transfer options), the system should use the secondary preference (Fastest) to determine the final ranking order.

<p align="right">(<a href="#testing-top">back to top</a>)</p>

### Scenario 4: Excluding a Common Mode (Metro)
**Goal:** Find a reasonable route from Bank Tower to Museum without using the Metro.

* **Network File:** `network.csv`
* **Origin:** `Bank Tower`
* **Destination:** `Museum`
* **First Preference:** `1`(Fastest Journeys)
* **Second Preference:** `2`(Cheapest Journeys)
* **Transport Filter:** `3`(Metro) then `6`(Finish Filter Input)

**Expected Result:** The program should successfully remove all Metro segments from consideration. The top-ranked result should be a Tram + Walking route with a total duration of 9 minutes.

<p align="right">(<a href="#testing-top">back to top</a>)</p>

### Scenario 5: Error Handling (Invalid Inputs and Missing Files)
**Goal:** Verify the system's robustness against user errors and missing data.

* **Network File:** `non_existent_file.csv`
* **Origin:** `Fake Stop`
* **Destination:** `University`

**Expected Result:** 
1. When attempting to load the invalid network file, the program should gracefully catch the error and display an error message (e.g., "Error: Cannot find the file").
2. After loading the correct `network.csv`, if the user enters `Fake Stop` as the origin, the program should reject the input and prompt the user again with "Stop not found!".
3. If the user enters the same stop for both Origin and Destination (e.g., `University` to `University`), the program should display an error stating "Destination cannot be the same as Origin!".

<p align="right">(<a href="#testing-top">back to top</a>)</p>
