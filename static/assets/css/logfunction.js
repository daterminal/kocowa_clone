    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    window.addEventListener("beforeunload", function(event){

        var myurl = document.documentURI;

        querystr = 'mutation { weblogCreate(serverDesc: "", urlDesc: "'+myurl+'", userAgent: "", action: "unload" , clientIp: "") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

        var csrftoken = getCookie('csrftoken');

        var grp = window.location.origin+'/graphql'
        var xhr = new XMLHttpRequest();
        xhr.open("POST",grp);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("Accept", "application/json");
        xhr.onload = function () {
          console.log('data returned:', xhr.response);
        }
        xhr.send(JSON.stringify({
            query: querystr,
        }));
        event.returnValue='wr';
    });

    window.onpageshow = function(event) {
        if((window.performance && window.performance.navigation.type == 0)){
            if(!document.referrer){
                //처음 페이지 들어왔을때만
                var req = new XMLHttpRequest();
                req.open('GET', document.location, false);
                req.send(null);

                var data = new Object();

                var headers = req.getAllResponseHeaders().toLowerCase();
                var aHeaders = headers.split('\n');
                var i =0;
                for (i= 0; i < aHeaders.length; i++) {
                    var thisItem = aHeaders[i];
                    var key = thisItem.substring(0, thisItem.indexOf(':'));
                    var value = thisItem.substring(thisItem.indexOf(':')+1);
                    if (key == "server") {
                        server = value;
                    }
                }
                req.abort();
                //ip주소 받기
                var ipurl = window.location.origin+'/get_client_ip/';
                var htr = new XMLHttpRequest();
                htr.open('GET', ipurl,false);
                htr.send(null);
                var myip = htr.response;
                htr.abort();

                myserver = server.slice(1,5); //wsgi
                var useragent = navigator.userAgent;
                var myurl = window.location.href;

                querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'", action: "enter", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'


                const options = {
                  method: "post",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    query: querystr
                  })
                };

                var grp = window.location.origin+'/graphql'
                fetch(grp, options)
                  .then(
                    function(response) {
                      if (response.status !== 200) {
                        console.log('Error : ' + response.status);
                        return;
                      }
                      response.json().then(function(data) {
                        var i;
                        var obj = data.data.weblogCreate.weblog;
                      });
                    }
                  )
                  .catch(function(err) {
                    console.log('Fetch error :-S', err);
                  });
            }else if(document.referrer == 'http://127.0.0.1:8000/accounts/login/'){
                //login후 로딩될 때 로그 떨어뜨리기
                var req = new XMLHttpRequest();
                req.open('GET', document.location, false);
                req.send(null);

                var data = new Object();

                var headers = req.getAllResponseHeaders().toLowerCase();
                var aHeaders = headers.split('\n');
                var i =0;
                for (i= 0; i < aHeaders.length; i++) {
                    var thisItem = aHeaders[i];
                    var key = thisItem.substring(0, thisItem.indexOf(':'));
                    var value = thisItem.substring(thisItem.indexOf(':')+1);
                    if (key == "server") {
                        server = value;
                    }
                }

                req.abort();
                //ip주소 받기
                var ipurl = window.location.origin+'/get_client_ip/';
                var htr = new XMLHttpRequest();
                htr.open('GET', ipurl,false);
                htr.send(null);
                var myip = htr.response;
                htr.abort();

                myserver = server.slice(1,5); //wsgi
                var useragent = navigator.userAgent;
                var myurl = window.location.href;

                querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'", action: "login Home", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

                const options = {
                  method: "post",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    query: querystr
                  })
                };

                var grp = window.location.origin+'/graphql'
                fetch(grp, options)
                  .then(
                    function(response) {
                      if (response.status !== 200) {
                        console.log('Error : ' + response.status);
                        return;
                      }
                      response.json().then(function(data) {
                        var i;
                        var obj = data.data.weblogCreate.weblog;
                      });
                    }
                  )
                  .catch(function(err) {
                    console.log('Fetch error :-S', err);
                  });
            }

        }
        if ((window.performance && window.performance.navigation.type == 1)) {
            // reload 했을 경우
            var req = new XMLHttpRequest();
            req.open('GET', document.location, false);
            req.send(null);

            var data = new Object();

            var headers = req.getAllResponseHeaders().toLowerCase();
            var aHeaders = headers.split('\n');
            var i =0;
            for (i= 0; i < aHeaders.length; i++) {
                var thisItem = aHeaders[i];
                var key = thisItem.substring(0, thisItem.indexOf(':'));
                var value = thisItem.substring(thisItem.indexOf(':')+1);
                if (key == "server") {
                    server = value;
                }
            }
            req.abort();
            //ip주소 받기
            var ipurl = window.location.origin+'/get_client_ip/';
            var htr = new XMLHttpRequest();
            htr.open('GET', ipurl,false);
            htr.send(null);
            var myip = htr.response;
            htr.abort();

            myserver = server.slice(1,5); //wsgi
            var useragent = navigator.userAgent;
            var myurl = window.location.href;

            querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'", action: "reload", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

            const options = {
              method: "post",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                query: querystr
              })
            };

            var grp = window.location.origin+'/graphql'
            fetch(grp, options)
              .then(
                function(response) {
                  if (response.status !== 200) {
                    console.log('Error : ' + response.status);
                    return;
                  }
                  response.json().then(function(data) {
                    var i;
                    var obj = data.data.weblogCreate.weblog;
                  });
                }
              )
              .catch(function(err) {
                console.log('Fetch error :-S', err);
              });
        }
        if ( event.persisted || (window.performance && window.performance.navigation.type == 2)) {
            // Back Forward Cache로 브라우저가 로딩될 경우 혹은 브라우저 뒤로가기 했을 경우
            var req = new XMLHttpRequest();
            req.open('GET', document.location, false);
            req.send(null);

            var data = new Object();

            var headers = req.getAllResponseHeaders().toLowerCase();
            var aHeaders = headers.split('\n');
            var i =0;
            for (i= 0; i < aHeaders.length; i++) {
                var thisItem = aHeaders[i];
                var key = thisItem.substring(0, thisItem.indexOf(':'));
                var value = thisItem.substring(thisItem.indexOf(':')+1);
                if (key == "server") {
                    server = value;
                }
            }
            req.abort();
            //ip주소 받기
            var ipurl = window.location.origin+'/get_client_ip/';
            var htr = new XMLHttpRequest();
            htr.open('GET', ipurl,false);
            htr.send(null);
            var myip = htr.response;
            htr.abort();

            myserver = server.slice(1,5); //wsgi
            var useragent = navigator.userAgent;
            var myurl = window.location.href;

            querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'", action: "historyback", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

            //return false;

            const options = {
              method: "post",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                query: querystr
              })
            };

            var grp = window.location.origin+'/graphql'
            fetch(grp, options)
              .then(
                function(response) {
                  if (response.status !== 200) {
                    console.log('Error : ' + response.status);
                    return;
                  }
                  response.json().then(function(data) {
                    var i;
                    var obj = data.data.weblogCreate.weblog;
                  });
                }
              )
              .catch(function(err) {
                console.log('Fetch error :-S', err);
              });
        }
    }

    function writeLog(menuUrl) {
        //메뉴에서 클릭했을 때 로그 떨어뜨리기
        var req = new XMLHttpRequest();
        var nextUrl = window.location.origin+menuUrl;
        req.open('GET', nextUrl, false);
        req.send(null);

        var data = new Object();

        var headers = req.getAllResponseHeaders().toLowerCase();
        var aHeaders = headers.split('\n');
        var i =0;
        for (i= 0; i < aHeaders.length; i++) {
            var thisItem = aHeaders[i];
            var key = thisItem.substring(0, thisItem.indexOf(':'));
            var value = thisItem.substring(thisItem.indexOf(':')+1);
            if (key == "server") {
                server = value;
            }
        }
        req.abort();
        //ip주소 받기
        var ipurl = window.location.origin+'/get_client_ip/';
        var htr = new XMLHttpRequest();
        htr.open('GET', ipurl,false);
        htr.send(null);
        var myip = htr.response;
        htr.abort();

        myserver = server.slice(1,5); //wsgi
        var useragent = navigator.userAgent;
        var myurl = window.location.origin+menuUrl;

        querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "menuClick/'+this.event.target.text+'", clientIp: "'+myip+'" ) { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

        const options = {
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: querystr
          })
        };

        var grp = window.location.origin+'/graphql'
        fetch(grp, options)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Error : ' + response.status);
                return;
              }
              response.json().then(function(data) {
                var i;
                var obj = data.data.weblogCreate.weblog;
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch error :-S', err);
          });
        req.abort();
        location.href = myurl;
    }
    function writeOutLog(logOutUrl) {
        //로그아웃 했을 때 로그 떨어뜨리기
        var req = new XMLHttpRequest();
        req.open('GET', document.location, false);
        req.send(null);

        var data = new Object();

        var headers = req.getAllResponseHeaders().toLowerCase();
        var aHeaders = headers.split('\n');
        var i =0;
        for (i= 0; i < aHeaders.length; i++) {
            var thisItem = aHeaders[i];
            var key = thisItem.substring(0, thisItem.indexOf(':'));
            var value = thisItem.substring(thisItem.indexOf(':')+1);
            if (key == "server") {
                server = value;
            }
        }
        req.abort();
        //ip주소 받기
        var ipurl = window.location.origin+'/get_client_ip/';
        var htr = new XMLHttpRequest();
        htr.open('GET', ipurl,false);
        htr.send(null);
        var myip = htr.response;
        htr.abort();

        myserver = server.slice(1,5); //wsgi
        var useragent = navigator.userAgent;
        var myurl = window.location.origin+logOutUrl;

        querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "LogOut", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

        const options = {
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: querystr
          })
        };

        var grp = window.location.origin+'/graphql'
        fetch(grp, options)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Error : ' + response.status);
                return;
              }
              response.json().then(function(data) {
                var i;
                var obj = data.data.weblogCreate.weblog;
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch error :-S', err);
          });
        location.href = myurl;
    }
    function writeContentLog(contentUrl) {
        //컨텐츠 클릭했을 때 로그 떨어뜨리기
        var req = new XMLHttpRequest();
        var nextUrl = window.location.origin+contentUrl;
        req.open('GET', nextUrl, false);
        req.send(null);

        var data = new Object();

        var headers = req.getAllResponseHeaders().toLowerCase();
        var aHeaders = headers.split('\n');
        var i =0;
        for (i= 0; i < aHeaders.length; i++) {
            var thisItem = aHeaders[i];
            var key = thisItem.substring(0, thisItem.indexOf(':'));
            var value = thisItem.substring(thisItem.indexOf(':')+1);
            if (key == "server") {
                server = value;
            }
        }
        req.abort();
        //ip주소 받기
        var ipurl = window.location.origin+'/get_client_ip/';
        var htr = new XMLHttpRequest();
        htr.open('GET', ipurl,false);
        htr.send(null);
        var myip = htr.response;
        htr.abort();

        myserver = server.slice(1,5); //wsgi
        var useragent = navigator.userAgent;
        var myurl = nextUrl;

        if(event.target.firstChild){
            //home contents의 메뉴,seeMore를 누르면
            querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "Click/'+this.event.target.firstChild.nodeValue+'", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'
        }else{
            //contents 누르면
            querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "Click/Content", clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'
        }

        const options = {
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: querystr
          })
        };

        var grp = window.location.origin+'/graphql'
        fetch(grp, options)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Error : ' + response.status);
                return;
              }
              response.json().then(function(data) {
                var i;
                var obj = data.data.weblogCreate.weblog;
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch error :-S', err);
          });
        location.href = myurl;
    }
    function writePlayLog(videoKey) {
        //컨텐츠 detail에서 재생버튼 클릭했을 때 로그 떨어뜨리기
        /*var req = new XMLHttpRequest();
        var nextUrl = window.location.origin+playUrl;
        req.open('GET', nextUrl, false);
        req.send(null);

        var data = new Object();

        var headers = req.getAllResponseHeaders().toLowerCase();
        var aHeaders = headers.split('\n');
        var i =0;
        for (i= 0; i < aHeaders.length; i++) {
            var thisItem = aHeaders[i];
            var key = thisItem.substring(0, thisItem.indexOf(':'));
            var value = thisItem.substring(thisItem.indexOf(':')+1);
            if (key == "server") {
                server = value;
            }
        }
        req.abort();
        //ip주소 받기
        var ipurl = window.location.origin+'/get_client_ip/';
        var htr = new XMLHttpRequest();
        htr.open('GET', ipurl,false);
        htr.send(null);
        var myip = htr.response;
        htr.abort();

        myserver = server.slice(1,5); //wsgi
        var useragent = navigator.userAgent;
        var myurl = nextUrl;

        querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "Click/Play",clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

        const options = {
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: querystr
          })
        };

        var grp = window.location.origin+'/graphql'
        fetch(grp, options)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Error : ' + response.status);
                return;
              }
              response.json().then(function(data) {
                var i;
                var obj = data.data.weblogCreate.weblog;
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch error :-S', err);
          });
        location.href = myurl;*/

        var req = new XMLHttpRequest();
        var nextUrl = window.location.origin+videoKey;
        req.open('GET', nextUrl, false);
        req.send(null);

        var data = new Object();

        var headers = req.getAllResponseHeaders().toLowerCase();
        var aHeaders = headers.split('\n');
        var i =0;
        for (i= 0; i < aHeaders.length; i++) {
            var thisItem = aHeaders[i];
            var key = thisItem.substring(0, thisItem.indexOf(':'));
            var value = thisItem.substring(thisItem.indexOf(':')+1);
            if (key == "server") {
                server = value;
            }
        }
        req.abort();
        //ip주소 받기
        var ipurl = window.location.origin+'/get_client_ip/';
        var htr = new XMLHttpRequest();
        htr.open('GET', ipurl,false);
        htr.send(null);
        var myip = htr.response;
        htr.abort();

        myserver = server.slice(1,5); //wsgi
        var useragent = navigator.userAgent;
        var myurl = nextUrl;

        querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "Click/Play",clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

        const options = {
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: querystr
          })
        };

        var grp = window.location.origin+'/graphql'
        fetch(grp, options)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Error : ' + response.status);
                return;
              }
              response.json().then(function(data) {
                var i;
                var obj = data.data.weblogCreate.weblog;
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch error :-S', err);
          });
        location.href = myurl;
    }
    function writeLikeLog(likeUrl) {
        //컨텐츠 detail에서 재생버튼 클릭했을 때 로그 떨어뜨리기
        var req = new XMLHttpRequest();
        var nextUrl = window.location.origin+likeUrl;
        req.open('GET', nextUrl, false);
        req.send(null);

        var data = new Object();

        var headers = req.getAllResponseHeaders().toLowerCase();
        var aHeaders = headers.split('\n');
        var i =0;
        for (i= 0; i < aHeaders.length; i++) {
            var thisItem = aHeaders[i];
            var key = thisItem.substring(0, thisItem.indexOf(':'));
            var value = thisItem.substring(thisItem.indexOf(':')+1);
            if (key == "server") {
                server = value;
            }
        }
        req.abort();
        //ip주소 받기
        var ipurl = window.location.origin+'/get_client_ip/';
        var htr = new XMLHttpRequest();
        htr.open('GET', ipurl,false);
        htr.send(null);
        var myip = htr.response;
        htr.abort();

        myserver = server.slice(1,5); //wsgi
        var useragent = navigator.userAgent;
        var myurl = nextUrl;

        querystr = 'mutation { weblogCreate(serverDesc: "'+myserver+'", urlDesc: "'+myurl+'", userAgent: "'+useragent+'",action: "mykocowa/Content",clientIp: "'+myip+'") { weblog { memberNo serverDesc useragent urlDesc action clientIp logDate } } }'

        const options = {
          method: "post",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            query: querystr
          })
        };

        var grp = window.location.origin+'/graphql'
        fetch(grp, options)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Error : ' + response.status);
                return;
              }
              response.json().then(function(data) {
                var i;
                var obj = data.data.weblogCreate.weblog;
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch error :-S', err);
          });
        location.href = myurl;
    }
