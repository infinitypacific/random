document.getElementById("trig").addEventListener("click",()=>{
    document.getElementById("hex").value = processh(document.getElementById("in").value)
    document.getElementById("octal").value = processo(document.getElementById("in").value)
    document.getElementById("binary").value = processb(document.getElementById("in").value)
  })
  
  function processh(s){
    let p = s.split(",");
    let out = [];
    for(let i=0; i<p.length; i++){
      let num = parseInt(p[i]);
      out.push("0x"+num.toString(16).toUpperCase());
    }
    return out.join(",")
  }
  
  function processo(s){
    let p = s.split(",");
    let out = [];
    for(let i=0; i<p.length; i++){
      let num = parseInt(p[i]);
      out.push("0o"+num.toString(8));
    }
    return out.join(",")
  }
  
  function processb(s){
    let p = s.split(",");
    let out = [];
    for(let i=0; i<p.length; i++){
      let num = parseInt(p[i]);
      out.push("0b"+num.toString(2));
    }
    return out.join(",")
  }