<script lang="js">
    // note: there may be a lot of "errors," but it's just javascript being javascript, this code works

    // result is a "dynamic" variable that holds the list of tuples as the result of fuzzysearch
    // basically, every time this variable gets updated in the code, svelte will rerender it to the screen
    let result = $state()

    // these variables are used to get user's input for the brand they want to query
    let brandText = $state("")
    let brandQuery = $state("");

    // the path will be fuzzysearch to go to the fuzzysearch endpoint
    // params will be the description and, optionally, the brand
    async function queryBackend(path, params) {
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

    // this will query the backend with the fuzzysearch path and necessary params
    async function fuzzySearch(description, brand=null) {
        if (brand != null) {
            return queryBackend("fuzzysearch", `?description=${description}&brand=${brand}`)
        } else {
            return queryBackend("fuzzysearch", `?description=${description}`)
        }
    }

    // this is used by the button "call fuzzy search"
    async function handleFuzz() {
    result = await fuzzySearch("eggs", brandQuery);
  }

</script>

<button onclick={handleFuzz}>
    call fuzzy search
</button>

<!-- this is one way to handle the user's input for the brand they want to query in fuzzysearch -->
<label for="brand">Brand:</label>
<input id="brand" type="text" bind:value={brandText}>
<input onclick={() => (brandQuery = brandText)} type="submit"/>

<!-- rendering the results here -->
<p>Brand to search: {brandQuery}</p>
{#if result}
<h1>Search Results</h1>
<ul>
    <!-- for loop in svelte: -->
	{#each result.products as foodTuple}
        <ul>
            {console.log(foodTuple[0])}
            <li>
                <!-- basically we want to create a button that corresponds to this food object, then we want to add that product id (foodTuple[2]) to a list that will get send to our calculate results function (hasn't been written yet, it will basically take a list of product ids and it will query our hash tables and return the sums of the nutritional info and the time it took to query each hash table) -->
                <button>
                    {foodTuple[0]}
                </button>
                </li>
            <li>{foodTuple[1]}</li>
            <!-- <li>{foodTuple[2]}</li> -->
        </ul>
	{/each}
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
</style>