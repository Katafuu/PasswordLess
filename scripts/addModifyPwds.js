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
	const options = {
		method: 'POST',
		headers: {
				'Authorization':
						getCookieToken()
		},
		body: JSON.stringify({
      site: document.getElementById("site").value,
			email: document.getElementById("email").value,
			username: document.getElementById("username").value,
			password: document.getElementById("password").value
		},)
	}
	fetch("https://passwordless.duckdns.org:8000/creds/addCred",options)
		.then(res => res.json())
		.then(d => {console.log(d)});
	window.location.href = "/"
};

function modifyCred() {
	const options = {
		method: 'PUT',
		headers: {
				'Authorization':
						getCookieToken()
		},
		body: JSON.stringify({
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


addEventListener("DOMContentLoaded", function(event) { // https://sentry.io/answers/how-to-get-values-from-urls-in-javascript

	if (this.window.location.pathname == "addCred.html") {
  	form = this.document.getElementById('addForm')
		form.addEventListener('submit', function(event) {
			event.preventDefault()
			addCred()
		})
	}
  else {
		form = this.document.getElementById("modifyForm")
		const searchParams = new URLSearchParams(window.location.search);
		this.document.getElementById('site').value = searchParams.get('site');
		this.document.getElementById('email').value = searchParams.get('email');
		this.document.getElementById('username').value = searchParams.get('username');
		this.document.getElementById('password').value = searchParams.get('pwd');
		form.addEventListener('submit', function(event) {
			event.preventDefault()
			modifyCred()
		})
    }}
);