<template>
  <div class="chat-container">
    <div v-for="(message, index) in messages" :key="index" :class="{'user-message': message.role === 'user', 'assistant-message': message.role === 'assistant'}">
      <div v-html="formatMessage(message.content)"></div>
    </div>
  </div>
</template>

<script>
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // 원하는 하이라이트 스타일

export default {
  props: {
      selectedModel: {
          type: String,
          required: true,
      }
  },
  data() {
      return {
          messages: []
      };
  },
  mounted() {
      this.$nextTick(() => {
          const codeBlocks = this.$el.querySelectorAll('pre code');
          codeBlocks.forEach((block) => {
              hljs.highlightBlock(block);
          });
      });
  },
  methods: {
      async sendMessage(userMessage) {
          if (userMessage.trim() === '') return;

          this.messages.push({ role: 'user', content: userMessage });

          const response = await fetch('http://localhost:8000/chat', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ message: userMessage, model: this.selectedModel }),
          });

          const data = await response.json();
          this.messages.push({ role: 'assistant', content: data.response });
      },
      formatMessage(content) {
          console.log('메시지 포맷 변경');
          console.log(content);

          if (content.trim().includes("```")) {
              console.log('코드 발견');
              const codeBlocks = [];
              const parts = content.split("```");
              console.log(parts.length);

              for (let i = 0; i < parts.length; i++) {
                  if (i % 2 === 1) {
                      const codeContent = parts[i].trim();
                      const [lang, ...codeLines] = codeContent.split('\n');
                      const code = codeLines.join('\n');
                      codeBlocks.push(
                          `<pre><code class="${lang || ''}">${this.escapeHtml(code)}</code></pre>`
                      );
                  } else {
                      codeBlocks.push(parts[i]);
                  }
              }

              console.log(codeBlocks);
              return codeBlocks.join('');
          }
          return content;
      },
      escapeHtml(text) {
          return text
              .replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#039;');
      }
  }
};
</script>

<style>
.chat-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 10px;
}

.user-message {
  text-align: right;
  margin-left: auto;
  background-color: #e0f7fa;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 80%;
}

.assistant-message {
  text-align: left;
  margin-right: auto;
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 80%;
}

pre {
  background-color: #272822;
  color: #f8f8f2;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
  max-width: 100%;
}

code {
  font-family: 'Source Code Pro', monospace;
}
</style>
