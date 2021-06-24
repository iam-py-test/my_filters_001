///my personal scriptlets

/// this is from https://github.com/uBlock-user/uBO-Scriptlets/commit/3d1f48573749ac85b20031f78e0d5f7c7bb0f3af#
/// cookie-set.js
/// alias cs.js
// example.com##+js(cs, name, value, age)
(() => {
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
// example.com##+js(cs, name, value, age)
(() => {
        'use strict';
console.log("{{1}}")
})();
