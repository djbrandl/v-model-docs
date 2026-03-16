#!/usr/bin/env python3
"""Generate an interactive HTML playground from a discovery report.

Reads a discovery-report JSON file produced by the scan phase, generates a
self-contained HTML questionnaire (no external dependencies), and opens it in
the default browser.  The playground auto-saves to localStorage and can export
a ``discovery-answers.json`` file for import back into the V-model workflow.
"""

import argparse
import json
import os
import sys
import tempfile
import webbrowser


def _load_report(path: str) -> dict:
	"""Load and minimally validate a discovery report JSON file.

	Returns the parsed dict.  Raises SystemExit on I/O or schema errors.
	"""
	if not os.path.isfile(path):
		print(f"ERROR: File not found: {path}", file=sys.stderr)
		sys.exit(1)

	try:
		with open(path, "r", encoding="utf-8") as fh:
			data = json.load(fh)
	except json.JSONDecodeError as exc:
		print(f"ERROR: Invalid JSON in {path}: {exc}", file=sys.stderr)
		sys.exit(1)

	required_keys = {"project_name", "components", "inferred_requirements", "unknowns"}
	missing = required_keys - set(data.keys())
	if missing:
		print(f"ERROR: Discovery report missing keys: {sorted(missing)}", file=sys.stderr)
		sys.exit(1)

	return data


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>V-Model Discovery Playground — {{PROJECT_NAME}}</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f8f9fa;--surface:#fff;--border:#dee2e6;--accent:#2563eb;--accent-light:#dbeafe;
--green:#16a34a;--green-light:#dcfce7;--red:#dc2626;--red-light:#fee2e2;
--text:#1e293b;--text-muted:#64748b;--radius:8px;--shadow:0 1px 3px rgba(0,0,0,.08)}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen,sans-serif;
background:var(--bg);color:var(--text);line-height:1.6;padding:0 0 4rem}
header{background:var(--surface);border-bottom:1px solid var(--border);padding:1.25rem 2rem;position:sticky;top:0;z-index:100}
header h1{font-size:1.25rem;font-weight:600}
header .subtitle{color:var(--text-muted);font-size:.875rem}
.progress-wrap{margin-top:.75rem;display:flex;align-items:center;gap:.75rem}
.progress-bar{flex:1;height:8px;background:var(--border);border-radius:99px;overflow:hidden}
.progress-fill{height:100%;background:var(--accent);border-radius:99px;transition:width .3s}
.progress-label{font-size:.8rem;color:var(--text-muted);min-width:3.5rem;text-align:right}
main{max-width:960px;margin:0 auto;padding:1.5rem 1rem}
.section{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
margin-bottom:1rem;box-shadow:var(--shadow)}
.section-header{display:flex;align-items:center;gap:.5rem;padding:1rem 1.25rem;cursor:pointer;
user-select:none;font-weight:600;font-size:1rem;border-bottom:1px solid transparent}
.section-header:hover{background:var(--accent-light)}
.section-header .chevron{transition:transform .2s;font-size:.75rem;color:var(--text-muted)}
.section-header .chevron.open{transform:rotate(90deg)}
.section-header .check{margin-left:auto;font-size:1rem;color:var(--green);opacity:0;transition:opacity .3s}
.section-header .check.visible{opacity:1}
.section-body{padding:1.25rem;display:none}
.section-body.open{display:block}
label{display:block;font-weight:500;margin-bottom:.25rem;font-size:.875rem}
label .req{color:var(--red);margin-left:2px}
input[type=text],input[type=number],textarea,select{width:100%;padding:.5rem .75rem;
border:1px solid var(--border);border-radius:var(--radius);font:inherit;font-size:.875rem;
background:var(--surface);transition:border-color .15s}
input:focus,textarea:focus,select:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-light)}
textarea{resize:vertical;min-height:60px}
.field{margin-bottom:1rem}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.card{border:1px solid var(--border);border-radius:var(--radius);padding:1rem;margin-bottom:.75rem;background:var(--bg)}
.card h4{font-size:.9rem;margin-bottom:.5rem}
.btn{display:inline-flex;align-items:center;gap:.35rem;padding:.45rem .9rem;border:1px solid var(--border);
border-radius:var(--radius);background:var(--surface);cursor:pointer;font-size:.8rem;font-weight:500;transition:all .15s}
.btn:hover{background:var(--accent-light);border-color:var(--accent)}
.btn-sm{padding:.3rem .6rem;font-size:.75rem}
.btn-primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn-primary:hover{background:#1d4ed8}
.btn-danger{color:var(--red);border-color:var(--red-light)}
.btn-danger:hover{background:var(--red-light)}
.btn-accept{color:var(--green);border-color:var(--green-light)}
.btn-accept:hover{background:var(--green-light)}
.actions{display:flex;gap:.5rem;margin-top:.5rem;flex-wrap:wrap}
.scope-toggle{display:inline-flex;gap:0;margin-top:.35rem}
.scope-toggle button{padding:.3rem .7rem;font-size:.75rem;border:1px solid var(--border);background:var(--surface);
cursor:pointer;font-weight:500;transition:all .15s}
.scope-toggle button:first-child{border-radius:var(--radius) 0 0 var(--radius)}
.scope-toggle button:last-child{border-radius:0 var(--radius) var(--radius) 0}
.scope-toggle button:not(:first-child){border-left:none}
.scope-toggle button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.idk-row{display:flex;align-items:center;gap:.5rem;margin-top:.25rem;font-size:.8rem;color:var(--text-muted)}
.idk-row input[type=checkbox]{width:auto}
.export-bar{position:fixed;bottom:0;left:0;right:0;background:var(--surface);border-top:1px solid var(--border);
padding:.75rem 2rem;display:flex;justify-content:flex-end;gap:.75rem;z-index:100}
table{width:100%;border-collapse:collapse;font-size:.85rem;margin-bottom:.75rem}
th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid var(--border)}
th{background:var(--bg);font-weight:600}
.tag{display:inline-block;padding:.15rem .5rem;border-radius:99px;font-size:.7rem;font-weight:600;background:var(--accent-light);color:var(--accent)}
</style>
</head>
<body>
<header>
<h1>V-Model Discovery Playground</h1>
<p class="subtitle" id="projectSubtitle"></p>
<div class="progress-wrap">
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
<span class="progress-label" id="progressLabel">0%</span>
</div>
</header>
<main id="app"></main>
<div class="export-bar">
<button class="btn" onclick="resetAll()">Reset All</button>
<button class="btn btn-primary" onclick="exportAnswers()">Export discovery-answers.json</button>
</div>

