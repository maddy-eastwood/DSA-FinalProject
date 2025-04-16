<script lang="js">
    // note: there may be a lot of "errors," but it's just javascript being javascript, this code works

    // result is a "dynamic" variable that holds the list of tuples as the result of fuzzysearch
    // basically, every time this variable gets updated in the code, svelte will rerender it to the screen
    let result = $state()
    let calculationResult = $state()

    // these variables are used to get user's input for the brand they want to query
    let brandText = $state("")
    let brandQuery = $state("")
    let descriptionText = $state("")
    let descriptionQuery = $state("")
    let productIds = $state([])
    let build_time_qp = $state("")
    let build_time_sc = $state("")
 


    // the path will be fuzzysearch to go to the fuzzysearch endpoint
    // params will be the description and, optionally, the brand
    async function queryBackendGET(path, params) {
        const backendUrl = `http://localhost:8000/${path}${params}`
        try {
        const fetchRequest = await fetch(backendUrl);
        if (fetchRequest.ok) {
            const body = await fetchRequest.json()
            console.log(body);
            return body;
        }
        }
        catch (e) {
            console.error(e);
            return null;
        }
    }


    async function queryBackendPOST(path, params){
        const backendUrl = `http://localhost:8000/${path}`;
        try {
            const fetchRequest = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                },
                body: JSON.stringify(params)
            });
            if (fetchRequest.ok){
                const body = await fetchRequest.json()
                console.log("backend response", body);
                return body;
            }
        }
        catch (e){
            console.error("error during fetch", e);
            return null;
        }
    }

    // this will query the backend with the fuzzysearch path and necessary params
    async function fuzzySearch(description, brand) {
        if (brand != "") {
            return queryBackendGET("fuzzysearch", `?description=${description}&brand=${brand}`)
        } else {
            return queryBackendGET("fuzzysearch", `?description=${description}`)
        }
    }

    // this is used by the button "call fuzzy search"
    async function handleFuzz() {
        result = await fuzzySearch(descriptionQuery, brandQuery);
     
    }

    function SelectProductId(id){
        productIds = [...productIds, id];
        console.log($state.snapshot(productIds));
    }

    async function calculateDailyNutrition(){
        return queryBackendPOST("calculate_daily_nutrition", productIds);
    }

    async function handleCalculations() {
        const rawResult = await calculateDailyNutrition();

        // for rounding - if the result is a number, round and add seconds
        if (rawResult) {
            if (typeof rawResult.query_time_qp === "number") {
                rawResult.query_time_qp = rawResult.query_time_qp.toFixed(6) + " seconds";
            }

            if (typeof rawResult.query_time_sc === "number") {
                rawResult.query_time_sc = rawResult.query_time_sc.toFixed(6) + " seconds";
            }
        }
        //storing the result in calculation result
        calculationResult = rawResult;
}




    async function fetchBuildTimeQP() {
    try {
        const response = await fetch("http://localhost:8000/buildtimeqp");
        const data = await response.json();
        if (data && typeof data.build_time_qp === "number") {
            build_time_qp = data.build_time_qp.toFixed(2) + " seconds";
        } else {
            build_time_qp = "Unavailable";
            console.error("Unexpected response:", data);
        }
    } catch (e) {
        build_time_qp = "Error";
        console.error("Failed to fetch build time qp:", e);
    }
}


async function fetchBuildTimeSC() {
    try {
        const response = await fetch("http://localhost:8000/buildtimesc");
        const data = await response.json();
        if (data && typeof data.build_time_sc === "number") {
            build_time_sc = data.build_time_sc.toFixed(2) + " seconds";
        } else {
            build_time_sc = "Unavailable";
            console.error("Unexpected response:", data);
        }
    } catch (e) {
        build_time_sc = "Error";
        console.error("Failed to fetch build time sc:", e);
    }
}

fetchBuildTimeSC();
fetchBuildTimeQP();

</script>


<!--input section for user to type in a food brand and description -->
<div class="input-section">
  <div class="brand-description-group">
    <!--group for entering the brand -->
    <div class="input-group">
      <label for="brand">Brand:</label>
      <!--this input box is for typing the brand name -->
      <!--whatever they type gets saved into the brandText variable -->
      <input id="brand" type="text" bind:value={brandText} />
      <!--cicking this button sets the brandQuery to whatever is in brandText -->
      <input type="submit" value="Set Brand" onclick={() => (brandQuery = brandText)} />
    </div>



    <!--group for entering the food description -->
    <div class="input-group">
      <label for="description">Description:</label>
      <!--this input box is for typing what kind of food it is-->
      <input id="description" type="text" bind:value={descriptionText} />
      <!--clicking this sets descriptionQuery to whatever the user typed -->
      <input type="submit" value="Set Description" onclick={() => (descriptionQuery = descriptionText)} />
    </div>
  </div>


  <!--this button runs the fuzzy search to find matches based on input -->
  <button class="button-main" onclick={handleFuzz}>Find Specific Brand</button>
</div>



