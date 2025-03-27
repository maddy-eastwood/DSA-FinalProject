<script lang="ts">
    let result = $state(0)
    async function quadraticProbing() {
        const backendUrl = 'http://localhost:8000/'
        try {
        const fetchRequest = await fetch(backendUrl);
        if (fetchRequest.ok) {
            const body = await fetchRequest.json()
            console.log(body);
        }
        }
        catch (e) {
            console.error(e);
        }
    }
</script>

<button onclick={quadraticProbing}>
    call backend
</button>
<p>{result}</p>
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