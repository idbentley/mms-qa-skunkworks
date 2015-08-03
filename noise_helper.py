import time

def insert_some(mongo_coll):
	mongo_coll.insert([
	  {
	    "index": 0,
	    "guid": "b8c40b0b-28a7-47f5-bff1-e6a398294694",
	    "isActive": False,
	    "balance": "$1,859.38",
	    "picture": "http://placehold.it/32x32",
	    "age": 32,
	    "eyeColor": "brown",
	    "name": "Massey Bartlett",
	    "gender": "male",
	    "company": "SUPREMIA",
	    "email": "masseybartlett@supremia.com",
	    "phone": "+1 (951) 456-2622",
	    "address": "388 Mill Street, Derwood, Georgia, 836",
	    "about": "Esse sit id nostrud eiusmod nostrud qui minim cupidatat. Nisi amet est esse velit voluptate laborum dolor reprehenderit Lorem ex anim officia. Minim ex minim duis incididunt aute culpa minim mollit consequat proident tempor irure enim et.\r\n",
	    "registered": "2014-03-25T10:19:20 +04:00",
	    "latitude": -12.696955,
	    "longitude": 145.686536,
	    "tags": [
	      "esse",
	      "culpa",
	      "ea",
	      "dolore",
	      "duis",
	      "do",
	      "fugiat"
	    ],
	    "friends": [
	      {
		"id": 0,
		"name": "Chavez Hays"
	      },
	      {
		"id": 1,
		"name": "Isabelle Cochran"
	      },
	      {
		"id": 2,
		"name": "Leah Riley"
	      }
	    ],
	    "greeting": "Hello, Massey Bartlett! You have 7 unread messages.",
	    "favoriteFruit": "apple"
	  },
	  {
	    "index": 1,
	    "guid": "9ca15d2c-2604-4818-8168-e82d1edfdf88",
	    "isActive": True,
	    "balance": "$1,658.14",
	    "picture": "http://placehold.it/32x32",
	    "age": 35,
	    "eyeColor": "brown",
	    "name": "Manning Yang",
	    "gender": "male",
	    "company": "COWTOWN",
	    "email": "manningyang@cowtown.com",
	    "phone": "+1 (906) 562-2334",
	    "address": "265 Rogers Avenue, Tyhee, Maine, 1616",
	    "about": "Aute anim nulla culpa est. Ex qui consequat consequat voluptate reprehenderit sunt enim incididunt ullamco reprehenderit. Ex do occaecat minim nisi ea eu mollit eiusmod ad cillum. Occaecat aliquip ex non esse consequat ut adipisicing aliquip. Cupidatat ex ullamco mollit eiusmod duis nisi officia mollit Lorem et et irure laboris. Labore voluptate eu tempor enim ad. Magna aute esse id sint nostrud excepteur proident enim ad anim magna.\r\n",
	    "registered": "2014-05-12T18:46:27 +04:00",
	    "latitude": -70.167698,
	    "longitude": 163.39374,
	    "tags": [
	      "laboris",
	      "qui",
	      "minim",
	      "pariatur",
	      "aliquip",
	      "aliquip",
	      "irure"
	    ],
	    "friends": [
	      {
		"id": 0,
		"name": "Schmidt Brock"
	      },
	      {
		"id": 1,
		"name": "Beatriz Richard"
	      },
	      {
		"id": 2,
		"name": "Jenifer Phelps"
	      }
	    ],
	    "greeting": "Hello, Manning Yang! You have 4 unread messages.",
	    "favoriteFruit": "apple"
	  },
	  {
	    "index": 2,
	    "guid": "547e42d9-52b8-435f-85c8-e9c627212da7",
	    "isActive": True,
	    "balance": "$2,081.29",
	    "picture": "http://placehold.it/32x32",
	    "age": 36,
	    "eyeColor": "blue",
	    "name": "Jenny Pope",
	    "gender": "female",
	    "company": "APEXTRI",
	    "email": "jennypope@apextri.com",
	    "phone": "+1 (962) 523-3936",
	    "address": "451 Fulton Street, Riegelwood, South Carolina, 7450",
	    "about": "Ut voluptate sunt cupidatat quis laborum. Velit laborum minim quis irure Lorem aliquip sint culpa ex nostrud do. Eu dolor consequat dolor deserunt laboris est. Anim do enim pariatur qui proident non duis veniam dolore. Officia mollit duis duis excepteur proident qui nostrud incididunt exercitation proident tempor esse. Officia irure quis fugiat occaecat do excepteur irure cupidatat dolore dolore aliqua deserunt cupidatat sunt. Reprehenderit nostrud non ex consectetur adipisicing nisi mollit adipisicing culpa sunt aliquip culpa aliquip.\r\n",
	    "registered": "2014-07-11T08:25:54 +04:00",
	    "latitude": 51.262842,
	    "longitude": 107.047594,
	    "tags": [
	      "et",
	      "consequat",
	      "nisi",
	      "cillum",
	      "id",
	      "esse",
	      "occaecat"
	    ],
	    "friends": [
	      {
		"id": 0,
		"name": "Patrick Shaffer"
	      },
	      {
		"id": 1,
		"name": "Nannie Kent"
	      },
	      {
		"id": 2,
		"name": "Cole Frank"
	      }
	    ],
	    "greeting": "Hello, Jenny Pope! You have 2 unread messages.",
	    "favoriteFruit": "apple"
	  },
	  {
	    "index": 3,
	    "guid": "ac972408-28bd-46ba-a960-b07c97a0db81",
	    "isActive": False,
	    "balance": "$3,895.78",
	    "picture": "http://placehold.it/32x32",
	    "age": 23,
	    "eyeColor": "blue",
	    "name": "Rojas Oliver",
	    "gender": "male",
	    "company": "DYNO",
	    "email": "rojasoliver@dyno.com",
	    "phone": "+1 (848) 538-2538",
	    "address": "366 Heyward Street, Osage, Wyoming, 432",
	    "about": "Id reprehenderit culpa velit irure sit. Excepteur enim adipisicing adipisicing deserunt proident sint exercitation occaecat id. Reprehenderit est consectetur aute reprehenderit. Sint deserunt non qui adipisicing magna dolor sunt deserunt aliquip ut do amet.\r\n",
	    "registered": "2014-01-23T01:29:13 +05:00",
	    "latitude": -29.107163,
	    "longitude": 17.626497,
	    "tags": [
	      "officia",
	      "id",
	      "deserunt",
	      "nisi",
	      "ut",
	      "anim",
	      "dolore"
	    ],
	    "friends": [
	      {
		"id": 0,
		"name": "Bass Bailey"
	      },
	      {
		"id": 1,
		"name": "Bernadine Cruz"
	      },
	      {
		"id": 2,
		"name": "Kent Green"
	      }
	    ],
	    "greeting": "Hello, Rojas Oliver! You have 1 unread messages.",
	    "favoriteFruit": "apple"
	  },
	  {
	    "index": 4,
	    "guid": "7be66753-97ee-4b18-97a9-5468b696f9cc",
	    "isActive": True,
	    "balance": "$1,480.85",
	    "picture": "http://placehold.it/32x32",
	    "age": 30,
	    "eyeColor": "green",
	    "name": "Tracie Sloan",
	    "gender": "female",
	    "company": "BRAINCLIP",
	    "email": "traciesloan@brainclip.com",
	    "phone": "+1 (980) 574-3706",
	    "address": "529 Summit Street, Kylertown, Idaho, 8663",
	    "about": "Est nisi ea consequat nostrud laboris mollit id. Aute fugiat aliqua excepteur quis consequat. Occaecat esse eiusmod irure mollit excepteur culpa voluptate incididunt ad pariatur voluptate quis nostrud. Officia tempor non dolor Lorem sint esse reprehenderit proident excepteur laborum anim cupidatat est. Ullamco culpa qui commodo id fugiat sunt.\r\n",
	    "registered": "2014-04-08T18:46:00 +04:00",
	    "latitude": -27.095015,
	    "longitude": -162.225008,
	    "tags": [
	      "laboris",
	      "tempor",
	      "incididunt",
	      "ea",
	      "occaecat",
	      "dolore",
	      "mollit"
	    ],
	    "friends": [
	      {
		"id": 0,
		"name": "Bernice Walter"
	      },
	      {
		"id": 1,
		"name": "Hoover Pacheco"
	      },
	      {
		"id": 2,
		"name": "Castillo Salas"
	      }
	    ],
	    "greeting": "Hello, Tracie Sloan! You have 1 unread messages.",
	    "favoriteFruit": "banana"
	  },
	  {
	    "index": 5,
	    "guid": "60c2499a-65b8-4319-a429-ec9de6474596",
	    "isActive": False,
	    "balance": "$2,067.90",
	    "picture": "http://placehold.it/32x32",
	    "age": 30,
	    "eyeColor": "brown",
	    "name": "Black Crosby",
	    "gender": "male",
	    "company": "ERSUM",
	    "email": "blackcrosby@ersum.com",
	    "phone": "+1 (807) 557-2090",
	    "address": "441 Williams Place, Rockingham, Tennessee, 5918",
	    "about": "Voluptate amet in pariatur reprehenderit esse ullamco nisi commodo est. Duis aliqua duis tempor laborum. Anim ad mollit eiusmod id aute non in reprehenderit Lorem quis officia quis exercitation. Nostrud quis eu nostrud sit adipisicing laborum dolore amet velit do consequat qui eu. Id occaecat proident excepteur est eu qui ad incididunt fugiat aliqua consectetur. Mollit officia id exercitation ex in exercitation in sint ut Lorem ad esse esse.\r\n",
	    "registered": "2014-03-12T08:10:39 +04:00",
	    "latitude": -27.997729,
	    "longitude": -144.341821,
	    "tags": [
	      "laboris",
	      "aliqua",
	      "proident",
	      "anim",
	      "in",
	      "adipisicing",
	      "reprehenderit"
	    ],
	    "friends": [
	      {
		"id": 0,
		"name": "Ida Mccullough"
	      },
	      {
		"id": 1,
		"name": "Letitia Parker"
	      },
	      {
		"id": 2,
		"name": "Nikki Johnston"
	      }
	    ],
	    "greeting": "Hello, Black Crosby! You have 4 unread messages.",
	    "favoriteFruit": "apple"
	  }
	])
	time.sleep(0.005)
