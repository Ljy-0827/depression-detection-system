<template>
  <div style="background-color: #EEF6F2; width: 100vw; height: 100vh;">
    <div class="container">
      <div class="illustration">
        <img src="../assets/blank-page-illustration.png">
      </div>
      <div class="text" style="margin-top: 10vh">
        请稍候
      </div>
      <div class="text">
        系统正在计算您的测试结果
      </div>
    </div>
  </div>
</template>

<script>
import { ipAddress, protocolMode } from "@/utils.js";
export default {
  name: "waitingResultPage",
  data() {
    return {
      intervalId: null,
      resultStatus: false,
      resultScore: -1,
    };
  },
  mounted() {
    // 开始定期检查
    this.intervalId = setInterval(this.checkResultStatus, 2000);
  },
  beforeDestroy() {
    // 在组件销毁前清除定时器
    clearInterval(this.intervalId);
  },
  methods: {
    checkResultStatus() {
      // 发送 GET 请求
      fetch(`${protocolMode}://${ipAddress}/get-result-status`)
          .then(response => response.json())
          .then(data => {
            // 获取 result_status 的值
            this.resultStatus = data.result_status;
            this.resultScore = data.result_score;

            // 如果 result_status 为 true，打印 True
            if (this.resultStatus) {
              console.log('True');
              this.$router.push({name: 'system-result-page', query: {score: this.resultScore}});
            }
          })
          .catch(error => {
            console.error('Error checking result status:', error);
          });
    }
  }
}
</script>

<style scoped>
@import "./stylesheets/waiting-result-page.css";
</style>