<script>
// --- Discovery data injected by Python ---
const DISCOVERY = {{DISCOVERY_JSON}};

const LS_KEY = "vmodel_playground_" + (DISCOVERY.project_name || "default").replace(/\W+/g,"_");
let STATE = loadState();

function loadState(){
	try{ const s=localStorage.getItem(LS_KEY); if(s) return JSON.parse(s); } catch(e){}
	return {};
}
function save(){ localStorage.setItem(LS_KEY, JSON.stringify(STATE)); updateProgress(); }
function val(key, def){ return STATE[key]!==undefined ? STATE[key] : def; }
function set(key, v){ STATE[key]=v; save(); }

// --- Utility: remove all child nodes from a container ---
function clearNode(node){ while(node.firstChild) node.removeChild(node.firstChild); }

// --- Progress ---
function countCompletion(){
	let total=0, done=0;
	// Section 1: 3 required fields
	["si_description","si_intended_use","si_gamp"].forEach(k=>{ total++; if(val(k,"")) done++; });
	// Section 2: each component needs a scope choice
	(DISCOVERY.components||[]).forEach((_,i)=>{ total++; if(val("scope_"+i,"")) done++; });
	// Section 3: each component confirmed
	(DISCOVERY.components||[]).forEach((_,i)=>{ total++; if(val("comp_confirmed_"+i,false)) done++; });
	// Section 4: each req has accept/reject
	(DISCOVERY.inferred_requirements||[]).forEach((_,i)=>{ total++; if(val("req_status_"+i,"")!=="") done++; });
	// Section 5: each unknown answered or idked
	(DISCOVERY.unknowns||[]).forEach((_,i)=>{ total++; if(val("unk_"+i,"")||val("unk_idk_"+i,false)) done++; });
	// Section 8: each test mapped
	(DISCOVERY.test_coverage||[]).forEach((_,i)=>{ total++; if(val("test_level_"+i,"")) done++; });
	return {total, done};
}
function updateProgress(){
	const {total,done}=countCompletion();
	const pct = total?Math.round(done/total*100):100;
	document.getElementById("progressFill").style.width=pct+"%";
	document.getElementById("progressLabel").textContent=pct+"%";
	// Section checks
	document.querySelectorAll("[data-section-check]").forEach(el=>{
		const fn=window["check_"+el.dataset.sectionCheck];
		if(fn) el.classList.toggle("visible", fn());
	});
}

