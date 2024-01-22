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
    <div class="media-box">
      <div class="media-instruction" v-if="!isCameraOpen" style="margin-top: 2.85vh">音视频将在{{this.countdown}}秒后</div>
      <div class="media-instruction" v-if="!isCameraOpen">自动尝试开启</div>
      <video ref="videoElement" autoplay class="camera" v-if="isCameraOpen || isTryOpenCamera" muted></video>
    </div>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";

export default {
  name: "interviewPage",
  data(){
    return{
      countdown: 3,
      timer: null,

      isTryOpenCamera: false,
      isCameraOpen: false,
      isMicOpen: false,
      isRecording: false,

      mediaStream: null,
      mediaRecorder: null,
      chunks: [],
    }
  },

  mounted() {
    this.startCountdown();
  },

  methods: {
    backToLandingPage() {
      this.$router.push('/');
    },
    nextDetection() {
      this.$router.push('/interview');
    },

    startCountdown() {
      this.countdown = 3;
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(this.timer);  // 清除计时器
          this.openCamera();
        }
      }, 1000);
    },

    async openCamera() {
      try {
        this.isTryOpenCamera = true;
        this.mediaStream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
        this.$refs.videoElement.srcObject = this.mediaStream;
        this.isTryOpenCamera = false;

        const videoTrack = this.mediaStream.getVideoTracks()[0];
        if (videoTrack.enabled) {
          this.isCameraOpen = true;
        }

        const audioTrack = this.mediaStream.getAudioTracks()[0];
        if (audioTrack.enabled) {
          this.isMicOpen = true;
        }

      } catch (error) {
        this.isCameraOpen = false;
        ElMessage.error('无法访问音视频');
        console.error('无法访问音视频', error);
      }
    },
  }
}
</script>

<style scoped>
@import "./stylesheets/interview-page.css";
</style>