const path = require('path')
const {spawn} = require('child_process')
const startBtn = document.getElementById('Start')
const {oks}= require('electron');
const { exec } = require('child_process');
const sadge = document.getElementById("sadge");
startBtn.addEventListener('click', (e) => {
   const fs = require('fs')
   let strictness = document.getElementById("strictness1").value;
   let time = document.getElementById("time1").value;
   data=strictness+" "+time;
   fs.writeFile('Output.txt', data, (err) => {
      if (err) throw err;
   })


  /**
     * Run python myscript, pass in `-u` to not buffer console output
     * @return {ChildProcess}
  */
  function runScript(){
  
     
     return spawn('python', [
        "-u",
        path.join(__dirname, '../main.py'),
       "--foo", "some value for foo",
     ]);
  }
  const subprocess = runScript()
  // print output of script
  subprocess.stdout.on('data', (data) => {
     sadge.innerHTML=`data:${data}`;
  });
  subprocess.stderr.on('data', (data) => {
     console.log(`error:${data}`);
  });
  subprocess.stderr.on('close', () => {
     console.log("Closed");
  });
  });