// --- Section completion checkers ---
window.check_identity=()=> !!(val("si_description","")&&val("si_intended_use","")&&val("si_gamp",""));
window.check_scope=()=> (DISCOVERY.components||[]).every((_,i)=>val("scope_"+i,""));
window.check_components=()=> (DISCOVERY.components||[]).every((_,i)=>val("comp_confirmed_"+i,false));
window.check_requirements=()=> (DISCOVERY.inferred_requirements||[]).every((_,i)=>val("req_status_"+i,""));
window.check_unknowns=()=> (DISCOVERY.unknowns||[]).every((_,i)=>val("unk_"+i,"")||val("unk_idk_"+i,false));
window.check_roles=()=> (val("roles",[])).length>0;
window.check_environment=()=> !!(val("env_topology","")&&val("env_os",""));
window.check_tests=()=> (DISCOVERY.test_coverage||[]).every((_,i)=>val("test_level_"+i,""));
window.check_overrides=()=> true;

// --- Render helpers ---
function h(tag,attrs,...children){
	const el=document.createElement(tag);
	if(attrs) Object.entries(attrs).forEach(([k,v])=>{
		if(k==="className") el.className=v;
		else if(k.startsWith("on")) el.addEventListener(k.slice(2).toLowerCase(),v);
		else el.setAttribute(k,v);
	});
	children.flat().forEach(c=>{ if(c==null)return; el.append(typeof c==="string"?document.createTextNode(c):c); });
	return el;
}

function makeSection(id, title, renderFn){
	const sec=h("div",{className:"section"});
	const chevron=h("span",{className:"chevron"});
	chevron.textContent="\u25B6";
	const check=h("span",{className:"check","data-section-check":id});
	check.textContent="\u2713";
	const hdr=h("div",{className:"section-header",onClick:()=>{
		const body=sec.querySelector(".section-body");
		const open=body.classList.toggle("open");
		chevron.classList.toggle("open",open);
	}}, chevron, " "+title, check);
	const body=h("div",{className:"section-body"});
	renderFn(body);
	sec.append(hdr,body);
	return sec;
}

function inputField(label_, key, opts){
	opts=opts||{};
	const wrap=h("div",{className:"field"});
	const lbl=h("label",null, label_);
	if(opts.required) lbl.append(h("span",{className:"req"},"*"));
	wrap.append(lbl);
	if(opts.type==="textarea"){
		const ta=h("textarea",{rows:String(opts.rows||3)});
		ta.value=val(key,"");
		ta.addEventListener("input",function(){ set(key,ta.value); });
		wrap.append(ta);
	} else if(opts.type==="select"){
		const sel=h("select");
		(opts.options||[]).forEach(function(o){
			var optVal=typeof o==="object"?o.value:o;
			var optLabel=typeof o==="object"?o.label:o;
			var opt=h("option",{value:optVal}, optLabel);
			sel.append(opt);
		});
		sel.value=val(key,opts.default||"");
		sel.addEventListener("change",function(){ set(key,sel.value); });
		wrap.append(sel);
	} else {
		const inp=h("input",{type:opts.type||"text"});
		inp.value=val(key,"");
		inp.addEventListener("input",function(){ set(key,inp.value); });
		wrap.append(inp);
	}
	if(opts.idk){
		var idkKey=key+"_idk";
		var row=h("div",{className:"idk-row"});
		var cb=h("input",{type:"checkbox"});
		cb.checked=val(idkKey,false);
		cb.addEventListener("change",function(){ set(idkKey,cb.checked); });
		row.append(cb, " I don't know");
		wrap.append(row);
	}
	return wrap;
}

