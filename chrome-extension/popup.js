// const API_URL = "http://127.0.0.1:8000";
// For deployed backend later, use:
const API_URL = "https://athul93-insighturl-backend.hf.space";

let currentKbId = null;
let currentChatId = null;

// temporary user id for extension
const EXTENSION_USER_ID = "00000000-0000-0000-0000-000000000001";

const urlInput = document.getElementById("urlInput");
const questionInput = document.getElementById("questionInput");
const ingestBtn = document.getElementById("ingestBtn");
const askBtn = document.getElementById("askBtn");
const statusBox = document.getElementById("status");
const answerBox = document.getElementById("answerBox");

function setStatus(message) {
  statusBox.textContent = message;
}

async function getCurrentTabUrl() {
  const tabs = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  if (tabs.length > 0) {
    return tabs[0].url;
  }

  return "";
}

async function loadCurrentUrl() {
  const currentUrl = await getCurrentTabUrl();
  urlInput.value = currentUrl;
}

async function ingestPage() {
  const url = urlInput.value.trim();

  if (!url) {
    setStatus("Please enter a URL.");
    return;
  }

  try {
    setStatus("Ingesting page...");
    answerBox.textContent = "";

    const ingestResponse = await fetch(`${API_URL}/ingest`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        url: url,
        user_id: EXTENSION_USER_ID
      })
    });

    const ingestData = await ingestResponse.json();

    console.log("INGEST DATA:", ingestData);

    if (!ingestData.kb_id) {
      setStatus("Ingestion failed.");
      answerBox.textContent = JSON.stringify(ingestData, null, 2);
      return;
    }

    currentKbId = ingestData.kb_id;

    const chatResponse = await fetch(`${API_URL}/create-chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: EXTENSION_USER_ID,
        kb_id: currentKbId,
        title: url
      })
    });

    const chatData = await chatResponse.json();

    console.log("CHAT DATA:", chatData);

    currentChatId = chatData.id;

    setStatus("Page ingested. You can ask questions now.");
  } catch (error) {
    console.error(error);
    setStatus("Error during ingestion.");
    answerBox.textContent = error.message;
  }
}

async function askQuestion() {
  const question = questionInput.value.trim();

  if (!question) {
    setStatus("Please enter a question.");
    return;
  }

  if (!currentKbId || !currentChatId) {
    setStatus("Please ingest the page first.");
    return;
  }

  try {
    setStatus("Thinking...");
    answerBox.textContent = "";

    const response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question,
        kb_id: currentKbId,
        chat_id: currentChatId
      })
    });

    const data = await response.json();

    console.log("ASK DATA:", data);

    answerBox.textContent = data.answer || "No answer received.";

    setStatus("Answer generated.");
  } catch (error) {
    console.error(error);
    setStatus("Error while asking question.");
    answerBox.textContent = error.message;
  }
}

ingestBtn.addEventListener("click", ingestPage);
askBtn.addEventListener("click", askQuestion);

loadCurrentUrl();