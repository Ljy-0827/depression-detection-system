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
            可能患有中重度抑郁症
          </div>
        </div>
        <div class="top-result-warning">
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
              16/27
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
          <li>您的分数处于15-19分区间，指示您可能患有：中重度抑郁症。</li>
          <li>建议您及时就医，并且需要保证积极的心理、药物或联合治疗。</li>
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
          <button class="description-button-pri">重新参与测试</button>
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
  name: "systemResultPage"
}
</script>

<style scoped>
@import "./stylesheets/system-result-page.css";
</style>