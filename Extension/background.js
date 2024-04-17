console.log("running")
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse){
    if (request.rq == 'token') {
      console.log("reached")
      chrome.cookies.get({ url: 'https://passwordless.duckdns.org/', name: 'token' },
      function (cookie) {
        if (cookie) {
          console.log(cookie);
          sendResponse({token:cookie.value});
        }
        else {
          console.log('Can\'t get cookie!');
          sendResponse({token:"fail"});
        };
        return true;
      });
    }
  }
)