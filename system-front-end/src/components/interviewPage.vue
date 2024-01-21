<template>
  <div class="head-container">
    <div class="back-button">
      <i class="bi bi-arrow-left-short" style="font-size: 4em; margin-left: 1.2vw; line-height: 6vh"></i>
      <div class="back-button-text">返回</div>
    </div>
    <div class="step-container">
      <div class="step-box">
        <el-steps :active="1" finish-status="success" align-center>
          <el-step title="文本朗读" />
          <el-step id="result-step" title="结构化访谈" />
          <el-step title="您的结果" />
        </el-steps>
      </div>
    </div>
  </div>
  <div class="page-title">结构化访谈</div>
  <div class="tool-container">
    <div class="left-tool-group">
      <div class="camera-button-open" v-if="isCameraOpen">
        <i class="bi bi-camera-video" style="font-size: 2.4em; line-height: 4vh;"></i>
      </div>
      <div class="camera-button-close" v-if="!isCameraOpen">
        <i class="bi bi-camera-video-off" style="font-size: 2.4em; line-height: 4vh;"></i>
      </div>
      <div class="mic-button-open" v-if="isMicOpen">
        <i class="bi bi-mic" style="font-size: 2.4em; line-height: 4vh;"></i>
      </div>
      <div class="mic-button-close" v-if="!isMicOpen">
        <i class="bi bi-mic-mute" style="font-size: 2.4em; line-height: 4vh;"></i>
      </div>
    </div>
    <div class="tool-text-box">
      <div class="tool-text">请您在确认音视频权限均已打开后，大声朗读屏幕上的两段短文。</div>
    </div>
    <div class="media-box"></div>
  </div>
</template>

<script>
export default {
  name: "interviewPage",
  data(){
    return{
      isCameraOpen: false,
      isMicOpen: true,
    }
  }
}
</script>

<style scoped>
@import "./stylesheets/interview-page.css";
</style>