const readline = require("readline");
const fs = require("fs");
const https = require("https");

//UID = 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
//SECRET = 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

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let clientId;
let clientSecret;
let maxElements;

const getToken = async () => {
    const postData = JSON.stringify({
      grant_type: "client_credentials",
      client_id: clientId,
      client_secret: clientSecret
    });
  
    const options = {
      hostname: "api.intra.42.fr",
      path: "/oauth/token",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": postData.length
      }
    };
  
    return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
        let data = "";
        res.on("data", chunk => {
          data += chunk;
        });
        res.on("end", () => {
          resolve(JSON.parse(data).access_token);
        });
      });
  
      req.on("error", error => {
        reject(error);
      });
  
      req.write(postData);
      req.end();
    });
  };

  const buildQueryString = (params) => {
    return Object.entries(params)
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
      .join('&');
  };
  
  const fetchData = (url, token, params) => {
    return new Promise((resolve, reject) => {
      const options = {
        headers: { Authorization: `Bearer ${token}` },
        searchParams: new URLSearchParams(params)
      };
  
      const request = https.get(url, options, response => {
        const contentType = response.headers['content-type'];
  
        if (!contentType || !contentType.includes('application/json')) {
          console.error('Error: Received non-JSON response');
          reject(new Error('Received non-JSON response'));
          return;
        }
  
        let data = "";
        response.on("data", chunk => {
          data += chunk;
        });
        response.on("end", () => {
          try {
            resolve(JSON.parse(data));
          } catch (error) {
            console.error("Error parsing response body as JSON:", error);
            resolve({});
          }
        });
      });
      request.on("error", error => {
        reject(error);
      });
    });
  };
  
  
  
  
const main = async () => {
    rl.question("What is your UID? ", uid => {
        clientId = uid;
        rl.question("What is your SECRET? ", secret => {
            clientSecret = secret;
            getToken().then(token => {
                console.log("Generated the token 🔑, now fetching from 42API");

                rl.question("How many elements do you want to see for each page? ", maxElems => {
                    maxElements = parseInt(maxElems) || 5;
                    menu(token);
                });
            });
        });
    });
};

const menu = token => {
    console.clear();
    console.log("1: Fetch Cursus");
    console.log("2: Fetch Projects");
    console.log("0: exit");
    console.log("-----------------");
    rl.question("Choose an option: ", option => {
        switch (parseInt(option)) {
            case 1:
                fetchCursus(token);
                break;
            case 2:
                fetchProjects(token);
                break;
            case 0:
                console.log("Program Terminated");
                rl.close();
                break;
            default:
                console.log("Sorry, that's not a valid option");
                menu(token);
        }
    });
};

const fetchCursus = async token => {
    console.log("You chose to fetch Cursus [Page <= 0 to escape]");
    rl.question("Please input the page you want to see: ", async page => {
        const pageNumber = parseInt(page);
        if (pageNumber > 0) {
            const response = await fetchData("https://api.intra.42.fr/v2/cursus", token, {
                page: { number: pageNumber, size: maxElements }
            });

            console.clear();
            console.log(" #  ID | NAME ");
            console.log("-------|------");
            response.forEach((cursus, index) => {
                console.log(`[${index + 1}] ${cursus.id} | ${cursus.name}`);
            });
            console.log(` --> Page ${pageNumber}, [${response.length} elements]`);

            fetchCursus(token);
        } else {
            menu(token);
        }
    });
};

const fetchProjects = async token => {
    console.log("You chose to fetch Projects [Page <= 0 to escape]");
    rl.question("Please input the id of the cursus for which you want to see the projects: ", cursusId => {
        const id = parseInt(cursusId);
        fetchProjectsByPage(token, id);
    });
}
const fetchProjectsByPage = async (token, cursusId) => {
	rl.question("Please input the page you want to see: ", async page => {
		const pageNumber = parseInt(page);
		if (pageNumber > 0) {
			const response = await fetchData(`https://api.intra.42.fr/v2/cursus/${cursusId}/projects`, token, {
				page: { number: pageNumber, size: maxElements }
			});

			console.clear();
			console.log("Sample data...");
			response.forEach((project, index) => {
				console.log(`[${index + 1}] ${project.id} | ${project.name} | ${project.slug}`);
			});

			console.log("-".repeat(130));
			const fileName = `cursus_${cursusId}_projects_page${pageNumber}.json`;
			console.log(` --> Because this fetch is too big, it generated a file '${fileName}' so you can use some tool to visualize the data`);
			fs.writeFileSync(fileName, JSON.stringify(response, null, 2));
			console.log(` --> ✅ [CREATED] ${fs.realpathSync(fileName)}`);
			console.log(` --> Page ${pageNumber}, [${response.length} elements]`);

			fetchProjectsByPage(token, cursusId);
		} else {
			menu(token);
		}
	});
};

main();