// --- Build sections ---
function renderIdentity(body){
	body.append(
		h("div",{className:"field"},
			h("label",null,"Project Name"),
			Object.assign(h("input",{type:"text",disabled:"true"}), {value:DISCOVERY.project_name||""})
		),
		inputField("System Description","si_description",{type:"textarea",required:true,rows:3}),
		inputField("Intended Use","si_intended_use",{type:"textarea",required:true,rows:2}),
		inputField("GAMP Category","si_gamp",{type:"select",required:true,
			options:[{value:"",label:"\u2014 Select \u2014"},{value:"1",label:"1 \u2014 Infrastructure"},{value:"3",label:"3 \u2014 Non-configured"},{value:"4",label:"4 \u2014 Configured"},{value:"5",label:"5 \u2014 Custom"}],
			default:""
		}),
		inputField("Regulatory Context","si_regulatory",{type:"text",idk:true})
	);
}

function renderScope(body){
	clearNode(body);
	var list=h("div");
	(DISCOVERY.components||[]).forEach(function(comp,i){
		var card=h("div",{className:"card"});
		card.append(h("h4",null,comp.name));
		if(comp.description) card.append(h("p",{className:"field",style:"font-size:.85rem;color:var(--text-muted);margin-bottom:.5rem"}, comp.description));
		var toggle=h("div",{className:"scope-toggle"});
		["in-scope","out-of-scope","external"].forEach(function(s){
			var btn=h("button",{onClick:function(){
				set("scope_"+i,s);
				toggle.querySelectorAll("button").forEach(function(b){b.classList.remove("active");});
				btn.classList.add("active");
			}},s);
			if(val("scope_"+i,"")===s) btn.classList.add("active");
			toggle.append(btn);
		});
		card.append(toggle);
		list.append(card);
	});
	var addBtn=h("button",{className:"btn",onClick:function(){
		var name=prompt("Component name:");
		if(!name) return;
		DISCOVERY.components.push({name:name,description:"",inferred_category:"5"});
		renderScope(body);
	}},"+ Add Component");
	body.append(list,addBtn);
}

function renderComponents(body){
	clearNode(body);
	(DISCOVERY.components||[]).forEach(function(comp,i){
		var card=h("div",{className:"card"});
		var confirmed=val("comp_confirmed_"+i,false);
		card.append(h("h4",null,comp.name+" ",h("span",{className:"tag"},"Cat "+comp.inferred_category)));
		card.append(inputField("Description","comp_desc_"+i,{type:"textarea",rows:2}));
		if(!val("comp_desc_"+i,"")) set("comp_desc_"+i, comp.description||"");
		card.querySelector("textarea").value=val("comp_desc_"+i,"");
		card.append(inputField("Criticality","comp_crit_"+i,{type:"select",
			options:[{value:"",label:"\u2014 Select \u2014"},{value:"high",label:"High"},{value:"medium",label:"Medium"},{value:"low",label:"Low"}]
		}));
		card.append(inputField("GAMP Category","comp_gamp_"+i,{type:"select",
			options:[{value:"",label:"\u2014 Select \u2014"},{value:"1",label:"1"},{value:"3",label:"3"},{value:"4",label:"4"},{value:"5",label:"5"}],
			default:comp.inferred_category
		}));
		if(!val("comp_gamp_"+i,"")) set("comp_gamp_"+i, comp.inferred_category);
		var selects=card.querySelectorAll("select");
		selects[selects.length-1].value=val("comp_gamp_"+i,"");
		var acts=h("div",{className:"actions"});
		var confirmBtn=h("button",{className:"btn btn-sm "+(confirmed?"btn-accept":""), onClick:function(){
			set("comp_confirmed_"+i,!val("comp_confirmed_"+i,false));
			renderComponents(body);
		}}, confirmed?"Confirmed":"Confirm");
		acts.append(confirmBtn);
		card.append(acts);
		body.append(card);
	});
}

