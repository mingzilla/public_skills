# Decisions and WHY

### Topic: why the document is called desired

Q: Why not `proposed`, or `plan`?
A: Both invite the wrong content. *Proposed* sets the document against something current, so it collects a comparison; *plan* is ambiguous - it can mean the steps as easily as the end. **Desired** names what the document holds and nothing else, so a writer reaching for "what it used to be" has already been told no by the filename.

### Topic: why dry-run at all

Q: Why not trust a document that reads well?
A: It is a claim about things that exist, and reading it tests nothing. A dry run walks a real case through it, and fails in ways the document's own text cannot show - the six-way fan-out is invisible until a result is counted.

### Topic: why forward only

Q: Why does the document never say what changed?
A: Because whatever it is compared against gets deleted. A comparison is the part that rots first, and the reader it was written for is gone. State what will be; the reasoning lives in the decisions.

### Topic: why re-run everything

Q: A fix touches one case. Why re-run the others?
A: The cases share the desired state. The fix that saved the fan-out changed how a result is stored, and the case that had already passed was the one that noticed. A case kept running is the cheap part; the re-run is the test.

### Topic: why number the findings

Q: Why not list problems in a summary?
A: A finding is a fix somebody makes. A number lets the document, the case, and the decision that cites it point at the same thing, and a finding with no home is the one that gets dropped.

### Topic: why the hard cases

Q: Why go looking for the case that breaks it?
A: The easy cases agree with anything. The value is in the one that does not - the second writer, the bulk data, the resource that must be serialised - and finding it on paper is the whole point.

### Topic: why run rather than reason

Q: When a check exists, why run it?
A: A reasoned answer is a guess in better clothes. Running the dependency check found a live violation in the library that states the rule, and running a rename experiment found that a half-renamed project passes with zero violations. Neither was reachable by thinking harder.

### Topic: when it is done

Q: How do you know the document is finished?
A: When the cases stop producing findings. Not when it reads well - it read well before the first dry run.

### Topic: what happens to the document

Q: Where does it go when the change lands?
A: Into the skills that carry it; then the document is deleted. A second copy beside them drifts, and one already did - a rule corrected in one file survived uncorrected in another.

### Topic: what to ask the caller

Q: Which decisions go back to the caller?
A: Only those no rule can settle - a preference between two workable shapes. Anything the document's own rules decide is not a question. Handing one over moves work rather than sharing it, and it reads as a question the caller cannot answer.
