import fetch from "node-fetch";
import fs from "fs";
import { FACTORIES, GLOBAL_DATA, TOKEN_DAY } from "./queries.js";  

const query = TOKEN_DAY(1647489600)
//console.log( JSON.stringify({query, variables: {}}))

const url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
const res = await fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  body: JSON.stringify({
    query,
    variables: {}
  })
})
const data = await res.json()

//console.log(JSON.stringify(data, null, 2))


var protocol = "Uniswap_Factory"
fs.writeFile(protocol+"_data_js.json", JSON.stringify(data, null, 4), function(err) {
    if (err) throw err;
    console.log('Data Saved Sucessfully');
    }
);