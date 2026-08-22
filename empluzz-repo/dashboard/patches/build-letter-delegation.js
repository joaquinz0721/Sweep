/* The button hands over an orchestration prompt, not the writing job itself.
   Paste it into a fresh Opus chat: Opus passes the brief to a Sonnet subagent,
   which runs the skill and files the doc, then Opus reads the result and fixes
   the voice before it reaches you. Sonnet does the assembly, Opus keeps the
   voice, and the long skill run never sits in the expensive thread. */
const PACKETS_FOLDER="1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP";
const LETTERS_FOLDER="1pPulXeoTIXN6sJXuAByc2sW37dThROoB";
function cvBrief(kind,r){
  if(kind==="int")return [
    "Write one cover letter for "+r[1]+", "+r[2]+", and file it in the Packets folder.",
    "Posting: "+r[7],
    "Source: "+r[6]+". Location: "+r[3]+". Term: "+r[4]+".",
    "Deadline: "+(r[5]||"rolling, no posted date"),
    "Tracker notes: "+r[9]
  ];
  return [
    "Write one application essay or letter for the "+r[1]+" scholarship, sponsored by "+r[2]+", and file it in the Packets folder.",
    "Link: "+r[7],
    "Award: "+r[3]+". Opens: "+r[4]+". Deadline: "+(r[5]||"not posted yet")+".",
    "Eligibility gate: "+r[6],
    "Tracker notes: "+r[9]
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
  return [
    "Do not write this one yourself. Hand the drafting to a Sonnet subagent and keep the voice pass for yourself.",
    "",
    "1. Spawn one subagent with the model set to Sonnet.",
    "2. Give it the brief below verbatim. It starts cold, so it cannot see this chat, my dashboard, or anything I have told you; the brief is everything it gets.",
    "3. Wait for it to return the Drive link, then read the "+what+" yourself before you show me anything.",
    "",
    "BRIEF FOR THE SONNET SUBAGENT, pass it through as written:",
    "---8<---"
  ].concat(cvBrief(kind,r)).concat([
    "",
    "Use the application-packet-builder skill and follow its format spec exactly. The deliverable is a native Google Doc in the Packets folder, Drive ID "+PACKETS_FOLDER+". Never chat text, never a .docx.",
    "Read one of my past letters in Drive folder "+LETTERS_FOLDER+" before drafting so the voice is mine.",
    "Hard rules: never submit or transmit anything, never read or write the frozen tracker spreadsheet, never use an em dash, never put a pay figure in the "+what+", and never claim FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, or Revit and BIM. SolidWorks is my CAD. Kelvin Thermal Technologies is past tense, that internship ended August 2026.",
    "Open with evidence, not intent. Every body paragraph carries a real number from my resume.",
    ask,
    "---8<---",
    "",
    "When it comes back, before you hand it to me:",
    "- Open the doc and read it for voice. Cut any sentence that would be equally true in a letter to a different employer.",
    "- Check every number is real and attributed right. The 50+ precision measurements belong to the ratcheting screwdriver project, not to Kelvin.",
    "- Scan for em dashes and for hedges like eager to, confident that, hope to.",
    "- Rewrite it in place if it reads generic. That pass is the reason this is your job and not the subagent's.",
    "",
    "Then give me the link, the verify list, and "+back+" in one short reply. Do not submit anything."
  ]).join("\n");
}
function cvBtn(kind,i,btn){
  const r=(kind==="int"?INT:SCH)[i];
  copyText(cvPrompt(kind,i)).then(()=>
    flash(btn,"Copied",'Opus prompt for '+r[1]+' copied. Paste it into a fresh Opus chat. It hands the draft to a Sonnet subagent, then checks the voice before the link comes back to you.'));
}
