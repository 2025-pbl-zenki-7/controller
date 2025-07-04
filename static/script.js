const API_URL = "http://127.0.0.1:8000/api";

let websocket = null;

let isConversationActive = false;

function setUIState(isConversationActive) {
	startConversationButton.disabled = isConversationActive;
	endConversationButton.disabled = !isConversationActive;
	sendInputButton.disabled = !isConversationActive;
	userInputField.disabled = !isConversationActive;
	if (!isConversationActive) {
		userInputField.value = ""; // 会話終了時に入力フィールドをクリア
	}
}

const pandaImage = document.getElementById("panda-image");
const pandaDialogText = document.getElementById("panda-dialog-text");
const messageHistory = document.getElementById("message-history");
const userInputField = document.getElementById("user-input-field");

const startConversationButton = document.getElementById(
	"start-conversation-button",
);
const sendInputButton = document.getElementById("send-input-button");
const endConversationButton = document.getElementById(
	"end-conversation-button",
);

// 管理者用要素
const adminTea1NameField = document.getElementById("admin-tea1-name");
const adminTea2NameField = document.getElementById("admin-tea2-name");
const adminTea3NameField = document.getElementById("admin-tea3-name");
const updateTeaNamesButton = document.getElementById("update-tea-names-button");
const getTeaNamesButton = document.getElementById("get-tea-names-button");
const adminMessageDiv = document.getElementById("admin-message");

const pandaExpressions = {
	neutral: "/static/images/panda_neutral.jpeg",
	smiling: "/static/images/panda_smiling.jpeg",
	surprised: "/static/images/panda_surprised.jpeg",
	thinking: "/static/images/panda_thinking.jpeg",
	anger: "/static/images/panda_angry.jpeg",
	thumbs_up: "/static/images/panda_thumbsup.jpeg",
	clapping: "/static/images/panda_clapping.jpeg",
	uh_huh: "/static/images/panda_uhhuh.jpeg",
};

function updatePandaImage(reactionType) {
	const src = pandaExpressions[reactionType];
	pandaImage.src = src;
}

function updatePandaDialog(text) {
	pandaDialogText.textContent = text;
}

// ---- Web Socket ----

function connectWebSock() {
	const url = `${API_URL}/conversation/communicate`;
	websocket = new WebSocket(url);

	websocket.onopen = (event) => {
		console.log("WebSocket connection opened: ", event);
	};

	websocket.onmessage = (event) => {
		const message = JSON.parse(event.data);
		console.log(message);

		updatePandaDialog(message.text);
		updatePandaImage(message.reaction);

		if (message.status == "finished") {
			console.log("status: finished");
			window.alert(
				`茶葉: ${message.tea_data.type}\n砂糖: ${message.tea_data.sugar}\nミルク: ${message.tea_data.milk}`,
			);
			// websocket.close();
		}
	};

	websocket.onclose = (event) => {
		console.log("WebSocket connection closed: ", event);
		updatePandaImage("neutral");
	};

	websocket.onerror = (event) => {
		console.error("WebSocket error: ", event);
	};
}

startConversationButton.addEventListener("click", async () => {
	console.log("startConversationButton");
	await fetch(`${API_URL}/conversation/start`);
	connectWebSock();
	isConversationActive = !isConversationActive;
	setUIState(isConversationActive);
});

sendInputButton.addEventListener("click", () => {
	const userText = userInputField.value.trim();
	if (userText && websocket && websocket.readyState === WebSocket.OPEN) {
		websocket.send(JSON.stringify({ text: userText }));
		userInputField.value = "";
	}
});

userInputField.addEventListener("keypress", (event) => {
	if (event.key === "Enter") {
		sendInputButton.click();
	}
});
