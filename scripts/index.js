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
      return False
    };
	};
};

if (getCookieToken()) {
  location.replace('https://passwordless.duckdns.org/managepwds.html')
}
else {
  location.replace('https://passwordless.duckdns.org/loginsignup.html')
};