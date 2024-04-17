console.log("running")
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse){
    switch(request.rq) {
      case 'token':
        console.log("reached")
        chrome.cookies.get({url: 'https://passwordless.duckdns.org/', name: 'token'},
        function (cookie) {
          if (cookie) {
            console.log(cookie);
            const response = {token:cookie.value};
            sendResponse(response);
          }
          else {
            console.log('Can\'t get cookie!');
            sendResponse({token:"fail"});
          };
        });
      case 'autofill_consent':
        chrome.cookies.get({url: 'https://passwordless.duckdns.org/', name: 'autofill_consent'},
        function(cookie) {
          console.log(cookie)
          sendResponse({'consent':cookie.value})
      });
    }
  return true; 
  }
)