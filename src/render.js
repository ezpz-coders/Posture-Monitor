const path = require("path");
console.log("js loaded");
const { spawn } = require("child_process");
const startBtn = document.getElementById("Start");
const { oks, shell } = require("electron");
const { exec } = require("child_process");
const sadge = document.getElementById("sadge");
startBtn.addEventListener("click", (e) => {
  const fs = require("fs");
  let strictness = document.getElementById("strictness1").value;
  let time = document.getElementById("time1").value;
  data = strictness + " " + time;
  fs.writeFile("Output.txt", data, (err) => {
    if (err) throw err;
  });

  /**
   * Run python myscript, pass in `-u` to not buffer console output
   * @return {ChildProcess}
   */
  function runScript() {
    console.log("spawning python");
    return spawn("python", [
      "-u",
      path.join(__dirname, "../main.py"),
      "--foo",
      "some value for foo",
    ]);
  }

  let threshold = Date.now();
  const subprocess = runScript();
  subprocess.stdout.on("data", (data) => {
    console.log(data);
    const convertedString = data.toString();
    if (convertedString.includes("BAD") && Date.now() > threshold) {
      threshold += Date.now() + 30 * 1000;
      const postureAlert = new Notification(
        "Hey! Your current Posture is not healthy",
        {
          body: "For more information read https://medlineplus.gov/guidetogoodposture.html",
        }
      );
      postureAlert.onclick = function (event) {
        event.preventDefault();
        shell.openExternal("https://medlineplus.gov/guidetogoodposture.html");
      };
    }
    sadge.innerHTML = `Output: ${data}`;
  });
  subprocess.stderr.on("data", (data) => {
    console.log(`error:${data}`);
  });
  subprocess.stderr.on("close", () => {
    console.log("Closed");
  });
});
