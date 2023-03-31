const https = require("https");
const readline = require("readline");
const querystring = require("querystring");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

const UID = "u-s4t2ud-a3460dc27a5dc4b8d1fbba961bfab6be66dc7eb02886000ce33e2b4c7976a0f6";
const SECRET = "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";

async function getToken(clientId, clientSecret) {
    return new Promise((resolve, reject) => {
      const postData = querystring.stringify({
        grant_type: "client_credentials",
        client_id: clientId,
        client_secret: clientSecret
      });
  
      const options = {
        hostname: "api.intra.42.fr",
        path: "/oauth/token",
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Content-Length": Buffer.byteLength(postData)
        }
      };
  
      const req = https.request(options, res => {
        res.setEncoding("utf8");
        let rawData = "";
        res.on("data", chunk => {
          rawData += chunk;
        });
        res.on("end", () => {
          try {
            const parsedData = JSON.parse(rawData);
            resolve(parsedData.access_token);
          } catch (error) {
            reject(error);
          }
        });
      });
  
      req.on("error", error => {
        reject(error);
      });
  
      req.write(postData);
      req.end();
    });
  }
  

  
  async function fetchData(url, token, params) {
    return new Promise((resolve, reject) => {
      const queryString = querystring.stringify(params);
      const options = {
        hostname: "api.intra.42.fr",
        path: `${url}?${queryString}`,
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      };
  
      const req = https.request(options, res => {
        res.setEncoding("utf8");
        let rawData = "";
        res.on("data", chunk => {
          rawData += chunk;
        });
        res.on("end", () => {
          try {
            const parsedData = JSON.parse(rawData);
            resolve(parsedData);
          } catch (error) {
            reject(error);
          }
        });
      });
  
      req.on("error", error => {
        reject(error);
      });
  
      req.end();
    });
  }
  
  async function getUsersFromCampus(token, campusId) {
    try {
      const params = {
        campus_id: campusId
      };
      const users = await fetchData("/v2/users", token, params);
      console.log(users);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  }
  
  
  function generatePortfolio() {
    console.log("Generating portfolio...");
    // Implement the portfolio generation logic here
  }
  
  function findUser() {
    console.log("Finding user...");
    // Implement the user search logic here
  }
  
  function menu() {
    console.log("\nChoose an option:");
    console.log("1. Generate Portfolio");
    console.log("2. Find User");
    console.log("0. Leave");
  
    rl.question("Your choice: ", choice => {
      switch (choice) {
        case "1":
          generatePortfolio();
          break;
        case "2":
          findUser();
          break;
        case "0":
          console.log("Goodbye!");
          rl.close();
          return;
        default:
          console.log("Invalid choice. Please try again.");
      }
      menu();
    });
  }
  
  getToken(UID, SECRET)
    .then(token => {
      console.log("Token retrieved successfully.");
      menu();
    })
    .catch(error => {
      console.error("Error getting token:", error);
    });