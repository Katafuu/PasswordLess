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
  d.setTime(d.getTime()+30*60*1000)  // 30 mins expiry
  document.cookie = "token="+token + ";expires="+d.toUTCString() + ";path=/";
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
	window.location.href = "https://passwordless.duckdns.org/loginsignup.html?created=True"
};

$(document).ready(function () {
  $("#loginForm").submit(function (event) {
		event.preventDefault();
		const formData = new FormData(document.querySelector("#loginForm"));
		const options = {
			method: 'POST',
			body: formData,
		};
		fetch("https://passwordless.duckdns.org:8000/getToken", options)
		.then(data => data.json())
		.then(function(data) {
			console.log(data)
			setToken(data['access_token']);
			window.location.href = "./"
		})
		})
});
