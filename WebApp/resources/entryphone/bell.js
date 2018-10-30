function animation(element) {
    style_class = "animated"
    var new_el = element.cloneNode(true);
    if(!new_el.classList.contains(style_class)){
	new_el.classList.add(style_class);
    }
    element.parentNode.replaceChild(new_el, element);
    const request_url = window.location.origin + "/api/entryphone?ring=1";
    console.log(request_url);
    const http = new XMLHttpRequest();
    http.open("POST",request_url);
    http.send();

    http.onreadystatechange=(e)=>{
	console.log(http.responseText);
    }   
}
