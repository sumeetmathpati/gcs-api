var fs = require('fs');
const { convertHtmlToDelta } = require('node-quill-converter');

var obj;
fs.readFile('db/backup/gcs.questions.json', 'utf8', function (err, data) {
  if (err) throw err;
  obj = JSON.parse(data);
  c = 0 
  obj.forEach(element => {
    try {
        let delta = convertHtmlToDelta(element.question);
        jsonString = JSON.stringify(delta);
        // element.delta = jsonString;
        console.log(c)
        c += 1;
        console.log(jsonString);
    }
    catch(e) {
        console.log(e);
    }
    
  });
});
