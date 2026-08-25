/* The button hands over an orchestration prompt, not the writing job itself.
   Paste it into a fresh Opus chat: Opus asks the four questions, passes the
   answers to a Sonnet subagent, which runs the skill and files the doc, then
   Opus reads the result and fixes the voice before it reaches you. Sonnet does
   the assembly, Opus keeps the voice, and the long skill run never sits in the
   expensive thread.

   The four questions come first and are asked by Opus, not by the subagent. A
   subagent cannot ask you anything, and the answer to the first-week question is
   the one paragraph of a letter that cannot be written for you. */
/* Pay never travels in the clipboard. The tracker note carries the posted wage
   and sometimes his Kelvin rate, and neither belongs in a letter or in a payload
   he may paste anywhere. Drop any sentence carrying a currency figure. The
   follow-up button spec already bans inlining the wage; the letter brief was
   leaking it through the note. */
function noPay(note){
  return String(note==null?"":note)
    .replace(/[^.!?]*\$\s?\d[^.!?]*[.!?]?/g,"")
    .replace(/\s{2,}/g," ").trim();
}
const PACKETS_FOLDER="1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP";
const LETTERS_FOLDER="1pPulXeoTIXN6sJXuAByc2sW37dThROoB";
function cvBrief(kind,r){
  if(kind==="int")return [
    "Write one cover letter for "+r[1]+", "+r[2]+", and file it in the Packets folder.",
    "Posting: "+r[7],
    "Source: "+r[6]+". Location: "+r[3]+". Term: "+r[4]+".",
    "Deadline: "+(r[5]||"rolling, no posted date"),
    "Tracker notes: "+noPay(r[9])
  ];
  return [
    "Write one application essay or letter for the "+r[1]+" scholarship, sponsored by "+r[2]+", and file it in the Packets folder.",
    "Link: "+r[7],
    "Award: "+r[3]+". Opens: "+r[4]+". Deadline: "+(r[5]||"not posted yet")+".",
    "Eligibility gate: "+r[6],
    "Tracker notes: "+noPay(r[9])
  ];
}
/* The writing rules travel inside the clipboard text because the session that
   receives the paste starts cold and may not have the skill loaded. Where this
   text and the skill disagree, the skill wins and this block gets regenerated
   from it. */
