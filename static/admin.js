// static/admin.js

document.addEventListener("DOMContentLoaded", () => {
	// --- DOM要素の取得 ---
	const tea1NameField = document.getElementById("tea1-name");
	const tea2NameField = document.getElementById("tea2-name");
	const tea3NameField = document.getElementById("tea3-name");
	const getTeaNamesBtn = document.getElementById("get-tea-names-btn");
	const updateTeaNamesBtn = document.getElementById("update-tea-names-btn");
	const teaNamesMessageDiv = document.getElementById("tea-names-message");

	const pandaPersonalityInstructionField = document.getElementById(
		"panda-personality-instruction",
	);
	const getPersonalityBtn = document.getElementById("get-personality-btn");
	const updatePersonalityBtn = document.getElementById(
		"update-personality-btn",
	);

	const personalityMessageDiv = document.getElementById("personality-message");

	// --- ヘルパー関数 ---

	/**
     * メッセージを表示する関数
     * @param {HTMLElement} element - メッセージを表示するDOM要素

     * @param {string} message - 表示するメッセージテキスト
     * @param {boolean} isSuccess - 成功メッセージならtrue, エラーメッセージならfalse
     */
	function displayMessage(element, message, isSuccess) {
		element.textContent = message;
		element.classList.remove("success", "error"); // 既存のクラスを削除
		element.classList.add(isSuccess ? "success" : "error"); // 新しいクラスを追加
		setTimeout(() => {
			element.textContent = "";
			element.classList.remove("success", "error");
		}, 5000); // 5秒後に消去
	}

	/**
	 * API呼び出しを行う汎用関数
	 * @param {string} url - APIエンドポイントのURL
	 * @param {string} method - HTTPメソッド ('GET' or 'POST')
	 * @param {object} [body=null] - POSTリクエストのボディデータ
	 * @returns {Promise<object>} - APIレスポンスのJSONデータ
	 */

	async function callApi(url, method, body = null) {
		const options = {
			method: method,
			headers: { "Content-Type": "application/json" },
		};
		if (body) {
			options.body = JSON.stringify(body);
		}

		const response = await fetch(url, options);

		if (!response.ok) {
			// エラーレスポンスを解析して詳細なエラーメッセージを取得

			let errorDetail = `Status: ${response.status}`;
			try {
				const errorJson = await response.json();
				errorDetail += `, Detail: ${JSON.stringify(errorJson)}`;
			} catch {
				errorDetail += `, Body: ${await response.text()}`;
			}
			throw new Error(`API呼び出しに失敗しました: ${errorDetail}`);
		}
		return response.json();
	}

	// --- 茶葉名設定機能 ---

	// 現在の茶葉名を取得
	getTeaNamesBtn.addEventListener("click", async () => {
		try {
			const data = await callApi("/api/admin/get_tea_types", "GET");
			tea1NameField.value = data.TEA1;
			tea2NameField.value = data.TEA2;
			tea3NameField.value = data.TEA3;
			displayMessage(teaNamesMessageDiv, "現在の茶葉名を取得しました。", true);
		} catch (error) {
			console.error("Error fetching tea names:", error);
			displayMessage(teaNamesMessageDiv, error.message, false);
		}
	});

	// 茶葉名を更新

	updateTeaNamesBtn.addEventListener("click", async () => {
		const teaNamesToUpdate = {};
		if (tea1NameField.value.trim())
			teaNamesToUpdate.TEA1 = tea1NameField.value.trim();
		if (tea2NameField.value.trim())
			teaNamesToUpdate.TEA2 = tea2NameField.value.trim();
		if (tea3NameField.value.trim())
			teaNamesToUpdate.TEA3 = tea3NameField.value.trim();

		if (Object.keys(teaNamesToUpdate).length === 0) {
			displayMessage(
				teaNamesMessageDiv,
				"更新する茶葉名を入力してください。",
				false,
			);
			return;
		}

		try {
			const data = await callApi(
				"/api/admin/update_tea_types",
				"POST",
				teaNamesToUpdate,
			);
			displayMessage(
				teaNamesMessageDiv,
				"茶葉名が正常に更新されました！",
				true,
			);
			console.log("Updated tea names:", data);
			// 更新後、再度取得してUIを確実に同期させる
			getTeaNamesBtn.click();
		} catch (error) {
			console.error("Error updating tea names:", error);
			displayMessage(teaNamesMessageDiv, error.message, false);
		}
	});

	// --- パンダ店主の性格設定機能 ---

	// 現在の性格を取得
	getPersonalityBtn.addEventListener("click", async () => {
		try {
			const data = await callApi(
				"/api/conversation/admin/panda_personality",
				"GET",
			);
			pandaPersonalityInstructionField.value = data.base_instruction;
			displayMessage(personalityMessageDiv, "現在の性格を取得しました。", true);
		} catch (error) {
			console.error("Error fetching panda personality:", error);

			displayMessage(personalityMessageDiv, error.message, false);
		}
	});

	// 性格を更新
	updatePersonalityBtn.addEventListener("click", async () => {
		const instruction = pandaPersonalityInstructionField.value.trim();
		if (!instruction) {
			displayMessage(
				personalityMessageDiv,
				"性格（指示）を入力してください。",
				false,
			);
			return;
		}

		try {
			const data = await callApi(
				"/api/conversation/admin/panda_personality",
				"POST",
				{ base_instruction: instruction },
			);
			displayMessage(
				personalityMessageDiv,
				"パンダ店主の性格が正常に更新されました！",
				true,
			);
			console.log("Updated panda personality:", data);

			// 更新後、再度取得してUIを確実に同期させる
			getPersonalityBtn.click();
		} catch (error) {
			console.error("Error updating panda personality:", error);
			displayMessage(personalityMessageDiv, error.message, false);
		}
	});

	// --- 初期ロード時に現在の設定を表示 ---
	getTeaNamesBtn.click(); // ページロード時に茶葉名を取得
	getPersonalityBtn.click(); // ページロード時に性格を取得
});