function renderRequirements(body){
	clearNode(body);
	(DISCOVERY.inferred_requirements||[]).forEach(function(req,i){
		var status=val("req_status_"+i,"");
		var card=h("div",{className:"card", style:status==="rejected"?"opacity:.5":""});
		card.append(h("h4",null, req.id+" "), h("span",{style:"font-size:.75rem;color:var(--text-muted)"},"Source: "+req.source));
		card.append(inputField("Requirement Text","req_text_"+i,{type:"textarea",rows:2}));
		if(!val("req_text_"+i,"")) set("req_text_"+i, req.text||"");
		card.querySelector("textarea").value=val("req_text_"+i,"");
		var acts=h("div",{className:"actions"});
		var acceptBtn=h("button",{className:"btn btn-sm "+(status==="accepted"?"btn-accept":""),
			onClick:function(){ set("req_status_"+i,"accepted"); renderRequirements(body); }}, "Accept");
		var rejectBtn=h("button",{className:"btn btn-sm "+(status==="rejected"?"btn-danger":""),
			onClick:function(){ set("req_status_"+i,"rejected"); renderRequirements(body); }}, "Reject");
		acts.append(acceptBtn,rejectBtn);
		card.append(acts);
		body.append(card);
	});
	var addBtn=h("button",{className:"btn",onClick:function(){
		var id=prompt("Requirement ID (e.g. URS-NEW-001):");
		if(!id) return;
		var idx=DISCOVERY.inferred_requirements.length;
		DISCOVERY.inferred_requirements.push({id:id,text:"",source:"manual"});
		set("req_status_"+idx,"accepted");
		renderRequirements(body);
	}},"+ Add Requirement");
	body.append(addBtn);
}

function renderUnknowns(body){
	clearNode(body);
	(DISCOVERY.unknowns||[]).forEach(function(u,i){
		var card=h("div",{className:"card"});
		card.append(h("h4",null, u.question));
		if(u.context) card.append(h("p",{style:"font-size:.8rem;color:var(--text-muted);margin-bottom:.5rem"},u.context));
		if(u.type==="choice"&&u.options&&u.options.length){
			card.append(inputField("Answer","unk_"+i,{type:"select",
				options:[{value:"",label:"\u2014 Select \u2014"}].concat(u.options.map(function(o){return{value:o,label:o};})),
				idk:true
			}));
		} else {
			card.append(inputField("Answer","unk_"+i,{type:"textarea",rows:2,idk:true}));
		}
		body.append(card);
	});
}

function renderRoles(body){
	clearNode(body);
	var roles=val("roles",[]);
	roles.forEach(function(r,i){
		var card=h("div",{className:"card"});
		card.append(inputField("Role Name","role_name_"+i,{type:"text"}));
		if(!val("role_name_"+i,"")) set("role_name_"+i, r.name||"");
		card.querySelector("input").value=val("role_name_"+i,"");
		card.append(inputField("Description","role_desc_"+i,{type:"textarea",rows:2}));
		if(!val("role_desc_"+i,"")) set("role_desc_"+i, r.description||"");
		card.querySelector("textarea").value=val("role_desc_"+i,"");
		card.append(inputField("Permission Level","role_perm_"+i,{type:"select",
			options:[{value:"",label:"\u2014 Select \u2014"},{value:"admin",label:"Admin"},{value:"power_user",label:"Power User"},{value:"standard",label:"Standard"},{value:"read_only",label:"Read Only"}]
		}));
		var delBtn=h("button",{className:"btn btn-sm btn-danger",onClick:function(){
			roles.splice(i,1); set("roles",roles); renderRoles(body);
		}},"Remove");
		card.append(h("div",{className:"actions"},delBtn));
		body.append(card);
	});
	var addBtn=h("button",{className:"btn",onClick:function(){
		roles.push({name:"",description:"",permission:""}); set("roles",roles); renderRoles(body);
	}},"+ Add Role");
	body.append(addBtn);
}

