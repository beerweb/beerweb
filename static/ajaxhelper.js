// we use this function so that we can abstract any support for older
// browsers into the details.
function createXmlHttp() {
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	} else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	if (!(xmlhttp)) {
		alert("Your browser does not support AJAX!");
	}
	return xmlhttp;
}

// use the given xmlHttp object to send the given parameters to the
// target URL.  parameters should be a URL formatted string.
function postParameters(xmlHttp, target, parameters) {
	if (xmlHttp) {
		xmlHttp.open("POST",target,true);
		xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xmlHttp.send(parameters);
	}
}
