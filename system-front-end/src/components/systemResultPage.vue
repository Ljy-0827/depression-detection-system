<template>
  <div style="background-color: #EEF6F2; width: 100vw; height: 100vh;">
    <div class="title">
      您的测试结果
    </div>
    <div class="result-box">
      <div class="top-result-box">
        <div class="top-result-text-box">
          <div class="top-result-instruction-small">
            您的测试结果为：
          </div>
          <div class="top-result-instruction">
            {{ this.depressionInstruction }}
          </div>
        </div>
        <div class="top-result-warning" v-if="isDoctor">
          <i class="bi bi-info-circle" style="margin-right: 1vw;"></i>
          建议就医
        </div>
      </div>
      <div class="bottom-result-box">
        <div class="score-tool-box">
          <div class="score">
            <div class="score-instruction-small">
              测试分数
            </div>
            <div class="score-instruction">
              {{ this.score }}/27
            </div>
          </div>
          <button class="print-button">
            打印结果
          </button>
        </div>
        <div class="result-graph-box">
          <img src="../assets/example-graph.png">
        </div>
      </div>
    </div>
    <div class="description-box">
      <div class="main-description">
        <ul>
          <li>您的分数处于{{ this.section }}区间，指示您{{ this.depressionInstruction }}。</li>
          <li>{{ this.recommendation }}</li>
        </ul>
      </div>
      <div class="second-description">
        一般来说，抑郁症不是一种患者可以自行治疗的疾病。但是，自助方案也能带来很大的帮助。除了谨遵医嘱坚持专业治疗外，您也可以参考我们提供的自助调节方法介绍，通过亲戚好友的帮助、自我生活习惯的调节等方式使症状得以缓解。
      </div>
      <div class="description-tool-box">
        <div class="description-illustration">
          <img src="../assets/system-result-illustration.png">
        </div>
        <div class="description-button-group">
          <button class="description-button-pri" @click="backToLandingPage">重新参与测试</button>
          <button class="description-button">详细结果发至邮箱</button>
          <button class="description-button">抑郁症知识普及</button>
        </div>
      </div>
    </div>
    <div class="foot-container">
      <div class="footer-top">
        <div class="logo-wrapper">
          <img src="../assets/sigs-logo.png">
        </div>
        <div class="lab-wrapper">实验室名称占位符占位符 | 实验室名称占位符占位符 | 中心机构名称占位符占位符</div>
      </div>
      <div class="footer-bottom">
        心理援助热线：400-995-995-9
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "systemResultPage",
  data(){
    return{
      score: -1,
      depressionDegree: '',
      depressionInstruction: '',
      recommendation: '',
      section: '',
      isDoctor: false,
    }
  },
  mounted() {
    this.score = this.$route.query.score;
    //this.score = 5;
    this.calculateInstruction();
  },
  methods:{
    backToLandingPage(){
      this.$router.push('/');
    },
    calculateInstruction(){
      if(this.score >= 0 && this.score <= 4){
        this.section = '0-4'
        this.isDoctor = false
        this.recommendation = '建议您经常监控自己的状态，可能无需治疗。'
      }else if(this.score >= 5 && this.score <= 9){
        this.depressionDegree = '轻度抑郁'
        this.section = '5-9'
        this.isDoctor = true
        this.recommendation = '需根据临床诊断（症状时间和功能损害等）确定治疗的必要性。'
      }else if(this.score >= 10 && this.score <= 14){
        this.depressionDegree = '中度抑郁'
        this.section = '10-14'
        this.isDoctor = true
        this.recommendation = '需根据临床诊断（症状时间和功能损害等）确定治疗的必要性。'
      }else if(this.score >= 15 && this.score <= 19){
        this.depressionDegree = '中重度抑郁'
        this.section = '15-19'
        this.isDoctor = true
        this.recommendation = '建议您及时就医，并且需要保证积极的心理、药物或联合治疗。'
      }else if(this.score >= 20 && this.score <= 27){
        this.depressionDegree = '重度抑郁'
        this.section = '20-27'
        this.isDoctor = true
        this.recommendation = '建议您及时就医，并且需要保证积极的心理、药物或联合治疗。'
      }

      if(this.score >= 0 && this.score <= 4){
        this.depressionInstruction = '无抑郁倾向'
      }else{
        this.depressionInstruction = '可能患有' + this.depressionDegree
      }
    },
  }
}
</script>

<style scoped>
@import "./stylesheets/system-result-page.css";
</style>