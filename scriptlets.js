///my personal scriptlets - not maintained

/// this is from https://github.com/uBlock-user/uBO-Scriptlets/commit/3d1f48573749ac85b20031f78e0d5f7c7bb0f3af#
/// cookie-set.js
/// alias cs.js
// example.com##+js(cs, name, value, age)
(() => {
	console.log("Running...")
		'use strict';
		const cs = ev => {
					if (ev) { window.removeEventListener(ev.type, cs, true); }
					try {
						document.cookie = '{{1}}={{2}}; max-age={{3}}; secure; path=/;';
					} catch { }
	   	};
	   	if (document.readyState === 'loading') {
		    	 window.addEventListener('DOMContentLoaded', cs, true);
	   	} else {
		    	 cs();
	   	}
})();	


/// console-log.js
/// alias clog.js
// example.com##+js(clog, data)
(() => {
        'use strict';
console.log("{{1}}")
})();


/// unload-diffuser.js
/// alias noul.js
/// example.com##+js(unload-diffuser)
(() => {
        'use strict';
window.onbeforeunload = null
	try{
		Object.defineProperity(window,"onbeforeunload",{value:null,writable:false})
	}
	catch(err){
		console.log(err)
	}
})();


/// redirect-to-localhost.js
/// alias redirectlocal.js
/// example.com##+js(redirectlocal)
(() => {
        'use strict';
	try{
		window.stop()
	}
	catch(err){
	}
location.href = "http://localhost"
})();

/// throw-if.js
/// alias towif.js
/// example.com##+js(throw-if,badfunc,badvalue)
/*(() => {
        'use strict';
	var funcName = "{{1}}"
	var arg = "{{2}}"
console.log(funcName)
	var func = window[funcName]
 window[funcName] = function(fArg){
	if(fArg === arg){
		throw new Error(Math.round(Math.random()*9000000))
	}
	else{
		window.setTimeout(func,0,fArg)
	}
}
})();*/

///https://github.com/NanoAdblocker/NanoFilters/blob/master/NanoFilters/NanoResources.txt#L307
/// click-element.js
/// alias clickelm.js
/// example.com##+js(clickelem,#badbutton)
(() => {
var selector = '{{1}}';
    if ( selector === '' || selector === '{{1}}' ) {
        return;
    }
    var click = function() {
        var elements = document.querySelectorAll(selector);
        for ( var element of elements ) {
            element.click();
        }
    };
    if ( document.readyState === 'complete' ) {
        click();
    } else {
        addEventListener('load', click);
    }
})();



/// derstandard-cookie-defuse.js
/// alias derstandard-c.js
/// derstandard.de##+js(derstandard-cookie-defuse)
(() => {
var selector = '{{1}}';
    var click = function() {
        var frame = document.getElementById("sp_message_iframe_485649").src
	var u = new URL(frame)
	u.searchParams.forEach(function(value,name){
		document.cookie = name + "=" + value
	})
    };
    if ( document.readyState === 'complete' ) {
        click();
    } else {
        addEventListener('load', click);
    }
})();

