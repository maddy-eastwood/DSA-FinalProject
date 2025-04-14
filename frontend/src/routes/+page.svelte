<script lang="js">
    let result = $state()

    let brandText = $state("")
    let brandQuery = $state("");

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

    async function fuzzySearch(description, brand=null) {
        if (brand != null) {
            return queryBackend("fuzzysearch", `?description=${description}&brand=${brand}`)
        } else {
            return queryBackend("fuzzysearch", `?description=${description}`)
        }
    }

    async function handleFuzz() {
    result = await fuzzySearch("eggs", brandQuery);
  }

</script>

<button onclick={handleFuzz}>
    call fuzzy search
</button>

<label for="brand">Brand:</label>
<input id="brand" type="text" bind:value={brandText}>
<input onclick={() => (brandQuery = brandText)} type="submit"/>


<p>Brand to search: {brandQuery}</p>
{#if result}
<h1>Search Results</h1>
<ul>
	{#each result.products as foodTuple}
        <ul>
            {console.log(foodTuple[0])}
            <li>
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