console.log("running")
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.rq == 'token') {
      chrome.cookies.get({ url: 'https://passwordless.duckdns.org/', name: 'token' },
      function (cookie) {
        if (cookie) {
          console.log(cookie);
          sendResponse(cookie.value)
        }
        else {
          console.log('Can\'t get cookie!');
        }
      });
    }
  }
)