function renderEnvironment(body){
	clearNode(body);
	body.append(
		inputField("Production Topology","env_topology",{type:"textarea",rows:2,required:true,idk:true}),
		h("div",{className:"field-row"},
			inputField("Operating System","env_os",{type:"text",required:true,idk:true}),
			inputField("Database","env_db",{type:"text",idk:true})
		),
		inputField("Network / Connectivity","env_network",{type:"textarea",rows:2,idk:true}),
		inputField("Hosting (on-prem / cloud / hybrid)","env_hosting",{type:"select",
			options:[{value:"",label:"\u2014 Select \u2014"},{value:"on-prem",label:"On-Premises"},{value:"cloud",label:"Cloud"},{value:"hybrid",label:"Hybrid"}],
			idk:true
		})
	);
	// Show discovered tech stack
	if((DISCOVERY.tech_stack||[]).length){
		body.append(h("h4",{style:"margin:1rem 0 .5rem"},"Discovered Tech Stack"));
		var tbl=h("table");
		tbl.append(h("thead",null,h("tr",null,h("th",null,"Name"),h("th",null,"Version"),h("th",null,"Layer"))));
		var tb=h("tbody");
		DISCOVERY.tech_stack.forEach(function(t){
			tb.append(h("tr",null,h("td",null,t.name),h("td",null,t.version||"\u2014"),h("td",null,t.layer||"\u2014")));
		});
		tbl.append(tb);
		body.append(tbl);
	}
}

function renderTestCoverage(body){
	clearNode(body);
	if(!(DISCOVERY.test_coverage||[]).length){
		body.append(h("p",{style:"color:var(--text-muted)"},"No test files were discovered."));
		return;
	}
	(DISCOVERY.test_coverage||[]).forEach(function(t,i){
		var card=h("div",{className:"card"});
		card.append(h("h4",null,t.test_file));
		if(t.description) card.append(h("p",{style:"font-size:.8rem;color:var(--text-muted);margin-bottom:.5rem"},t.description));
		card.append(h("span",{style:"font-size:.8rem;color:var(--text-muted)"},"Inferred: "+t.inferred_mapping));
		card.append(inputField("V-Model Level","test_level_"+i,{type:"select",
			options:[{value:"",label:"\u2014 Select \u2014"},{value:"IQ",label:"IQ \u2014 Installation Qualification"},
				{value:"OQ",label:"OQ \u2014 Operational Qualification"},{value:"PQ",label:"PQ \u2014 Performance Qualification"}],
			default:t.inferred_mapping
		}));
		if(!val("test_level_"+i,"")) set("test_level_"+i, t.inferred_mapping||"");
		card.querySelector("select").value=val("test_level_"+i,"");
		body.append(card);
	});
}

function renderOverrides(body){
	clearNode(body);
	var docTypes=["vp","urs","fs","ds","iq","oq","pq","traceability","vendor_assessment"];
	body.append(h("p",{style:"font-size:.85rem;color:var(--text-muted);margin-bottom:1rem"},
		"Add or remove sections from each document type. Leave blank to use defaults."));
	docTypes.forEach(function(dt){
		var card=h("div",{className:"card"});
		card.append(h("h4",null,dt.toUpperCase()));
		var key="override_"+dt;
		card.append(inputField("Include Sections (comma-separated)",key+"_include",{type:"text"}));
		card.append(inputField("Exclude Sections (comma-separated)",key+"_exclude",{type:"text"}));
		card.append(inputField("Custom Sections (comma-separated)",key+"_custom",{type:"text"}));
		body.append(card);
	});
}

// --- Build app ---
function buildApp(){
	document.getElementById("projectSubtitle").textContent=DISCOVERY.project_name||"Untitled Project";
	var app=document.getElementById("app");
	clearNode(app);
	app.append(
		makeSection("identity","1. System Identity",renderIdentity),
		makeSection("scope","2. Scope Boundaries",renderScope),
		makeSection("components","3. Component Review",renderComponents),
		makeSection("requirements","4. Requirements Candidates",renderRequirements),
		makeSection("unknowns","5. Architecture Unknowns",renderUnknowns),
		makeSection("roles","6. User Roles",renderRoles),
		makeSection("environment","7. Environment & Deployment",renderEnvironment),
		makeSection("tests","8. Test Coverage Review",renderTestCoverage),
		makeSection("overrides","9. Overrides & Custom Sections",renderOverrides)
	);
	updateProgress();
}

