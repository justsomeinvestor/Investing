# AI Workflow: End-of-Day Close Probability Update

**Objective:** To automatically parse the daily options data, calculate the end-of-day close probability for SPY, and update the research dashboard.

**Operator:** AI Assistant

**Input:** `Research/Options Data/YYYY-MM-DD-StockAndOptionQuoteForSPY.csv`

**Output:** Updated `master-plan/master-plan.md` and a correctly rendered "End-of-Day Close Probability" card on the dashboard.

---

## Workflow Steps

### 1. Read and Parse the Options Data

1.  **Locate the latest CSV file:** Find the most recent `...StockAndOptionQuoteForSPY.csv` file in the `Research/Options Data/` directory.
2.  **Read the file content:** Read the entire content of the CSV file.
3.  **Parse the data:**
    *   **Caution:** The CSV file is not a clean CSV. It is a text report with a messy format. You will need to use string manipulation and regular expressions to extract the required data.
    *   **Extract the following data points for SPY:**
        *   The current price of SPY.
        *   The strike price and delta of the nearest out-of-the-money (OTM) call option.
        *   The strike price and delta of the nearest out-of-the-money (OTM) put option.
    *   **Calculate the probabilities:**
        *   The probability of the price closing above the call strike is the delta of the call option.
        *   The probability of the price closing below the put strike is the delta of the put option.
        *   The probability of the price closing between the strikes is `100 - (call_delta + put_delta)`.

### 2. Update the `master-plan.md` File

1.  **Read the `master-plan.md` file:** Read the entire content of the `master-plan/master-plan.md` file.
2.  **Locate the `closeProbability` object:** Find the `closeProbability` object within the `technicals` tab of the `dashboard` JSON object.
3.  **Update the `closeProbability` object:**
    *   **Verification:** Before writing, ensure the `closeProbability` object has the following schema. If it does not, correct it.
        ```json
        "closeProbability": {
          "SPY": {
            "model": "0DTE Options Delta",
            "lastUpdated": "...",
            "probabilities": {
              "higher": 0,
              "flat": 0,
              "lower": 0
            },
            "keyLevels": {
                "above": "0",
                "below": "0"
            }
          }
        }
        ```
    *   **Update the values:**
        *   `lastUpdated`: The current time.
        *   `probabilities.higher`: The calculated probability of closing higher.
        *   `probabilities.flat`: The calculated probability of closing flat.
        *   `probabilities.lower`: The calculated probability of closing lower.
        *   `keyLevels.above`: The call strike price.
        *   `keyLevels.below`: The put strike price.
        *   `factors`: An array of objects, each with a `text` (string) and `impact` (string: "bullish", "bearish", or "neutral") property, explaining the drivers of the probabilities.
4.  **Write the updated content back to `master-plan.md`:** Use the `replace` tool to update the `closeProbability` object.

### 3. Verify the Dashboard

1.  **Read the `research-dashboard.html` file:** Read the entire content of the `master-plan/research-dashboard.html` file.
2.  **Verify the `renderCloseProbability` function:**
    *   **Verification:** Ensure there is only one `renderCloseProbability` function in the file. If there are duplicates, remove the older one (the one that returns an HTML string).
3.  **Verify the `renderProviderTabs` function:**
    *   **Verification:** Ensure the `renderProviderTabs` function is correctly mapping the data from `master-plan.md` to the `renderCloseProbability` function. It should include a mapping layer to handle the new schema and pass the `dashboard` object as a parameter.
4.  **Final Check:**
    *   After updating the files, mentally (or with a tool if available) render the dashboard and confirm that the "End-of-Day Close Probability" card is displayed correctly with the new data and without any errors.

---

**Cautions and Error Handling:**

*   If the CSV file format changes, the parsing logic will need to be updated.
*   If the `master-plan.md` schema changes, the update logic will need to be updated.
*   If the dashboard is still showing errors after following these steps, carefully re-read the error message and the relevant code to identify the root cause. Do not blindly try to fix the issue without understanding it.
