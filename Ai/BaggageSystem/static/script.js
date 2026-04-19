const canvas = document.getElementById('mainCanvas');
const ctx = canvas.getContext('2d');
let airportData = { nodes: {}, edges: [] };

// Initialize App
async function init() {
    const res = await fetch('/config');
    airportData = await res.json();
    resize();
    populateDropdowns();
    renderBase();
}

function populateDropdowns() {
    const startS = document.getElementById('startSelect');
    const endS = document.getElementById('endSelect');
    
    for (let id in airportData.nodes) {
        let opt = `<option value="${id}">${airportData.nodes[id].name}</option>`;
        startS.innerHTML += opt;
        endS.innerHTML += opt;
    }
}

function renderBase() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw Belts (Edges)
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    airportData.edges.forEach(([u, v]) => {
        const n1 = airportData.nodes[u].pos;
        const n2 = airportData.nodes[v].pos;
        ctx.beginPath();
        ctx.moveTo(n1[0], n1[1]);
        ctx.lineTo(n2[0], n2[1]);
        ctx.stroke();
    });

    // Draw Nodes
    ctx.setLineDash([]);
    for (let id in airportData.nodes) {
        const node = airportData.nodes[id];
        ctx.fillStyle = node.type === 'gate' ? '#ef4444' : '#3b82f6';
        ctx.beginPath();
        ctx.arc(node.pos[0], node.pos[1], 8, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = "#94a3b8";
        ctx.font = "10px Inter, sans-serif";
        ctx.fillText(node.name, node.pos[0] - 20, node.pos[1] + 20);
    }
}

document.getElementById('dispatchBtn').onclick = async () => {
    const start = document.getElementById('startSelect').value;
    const end = document.getElementById('endSelect').value;
    
    const res = await fetch('/route', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({start, end})
    });
    
    const data = await res.json();
    document.getElementById('statusLabel').innerText = "DISPATCHING";
    document.getElementById('statusLabel').className = "value active";
    document.getElementById('timeLabel').innerText = data.cost + "s";
    
    animatePath(data.path);
};

function animatePath(path) {
    let i = 0;
    function step() {
        if (i >= path.length) {
            document.getElementById('statusLabel').innerText = "ARRIVED";
            document.getElementById('statusLabel').className = "value idle";
            return;
        }
        renderBase();
        const pos = airportData.nodes[path[i]].pos;
        
        // Bag Icon
        ctx.fillStyle = "#facc15";
        ctx.shadowBlur = 15;
        ctx.shadowColor = "#facc15";
        ctx.fillRect(pos[0]-10, pos[1]-10, 20, 15);
        ctx.shadowBlur = 0;
        
        i++;
        setTimeout(step, 600);
    }
    step();
}

function resize() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

init();