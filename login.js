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
	fetch("http://passwordless.duckdns.org:8000/users/addUser",options)
		.then(res => res.json())
		.then(d => {console.log(d)});
}; 


function sendLoginData() {
	let options = {
		method: 'POST',
		headers: {
				'Content-Type':
						'application/json'
		},
		body: JSON.stringify({
			email: document.getElementById("logEmail").value,
			username: "placeholder to allow send",
			password: document.getElementById("logPassword").value
		},)
	};
	fetch("http://passwordless.duckdns.org/users/loginUser",options)
		.then(res => res.json())
		.then(d => {console.log(d)});
}; 
