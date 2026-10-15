 
    document.addEventListener("DOMContentLoaded", function() {
        const chatFab = document.getElementById("agent-chat-toggle");
        const chatDrawer = document.getElementById("agent-chat-drawer");
        const closeBtn = document.getElementById("agent-drawer-close");
        const sendBtn = document.getElementById("agent-send-btn");
        const userInput = document.getElementById("agent-user-input");
        const messagesContainer = document.getElementById("agent-chat-messages");

        // Open Drawer
        chatFab.addEventListener("click", () => {
            chatDrawer.classList.add("open");
            chatDrawer.setAttribute("aria-hidden", "false");
            userInput.focus();
        });

        // Close Drawer
        closeBtn.addEventListener("click", () => {
            chatDrawer.classList.remove("open");
            chatDrawer.setAttribute("aria-hidden", "true");
        });

        // Async Payload Delivery Dispatcher
        async function sendMessage() {
            const queryText = userInput.value.trim();
            if (!queryText) return;

            appendMessage(queryText, "user-msg");
            userInput.value = "";

            const loadingDiv = appendMessage("Thinking...", "system-msg");

            try {
                const response = await fetch("/api/agent/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: queryText })
                });

                const data = await response.json();
                loadingDiv.remove();

                if (response.ok) {
                    appendMessage(data.response, "system-msg");
                } else {
                    appendMessage(data.error || "Systems disruption encountered.", "system-msg");
                }
            } catch (error) {
                loadingDiv.remove();
                appendMessage("Unable to reach inference engine gateway.", "system-msg");
            }
        }

        function appendMessage(text, className) {
            const msgDiv = document.createElement("div");
            msgDiv.className = `message ${className}`;
            msgDiv.textContent = text;
            messagesContainer.appendChild(msgDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            return msgDiv;
        }

        sendBtn.addEventListener("click", sendMessage);
        userInput.addEventListener("keydown", function(e) {
            if (e.key === "Enter") sendMessage();
        });
    });
    