<template style="background-color: #EEF6F2">
  <div style="background-color: #EEF6F2; width: 100vw; height: 100vh;">
    <div class="head-container">
      <div class="header">
        抑郁症多模态筛查系统
      </div>
      <div class="header-description">
        早期识别抑郁症迹象对于及时干预和治疗至关重要，我们希望通过结合视频、声音等多种模态信息，为用户提供更全面的心理健康关注。
      </div>
    </div>
    <div class="mid-container">
      <div class="input-bar-box">
        <el-input v-model="userID" placeholder="请输入您的测试ID" />
      </div>
      <button class="system-begin-button" @click="startDetection">开始系统检测</button>
      <button class="upload-id-button">确认</button>
    </div>
    <div class="system-process-container">
      <div class="area-header">
        系统多模态筛查流程
      </div>
      <div class="area-content-wrapper">
        <div class="process-box">
          <div class="item-box">
            <div class="item-box-index">
              1
            </div>
            <div class="item-box-content">
              <div class="item-header">
                文本朗读
              </div>
              <div class="item-description">
                请您朗读屏幕上的文段，我们将采集您的音视频数据。
              </div>
            </div>
          </div>
          <div class="item-box" style="margin-top: 2vh">
            <div class="item-box-index">
              2
            </div>
            <div class="item-box-content">
              <div class="item-header">
                访谈
              </div>
              <div class="item-description">
                请您根据屏幕上的问题，简单谈谈您的经历与感受。
              </div>
            </div>
          </div>
        </div>
        <div class="illustration">
          <img src="../assets/system-process-illustration-wide.png">
        </div>
      </div>
      <button class="area-button" @click="startDetection">
        开始系统检测
      </button>
    </div>
    <div class="questionnaire-container">
      <div class="area-header">
        快速了解您的心理情况 - PHQ-9及GAD-7量表
      </div>
      <div class="area-column-wrapper">
        <div class="area-column-left">
          量表测评是抑郁症筛查的常用工具，请您根据最近两周的真实情况进行填写，有助于快速、初步地评估症状水平。
        </div>
        <button class="questionnaire-button" @click="startQuestionnaire">参与量表测评</button>
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
  name: "landingPageWide",
  data(){
    return{
      userID: '',
    }
  },
  methods:{
    startDetection(){
      this.$router.push('/read_wide');
    },
    startQuestionnaire(){
      this.$router.push('/questionnaire')
    },
  }
}
</script>

<style scoped>
@import "./stylesheets/landing-page-wide.css";
</style>