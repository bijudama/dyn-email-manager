const express = require('express')
const hb = require('handlebars')
const bodyParser = require("body-parser");
const AppConfig = require("./config").Config

// Set up the express app
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// TODO: this shouldn't be a post method, we are not inserting an element here. I had to make it post so that i can send body in the request
app.post('/bars', (req, res) => {
    const template = req.body.template
    const contextData = req.body.data
    const helpers = req.body.helpers
    helpers.forEach(helper => {
        console.log("helper")
        console.log(helper)
        eval(helper)
        const startIndex = helper.indexOf(' ')
        const endIndex = helper.indexOf(' ', startIndex + 1)
        const functionName = helper.substr(startIndex, endIndex - startIndex)
        console.log("functionName")
        console.log(functionName)
        hb.registerHelper(functionName)
    });
    rendered = hb.compile(template)(contextData)
    res.send({ rendered })
});



app.listen(AppConfig.PORT, () => {
    console.log(`server running on port ${AppConfig.PORT}`)
});