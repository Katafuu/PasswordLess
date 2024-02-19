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
						'application/json'
		},
		body: JSON.stringify({
			email: document.getElementById("signEmail").value,
			username: document.getElementById("signName").value,
			password: document.getElementById("signPassword").value
		},)
	}
	let fetchRes = fetch("http://192.168.0.135:8000/users/addUser",options);
		fetchRes.then(res => res.json())
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
}; 


function testGet() {
	fetch("http://192.168.0.135:8000/")
	.then(data => data.json())
	.then(msg => console.log(msg));
}
$(document).ready(function(){
$("button").click(function(){
	sendSignupData()
});
});