

var q = window.location.href.split("?")[-1];
function setToken(token) {
	const d = new Date();
	d.setTime(d.getTime()+30*1000)  // 30 mins expiry
	document.cookie = "name=token" + ";token="+token + ";expires="+d.toUTCString() + ";path=/";
};
if (q) {
  setToken(q)
  window.location.href = "https://passwordless.duckdns.org/managepwds.html";
}

window.location.href = "https://passwordless.duckdns.org/managepwds.html";

