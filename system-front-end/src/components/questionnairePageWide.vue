<template>
  <div class="head-container">
    <div class="back-button" @click="backToLandingPage">
      <i class="bi bi-arrow-left-short" style="font-size: 1.6em; margin-left: 1vw; line-height: 6.5vh"></i>
      <div class="back-button-text" @click="backToLandingPage">返回</div>
    </div>
    <div class="step-container">
      <div class="step-box">
        <el-steps :active="0" finish-status="success" align-center>
          <el-step id="result-step" title="量表填写" />
          <el-step title="您的结果" />
        </el-steps>
      </div>
    </div>
  </div>
  <div class="page-title">量表填写</div>
  <div class="tool-container">
    <div class="tool-text-box">
      <div class="tool-text">过去的两周里，您生活中以下症状出现的频率有多少？选择您认为最合适的选项。</div>
    </div>
    <div class="process-box">
      <div class="process-instruction-small">您已填写</div>
      <div class="process-instruction">{{this.answer.length}}/16</div>
    </div>
  </div>
  <div class="main-carousel">
    <el-form :model="questionnaire" label-position="top">
      <el-carousel indicator-position="none" :autoplay="false" arrow="always">
        <el-carousel-item v-for="(item, index) in questionnaire">
          <div class="question-index" :id="'question-index' + index">No.{{index +1}}</div>
          <el-form-item  :label="item.question" required>
            <el-radio-group  v-model="this.answer[index]" style="text-align: left"  :id="'question-option' + index">
              <el-radio v-for="option in item.options" :label="option">
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </el-carousel-item>
      </el-carousel>
    </el-form>
  </div>
  <div class="carousel-bg"></div>
  <button class="submit-button" @click="this.moveToQuestionnaireResult">提交并查看结果</button>
</template>

<script>
import {protocolMode, ipAddress, questionnaire} from "@/utils.js";
import {ElMessage} from "element-plus";

export default {
  name: "questionnairePageWide",
  data(){
    return{
      questionnaire,
      answer:[],
      depressionScore:0,
      anxietyScore:0,
      id:'',
    }
  },
  mounted() {
    this.id = this.$route.query.id;
  },
  methods:{
    backToLandingPage(){
      this.$router.push('/');
    },
    moveToQuestionnaireResult(){
      if(this.answer.length === this.questionnaire.length){
        ElMessage({
          message: '量表填写完成',
          type: 'success',
        });
        this.calculateScore();
        this.$router.push({name: 'questionnaire-result-page-wide', query: {dScore: this.depressionScore, aScore: this.anxietyScore}});
      } else{
        ElMessage.error('请您作答全部题目');
      }
    },
    calculateScore(){
      for(let i = 0; i < 7; i++){
        if(this.answer[i] === '好几天'){
          this.anxietyScore = this.anxietyScore + 1;
        }else if(this.answer[i] === '超过一周'){
          this.anxietyScore = this.anxietyScore + 2;
        }else if(this.answer[i] === '几乎每天') {
          this.anxietyScore = this.anxietyScore + 3;
        }
      }
      for(let i = 7; i < 16; i++){
        if(this.answer[i] === '有几天'){
          this.depressionScore = this.depressionScore + 1;
        }else if(this.answer[i] === '一半以上时间'){
          this.depressionScore = this.depressionScore + 2;
        }else if(this.answer[i] === '几乎天天') {
          this.depressionScore = this.depressionScore + 3;
        }
      }
    }
  }
}
</script>

<style scoped>
@import "./stylesheets/questionnaire-page-wide.css";
</style>