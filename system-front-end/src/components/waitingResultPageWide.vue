<template>
  <div style="background-color: #EEF6F2; width: 100vw; height: 100vh;">
    <div class="container">
      <div class="illustration">
        <img src="../assets/blank-page-illustration.png">
      </div>
      <div class="text" style="margin-top: 4vh">
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
  name: "waitingResultPageWide",
  data() {
    return {
      id: '',
      intervalId: null,
      resultStatus: false,
      resultScore: -1,
    };
  },
  mounted() {
    this.id = this.$route.query.id;
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
            //console.log(data)
            const userResult = data.results.find(result => result.id === this.id);
            //const userResult = data.find(result => result.id === this.id);
            console.log(userResult)

            // 获取 result_status 的值
            this.resultStatus = userResult.result_status;
            this.resultScore = userResult.result_score;

            // 如果 result_status 为 true，打印 True
            if (this.resultStatus) {
              console.log('True');
              clearInterval(this.intervalId);
              this.$router.push({name: 'system-result-page-wide', query: {score: this.resultScore}});
/*
              fetch(`${protocolMode}://${ipAddress}/trigger-initialize`, {
                method: 'POST',
              })
                  .then(response => response.json())
                  .then(data => {
                    console.log('Initialization triggered:', data.message);
                  })
                  .catch(error => {
                    console.error('Error triggering initialization:', error);
                  });

 */
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
@import "./stylesheets/waiting-result-page-wide.css";
</style>