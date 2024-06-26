$(window).on("hashchange", function () {
	if (location.hash.slice(1) == "signup") {
		$(".page").addClass("extend");
		$("#login").removeClass("active");
		$("#signup").addClass("active");
	} else {
		$(".page").removeClass("extend");
		$("#login").addClass("active");
		$("#signup").removeClass("active");
	}
});
$(window).trigger("hashchange");

function setToken(token) {
  const d = new Date();
  d.setTime(d.getTime()+60*60*1000)  // 60 mins expiry
  document.cookie = "token="+token + ";expires="+d.toUTCString() + ";path=/";
};

function getStatus() {
	const searchParams = new URLSearchParams(window.location.search);
  const status = searchParams.get("status");
	const StatusText = document.getElementById('errorMsg');
	if (status == 'SessionTimeOut') {
		StatusText.innerText = "Session Timed Out. Please Login Again";
	}
	else {
		if(status == 'created') {
			StatusText.setAttribute('style','color: green;')
			StatusText.innerText = "Account Successfully Created! Please Login"
		}
	}
};
function sendSignupData() {
	const options = {
		method: 'POST',
		headers: {
				'Content-Type':
						'application/json;charset=utf-8'
		},
		body: JSON.stringify({
			email: document.getElementById("signEmail").value,
			username: document.getElementById("signName").value,
			password: document.getElementById("signPassword").value
		},)
	}
	fetch("https://passwordless.duckdns.org:8000/users/addUser",options)
		.then(res => res.json())
		.then(d => {console.log(d)});
	window.location.href = "https://passwordless.duckdns.org/loginsignup.html?status=created";
	getStatus();
};

$(document).ready(function () {
	getStatus();
  $("#loginForm").submit(function (event) {
		event.preventDefault();
		const formData = new FormData(document.querySelector("#loginForm"));
		const options = {
			method: 'POST',
			body: formData,
		};
		fetch("https://passwordless.duckdns.org:8000/getToken", options)
		.then(function(response) {
			const errordiv = document.getElementById('errorMsg')
			errordiv.innerText = ' ';
			if (response.status==200) {
				return response.json()
			} else {
				if (response.status==401 || response.status==422)
				errordiv.innerText = "Error, invalid username or password. Please try again" 
				throw new Error("Unauthorized")
			};
		})
		.then(function(data) {
			console.log(data)
			setToken(data['access_token']);
			window.location.href = "./"
		})
		})
});
