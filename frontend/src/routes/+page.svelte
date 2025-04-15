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

    let build_time_qp = $state()
    let build_time_sc = $state()


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

    async function queryBackendGET2(path) {
        const backendUrl = `http://localhost:8000/${path}`
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
        getBuildTimeQP();
        getBuildTimeSC();
    }

    function SelectProductId(id){
        productIds = [...productIds, id];
        console.log($state.snapshot(productIds));
    }

    async function calculateDailyNutrition(){
        return queryBackendPOST("calculate_daily_nutrition", productIds);
    }

    async function handleCalculations(){
        calculationResult = await calculateDailyNutrition();
    }

    async function getBuildTimeQP(){
        build_time_qp = await queryBackendGET2("buildtimeqp");
    }

    async function getBuildTimeSC(){
        build_time_sc = await queryBackendGET2("buildtimesc");
    }


</script>

<button onclick={handleFuzz}>
    call fuzzy search
</button>

<!-- this is one way to handle the user's input for the brand they want to query in fuzzysearch -->
<label for="brand">Brand:</label>
<input id="brand" type="text" bind:value={brandText}>
<input onclick={() => (brandQuery = brandText)} type="submit"/>

<label for="description">Description:</label>
<input id="description" type="text" bind:value={descriptionText}>
<input onclick={() => (descriptionQuery = descriptionText)} type="submit"/>

<!-- rendering the results here -->
<p>build time qp{build_time_qp}</p>
<p>build time sc{build_time_sc}</p>

<p>Brand to search: {brandQuery}</p>
<p>Description to search: {descriptionQuery}</p>
{#if result}
<h1>Search Results</h1>
<ul>
    <!-- for loop in svelte: -->
	{#each result.products as foodTuple}
        <ul>
            {console.log(foodTuple[0])}
            <li>{foodTuple[0]}</li>
            <li>{foodTuple[1]}</li>
            <li>
                <!-- basically we want to create a button that corresponds to this food object, then we want to add that product id (foodTuple[2]) to a list that will get send to our calculate results function (hasn't been written yet, it will basically take a list of product ids and it will query our hash tables and return the sums of the nutritional info and the time it took to query each hash table) -->
                <button onclick={() => SelectProductId(foodTuple[2])}>
                    select
                </button>
                </li>
            <!-- <li>{foodTuple[2]}</li> -->
        </ul>
	{/each}
</ul>
{/if}

<button onclick={handleCalculations}>
    calculate daily nutrition
</button>

{#if calculationResult}
<p>Daily Results:</p>
<ul>
    <li>
        protein: {calculationResult.protein}
        calories: {calculationResult.calories}
        sugar: {calculationResult.sugar}
        time to query quadratic probing table: {calculationResult.query_time_qp}
    </li>
</ul>
{/if}


<style>


.webpage-title {
    font-size: 28px;
    font-weight: 500;
    color: #079CFF;
}

.title-outer-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #80D2FF;
    padding: 10px 24px;
    border-radius: 50px;
}

.title-inner-container {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #92D5FA;
    width: 300px;
    height: 100px;
    border-radius: 50px;
}


.brand {
    

}

.description {
    
}
</style>