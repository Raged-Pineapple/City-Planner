// Slime Mold Algorithm Animation Demo
// Author: CityPlanner AI

const canvas = document.getElementById('demo-canvas');
const ctx = canvas.getContext('2d');

let nodes = [];
let agents = [];
let running = false;
const AGENT_COUNT = 500;
const AGENT_SPEED = 1.5;
const AGENT_SENSE_DIST = 8;
const AGENT_TURN_ANGLE = Math.PI / 8;

canvas.addEventListener('click', function(e) {
  if (running) return;
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  nodes.push({ x, y });
  drawDemo();
});

function clearDemo() {
  running = false;
  nodes = [];
  agents = [];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawDemo() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Draw nodes
  ctx.fillStyle = '#007bff';
  for (const node of nodes) {
    ctx.beginPath();
    ctx.arc(node.x, node.y, 10, 0, 2 * Math.PI);
    ctx.fill();
    ctx.strokeStyle = '#333';
    ctx.stroke();
  }
}

drawDemo();

function startSlimeMold() {
  if (nodes.length < 2) {
    alert('Add at least 2 nodes to start the simulation.');
    return;
  }
  running = true;
  agents = [];
  // Spawn agents at random nodes
  for (let i = 0; i < AGENT_COUNT; i++) {
    const startNode = nodes[Math.floor(Math.random() * nodes.length)];
    agents.push({
      x: startNode.x + (Math.random() - 0.5) * 10,
      y: startNode.y + (Math.random() - 0.5) * 10,
      angle: Math.random() * 2 * Math.PI,
      path: [{ x: startNode.x, y: startNode.y }],
      target: getRandomTarget(startNode)
    });
  }
  animateSlimeMold();
}

function getRandomTarget(excludeNode) {
  let filtered = nodes.filter(n => n !== excludeNode);
  return filtered[Math.floor(Math.random() * filtered.length)];
}

function animateSlimeMold() {
  if (!running) return;
  // Fade trails
  ctx.fillStyle = 'rgba(255,255,255,0.08)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  // Draw nodes
  for (const node of nodes) {
    ctx.beginPath();
    ctx.arc(node.x, node.y, 10, 0, 2 * Math.PI);
    ctx.fillStyle = '#007bff';
    ctx.fill();
    ctx.strokeStyle = '#333';
    ctx.stroke();
  }
  // Move agents
  for (const agent of agents) {
    // Sense direction to target
    let dx = agent.target.x - agent.x;
    let dy = agent.target.y - agent.y;
    let dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < 8) {
      // Arrived at target, pick a new one
      agent.target = getRandomTarget(agent.target);
      agent.path.push({ x: agent.x, y: agent.y });
    } else {
      let angleToTarget = Math.atan2(dy, dx);
      // Small random turn to simulate exploration
      agent.angle += (angleToTarget - agent.angle) * 0.2 + (Math.random() - 0.5) * AGENT_TURN_ANGLE;
      agent.x += Math.cos(agent.angle) * AGENT_SPEED;
      agent.y += Math.sin(agent.angle) * AGENT_SPEED;
      agent.path.push({ x: agent.x, y: agent.y });
    }
    // Draw agent trail
    ctx.beginPath();
    ctx.moveTo(agent.path[0].x, agent.path[0].y);
    for (let i = 1; i < agent.path.length; i++) {
      ctx.lineTo(agent.path[i].x, agent.path[i].y);
    }
    ctx.strokeStyle = 'rgba(0,200,0,0.15)';
    ctx.lineWidth = 2;
    ctx.stroke();
    // Draw agent
    ctx.beginPath();
    ctx.arc(agent.x, agent.y, 2, 0, 2 * Math.PI);
    ctx.fillStyle = '#28a745';
    ctx.fill();
  }
  requestAnimationFrame(animateSlimeMold);
} 