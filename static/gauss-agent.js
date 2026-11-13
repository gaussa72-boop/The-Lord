(function () {
  const script = document.currentScript;
  const apiBase = (script && script.dataset.apiBase || "").replace(/\/$/, "");
  if (!apiBase || !/^https:\/\//i.test(apiBase)) return;
  if (document.getElementById("gauss-agent-launcher")) return;
  const button = document.createElement("button");
  button.id = "gauss-agent-launcher";
  button.type = "button";
  button.textContent = "✦ KI-Assistent";
  button.setAttribute("aria-label", "THE LORD KI-Assistent öffnen");
  Object.assign(button.style, {position:"fixed",right:"18px",bottom:"18px",zIndex:"2147483000",padding:"12px 16px",borderRadius:"999px",border:"1px solid #b99b58",background:"#171923",color:"#fff",font:"600 14px system-ui",boxShadow:"0 8px 30px #0008",cursor:"pointer"});
  const panel = document.createElement("section");
  panel.setAttribute("aria-label","THE LORD KI-Assistent");
  Object.assign(panel.style,{display:"none",position:"fixed",right:"18px",bottom:"76px",zIndex:"2147483000",width:"min(360px,calc(100vw - 36px))",padding:"16px",borderRadius:"18px",border:"1px solid #34384a",background:"#11131c",color:"#fff",font:"14px system-ui",boxShadow:"0 12px 40px #000a"});
  panel.innerHTML='<strong>THE LORD · KI-Netzwerk</strong><p style="color:#aeb3c2">Stelle eine Frage an die verbundenen Agenten.</p><textarea aria-label="Deine Nachricht" style="width:100%;min-height:90px;box-sizing:border-box;background:#090b12;color:white;border:1px solid #34384a;border-radius:10px;padding:10px"></textarea><div style="display:flex;gap:8px;margin-top:10px"><button type="button" data-send style="background:#d8b66a;border:0;border-radius:8px;padding:9px 14px">Senden</button><button type="button" data-close style="background:#292d3a;color:white;border:0;border-radius:8px;padding:9px 14px">Schließen</button></div><pre data-result style="white-space:pre-wrap;overflow-wrap:anywhere;max-height:220px;overflow:auto;color:#d9dbea"></pre>';
  document.body.append(button,panel);
  button.addEventListener("click",()=>panel.style.display=panel.style.display==="none"?"block":"none");
  panel.querySelector("[data-close]").addEventListener("click",()=>panel.style.display="none");
  panel.querySelector("[data-send]").addEventListener("click",async()=>{
    const text=panel.querySelector("textarea").value.trim(), out=panel.querySelector("[data-result]");
    if(!text){out.textContent="Bitte gib eine Nachricht ein.";return;}
    out.textContent="Agenten werden angefragt …";
    try{
      const res=await fetch(apiBase+"/api/v1/agents/run",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({goal:text,agents:["quantum-ultra","ionos"]})});
      const data=await res.json();out.textContent=JSON.stringify(data,null,2);
    }catch(e){out.textContent="Der KI-Dienst ist momentan nicht erreichbar.";}
  });
})();