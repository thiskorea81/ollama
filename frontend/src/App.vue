<template>
  <div id="app">
    <header>
      <h1>AI Chatbot</h1>
      <div class="model-selection">
        <label for="model-select">Select Model:</label>
        <select id="model-select" v-model="selectedModel">
          <option v-for="model in models" :key="model" :value="model">
            {{ model }}
          </option>
        </select>
      </div>
    </header>
    <main>
      <ChatBot ref="chatbot" :selectedModel="selectedModel" />
    </main>
    <footer>
      <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message here..." />
      <button @click="sendMessage">Send</button>
    </footer>
  </div>
</template>

<script>
import ChatBot from '@/components/ChatBot.vue';

export default {
  name: 'App',
  components: {
    ChatBot,
  },
  data() {
    return {
      userInput: '',
      selectedModel: 'llama3.1:8b', // 기본 선택된 모델
      models: ['llama3.2:1b', 'codellama', 'llama3.1:8b'] // 선택 가능한 모델 목록
    };
  },
  methods: {
    sendMessage() {
      const chatbotComponent = this.$refs.chatbot;
      if (chatbotComponent) {
        chatbotComponent.sendMessage(this.userInput);
        this.userInput = '';  // 메시지 전송 후 입력 필드 초기화
      } else {
        console.error("ChatBot component is not found.");
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #42b983;
  padding: 10px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-selection {
  display: flex;
  align-items: center;
}

main {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

footer {
  background-color: #f1f1f1;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  bottom: 0;
}

input {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

select {
  margin-left: 10px;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}
</style>
