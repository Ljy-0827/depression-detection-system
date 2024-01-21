<template>
  <div class="head-container">
    <div class="back-button">
      <i class="bi bi-arrow-left-short" style="font-size: 4em; margin-left: 1.2vw; line-height: 6vh"></i>
      <div class="back-button-text">返回</div>
    </div>
    <div class="step-container">
        <div class="step-box">
          <el-steps :active="0" finish-status="success" align-center>
            <el-step id="result-step" title="文本朗读" />
            <el-step title="结构化访谈" />
            <el-step title="您的结果" />
          </el-steps>
        </div>
    </div>
  </div>
  <div class="page-title">文本朗读</div>
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
  <div class="read-text-container">
    <div class="read-text-instruction" v-if="currentPage === 0">
      当您做好准备时，请点击下方按钮开始朗读
    </div>
    <div class="read-text" v-if="currentPage === 1">
      {{this.readText1}}
    </div>
    <div class="read-text" v-if="currentPage === 2">
      {{this.readText2}}
    </div>
  </div>
  <button class="read-button" v-if="isAllowStart" @click="startReading">开始朗读</button>
  <button class="read-button" v-if="isAllowNextPage" @click="nextPage">下一页</button>
  <button class="read-button" v-if="isAllowStop">结束朗读</button>
</template>

<script>
import { text1, text2 } from "@/utils.js";

export default {
  name: "readingPage",
  data(){
    return{
      readText1: text1,
      readText2: text2,

      isAllowNextPage: false,
      isAllowStop: false,
      isAllowStart: true,

      isCameraOpen: false,
      isMicOpen: true,
      currentPage: 0,
    }
  },
  methods:{
    startReading(){
      this.isAllowStart = false;
      this.isAllowNextPage = true;
      this.isAllowStop = false;
      this.currentPage ++;
    },
    nextPage(){
      this.isAllowStart = false;
      this.isAllowNextPage = false;
      this.isAllowStop = true;
      this.currentPage ++;
    },
  }
}
</script>

<style scoped>
@import "./stylesheets/reading-page.css";
</style>