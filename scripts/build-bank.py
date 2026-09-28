"""One-time, editable source for the curated interview bank. Run with python3 scripts/build-bank.py."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://github.com/DevLoversTeam/{}-interview-questions"

# Each row is subtopic | original interviewer prompt | expected core points.
RAW = {
"javascript": """
types|Which JavaScript values are primitives, and how does assigning a primitive differ from assigning an object?|Primitives are immutable values copied on assignment; objects are reference values and assigned by shared reference.
types|What does typeof null return, and why should you be careful with it?|It returns object due to historical behavior; null is still a primitive.
types|How would you reliably check whether a value is an array?|Array.isArray(value).
truthiness|Name the falsy JavaScript values you commonly encounter.|false, 0, -0, empty string, null, undefined, NaN; 0n is falsy too.
equality|Explain == and === using one example where they differ.|== coerces types; === does not; 0 == false is true but 0 === false is false.
variables|When would you choose let instead of const?|When rebinding is needed; const prevents rebinding, not object mutation.
scope|How does var scope differ from let and const inside a block?|var is function scoped; let and const are block scoped.
scope|What is lexical scope, and which variables can a nested function access?|Access is determined by where a function is defined; it can access outer scope variables.
hoisting|What happens if you read a let variable before its declaration?|ReferenceError during the temporal dead zone.
hoisting|How are function declarations and function expressions different before their definitions execute?|Declarations are callable early; expression bindings follow their variable initialization rules.
functions|What does an arrow function do differently with this?|It captures this lexically; it has no own this binding.
functions|What is a default parameter and when is it used?|Default applies when an argument is omitted or undefined, not null.
functions|How are rest parameters and spread syntax different?|Rest collects values; spread expands an iterable or object properties in supported contexts.
destructuring|Show how to extract name and age from a user object with destructuring.|const { name, age } = user.
template-literals|Why use a template literal instead of string concatenation?|Interpolation with ${...} and multiline text.
objects|Compare dot and bracket property access; when is bracket notation necessary?|Bracket accepts computed keys and keys unsuitable for dot syntax.
objects|How do Object.keys, Object.values, and Object.entries differ?|They return own enumerable keys, values, and key-value pairs respectively.
copying|Why might {...user} fail to isolate a nested address object?|Object spread makes a shallow copy; nested objects retain shared references.
copying|When is structuredClone useful, and what kind of value can it not clone?|It can clone many nested structured values but not functions.
immutability|What does it mean to update an array without mutating the original?|Create a new array, e.g. map, filter, or spread; avoid changing original entries.
arrays|Compare slice and splice when removing array elements.|slice returns a copy and does not mutate; splice changes original array.
arrays|How would you turn an array of users into their email addresses?|users.map(user => user.email).
arrays|When should you use filter instead of find?|filter returns all matches as array; find returns first matching value or undefined.
arrays|What do some and every return for an array?|Booleans: at least one match versus all matches.
arrays|When is reduce useful for an object-counting task?|Accumulate counts into an object with an initial accumulator.
arrays|Why can [10, 2, 1].sort() produce a surprising order?|Default sort compares strings; pass numeric comparator (a,b)=>a-b.
collections|When is Set a convenient choice for an array transformation?|Unique values / membership checks.
collections|How does Map differ from a plain object for keyed lookup?|Map accepts any key type and has size and iteration semantics.
callbacks|What does it mean that functions are first-class values?|They can be stored, passed as arguments, and returned.
callbacks|Define a higher-order function and give a common example.|It accepts or returns a function; map/filter are examples.
closures|What is a closure in practical terms?|A function retains access to variables from its defining lexical scope.
closures|How can a closure keep a counter private?|Return a function that increments a variable in its enclosing function.
currying|What does a curried add(a)(b) function do?|It returns a function for the next argument; result is a+b.
purity|What makes a function pure, and why is that useful for testing?|Same inputs yield same output; no externally visible side effects.
this|How is this determined for an ordinary function called as obj.method()?|By call site; this is obj for a method call.
this|What does bind do compared with call and apply?|bind returns a bound function; call/apply invoke immediately with args list/array.
prototypes|How does JavaScript find a missing property on an object?|It searches up the prototype chain until found or null reached.
prototypes|What is the relationship between class methods and prototypes?|Class syntax builds prototype methods; instances share them.
classes|What does extends provide in a JavaScript class?|Prototype inheritance and access to parent behavior via super.
async|What does synchronous execution mean compared with asynchronous work?|Synchronous runs in order on stack; asynchronous completion is scheduled later.
event-loop|What must happen before a queued callback can run?|The current call stack must finish; event loop schedules ready callbacks.
event-loop|How do microtasks from Promise.then relate to setTimeout callbacks in a browser?|Microtasks are drained before the next timer task after current stack.
promises|What are the three states of a Promise?|pending, fulfilled, rejected.
promises|What does returning a value from a then callback do to the next then?|Next Promise fulfills with that value; returned Promise is adopted.
promises|How does Promise.all behave when one input rejects?|It rejects with that reason; other operations may continue running.
promises|When would Promise.allSettled be preferable to Promise.all?|When outcomes of all tasks are needed even if some reject.
promises|What does Promise.race resolve or reject with?|Settlement of the first settled input Promise.
async-await|What does an async function always return?|A Promise; returned values fulfill it and thrown errors reject it.
async-await|Why might await inside a loop be slower than Promise.all?|It serializes independent operations; Promise.all starts them concurrently.
errors|How do you handle a rejected Promise with async/await?|try/catch around await, or catch the returned Promise.
timers|Does setTimeout(fn, 0) run fn immediately? Explain.|No; callback waits for current stack and preceding microtasks, then a timer task.
dom|How would you select one element by CSS selector and change its text?|document.querySelector(selector).textContent = value.
dom|What is the difference between textContent and innerHTML for user-provided text?|textContent inserts text safely; innerHTML parses markup and can introduce XSS.
events|Explain event bubbling with a nested button and container.|Event reaches target then bubbles through ancestors unless propagation is stopped.
events|What is event capture?|Event travels from ancestors toward target before target/bubble phases.
events|What is event delegation and why is it useful for dynamic lists?|Put one listener on ancestor and inspect event.target; handles future children.
events|When would you call preventDefault on an event?|To prevent browser default action such as form navigation; it does not stop propagation.
events|How does stopPropagation differ from preventDefault?|Stops propagation through DOM versus cancels default browser behavior.
storage|Compare localStorage and sessionStorage lifetimes.|localStorage persists across sessions; sessionStorage is scoped to a tab/session.
storage|Why should you avoid assuming localStorage stores JavaScript objects directly?|It stores strings; serialize with JSON.stringify and parse on read.
cookies|What is one important difference between cookies and localStorage for HTTP requests?|Cookies can be sent automatically with matching HTTP requests; localStorage is not.
fetch|How do you detect an HTTP 404 when using fetch?|fetch usually fulfills on HTTP errors; check response.ok/status.
json|What do JSON.stringify and JSON.parse do?|Serialize JS value to JSON text and parse JSON text into JS value.
cors|What is CORS trying to control in a browser?|Whether scripts from one origin may read responses from another origin under server policy.
modules|What is the difference between named and default ES module exports?|Named imports use exported names; default is one default export with chosen import name.
modules|What is a key syntax difference between CommonJS and ES modules?|require/module.exports versus import/export; module semantics differ.
complexity|What is the time complexity of scanning an array once?|O(n) for n elements.
recursion|What are a base case and recursive step?|Base case stops; recursive step reduces toward it.
debugging|A click listener appears twice after every page navigation. What would you inspect?|Repeated registration and missing cleanup; remove listener or register once.
debugging|A search response from an older request overwrites newer results. How might you prevent this?|Cancel/ignore stale requests or use switchMap for observable requests.
""",
"angular": """
fundamentals|What is Angular and what role does a component play?|Angular is a TypeScript web framework; components combine template, behavior, and metadata for UI.
fundamentals|What makes an application a single-page application?|Navigation updates view client-side without reloading full document each time.
structure|What files are commonly involved in an Angular component?|TypeScript class/metadata, template, optional styles and tests.
standalone|What does standalone: true mean for an Angular component?|It can import its own dependencies and be used without declaration in an NgModule.
templates|What does {{ user.name }} do in an Angular template?|Interpolation renders expression as text.
binding|When would you use [disabled] instead of disabled on a button?|Property binding controls DOM property from component expression dynamically.
binding|How does (click)="save()" work?|Event binding invokes component handler when click occurs.
binding|What does [(ngModel)] express, and what must be available to use it?|Two-way binding; FormsModule/ngModel support must be imported.
control-flow|How would you conditionally render content in a modern Angular template?|Use @if block; older *ngIf may appear in existing apps.
control-flow|How would you render a list with a stable identity in modern Angular?|Use @for (item of items; track item.id); older *ngFor exists.
directives|How do attribute directives differ from structural/control-flow rendering?|Attribute directives change behavior/style of existing element; control flow creates/removes views.
pipes|What does a pipe do in a template?|Transforms displayed value; e.g. date/currency/async.
pipes|When might you write a custom pipe?|Reusable display transformation; avoid heavy impure work in templates.
input-output|What is an input in parent-child communication?|Parent passes data to child through input binding / input API.
input-output|What is an output in parent-child communication?|Child emits an event that parent listens to.
input-output|How would a child report a selected item to its parent?|Output event emitter/output API; parent handles ($event).
viewchild|What is ViewChild used for?|Access a child component/directive or template element after view creation.
projection|What does ng-content enable?|Parent projects markup into a child component's template.
lifecycle|When does ngOnInit run?|Once after Angular initializes bound inputs; suitable for initialization.
lifecycle|What does ngOnChanges receive?|Changes to bound inputs, including previous/current values.
lifecycle|What cleanup belongs in ngOnDestroy?|Subscriptions, timers, listeners, or other resources not automatically cleaned.
di|Why put shared logic in an injectable service?|Reuse behavior/state and obtain via dependency injection.
di|What does dependency injection do in Angular?|Injector provides dependencies to classes rather than constructing them manually.
di|What does providedIn: 'root' usually imply?|App root-level singleton service instance (subject to provider overrides).
di|Can a component-level provider create a different service instance?|Yes, component injector can provide a scoped instance.
di|How can a standalone component request a service using a modern API?|inject(Service) in an injection context; constructor injection also supported.
observables|What is an Observable in Angular/RxJS terms?|A subscribable stream that may emit multiple values over time.
observables|How does an Observable differ from a Promise?|Observable may emit multiple values and is cancellable by unsubscribe; Promise settles once.
observables|What is a subscription?|Connection to observable emissions; may need cleanup.
observables|What is a Subject?|Both observable and observer; can multicast next values to subscribers.
observables|Why use BehaviorSubject for current state?|It stores a current value and immediately emits latest to new subscribers.
observables|What does the async pipe do?|Subscribes in template, renders latest value, and cleans up subscription.
rxjs|What does map do in an RxJS pipe?|Transforms each emitted value.
rxjs|What does filter do in an RxJS pipe?|Allows emissions matching predicate.
rxjs|When is tap useful?|Side effects such as logging without changing emitted value.
rxjs|Why is switchMap suitable for autocomplete requests?|Switches to latest inner observable and unsubscribes prior request stream.
rxjs|What does catchError need to return?|An Observable to continue/recover or rethrow via throwError.
rxjs|Name a modern way to clean up a component subscription.|takeUntilDestroyed, async pipe, or explicit unsubscribe in ngOnDestroy.
http|What does HttpClient.get return?|An Observable of response data; request generally starts on subscription.
http|Where would you handle loading, success, and error states for a request?|Track loading/error/data in component/service and clear loading on completion/error.
http|What can an HTTP interceptor do?|Inspect/modify requests or responses, e.g. add auth header or central error handling.
http|Why should auth tokens be attached conditionally in an interceptor?|Avoid leaking tokens to unintended hosts/endpoints.
forms|What is the difference between template-driven and reactive forms?|Template-driven declares form behavior mainly in template; reactive forms define controls/model in class.
forms|What are FormControl and FormGroup?|Control tracks a value/status; group combines named controls.
forms|How do you show validation errors without showing them immediately on page load?|Check invalid plus touched/dirty/submitted.
forms|What does a custom validator return when input is valid?|null; otherwise validation errors object.
routing|What does routerLink do?|Navigates using Angular Router without full page reload.
routing|How can a component read a route parameter?|ActivatedRoute paramMap snapshot or observable.
routing|What does lazy loading a route achieve?|Loads route code when needed, reducing initial bundle work.
routing|What is a route guard for?|Controls navigation based on condition; server must still enforce security.
change-detection|What does change detection do?|Updates template when state changes.
change-detection|What is the basic idea of OnPush?|Reduce checks; update via new input references, events, observable emissions, signals, etc.
change-detection|Why may mutating an input object cause an OnPush child to appear stale?|Same reference may not trigger expected input change detection; pass a new reference.
modern|How do standalone components relate to NgModules in existing projects?|Standalone is modern default approach; older apps may organize declarations/imports in NgModules.
modern|Compare @if with *ngIf at a high level.|Both conditionally display content; @if is modern built-in syntax, *ngIf older directive syntax.
debugging|An Angular template says an imported pipe is unknown. What would you check?|Import pipe/dependency into standalone component or owning NgModule.
debugging|A list renders with wrong reused rows after reorder. What should you inspect?|@for track expression / identity stability.
""",
"node": """
fundamentals|What is Node.js?|JavaScript runtime outside browser built on V8, commonly used for servers and tooling.
fundamentals|What is V8's role in Node.js?|It executes JavaScript; Node adds runtime APIs.
architecture|What does event-driven programming mean in a Node server?|Callbacks/listeners react to events such as requests or I/O completion.
architecture|What does non-blocking I/O mean in practice?|I/O is started without waiting synchronously on main JS thread; completion handled later.
architecture|Why can CPU-heavy synchronous work hurt a Node server?|It blocks event loop from serving other requests.
architecture|What sort of work should generally use asynchronous Node APIs?|I/O such as file and network operations so the main thread can continue.
event-loop|What is the Node event loop responsible for at a junior level?|Scheduling callbacks for timers, I/O, and other phases while JS runs on main thread.
event-loop|Do setTimeout callbacks always run at their exact delay?|No, delay is minimum-ish and depends on event loop availability.
runtime|Name two APIs in Node that are absent or different in browser JS.|fs, process, path, Buffer; DOM APIs are browser-specific.
modules|How do you export/import with CommonJS?|module.exports / require.
modules|How do you export/import with ES modules in Node?|export / import with ESM configuration or .mjs.
npm|What is package.json used for?|Package metadata, scripts, dependencies and configuration.
npm|When does a package belong in devDependencies?|Needed for development/build/test but not runtime deployment.
npm|What does npm run test do?|Runs the test script defined in package.json.
environment|How do you read an environment variable in Node?|process.env.NAME, typically configure outside source.
environment|Why should secrets usually not be hard-coded into source?|Risk of exposure and difficult per-environment configuration.
process|What is process.argv?|Array of command-line arguments passed to process.
fs|How would you read a text file without blocking the event loop?|Use fs/promises readFile(path, 'utf8') and await it.
fs|Why is fs.readFileSync often inappropriate in a request handler?|Blocks main JS thread until file operation completes.
path|Why use path.join instead of manual slash concatenation?|Portable path separators and normalization.
events|What does EventEmitter.on and emit do?|Register a listener and trigger event with arguments.
buffers|What is a Buffer used for?|Represent binary bytes, e.g. network/file data.
streams|Why stream a large file rather than read it all into memory?|Process chunks with lower memory use / backpressure support.
streams|What is backpressure in a stream at a high level?|Consumer cannot keep up with producer; flow should slow or buffer within limits.
async|How do you handle an error from an awaited fs promise?|try/catch or Promise rejection handling.
async|What can happen if you forget to await a Promise in a request handler?|Response may use unresolved value or errors may escape intended handling.
http|What are request method and URL in an HTTP server used for?|Identify operation and resource/route.
http|What is a response status code?|Numeric result category such as 200 success, 404 missing, 500 server error.
debugging|A server stops responding during a huge JSON calculation. What is a likely cause?|CPU work blocks event loop; split/offload work or use worker thread.
""",
"express": """
fundamentals|What does Express add on top of Node's HTTP server?|Convenient routing, middleware, request/response helpers.
routing|How would you define a GET /health route?|app.get('/health', (req,res)=>res.json({ok:true})).
routing|What is the difference between req.params.id and req.query.id?|Route path parameter versus URL query parameter.
routing|Where does JSON POST data appear after JSON body middleware?|req.body.
middleware|What is Express middleware?|Function with req,res,next that can process request, respond, or pass control.
middleware|Why does middleware order matter?|Handlers run in registration order; parsing/auth must happen before dependent routes.
middleware|What happens if middleware neither responds nor calls next?|Request hangs without proceeding.
middleware|How would you make a simple request logger middleware?|Log req.method and req.url then call next().
errors|What makes Express error middleware distinct?|Four parameters (err, req, res, next), registered after routes.
errors|Why centralize error handling in an API?|Consistent status/body and less duplicated route logic.
status|When is 201 preferable to 200?|Resource successfully created.
status|When should a missing resource return 404?|Requested resource does not exist.
status|How do 400 and 500 differ?|Bad client request versus unexpected server failure.
rest|What does CRUD stand for and how might it map to HTTP verbs?|Create POST, Read GET, Update PUT/PATCH, Delete DELETE.
rest|How do PUT and PATCH usually differ?|PUT replaces representation; PATCH applies partial update.
responses|What does res.json do?|Serializes object to JSON response and sets content type.
validation|Why validate req.body before using it?|Client input can be missing, wrong type, or malicious; return clear 400.
validation|What should an API return for invalid input?|A 400/422 status with concise useful error details.
async|How do you ensure errors from an async route reach error handling?|Use Express version behavior or pass errors to next; Express 5 forwards rejected promises.
async|Why should an awaited DB/API operation be handled for failure?|Prevent unhandled rejection and return meaningful API error.
auth|What is authentication versus authorization?|Identity verification versus permission to perform action.
auth|Where can a bearer token be sent in a request?|Authorization: Bearer header; verify server-side.
cors|What does CORS middleware configure?|Browser cross-origin access via response headers.
environment|Why read server port from process.env?|Deployment environment can set port without source edit.
structure|Why split routes and business logic in a growing Express app?|Clear responsibilities, reuse, easier testing.
debugging|A POST route sees undefined req.body. What would you inspect?|Express JSON parser setup and Content-Type plus middleware order.
debugging|Your /users/:id route catches /users/new. How can you fix it?|Register specific route first or constrain param matching.
debugging|An API responds twice and throws headers sent. What went wrong?|Code attempted second response; return after response or control flow fix.
""",
"html": """
semantics|Why use semantic elements such as main, nav, and article?|Meaningful structure for accessibility, browser tools, and SEO.
document|What are doctype, html, head, and body for?|Standards mode and document root, metadata, visible content.
document|What does the lang attribute on html help with?|Screen readers and language processing.
elements|How do block and inline elements typically affect layout?|Block starts new line/full available width; inline flows with text, though CSS can alter display.
forms|Why should an input have an associated label?|Accessible name and larger click target.
forms|What is the difference between input type=email and type=text?|Email offers browser validation/input hints; server validation still needed.
forms|What does the name attribute on a form control affect?|Key submitted with form data.
forms|What does required do, and is it enough for server validation?|Browser constraint validation; server must validate independently.
forms|When do you use a button with type=button inside a form?|To prevent default form submission for non-submit action.
accessibility|What makes alt text useful on an image?|Conveys relevant image meaning to assistive tech or when unavailable.
accessibility|When should a decorative image use alt=""?|When it adds no content and should be skipped by screen readers.
accessibility|When is a button preferable to a link?|For an action on the current page; links navigate to a destination.
accessibility|Why should headings follow a meaningful hierarchy?|Navigable document outline and understandable structure.
accessibility|Why not add ARIA roles when a native HTML element already provides behavior?|Native semantics and keyboard behavior are usually more reliable.
tables|What should a data table use for column headers?|th cells with appropriate scope where helpful.
data|What are data-* attributes for?|Custom metadata accessible in DOM via dataset.
meta|What does meta viewport help with on mobile?|Controls layout viewport scaling for responsive layouts.
seo|Name two HTML features helpful for basic SEO.|Descriptive title, semantic headings, meta description, meaningful links.
scripts|How do defer and async differ for external scripts?|defer executes after parse in order; async executes when fetched, order not guaranteed.
dom|What is the DOM in relation to HTML source?|Browser-created document object tree that scripts can inspect/change.
security|Why should you avoid inserting untrusted text with innerHTML?|It parses markup and can create XSS.
forms|How can fieldset and legend help a group of controls?|Give group a semantic label/context.
links|What should link text communicate?|Destination or purpose without relying on surrounding context.
media|Why might a video need captions?|Access for deaf/hard-of-hearing users and other contexts.
""",
"css": """
cascade|What does the CSS cascade decide?|Which declaration wins based on origin, importance, layer, specificity, and order.
specificity|How do class and ID selectors compare in specificity?|ID generally higher specificity than class.
inheritance|Give one CSS property that normally inherits and one that usually does not.|color inherits; margin does not.
box-model|What contributes to an element's rendered box size?|Content, padding, border, margin outside box.
box-model|What does box-sizing: border-box change?|Declared width/height include padding and border.
display|Compare display:none and visibility:hidden.|none removes layout box; hidden preserves space but hides content.
display|When would inline-block be useful?|Inline flow with controllable width/height and box dimensions.
position|How does position: absolute find its containing block?|Nearest positioned ancestor usually; otherwise initial containing block.
position|What does position: fixed attach to in common cases?|Viewport, subject to containing block exceptions.
position|What is sticky positioning good for?|Element sticks to scroll threshold within scroll container.
flexbox|Which axis does justify-content control in Flexbox?|Main axis.
flexbox|How do align-items and justify-content differ in a row flex container?|align-items cross axis; justify-content main axis.
flexbox|How could you center a child horizontally and vertically with Flexbox?|display:flex; justify-content:center; align-items:center.
flexbox|What does flex-wrap solve?|Allows items to move to new line when insufficient space.
grid|When is CSS Grid more convenient than Flexbox?|Two-dimensional row/column layout.
grid|What does grid-template-columns: repeat(3, 1fr) create?|Three equal fractional columns.
spacing|How do margin and padding differ?|Margin outside border; padding between content and border.
units|When might rem be preferable to px for font sizes?|Scales with root font size and user preferences.
responsive|What is a media query useful for?|Apply styles conditionally by viewport or media features.
responsive|What does a mobile-first CSS approach look like?|Base narrow-screen styles then min-width enhancements.
selectors|What does .card > p select compared with .card p?|Direct child paragraphs versus any descendant paragraphs.
pseudo|When would you use :focus-visible?|Visible keyboard focus styles without forcing same outline on every pointer click.
pseudo|What is ::before used for?|Generated content/styling before element content; not primary accessible content.
overflow|What does overflow:auto do when content exceeds box?|Adds scrolling as needed.
stacking|Why may z-index:9999 fail to place an element above another?|Different stacking contexts constrain stacking order.
transitions|What does transition change in a hover effect?|Animates interpolable property changes over time.
variables|How do you define and use a CSS custom property?|--name: value; then var(--name).
bem|What does BEM naming aim to communicate?|Block, element, modifier relationship in class names.
debugging|A flex child overflows despite flex-shrink. What common fix might help?|Set min-width:0 on flex item, inspect long unbreakable content.
debugging|A margin between two vertical blocks seems smaller than sum. Why?|Vertical margin collapse may combine margins.
"""
}

def parse(raw, topic):
    result=[]
    for index, line in enumerate(raw.strip().splitlines(),1):
        sub,prompt,answer=line.split('|')
        result.append(dict(id=f"{topic[:3]}-{sub}-{index:03d}",topic=topic,subtopic=sub,
          difficulty="easy" if index%7==0 else "junior",type="open",question=prompt,
          expectedPoints=[answer],commonMistakes=[],followUps=[],tags=[sub],
          source={"type":"adapted" if topic != "express" else "original", "url": BASE.format("nodejs" if topic=="express" else topic) if topic != "express" else "https://expressjs.com/en/guide/routing.html", "note":"Original wording; topic cross-checked against source."}))
    return result

bank={topic:parse(raw,topic) for topic,raw in RAW.items()}

def add(topic, sub, typ, question, answer, **kw):
    i=len(bank[topic])+1
    bank[topic].append(dict(id=f"{topic[:3]}-{sub}-{i:03d}",topic=topic,subtopic=sub,
      difficulty="junior",type=typ,question=question,expectedPoints=[answer],
      commonMistakes=[],followUps=[],tags=[sub],source={"type":"original","url":"https://developer.mozilla.org/en-US/docs/Web/JavaScript" if topic=="javascript" else "https://angular.dev/guide/components","note":"Original practical scenario."},**kw))

# One clear best answer. Correct positions deliberately vary.
MCQS={
"javascript":[
("scope","Which binding is block scoped?","let",["var","let","function declaration in outer scope","undeclared assignment"]),
("arrays","Which method returns the first matching element?","find",["filter","map","find","some"]),
("promises","Which method gives an outcome for every promise even after rejection?","allSettled",["race","allSettled","all","then"]),
("equality","Which comparison is true?","0 == false",["0 === false","null === undefined","0 == false","NaN === NaN"]),
("copying","Which expression creates a new top-level array?","[...items]",["items.sort()","items.push(1)","[...items]","items.splice(0)"]),
("storage","Which storage typically survives closing the browser?","localStorage",["sessionStorage","localStorage","a local variable","event.target"]),
("events","Where should a single click listener for dynamic list items usually go?","a stable parent element",["each future item before creation","window only","a stable parent element","the stylesheet"]),
("async-await","What does await do to its enclosing async function?","suspends its continuation until settlement",["blocks the whole JS process","returns a raw Promise immediately from await","suspends its continuation until settlement","turns it synchronous"]),
],
"angular":[
("di","Where is a providedIn: root service usually shared?","through the root injector",["only within one component","through the root injector","between browser tabs automatically","only in templates"]),
("rxjs","Which operator is usually appropriate for latest-only search requests?","switchMap",["tap","filter","switchMap","map"]),
("forms","Which object groups named reactive form controls?","FormGroup",["FormControl","NgModule","FormGroup","Router"]),
("routing","Which service exposes route parameters?","ActivatedRoute",["HttpClient","ActivatedRoute","ChangeDetectorRef","FormBuilder"]),
],
"express":[
("status","Which status best fits successful creation?","201",["200","201","404","500"]),
("middleware","What must ordinary middleware call to continue?","next()",["res.json()","process.exit()","next()","listen()"]),
],
"html":[("accessibility","Which element normally performs an action without navigation?","button",["a","span","button","div"])],
"css":[("layout","Which layout system directly supports two-dimensional tracks?","Grid",["Flexbox","Grid","inline","float"])],
"node":[("fs","Which API reads a file asynchronously as a Promise?","fs/promises readFile",["fs.readFileSync","fs/promises readFile","path.join","process.argv"])],
}
mcq_number=0
mcq_positions=[2,0,3,1,1,3,0,2,3,1,2,0,0,2,1,3,2]
for topic, rows in MCQS.items():
    for sub,q,a,options in rows:
        # Stable shuffled positions avoid a visible A-B-C-D pattern.
        desired=mcq_positions[mcq_number]
        current=options.index(a)
        options=options.copy()
        options[current],options[desired]=options[desired],options[current]
        add(topic,sub,"mcq",q,a,options=options,correctOption="ABCD"[desired])
        mcq_number+=1

OUTPUTS=[
("scope","console.log(x); var x = 3;","undefined"),
("scope","let x = 1; { let x = 2; } console.log(x);","1"),
("closures","function make(){let n=0;return ()=>++n}; const c=make(); console.log(c(),c());","1 2"),
("references","const a={n:1}; const b=a; b.n=2; console.log(a.n);","2"),
("arrays","console.log([1,2,3].filter(x=>x>1).map(x=>x*2));","[4, 6]"),
("coercion","console.log(0 == false, 0 === false);","true false"),
("event-loop","console.log('A'); setTimeout(()=>console.log('B'),0); Promise.resolve().then(()=>console.log('C')); console.log('D');","A D C B"),
("async-await","async function f(){return 4}; f().then(x=>console.log(x)); console.log(1);","1 4"),
("promises","Promise.resolve(2).then(x=>x+1).then(console.log); console.log('sync');","sync then 3"),
("this","const obj={n:3, get(){return this.n}}; console.log(obj.get());","3"),
("arrays","console.log([10,2,1].sort());","[1, 10, 2]"),
("timers","for(let i=0;i<3;i++) setTimeout(()=>console.log(i),0);","0 1 2"),
("copying","const a={nested:{n:1}}; const b={...a}; b.nested.n=5; console.log(a.nested.n);","5"),
("prototypes","const base={x:2}; const child=Object.create(base); console.log(child.x);","2"),
("truthiness","console.log(Boolean([]), Boolean(''), Boolean(0));","true false false"),
]
for sub,snip,out in OUTPUTS:
    add("javascript",sub,"output","What is logged, in order? Briefly explain.",out,snippet=snip,expectedOutput=out)

DEBUGS={
"javascript":[("async","Why does this log an unresolved Promise? Fix it.","async function load(){ return 42 }; console.log(load());","await load() inside async context or use .then"),
("arrays","Why did the source array change? Fix it without mutation.","const sorted = items.sort((a,b)=>a-b);","Use [...items].sort(...) or toSorted()."),
("closure","Why do all callbacks print the final loop value? Fix it.","for(var i=0;i<3;i++) setTimeout(()=>console.log(i),0);","Use let i, creating a new binding per iteration."),
("fetch","Why does the catch not handle HTTP 404?","try { await fetch('/missing') } catch(e) { console.log(e) }","Check response.ok and throw on unsuccessful HTTP status.")],
"angular":[("subscription","Find a leak and describe a fix.","ngOnInit(){ this.data$.subscribe(x => this.value=x) }","Use async pipe, takeUntilDestroyed, or explicit cleanup."),
("binding","Why is button disabled even when canSave is true?","<button disabled=\"canSave\">Save</button>","Use [disabled]=\"!canSave\"."),
("change-detection","Why may this OnPush child fail to refresh?","this.user.name = 'Ada'; // user passed as @Input to OnPush child","Create new object reference or use reactive state.")],
"express":[("middleware","Why does the route never see parsed JSON?","app.post('/items', handler); app.use(express.json());","Move express.json() before route."),
("response","Find the double-response bug.","if (!item) res.status(404).json({error:'missing'}); res.json(item);","Return after 404 response or use else.")]
}
for topic,rows in DEBUGS.items():
    for sub,q,snip,answer in rows:
        add(topic,sub,"debug",q,answer,snippet=snip)

for topic,items in bank.items():
    path=ROOT/"data"/"questions"/f"{topic}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(items,ensure_ascii=False,indent=2)+"\n")

CODING={
"javascript": [
("reverse-string","Reverse a string without using Array.reverse.","reverse('abc') -> 'cba'","Return a string; handle empty input."),
("palindrome","Check whether a string is a palindrome ignoring case and spaces.","isPalindrome('Never odd or even') -> true","Return boolean; document punctuation choice."),
("unique","Remove duplicates from an array preserving first occurrence order.","unique([1,2,1]) -> [1,2]","Use strict/reference identity semantics or explain alternative."),
("count","Count occurrences of each string in an array.","count(['a','b','a']) -> {a:2,b:1}","Return plain object or Map; handle empty array."),
("most-frequent","Return the most frequent item and its count.","mostFrequent(['a','b','a']) -> {value:'a',count:2}","Define tie behavior; handle empty input."),
("chunk","Split an array into chunks of positive size n.","chunk([1,2,3],2) -> [[1,2],[3]]","Do not mutate input; reject invalid n."),
("flatten","Flatten a nested array recursively.","flatten([1,[2,[3]]]) -> [1,2,3]","Preserve order; handle empty arrays."),
("flatten-object","Flatten nested object keys with dot paths.","flattenObject({a:{b:2}}) -> {'a.b':2}","Handle nested plain objects; define array behavior."),
("group-by","Group an array of objects by a chosen key.","groupBy([{k:'a'},{k:'b'}],'k') -> {a:[...],b:[...]}","Preserve item order; handle missing keys explicitly."),
("custom-map","Implement myMap(array, fn) without Array.map.","myMap([1,2],x=>x*2) -> [2,4]","Return new array; pass value/index if desired."),
("custom-filter","Implement myFilter(array, predicate) without Array.filter.","myFilter([1,2,3],x=>x>1) -> [2,3]","Do not mutate input."),
("custom-reduce","Implement myReduce(array, fn, initial) without Array.reduce.","myReduce([1,2],(a,b)=>a+b,0) -> 3","Use initial accumulator; handle empty array."),
("debounce","Implement debounce(fn, delay) so only last call in a burst runs.","Three calls close together -> one trailing call","Preserve this and latest args; allow timer cancellation internally."),
("throttle","Implement throttle(fn, interval) with at most one call per interval.","Rapid calls -> bounded calls","State whether leading/trailing calls run; preserve args."),
("memoize","Memoize a pure single-argument function.","memoized(2) twice -> underlying fn once","Cache results; define key strategy."),
("curry","Implement curry2(fn) so curry2(add)(1)(2) returns 3.","curry2((a,b)=>a+b)(1)(2) -> 3","Support exactly two arguments."),
("compose","Implement compose(f,g) returning x => f(g(x)).","compose(x=>x+1,x=>x*2)(3) -> 7","Preserve function order."),
("once","Implement once(fn) that invokes fn only on first call.","once(increment) called twice -> increment once","Return cached first result on later calls."),
("event-emitter","Implement on, off, and emit for a small EventEmitter.","on('x',fn); emit('x',2) calls fn(2)","Multiple listeners; removing one works."),
("promise-all","Implement a simplified promiseAll(values).","promiseAll([Promise.resolve(1),2]) -> [1,2]","Preserve order; reject on first rejection; empty -> []."),
("intersection","Find unique common elements of two arrays.","intersection([1,2,2],[2,3]) -> [2]","Preserve first array order; no duplicates."),
("merge-arrays","Merge two arrays of records by id, second array wins.","merge([{id:1,a:1}],[{id:1,a:2}]) -> [{id:1,a:2}]","Preserve first-seen id order; avoid mutating records."),
("sort-group","Group records by status and sort each group by name.","[{status:'open',name:'B'},{status:'open',name:'A'}] -> {open:[A,B]}","No input mutation."),
("api-transform","Turn API users into {id,label} options using name as label.","[{id:1,name:'Ada'}] -> [{id:1,label:'Ada'}]","Handle empty array; keep order."),
("lookup","Build an id-to-user lookup from an array of users.","[{id:1,name:'A'}] -> {'1':{id:1,name:'A'}}","Define duplicate id behavior."),
("nested-get","Implement getPath(object, 'a.b.c', fallback).","getPath({a:{b:2}},'a.b',0) -> 2","Return fallback when path missing; don't throw on null."),
("traverse","Recursively collect all leaf values in nested objects.","leaves({a:1,b:{c:2}}) -> [1,2]","Define array handling; preserve traversal order."),
("counter","Create makeCounter that returns increment and get methods.","counter.increment(); counter.get() -> 1","Keep state private via closure."),
("retry","Implement retry(asyncFn, attempts) until success or exhausted.","First rejection then success -> success","Await attempts sequentially; reject final failure."),
("sequence","Run an array of async functions sequentially and collect values.","tasks resolving 1,2 -> [1,2]","No overlap; preserve order; propagate rejection."),
("concurrency","Run async tasks with a maximum of two active at once.","four tasks, limit 2 -> max active 2","Preserve result order; validate positive limit."),
("stale-closure","Fix callbacks that capture the final var loop index.","for(var i=0;i<3;i++) setTimeout(()=>console.log(i),0)","Produce 0,1,2 and explain why."),
],
"angular": [
("standalone-list","Create a standalone component that renders an input list of names.","Input ['Ada','Lin'] -> two list items","Use modern @for with stable track; .ts and optional .html."),
("input-output","Create child counter with input start and output changed.","Parent receives changed value after click","Use input/output APIs or @Input/@Output; show parent binding."),
("filter-list","Create component that filters displayed items by a search term.","Term 'an' -> matching items","Case-insensitive; do not mutate source."),
("reactive-form","Create a reactive form with required email and submit guard.","Invalid email -> no submit","Show validation feedback after touch; import needed APIs."),
("service","Write injectable service storing a small list of tasks.","add then list -> new task visible","Provide in root; expose read and add operations."),
("http","Write service method getUser(id) using HttpClient.","getUser(2) -> Observable<User>","Encode/id route; type return value; no manual subscribe in service."),
("observable-map","Transform Observable<User[]> into Observable<string[]> of names.","[{name:'Ada'}] -> ['Ada']","Use pipe(map(...)); type output."),
("switchmap-search","Build search stream using debounceTime and switchMap.","Latest term -> latest results","Avoid request on empty term; handle errors simply."),
("unsubscribe","Fix a component subscription leak.","Repeated mount/unmount -> no old listener","Use async pipe or takeUntilDestroyed."),
("binding-fix","Fix a disabled button binding.","canSave=true -> enabled","Use property binding correctly; explain expression."),
("loading-state","Implement loading/data/error rendering for a fetch.","Request pending -> loading, rejection -> error","Avoid stale loading state; show retry or refresh path."),
("route-param","Read route id and fetch matching item.","/users/2 -> fetch user 2","Respond when route param changes; use appropriate stream."),
("interceptor","Sketch functional interceptor that adds auth token for own API.","Own API -> Authorization header","Do not attach token to third-party URL; return next(cloned)."),
("async-pipe","Convert manual subscription in component to async-pipe-friendly template.","data$ displayed without manual subscribe","Show .ts and template; cleanup automatic."),
("onpush-fix","Fix stale OnPush child after parent mutates input object.","Updated name appears","Create new input reference or use reactive signal."),
("pipe","Create a simple pure pipe that shortens long text.","'abcdef',4 -> 'abcd…'","Handle short/empty text; standalone import."),
("validation","Write a custom validator disallowing whitespace-only text.","'   ' -> invalid","Return null for valid value and error object otherwise."),
("projection","Create card component with projected body content.","Parent markup appears inside card","Use ng-content and accessible heading."),
],
"node-express": [
("get-route","Write a GET /health Express route returning JSON.","GET /health -> 200 {ok:true}","Use Express app or router; include response."),
("post-route","Write POST /tasks that validates a title and stores in memory.","Valid -> 201 task; invalid -> 400","Use express.json; no database."),
("crud","Implement in-memory GET/POST/DELETE /tasks routes.","Create, list, delete by id","Appropriate status codes; missing item -> 404."),
("logger","Implement middleware logging method and path then calling next.","GET /x -> log GET /x","Must not hang request."),
("validation","Create reusable title validation middleware.","Blank title -> 400","Trim string; call next on valid input."),
("error-handler","Create centralized Express error handler returning safe JSON.","Thrown error -> 500 response","Four args; avoid leaking stack/details."),
("params","Write GET /users/:id against in-memory users.","Missing id -> 404","Use req.params.id; handle string/number comparison."),
("async-handler","Write async route that handles rejected service call.","Service rejects -> error middleware","Support Express 5 or explicitly next(err)."),
("refactor","Refactor duplicated GET routes to shared lookup helper.","Two routes -> one lookup pattern","Keep correct 404 behavior."),
("cors","Configure CORS for a specified frontend origin.","Allowed origin -> CORS header","Restrict configured origin; explain preflight briefly."),
],
}

for file,rows in CODING.items():
    topic="javascript" if file=="javascript" else "angular" if file=="angular" else "express"
    out=[]
    for i,(slug,prompt,example,criteria) in enumerate(rows,1):
        out.append(dict(id=f"code-{file[:3]}-{i:03d}",topic=topic,subtopic=slug,
          difficulty="junior_plus" if slug in {"promise-all","concurrency","switchmap-search","crud"} else "junior",
          type="coding",title=slug.replace('-',' ').title(),prompt=prompt,
          examples=[example],constraints=["Keep the solution short and explain any assumptions."],
          expectedBehavior=[criteria],starterCode="",evaluationNotes=["Inspect code before running it.","Test the example and at least one edge case; give partial credit for sound approach."],
          hiddenTests=[criteria],conceptsTested=[slug],tags=[slug],
          source={"type":"original","url":"https://javascript.info/task/debounce" if slug in {"debounce","throttle"} else "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "note":"Original practical exercise informed by common interview patterns."}))
    path=ROOT/"data"/"coding"/f"{file}.json"
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")

print({k:len(v) for k,v in bank.items()}, {k:len(v) for k,v in CODING.items()})
