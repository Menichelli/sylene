function toggle_visibility(id,button) {
    var e = document.getElementById(id);
    var f = document.getElementById(button);
    if(e.style.display == 'block') {
        e.style.display = 'none';
        f.style.borderRadius = '15px 15px 15px 15px';
    } else {
        e.style.display = 'block';
        f.style.borderRadius = '15px 15px 0px 0px';
    }
}