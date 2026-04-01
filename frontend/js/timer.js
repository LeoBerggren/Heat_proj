function startHeatTimer(elementId, heatId) {
    const el = document.getElementById(elementId);

    async function update() {
        const res = await fetch(`http://localhost:8000/heat/${heatId}/timer`);
        const data = await res.json();

        if (!data.is_running) {
            el.innerText = "Heat not running";
            return;
        }

        const mins = Math.floor(data.time_remaining / 60);
        const secs = data.time_remaining % 60;

        el.innerText = `Time Remaining: ${mins}:${secs.toString().padStart(2, "0")}`;
    }

    update();
    return setInterval(update, 1000);
}
