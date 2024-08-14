let div = document.querySelector("div");
div.addEventListener("mousemove", (e)=>{
  div.style.background = `radial-gradient(circle at ${e.offsetX}px ${e.offsetY}px, lightgrey 0%, grey 70%)`;
})
div.addEventListener("mouseleave", ()=>{
  div.style = "";
})