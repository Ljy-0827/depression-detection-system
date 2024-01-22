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
      <div class="tool-text">请您在确认音视频权限均已打开后，大声回答下方访谈的问题。</div>
    </div>
    <div class="media-box">
      <div class="media-instruction" v-if="!isCameraOpen" style="margin-top: 2.85vh">音视频将在{{this.countdown}}秒后</div>
      <div class="media-instruction" v-if="!isCameraOpen">自动尝试开启</div>
      <video ref="videoElement" autoplay class="camera" v-if="isCameraOpen || isTryOpenCamera" muted></video>
    </div>
  </div>
  <div class="interview-container">
    <div class="interview-instruction" v-if="!isStartInterview">
      当您做好准备时，请点击下方按钮开始访谈
    </div>
    <div class="interview-media-container">

    </div>
    <div class="question-tool-container" v-for="(item, index) in this.questionAndAnswer" v-show="item.isReadyShow" :key="index">
      <div class="question-text">
        Q{{index + 1}}. {{ item.question }}
      </div>
      <div class="question-util-box">
        <button class="question-big-button" v-if="isAllowStart" @click="startRecording">开始作答</button>
        <button class="question-big-button" v-if="isAllowStop" @click="stopRecording">结束作答</button>
        <button class="question-button" v-if="isAllowRestart" @click="startRecordingAgain">重新录制</button>
        <button class="question-button-pri" v-if="isAllowUpload" @click="moveToNextQuestion">上传作答</button>
        <div class="answer-box" v-show="item.answer !== 0">  <!-- item.answer !== 0 -->
          <div class="answer-mix" disabled="item.status" @click="onClickAudio">
            <i class="bi bi-play-fill" style="margin-right: 12.5vw" v-show="!item.status && !this.isPlaying"></i>
            <i class="bi bi-pause-fill" style="margin-right: 12.5vw" v-show="!item.status && this.isPlaying"></i>
            <i class="bi bi-check" style="margin-right: 12.5vw" v-show="item.status"></i>
            {{item.answer}}''
            <i class="bi bi-soundwave" style="margin-left: 2vw"></i>
          </div>
          <div class="answer-avatar"></div>
        </div>
      </div>

    </div>
  </div>
  <button class="interview-button" v-if="!isStartInterview" @click="startInterview">开始访谈</button>
  <button class="interview-button" v-if="isAllowResult">查看结果</button>
</template>

<script>
import {interview} from "@/utils.js"
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

      isStartInterview: false,
      isAllowResult: false,

      questionAndAnswer:[],
      questionAnswering: 0,

      isAllowStart: true,
      isAllowStop: false,
      isAllowRestart: false,
      isAllowUpload: false,
      isPlaying: false,

      mediaStream: null,

      audioElement: null,
      audioChunks: [],
      audioUrl: null,
      mediaRecorderAudio: null,

      videoChunks: [],
      videoUrl: null,
      mediaRecorderVideo: null,

      recordingStartTime: null,
      tmpSeconds: 0,
    }
  },

  mounted() {
    this.initialQuestionAndAnswer();
    this.startCountdown();
  },

  methods: {
    initialQuestionAndAnswer(){
      for(let i = 0; i < interview.length; i++){
        this.questionAndAnswer.push({question: interview[i], answer: 0, isReadyShow: false})
      }
      console.log(this.questionAndAnswer);
    },

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

    startInterview(){
      this.isAllowStart = true;
      this.isAllowStop = false;
      this.isAllowRestart = false;
      this.isAllowUpload = false;

      this.isStartInterview = true;
      this.questionAndAnswer[0].isReadyShow = true;
    },

    startRecording() {
      this.isAllowStart = false;
      this.isAllowStop = true;
      this.isAllowRestart = false;
      this.isAllowUpload = false;

      navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then((stream) => {
        this.isRecording = true;
        this.audioChunks = [];
        this.videoChunks = [];

        this.mediaRecorderAudio = new MediaRecorder(stream);
        this.mediaRecorderVideo = new MediaRecorder(stream, { mimeType: 'video/webm' });

        this.mediaRecorderAudio.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };

        this.mediaRecorderVideo.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.videoChunks.push(event.data);
          }
        };

        this.mediaRecorderAudio.onstop = () => {
          this.isRecording = false;
          const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
          this.audioUrl = URL.createObjectURL(audioBlob);
        };

        this.mediaRecorderVideo.onstop = () => {
          const videoBlob = new Blob(this.videoChunks, { type: "video/webm" });
          this.videoUrl = URL.createObjectURL(videoBlob);
        };

        this.mediaRecorderAudio.start();
        this.mediaRecorderVideo.start();
        this.recordingStartTime = new Date();
      });
    },

    stopRecording() {
      this.isAllowStart = false;
      this.isAllowStop = false;
      this.isAllowRestart = true;
      this.isAllowUpload = true;

      if (this.mediaRecorderAudio && this.isRecording) {
        this.mediaRecorderAudio.stop();
        this.mediaRecorderVideo.stop();
      }

      if (this.recordingStartTime) {
        const endTime = new Date();
        const seconds = Math.round((endTime - this.recordingStartTime) / 1000);
        this.tmpSeconds = seconds;
      }

      // 处理音频
      const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
      this.audioUrl = URL.createObjectURL(audioBlob);

      // 处理视频
      const videoBlob = new Blob(this.videoChunks, { type: "video/webm" });
      this.videoUrl = URL.createObjectURL(videoBlob);

      this.questionAndAnswer[this.questionAnswering].answer = this.tmpSeconds;
    },

    startRecordingAgain(){
      this.audioChunks = [];
      this.audioUrl = null;
      this.mediaRecorderAudio = null;
      this.mediaRecorderVideo = null;
      this.videoUrl = null;
      this.videoChunks = [];
      this.audioElement = null;
      this.startRecording();
    },

    onClickAudio(){
      if (this.isPlaying) {
        if (this.audioElement && this.isPlaying) {
          this.audioElement.pause();
          this.isPlaying = false;
        }
      } else {
        console.log("status:", this.audioUrl);
        if (this.audioUrl && !this.isPlaying) {
          if (this.audioElement) {
            this.audioElement.pause(); // 先暂停任何正在播放的音频
          }

          this.audioElement = new Audio(this.audioUrl);
          this.audioElement.addEventListener("ended", () => {
            this.isPlaying = false;
          });
          this.audioElement.play();
          this.isPlaying = true;
        }
      }
    },

    moveToNextQuestion(){
      //this.postVideoToBackend();
      this.questionAndAnswer[this.questionAnswering].isReadyShow = false;
      this.questionAndAnswer[this.questionAnswering].status = true;
      this.questionAnswering ++;
      this.questionAndAnswer[this.questionAnswering].isReadyShow = true;
      this.audioChunks = [];
      this.videoChunks = [];
      this.audioUrl = null;
      this.videoUrl = null;
      this.mediaRecorderAudio = null;
      this.mediaRecorderVideo = null;
      this.audioElement = null;
      this.isAllowStart = true;
      this.isAllowStop = false;
      this.isAllowRestart = false;
      this.isAllowUpload = false;
    },
  }
}
</script>

<style scoped>
@import "./stylesheets/interview-page.css";
</style>