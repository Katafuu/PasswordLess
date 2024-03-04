function getCookieToken() {
	let cookies = document.cookie.split(';');
	for(let i = 0; i < cookies.length; i++) {
	  cookies[i] = cookies[i].split('=')
	};
	for (let x = 0; x < cookies.length; x++){
	  if (cookies[x][0] == 'token') {
		  return cookies[x][1];
	  }
    else {
      return null
    };
	};
};


function addCred() {
	const token = getCookieToken()
	const options = {
		method: 'POST',
		headers: {
			'Content-Type':
				'application/json;charset=utf-8',
			'Authorization':
				'Bearer '+token,
		},
		body: JSON.stringify({
      "site": document.getElementById("site").value,
			"email": document.getElementById("email").value,
			"username": document.getElementById("username").value,
			"password": document.getElementById("password").value
		},)
	};
	fetch("https://passwordless.duckdns.org:8000/creds/addCred",options)
		.then(res => res.json())
		.then(d => {alert(JSON.stringify(d))});
	window.location.href = "/"
};

function modifyCred(id) {
	const token = getCookieToken();
	const options = {
		method: 'PUT',
		headers: {
				'Authorization':
						'Bearer '+token
		},
		body: JSON.stringify({
			credid: id,
      site: document.getElementById("site").value,
			email: document.getElementById("email").value,
			username: document.getElementById("username").value,
			password: document.getElementById("password").value
		},)
	}
	fetch("https://passwordless.duckdns.org:8000/creds/modifyCred",options)
		.then(res => res.json())
		.then(d => {console.log(d)});
	window.location.href = "/"
};


$(document).ready(function () {
	if (window.location.pathname == "/addCred.html") {
  	$("#addForm").submit(function (event) {
			event.preventDefault();
			addCred();
		})
	}
  else {
		console.log(window.location.pathname)
		const searchParams = new URLSearchParams(window.location.search);
		// loads values into DOM
		document.getElementById('site').value = searchParams.get('site');
		document.getElementById('email').value = searchParams.get('email');
		document.getElementById('username').value = searchParams.get('username');
		$("#modifyForm").submit(function (event) {
			event.preventDefault();
			modifyCred(searchParams.get('credid'));
		})
    }}
);