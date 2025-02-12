<script>
    import { onMount } from 'svelte';
    import uPlot from 'uplot';
    import 'uplot/dist/uPlot.min.css';

    let messages = [];
    let socket;
    let uplot;
    let uplotContainer;

    const MAX_SECONDS = 10; // Rolling window in seconds
    const FREQUENCY = 25; // Data frequency (Hz)
    const MAX_POINTS = MAX_SECONDS * FREQUENCY;

    let plotData = [Array(MAX_POINTS).fill(null), Array(MAX_POINTS).fill(null), Array(MAX_POINTS).fill(null)];
    let timeStamps = Array.from({ length: MAX_POINTS }, (_, i) => -MAX_SECONDS + i / FREQUENCY); // X-axis

    onMount(() => {
        socket = new WebSocket('ws://localhost:8765');

        socket.onopen = () => addMessage('WebSocket connected.');
        socket.onclose = () => addMessage('WebSocket disconnected.');
        socket.onerror = (err) => addMessage(`WebSocket error: ${err}`);
        socket.onmessage = (event) => handleData(event.data);

        initPlot();

        return () => socket.close();
    });

    function addMessage(message) {
        const timestamp = new Date().toLocaleTimeString();
        messages = [...messages, `[${timestamp}] ${message}`].slice(-50);
        scrollToBottom();
    }

    function handleData(data) {
        const parsed = JSON.parse(data);

        // Shift old data and append new values
        plotData[0].shift();
        plotData[0].push(parsed.state1 || null);

        plotData[1].shift();
        plotData[1].push(parsed.state2 || null);

        plotData[2].shift();
        plotData[2].push(parsed.state3 || null);

        // Update the chart
        uplot.setData([timeStamps, ...plotData]);
    }

    function initPlot() {
        const options = {
            title: "Robot States",
            width: 600,
            height: 300,
            scales: {
                x: {
                    time: false,
                },
                y: {
                    auto: true,
                },
            },
            series: [
                { label: "Time (s)" },
                { label: "State 1", stroke: "red", width: 2 },
                { label: "State 2", stroke: "blue", width: 2 },
                { label: "State 3", stroke: "green", width: 2 },
            ],
            axes: [
                { grid: { show: true }, size: 50 },
                { grid: { show: true }, size: 50 },
            ],
        };

        uplot = new uPlot(options, [timeStamps, ...plotData], uplotContainer);
    }

    function scrollToBottom() {
        const logContainer = document.querySelector('.log');
        if (logContainer) {
            logContainer.scrollTop = logContainer.scrollHeight;
        }
    }
</script>

<style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #1e90ff, #87cefa);
        color: white;
        text-align: center;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    h1 {
        margin-bottom: 20px;
    }

    button {
        padding: 10px 20px;
        background-color: #4caf50;
        border: none;
        border-radius: 5px;
        color: white;
        font-size: 1rem;
        cursor: pointer;
        margin-bottom: 20px;
    }

    button:hover {
        background-color: #45a049;
    }

    .log {
        width: 90%;
        max-width: 600px;
        background: black;
        color: white;
        padding: 10px;
        border-radius: 5px;
        max-height: 200px;
        overflow-y: auto;
        text-align: left;
        margin-bottom: 20px;
    }

    #plot {
        width: 600px;
        height: 300px;
    }
</style>

<main>
    <h1>Robot Dashboard</h1>
    <button on:click={() => socket.send('Button pressed')}>Send Message</button>
    <div class="log">
        {#each messages as message}
            <p>{message}</p>
        {/each}
    </div>
    <div id="plot" bind:this={uplotContainer}></div>
</main>