<!--this part handles the nutrition calculation -->
<div class="calculate-section">
    <!--button to calculate total nutrition based on selected foods -->
  <button class="button-main" onclick={handleCalculations}>Calculate Daily Nutrition</button>

  <!--only show the results if they exist -->
  {#if calculationResult}
    <div class="result-section">
      <p><strong>Daily Results:</strong></p>
      <ul>
        <li>Calories: {calculationResult.calories.toFixed(2)}</li>
        <li>Protein: {calculationResult.protein.toFixed(2)}g</li>
        <li>Sugar: {calculationResult.sugar.toFixed(2)}g</li>
      </ul>
    </div>
  {/if}
</div>

<!--section to show how long it took to build each hash table -->
<div class="build-time-section">
  <h3>Build Times</h3>
  <div class="build-box">
    <!--span just holds the size of the text rather than div which is like a whole block-->
    <span>Quadratic Probing:</span>
    <!--strong is just bolding it - also makes it treated as important by browsers rather than just using <b>-->
    <strong>{build_time_qp}</strong>
  </div>
  <div class="build-box">
    <span>Separate Chaining:</span>
    <strong>{build_time_sc}</strong>
  </div>
</div>

<!--section to show how long the search took using each hash table -->
<div class="search-time-section">
  <h3>Overall Search Times</h3>
  <div class="build-box">
    <span>Search Time (Quadratic Probing):</span>
    <strong>{calculationResult?.query_time_qp}</strong>
  </div>
  <div class="build-box">
    <span>Search Time (Separate Chaining):</span>
    <strong>{calculationResult?.query_time_sc}</strong>
  </div>
</div>

<!--showing current brand and description that will be used for searching -->
<p><strong>Brand to search:</strong> {brandQuery}</p>
<p><strong>Description to search:</strong>{descriptionQuery}</p>

<!--if there are results - this will display them -->
{#if result}
  <div class="result-section">
    <h1>Search Results</h1>
    <ul>
      <!--loop thru each food item we got from the backend -->
      {#each result.products as foodTuple}
        <ul class="product-list-item">
          <!--show brand and description for each item -->
          <li><strong>Brand:</strong> {foodTuple[1]}</li>
          <li><strong>Description:</strong> {foodTuple[0]}</li>
          <li>
            <!-- button to select the item -->
            <button class="button-select" onclick={() => SelectProductId(foodTuple[2])}>
              <!--if it exists im prodict ids, change the button text from select to selected show a checkmark - added this to make it more clear so they knew -->
              {productIds.includes(foodTuple[2]) ? '✔ Selected' : 'Select'}
            </button>
          </li>
        </ul>
      {/each}
    </ul>
  </div>
{/if}

<style>
/* ---------- button stylezzzz!!!! ---------- */

/*general button looooook */
button {
  background-color: #4CAF50;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  margin: 10px 0;
}

/*make button a little bigger when you hover with transform */
button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

/*remove the blue outline when clicked - helps show when on the button*/
button:focus {
  outline: none;
}

/*main action buttons - the ones that calculate big stuff */
.button-main {
  background-color: #007BFF;
}

.button-main:hover {
  background-color: #0056b3;
}

/*buttons for picking food items */
.button-select {
  background-color: #f0ad4e;
  font-size: 14px;
  padding: 8px 14px;
}

.button-select:hover {
  background-color: #ec971f;
}

/* ---------- RESULLT STYLING ---------- */

.product-list-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f9f9f9;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 8px;
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
}

/*style for the select button inside each product */
.product-list-item button {
  margin-top: 10px;
  background-color: #5bc0de;
  font-size: 16px;
  padding: 10px;
  transition: background-color 0.2s ease;
}

.product-list-item button:hover {
  background-color: #31b0d5;
}

/*style if it product is already selected */
.product-list-item button.selected {
  background-color: #28a745;
  color: white;
  font-weight: bold;
}

.product-list-item button.selected:hover {
  background-color: #218838;
}

/* ---------- INPUT SECTIONNNN ---------- */

.input-section {
  background: #e6f0ff;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.05);
}

/*layout for each input and label */
.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

/*make the labels bold */
.input-group label {
  font-weight: bold;
}

/*style the text inputs */
.input-group input[type="text"] {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  margin-right: 8px;
}

/*style the small submit buttons */
.input-group input[type="submit"] {
  padding: 8px 14px;
  background-color: #007BFF;
  color: white;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.input-group input[type="submit"]:hover {
  background-color: #0056b3;
}

/* ---------- BUILD TIME ---------- */

.build-time-section {
  background: #f7faff;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 20px;
  max-width: 500px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.build-time-section h3 {
  margin-bottom: 10px;
  color: #333;
}

/*box for showing timing info */
.build-box {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background-color: #fff;
  border-radius: 8px;
  margin-bottom: 6px;
  font-size: 14px;
  border: 1px solid #e0e6f0;
}

/* ---------- SEARCH TIME ---------- */

.search-time-section {
  background: #e7f3ff;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.05);
}

.search-time-section h3 {
  margin-bottom: 10px;
  color: #333;
}

/* Reusing build-box for layout */
.search-time-section .build-box {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 6px;
}

/* ---------- RESULTS ---------- */

.result-section {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
}

/*styling for list (protein, cals, sugar) inside results */
.result-section ul {
  padding-left: 20px;
}

.result-section ul > ul {
  margin-top: 12px;
}

/*layout for the calculate-section */
.calculate-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}
</style>