// --- Export ---
function exportAnswers(){
	var out={
		project_name: DISCOVERY.project_name,
		identity:{
			description:val("si_description",""),
			intended_use:val("si_intended_use",""),
			gamp_category:val("si_gamp",""),
			regulatory_context:val("si_regulatory","")
		},
		scope:(DISCOVERY.components||[]).map(function(c,i){return{name:c.name,scope:val("scope_"+i,"")};}),
		components:(DISCOVERY.components||[]).map(function(c,i){return{
			name:c.name,
			description:val("comp_desc_"+i,""),
			criticality:val("comp_crit_"+i,""),
			gamp_category:val("comp_gamp_"+i,""),
			confirmed:val("comp_confirmed_"+i,false)
		};}),
		requirements:(DISCOVERY.inferred_requirements||[]).map(function(r,i){return{
			id:r.id,
			text:val("req_text_"+i,""),
			status:val("req_status_"+i,""),
			source:r.source
		};}),
		unknowns:(DISCOVERY.unknowns||[]).map(function(u,i){return{
			question:u.question,
			answer:val("unk_"+i,""),
			skipped:val("unk_idk_"+i,false)
		};}),
		roles:(val("roles",[])).map(function(_,i){return{
			name:val("role_name_"+i,""),
			description:val("role_desc_"+i,""),
			permission:val("role_perm_"+i,"")
		};}),
		environment:{
			topology:val("env_topology",""),
			os:val("env_os",""),
			database:val("env_db",""),
			network:val("env_network",""),
			hosting:val("env_hosting","")
		},
		test_coverage:(DISCOVERY.test_coverage||[]).map(function(t,i){return{
			test_file:t.test_file,
			assigned_level:val("test_level_"+i,"")
		};}),
		overrides:{}
	};
	["vp","urs","fs","ds","iq","oq","pq","traceability","vendor_assessment"].forEach(function(dt){
		var inc=val("override_"+dt+"_include","");
		var exc=val("override_"+dt+"_exclude","");
		var cust=val("override_"+dt+"_custom","");
		if(inc||exc||cust){
			out.overrides[dt]={
				include_sections:inc?inc.split(",").map(function(s){return s.trim();}).filter(Boolean):[],
				exclude_sections:exc?exc.split(",").map(function(s){return s.trim();}).filter(Boolean):[],
				custom_sections:cust?cust.split(",").map(function(s){return s.trim();}).filter(Boolean):[]
			};
		}
	});
	var blob=new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
	var a=document.createElement("a");
	a.href=URL.createObjectURL(blob);
	a.download="discovery-answers.json";
	a.click();
	URL.revokeObjectURL(a.href);
}

function resetAll(){
	if(!confirm("Clear all answers? This cannot be undone.")) return;
	localStorage.removeItem(LS_KEY);
	STATE={};
	buildApp();
}

buildApp();
</script>
</body>
</html>"""


def generate_html(report: dict) -> str:
	"""Return a self-contained HTML string with *report* data embedded."""
	project_name = report.get("project_name", "Untitled Project")
	discovery_json = json.dumps(report, ensure_ascii=True).replace("</", "<\\/")


	html = _HTML_TEMPLATE
	html = html.replace("{{PROJECT_NAME}}", _html_escape(project_name))
	html = html.replace("{{DISCOVERY_JSON}}", discovery_json)
	return html


def _html_escape(text: str) -> str:
	"""Minimal HTML escaping for attribute-safe injection."""
	return (
		text
		.replace("&", "&amp;")
		.replace("<", "&lt;")
		.replace(">", "&gt;")
		.replace('"', "&quot;")
	)


def _build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Generate an interactive HTML playground from a V-model discovery report.",
	)
	parser.add_argument(
		"--input",
		required=True,
		help="Path to the discovery report JSON file",
	)
	parser.add_argument(
		"--output",
		default=None,
		help="Output path for the HTML file (default: temp file)",
	)
	return parser


def main() -> None:
	parser = _build_parser()
	args = parser.parse_args()

	report = _load_report(args.input)
	html = generate_html(report)

	if args.output:
		out_path = os.path.abspath(args.output)
		os.makedirs(os.path.dirname(out_path), exist_ok=True)
	else:
		fd, out_path = tempfile.mkstemp(suffix=".html", prefix="vmodel_playground_")
		os.close(fd)

	with open(out_path, "w", encoding="utf-8") as fh:
		fh.write(html)

	print(f"Playground generated: {out_path}")

	try:
		webbrowser.open("file://" + out_path.replace("\\", "/"))
		print("Opened in default browser.")
	except Exception:
		print("Could not open browser automatically. Open the file above manually.")


if __name__ == "__main__":
	main()
