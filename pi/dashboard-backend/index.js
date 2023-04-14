const express = require('express')
const app = express()
const port = 3000
app.use(express.json());

// initial data
let carData = {
    "rpm": 1300,
    "gear": 1,
    "speed": 100,
}

// add middlewear to allow any domain to access the resource
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    next();
  });

app.get('/', (req, res) => {
    res.send('Hello World!')
  })

app.get('/car', (req, res) => {
  res.json(carData)
})

app.post('/car', (req, res) => {
    carData = req.body 
    // console.log("received car data: ", carData)
    res.sendStatus(200);
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})