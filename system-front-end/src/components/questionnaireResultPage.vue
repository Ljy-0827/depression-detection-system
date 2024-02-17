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
            {{this.mainInstruction}}
          </div>
        </div>
        <div class="top-result-warning" v-if="isDoctor">
          <i class="bi bi-info-circle" style="margin-right: 1vw;"></i>
          建议就医
        </div>
      </div>
      <div class="bottom-result-box">
        <div class="questionnaire-result-box">
          <div class="score-box">
            <div class="score-instruction-small">抑郁评分</div>
            <div class="score-instruction">{{this.depressionScore}}/27</div>
          </div>
          <div class="score-slider-box">
            <el-slider v-model="this.depressionScore" :min="0" max="27" disabled/>
            <div class="slider-instruction-box">
              <div class="slider-instruction-name">PHQ-9</div>
              <div class="slider-instruction-result">{{ this.depressionInstruction }}</div>
            </div>
          </div>
        </div>
        <div class="questionnaire-result-box" style="margin-top: 2vh">
          <div class="score-box">
            <div class="score-instruction-small">焦虑评分</div>
            <div class="score-instruction">{{this.anxietyScore}}/21</div>
          </div>
          <div class="score-slider-box">
            <el-slider v-model="this.anxietyScore" :min="0" max="21" disabled/>
            <div class="slider-instruction-box">
              <div class="slider-instruction-name">GAD-7</div>
              <div class="slider-instruction-result">{{ this.anxietyInstruction }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="description-box">
      <div class="main-description">
        <ul>
          <li>{{ this.recommendation }}</li>
        </ul>
      </div>
      <div class="second-description">
        偶尔感觉沮丧或情绪低落是对应激情况的正常反应，但严重或长期的抑郁和焦虑可能是基础心理健康疾病的征兆。通常采用心理咨询、用药或二者兼之改善这两种疾病的症状。改变生活方式（如改善睡眠习惯、定期运动等）也可能有帮助。如果您患有其中一种疾病，请避免饮酒、抽烟和使用娱乐性药物。
      </div>
      <div class="description-tool-box">
        <div class="description-illustration">
          <img src="../assets/system-result-illustration.png">
        </div>
        <div class="description-button-group">
          <button class="description-button-pri" @click="backToLandingPage">重新参与测试</button>
          <button class="description-button-pri">打印详细结果</button>
          <button class="description-button">详细结果发至邮箱</button>
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
  name: "questionnaireResultPage",
  data(){
    return{
      depressionScore: 0,
      anxietyScore: 0,
      depressionDegree: '',
      anxietyDegree: '',
      depressionInstruction: '',
      anxietyInstruction: '',
      mainInstruction: '',
      recommendation: '',
      isDoctor: false,
    }
  },
  mounted() {
    this.depressionScore = Number(this.$route.query.dScore);
    this.anxietyScore = Number(this.$route.query.aScore);
    this.calculateInstruction();
  },
  methods:{
    calculateInstruction(){
      if(this.depressionScore >= 5 && this.depressionScore <= 9){
        this.depressionDegree = '轻度抑郁'
      }else if(this.depressionScore >= 10 && this.depressionScore <= 14){
        this.depressionDegree = '中度抑郁'
      }else if(this.depressionScore >= 15 && this.depressionScore <= 19){
        this.depressionDegree = '中重度抑郁'
      }else if(this.depressionScore >= 20 && this.depressionScore <= 27){
        this.depressionDegree = '重度抑郁'
      }

      if(this.depressionScore >= 0 && this.depressionScore <= 4){
        this.depressionInstruction = '无抑郁倾向'
      }else{
        this.depressionInstruction = '可能患有' + this.depressionDegree
      }

      if(this.anxietyScore >= 6 && this.anxietyScore <= 9){
        this.anxietyDegree = '轻度焦虑'
      }else if(this.anxietyScore >= 10 && this.anxietyScore <= 14){
        this.anxietyDegree = '中度焦虑'
      }else if(this.anxietyScore >= 15 && this.anxietyScore <= 21) {
        this.anxietyDegree = '重度焦虑'
      }

      if(this.anxietyScore >= 0 && this.anxietyScore <= 5){
        this.anxietyInstruction = '无焦虑倾向'
      }else{
        this.anxietyInstruction = '可能患有' + this.anxietyDegree
      }

      if(this.anxietyScore >= 6 && this.depressionScore >= 5){
        this.mainInstruction = '可能患有' + this.depressionDegree + '及' + this.anxietyDegree
      }else{
        this.mainInstruction = this.depressionInstruction + '，' + this.anxietyInstruction
      }

      if(this.anxietyScore <= 5 && this.depressionScore <= 4){
        this.isDoctor = false
        this.recommendation = '建议您经常监控自己的状态，可能无需治疗。'
      }else if(this.anxietyScore >= 15 || this. depressionScore >= 15){
        this.isDoctor = true
        this.recommendation = '建议您及时就医，并且需要保证积极的心理、药物或联合治疗。'
      }else{
        this.isDoctor = true
        this.recommendation = '需根据临床诊断（症状时间和功能损害等）确定治疗的必要性。'
      }
    },
    backToLandingPage(){
      this.$router.push('/');
    },
  }
}
</script>

<style scoped>
@import "./stylesheets/questionnaire-result-page.css";
</style>