function cvRules(what){
  return [
    "Use the application-packet-builder skill and follow it exactly. Read its references/voice-dna.md, references/profile.md and references/writing.md before drafting. The deliverable is a native Google Doc in the Packets folder, Drive ID "+PACKETS_FOLDER+". Never chat text, never a .docx, and do not set disableConversionToGoogleType.",
    "Read one of my past letters in Drive folder "+LETTERS_FOLDER+" before drafting so the voice is mine.",
    "Hard rules: never submit or transmit anything, never read or write the frozen tracker spreadsheet, never use an em dash, never put a pay figure in the "+what+", and never claim FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, Revit, BIM, Creo, or welding. SolidWorks is my CAD. Kelvin Thermal Technologies is past tense, that internship ended August 2026.",
    "Never a negative parallelism. No sentence that negates one framing and then asserts a corrected one: not \"it is not X, it is Y\", not \"not just X but Y\", not \"less X, more Y\", and not the disguised forms that concede a point and pivot. This is the single most obvious sign a letter was machine written. Delete everything before the positive claim and keep only what the thing is.",
    "No dead AI vocabulary: leverage, robust, seamless, innovative, spearheaded, facilitated, meticulous, passionate, showcase, foster, testament, cutting-edge, best practices, proven track record. Say the plain thing.",
    "Open with evidence, not intent. Most body paragraphs carry a real number from my resume, but do not put one in every paragraph on a cadence and do not make every paragraph the same length. Even pacing is what makes a letter read as machine written.",
    "The 50+ precision measurements belong to my ratcheting screwdriver project, never to Kelvin.",
    "The ratcheting screwdriver reverse-engineering project and the compressed-air wobbler engine were school coursework. Never call either one personal, independent, self-directed, done on my own time, or ungraded.",
    "Before building the doc you must pass the letter gate. The skill carries the tool inside it: run the setup block under its Path 1 heading once, which writes the gate to /tmp/apb/scripts/. Then run: python3 /tmp/apb/scripts/check_letter.py /tmp/spec.json . Exit code 2 means do not build. Fix the draft and run it again. There is no bypass. If a number in the letter came from the posting rather than my resume, pass it with --allow so it is a deliberate choice. If you have no shell at all, work the no-shell checklist in the skill by hand and say in your report that you did."
  ];
}
function cvPrompt(kind,i){
  const r=(kind==="int"?INT:SCH)[i],int=kind==="int";
  const what=int?"cover letter":"essay";
  /* The last thing the subagent reports differs by kind. An internship letter
     lives or dies on the housing question; a scholarship essay lives or dies on
     whether the bank already had an answer for the prompt. */
  const ask=int
    ?"Report back three things: the Drive link, the company-specific claims that still need verifying, and whether the posting states anything about housing or relocation. Silence on relocation is not a refusal, so say which of the two it is."
    :"Adapt from my essay bank rather than writing cold, and say which bank entry each answer came from. Report back three things: the Drive link, any prompt with no match in the bank, and whether I clear the eligibility gate above.";
  const back=int?"the housing line":"the bank coverage";
  const subject=int?r[1]:r[2];
  return [
    "Do not write this one yourself. Ask me the four questions below, then hand the drafting to a Sonnet subagent and keep the voice pass for yourself.",
    "",
    "FIRST, before you spawn anything, ask me these and wait for my answers. A subagent cannot ask me anything, and my answer to question C is the one paragraph of this "+what+" that cannot be written for me. Do not skip this step even if I sound like I am in a hurry.",
    "",
    "  A. Why "+subject+"? Read the posting and my notes above, then offer me two or three specific angles you actually found, numbered, so I can answer with a number.",
    "  B. What would I be good at here? Tell me what the posting seems to need and ask me if that is the right read.",
    "  C. What would I want to be working on in my first week? One or two sentences, in my words.",
    "  D. Tone: plain and direct like my last letters, or a little warmer?",
    "",
    "THEN:",
    "1. Spawn one subagent with the model set to Sonnet.",
    "2. Give it the brief below verbatim, with my four answers appended. It starts cold, so it cannot see this chat, my dashboard, or anything I have told you; the brief is everything it gets.",
    "3. Wait for it to return the Drive link, then read the "+what+" yourself before you show me anything.",
    "",
    "BRIEF FOR THE SONNET SUBAGENT, pass it through as written:",
    "---8<---"
  ].concat(cvBrief(kind,r)).concat(cvRules(what)).concat([
    "Build the paragraph carrying my answer to C in my own words, with none of the posting's vocabulary mirrored into it.",
    ask,
    "---8<---",
    "",
    "When it comes back, before you hand it to me:",
    "- Open the doc and read it for voice. Cut any sentence that would be equally true in a letter to a different employer.",
    "- Check every number is real and attributed right. The 50+ precision measurements belong to the ratcheting screwdriver project, not to Kelvin. The screwdriver and the wobbler engine are school coursework, so cut any sentence calling them personal or done on my own time.",
    "- Scan for em dashes, for negative parallelisms, and for hedges like eager to, confident that, hope to.",
    "- Read it once against the question: does this sound like something I would actually write, or like an AI trying hard to imitate me?",
    "- Rewrite it in place if it reads generic. That pass is the reason this is your job and not the subagent's.",
    "",
    "Then give me the link, the verify list, and "+back+" in one short reply. Do not submit anything."
  ]).join("\n");
}
function cvBtn(kind,i,btn){
  const r=(kind==="int"?INT:SCH)[i];
  copyText(cvPrompt(kind,i)).then(()=>
    flash(btn,"Copied",'Opus prompt for '+r[1]+' copied. Paste it into a fresh Opus chat. It asks you four questions first, then hands the draft to a Sonnet subagent and checks the voice before the link comes back to you.'));
}
