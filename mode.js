function log() {
    var btn = document.getElementById('btn');
    var obj = document.getElementById('myarticle');
    var total_height =  obj.scrollHeight;
    var show_height = 300;
    if(total_height>show_height){
    btn.style.display = 'block';
    }
    btn.onclick = function(){
        obj.style.height = total_height + 'px';
        btn.style.display = "none";
    }
}

output_list = Array();

/* level - 0:Summary; 1:Failed; 2:All */
function showCase(level) {
    trs = document.getElementsByClassName("testclass");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        if(0==level && tr.className.indexOf("active") != -1){
            tr.className = tr.className.replace("active", "").replace("  ", " ").trim();
        }else if (2 == level && tr.className.indexOf("active") == -1){
            tr.className+=" active";
        }else if (1 == level){
            if(tr.className.indexOf("passClass") != -1){
                if(tr.className.indexOf("active") != -1){
                    tr.className = tr.className.replace("active", "").replace("  ", " ").trim();
                }
            }else if (tr.className.indexOf("active") == -1){
                tr.className+=" active";
            }
        }
    }
}

function showClassDetail(element) {
    var currentClassValue = element.className || "";

    if (currentClassValue.indexOf("active") == -1) {
        currentClassValue += " active";
    } else {
        currentClassValue = currentClassValue.replace("active", "").replace("  ", " ");
    }
    element.className = currentClassValue.trim();
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
    
}

function togleClass(element, clas){
        var currentClassValue = element.className || "";

        if (currentClassValue.indexOf(clas) == -1) {
            currentClassValue += " "+clas;
        } else {
            currentClassValue = currentClassValue.replace(clas, "").replace("  ", " ");
        }
        element.className = currentClassValue.trim()
    }

function showRawLog(element){
        togleClass(element, "popup_window")
    }

function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}