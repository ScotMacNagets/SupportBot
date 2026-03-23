const userId = 1;
let ws;
let messageCounter = 0;

const messagesDiv = document.getElementById("messages");

/* TOGGLE */
function toggleChat() {
    const chat = document.getElementById("chat");
    chat.style.display = chat.style.display === "flex" ? "none" : "flex";
}

/* CONNECT */
function connect() {
    ws = new WebSocket(`ws://localhost:8000/api/v1/websocket/ws?user_id=${userId}`);

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "message") {
            const msg = data.message;

            // обновляем статус если это наше сообщение
            updateMessageStatus(msg.id, "delivered");

            addMessage(
                msg.text,
                msg.sender_role === "user" ? "user" : "support",
                msg.created_at,
                msg.id
            );
        }
    };

    ws.onclose = () => setTimeout(connect, 2000);
}

connect();

/* ADD MESSAGE */
function addMessage(text, type, time, id=null) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("message", type);

    if (id) wrapper.dataset.id = id;

    wrapper.innerHTML = `
        <div class="bubble">${text}</div>
        <div class="meta">
            <span>${new Date(time).toLocaleTimeString()}</span>
            ${type === "user" ? `<span class="status">✓</span>` : ""}
        </div>
    `;

    messagesDiv.appendChild(wrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

/* SEND */
function sendMessage() {
    const input = document.getElementById("input");
    const text = input.value;

    if (!text) return;

    const tempId = "temp-" + (++messageCounter);

    ws.send(JSON.stringify({ message: text }));

    addMessage(text, "user", new Date().toISOString(), tempId);

    input.value = "";
}

/* UPDATE STATUS */
function updateMessageStatus(id, status) {
    const msgs = document.querySelectorAll(".message");

    msgs.forEach(msg => {
        if (msg.dataset.id === id) {
            const statusEl = msg.querySelector(".status");

            if (statusEl) {
                statusEl.innerText = status === "delivered" ? "✓✓" : "✓";
            }
        }
    });
}

/* ENTER */
document.getElementById("input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});