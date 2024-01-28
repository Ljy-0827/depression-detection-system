<template>
  <div class="head-container">
    <div class="back-button" @click="backToLandingPage">
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
    <div class="media-box">
      <div class="media-instruction" v-if="!isCameraOpen" style="margin-top: 2.85vh">音视频将在{{this.countdown}}秒后</div>
      <div class="media-instruction" v-if="!isCameraOpen">自动尝试开启</div>
      <video ref="videoElement" autoplay class="camera" v-if="isCameraOpen || isTryOpenCamera" muted></video>
    </div>
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
  <button class="read-button" v-if="isAllowStop" @click="stopRecording">结束朗读</button>
</template>

<script>
import { text1, text2, ipAddress, protocolMode } from "@/utils.js";
import { ElMessage } from "element-plus";

export default {
  name: "readingPage",
  data(){
    return{
      countdown: 3,
      timer: null,

      readText1: text1,
      readText2: text2,

      isAllowNextPage: false,
      isAllowStop: false,
      isAllowStart: true,
      currentPage: 0,

      isTryOpenCamera: false,
      isCameraOpen: false,
      isMicOpen: false,
      isRecording: false,
      isUploading: false,

      mediaStream: null,
      mediaRecorder: null,
      chunks: [],
    }
  },

  mounted() {
    this.startCountdown();
  },

  methods:{
    backToLandingPage(){
      this.$router.push('/');
    },
    nextDetection(){
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
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
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


    startReading(){
      this.isAllowStart = false;
      this.isAllowNextPage = true;
      this.isAllowStop = false;
      this.currentPage ++;
      this.startRecording();
    },

    nextPage(){
      this.isAllowStart = false;
      this.isAllowNextPage = false;
      this.isAllowStop = true;
      this.currentPage ++;
    },

    startRecording() {
      this.isRecording = true;

      this.mediaRecorder = new MediaRecorder(this.mediaStream);
      this.chunks = [];

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.chunks.push(event.data);
        }
      };

      this.mediaRecorder.start();
    },

    stopRecording() {
      this.isRecording = false;
      //this.isCameraOpen = false;
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop();
        this.mediaStream.getTracks().forEach((track) => track.stop());
        this.$refs.videoElement.srcObject = null;
      }

      setTimeout(this.postMediaToBackend, 1000);
    },

    async postMediaToBackend() {
      this.isUploading = true;
      console.log(this.chunks.length);
      if (this.chunks.length === 0) {
        console.log('录制数据为空，无法发送至后端');
        ElMessage.error('录制数据为空，上传失败');
        this.isUploading = false;
        return;
      }

      try {
        const blob = new Blob(this.chunks, {type: 'video/webm'});

        const fileSizeInBytes = blob.size;
        //const fileSizeInMB = fileSizeInBytes / (1024 * 1024);
        //console.log(`视频文件大小: ${fileSizeInMB} MB`);

        const formData = new FormData();
        formData.append('video', blob, 'reading.webm');
        formData.append('fileSize', fileSizeInBytes);

        // 使用fetch API将数据POST到后端
        const response = await fetch(`${protocolMode}://${ipAddress}/upload-video`, {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
          console.log('视频上传成功！');
          ElMessage({
            message: '视频已成功上传',
            type: 'success',
          });
          this.isUploading = false;
          this.$router.push('/interview');
        } else {
          ElMessage.error('视频上传失败');
          console.error('视频上传失败：', response.statusText);
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('视频上传失败');
        console.error('视频上传出错：', error);
        this.isUploading = false;
      }
    }
  }

}
</script>

<style scoped>
@import "./stylesheets/reading-page.css";
</style>